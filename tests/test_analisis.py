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
