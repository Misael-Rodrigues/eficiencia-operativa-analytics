"""Validación, KPIs y agregación para eficiencia operativa."""
from pathlib import Path

import numpy as np
import pandas as pd

COLUMNAS_REQUERIDAS = {
    "fecha", "planta", "turno", "minutos_planificados", "minutos_parada",
    "minutos_operativos", "velocidad_ideal_u_min", "unidades_producidas",
    "unidades_defectuosas", "unidades_buenas", "objetivo_unidades_buenas",
    "energia_kwh", "costo_mantenimiento_usd",
}


def cargar_datos(ruta: str | Path) -> pd.DataFrame:
    df = pd.read_csv(ruta, parse_dates=["fecha"])
    validar_datos(df)
    return df


def validar_datos(df: pd.DataFrame) -> None:
    faltantes = COLUMNAS_REQUERIDAS - set(df.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas: {sorted(faltantes)}")
    if df.empty or df[list(COLUMNAS_REQUERIDAS)].isna().any().any():
        raise ValueError("El conjunto de datos está vacío o contiene valores nulos.")
    if pd.to_datetime(df["fecha"], format="%Y-%m-%d", errors="coerce").isna().any():
        raise ValueError("Se detectaron fechas no válidas.")
    if df[["planta", "turno"]].astype(str).apply(lambda s: s.str.strip().eq("")).any().any():
        raise ValueError("Planta y turno son obligatorios.")
    numericas = sorted(COLUMNAS_REQUERIDAS - {"fecha", "planta", "turno"})
    if any(not pd.api.types.is_numeric_dtype(df[c]) for c in numericas):
        raise ValueError("Las variables cuantitativas deben ser numéricas.")
    if not np.isfinite(df[numericas].to_numpy(dtype=float)).all():
        raise ValueError("Se detectaron valores numéricos no finitos.")
    for columna in ("minutos_planificados", "minutos_parada", "minutos_operativos",
                    "unidades_producidas", "unidades_defectuosas", "unidades_buenas",
                    "objetivo_unidades_buenas"):
        if (df[columna] % 1 != 0).any():
            raise ValueError(f"{columna} debe contener números enteros.")
    if (df[numericas] < 0).any().any():
        raise ValueError("Se detectaron valores negativos.")
    if not (df["minutos_planificados"] > 0).all():
        raise ValueError("Los minutos planificados deben ser positivos.")
    if not (df["velocidad_ideal_u_min"] > 0).all():
        raise ValueError("La velocidad ideal debe ser positiva.")
    if not (df["minutos_operativos"] == df["minutos_planificados"] - df["minutos_parada"]).all():
        raise ValueError("Inconsistencia en minutos operativos.")
    if not (df["unidades_buenas"] == df["unidades_producidas"] - df["unidades_defectuosas"]).all():
        raise ValueError("Inconsistencia en unidades buenas.")
    if (df["minutos_operativos"] < 0).any() or (df["unidades_defectuosas"] > df["unidades_producidas"]).any():
        raise ValueError("Se detectaron valores físicamente imposibles.")
    if (df["unidades_producidas"] > df["minutos_operativos"] * df["velocidad_ideal_u_min"] + 1e-8).any():
        raise ValueError("La producción excede la capacidad ideal del tiempo operativo.")
    if df.duplicated(subset=["fecha", "planta", "turno"]).any():
        raise ValueError("Se detectaron combinaciones fecha-planta-turno duplicadas.")


def calcular_kpis(df: pd.DataFrame) -> dict:
    """Métricas ponderadas por totales, evitando promediar porcentajes de turnos."""
    planificados = df["minutos_planificados"].sum()
    operativos = df["minutos_operativos"].sum()
    producidas = df["unidades_producidas"].sum()
    buenas = df["unidades_buenas"].sum()
    capacidad_ideal_operativa = (df["minutos_operativos"] * df["velocidad_ideal_u_min"]).sum()
    capacidad_ideal_planificada = (df["minutos_planificados"] * df["velocidad_ideal_u_min"]).sum()
    disponibilidad = operativos / planificados if planificados else np.nan
    rendimiento = producidas / capacidad_ideal_operativa if capacidad_ideal_operativa else np.nan
    calidad = buenas / producidas if producidas else np.nan
    # OEE agregado = unidades buenas / capacidad ideal planificada.
    # Con velocidades diferentes no es necesariamente el producto de los tres
    # factores anteriores, ya que disponibilidad está ponderada por tiempo.
    oee = buenas / capacidad_ideal_planificada if capacidad_ideal_planificada else np.nan
    objetivo_total = df["objetivo_unidades_buenas"].sum()
    return {
        "turnos": int(len(df)),
        "unidades_buenas": int(buenas),
        "disponibilidad": float(disponibilidad),
        "rendimiento": float(rendimiento),
        "calidad": float(calidad),
        "oee": float(oee),
        "cumplimiento_objetivo": float(buenas / objetivo_total) if objetivo_total else np.nan,
        "minutos_parada": int(df["minutos_parada"].sum()),
        "energia_kwh_por_unidad_buena": float(df["energia_kwh"].sum() / buenas) if buenas else np.nan,
        "costo_mantenimiento_usd": float(df["costo_mantenimiento_usd"].sum()),
    }


def resumen_por(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    if columna not in {"planta", "turno", "mes"}:
        raise ValueError("Agrupación no permitida.")
    copia = df.copy()
    copia["mes"] = pd.to_datetime(copia["fecha"]).dt.to_period("M").astype(str)
    filas = []
    for grupo, sub in copia.groupby(columna, sort=True):
        filas.append({columna: grupo, **calcular_kpis(sub)})
    return pd.DataFrame(filas).sort_values(columna).reset_index(drop=True)
