"""Pruebas automáticas con pytest."""
import pandas as pd
import pytest

from src.analisis import calcular_kpis, resumen_por, validar_datos
from src.generar_datos import generar_datos


def test_generacion_reproducible():
    a = generar_datos(42)
    b = generar_datos(42)
    pd.testing.assert_frame_equal(a, b)
    assert len(a) == 181 * 3 * 2


def test_kpis_en_rango():
    df = generar_datos(42)
    validar_datos(df)
    metricas = calcular_kpis(df)
    for nombre in ("disponibilidad", "rendimiento", "calidad", "oee"):
        assert 0 <= metricas[nombre] <= 1


def test_oee_formula_exacta_velocidad_comun():
    df = generar_datos(42)
    metricas = calcular_kpis(df)
    esperado = df["unidades_buenas"].sum() / df["minutos_planificados"].sum()
    assert metricas["oee"] == pytest.approx(esperado)
    assert metricas["oee"] == pytest.approx(
        metricas["disponibilidad"] * metricas["rendimiento"] * metricas["calidad"]
    )


def test_grupos():
    assert len(resumen_por(generar_datos(), "planta")) == 3
    assert len(resumen_por(generar_datos(), "mes")) == 6


def test_rechaza_inconsistencias():
    df = generar_datos().iloc[:2].copy()
    df.loc[df.index[0], "unidades_buenas"] = -1
    with pytest.raises(ValueError):
        validar_datos(df)


def test_rechaza_duplicados():
    df = generar_datos().iloc[:2].copy()
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError, match="duplicadas"):
        validar_datos(df)


@pytest.mark.parametrize("columna,valor,mensaje", [
    ("minutos_parada", 999, "Inconsistencia"),
    ("unidades_defectuosas", 9999, "Inconsistencia"),
    ("velocidad_ideal_u_min", 0, "positiva"),
    ("energia_kwh", -1, "negativos"),
    ("energia_kwh", float("inf"), "no finitos"),
    ("minutos_planificados", 1.5, "enteros"),
])
def test_valida_invariantes(columna, valor, mensaje):
    df = generar_datos().iloc[:2].copy()
    if columna == "minutos_planificados" and isinstance(valor, float):
        df[columna] = df[columna].astype(float)
    df.loc[df.index[0], columna] = valor
    with pytest.raises(ValueError, match=mensaje):
        validar_datos(df)


def test_rechaza_fecha_invalida():
    df = generar_datos().iloc[:2].copy()
    df.loc[df.index[0], "fecha"] = "fecha-invalida"
    with pytest.raises(ValueError, match="fechas"):
        validar_datos(df)


def test_rechaza_columnas_ausentes():
    df = generar_datos().iloc[:2].drop(columns="planta")
    with pytest.raises(ValueError, match="Faltan columnas"):
        validar_datos(df)


def test_rechaza_grupos_desconocidos():
    with pytest.raises(ValueError, match="permitida"):
        resumen_por(generar_datos(), "region")


def test_agregacion_oee_velocidades_diferentes():
    df = generar_datos().iloc[:2].copy()
    df.loc[df.index[0], "velocidad_ideal_u_min"] = 2.0
    validar_datos(df)
    metricas = calcular_kpis(df)
    esperado = df["unidades_buenas"].sum() / (
        df["minutos_planificados"] * df["velocidad_ideal_u_min"]
    ).sum()
    assert metricas["oee"] == pytest.approx(esperado)


def test_integridad_agregaciones():
    df = generar_datos()
    globales = calcular_kpis(df)
    por_planta = resumen_por(df, "planta")
    assert por_planta["turnos"].sum() == globales["turnos"]
    assert por_planta["unidades_buenas"].sum() == globales["unidades_buenas"]
    assert por_planta["minutos_parada"].sum() == globales["minutos_parada"]


def test_generacion_reporte(tmp_path, monkeypatch):
    import json
    from src import ejecutar as modulo
    monkeypatch.setattr(modulo, "SALIDA", tmp_path)
    monkeypatch.setattr(modulo, "FIGURAS", tmp_path / "figures")
    modulo.ejecutar()
    metricas = json.loads((tmp_path / "indicadores.json").read_text(encoding="utf-8"))
    assert metricas["turnos"] == 1086
    assert 0 < metricas["oee"] < 1
    for nombre in ("oee_por_planta", "tendencia_oee", "paradas_por_planta"):
        assert (tmp_path / "figures" / f"{nombre}.png").stat().st_size > 10000
    for nombre in ("kpis_por_mes", "kpis_por_planta", "kpis_por_turno"):
        assert not pd.read_csv(tmp_path / f"{nombre}.csv").empty
    assert "Datos 100 % sintéticos" in (tmp_path / "resultados.md").read_text(encoding="utf-8")
