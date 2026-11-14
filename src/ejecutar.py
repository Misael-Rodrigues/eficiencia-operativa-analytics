"""Punto de entrada: python -m src.ejecutar"""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.analisis import cargar_datos, calcular_kpis, resumen_por

BASE = Path(__file__).resolve().parents[1]
SALIDA = BASE / "reports"
FIGURAS = SALIDA / "figures"


def ejecutar() -> None:
    FIGURAS.mkdir(parents=True, exist_ok=True)
    df = cargar_datos(BASE / "data" / "operaciones.csv")
    globales = calcular_kpis(df)
    por_planta = resumen_por(df, "planta")
    por_mes = resumen_por(df, "mes")
    por_turno = resumen_por(df, "turno")

    with open(SALIDA / "indicadores.json", "w", encoding="utf-8") as f:
        json.dump(globales, f, indent=2, ensure_ascii=False)
    por_planta.to_csv(SALIDA / "kpis_por_planta.csv", index=False, float_format="%.6f")
    por_mes.to_csv(SALIDA / "kpis_por_mes.csv", index=False, float_format="%.6f")
    por_turno.to_csv(SALIDA / "kpis_por_turno.csv", index=False, float_format="%.6f")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(por_planta["planta"], por_planta["oee"] * 100)
    ax.axhline(85, color="gray", linestyle="--", label="Referencia ilustrativa: 85 %")
    ax.set_ylim(0, 100)
    ax.set_ylabel("OEE (%)")
    ax.set_title("Eficiencia global de equipos por planta")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURAS / "oee_por_planta.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(por_mes["mes"], por_mes["oee"] * 100, marker="o")
    ax.set_ylim(0, 100)
    ax.set_ylabel("OEE (%)")
    ax.set_xlabel("Mes")
    ax.set_title("Evolución mensual del OEE")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURAS / "tendencia_oee.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(por_planta["planta"], por_planta["minutos_parada"] / 60)
    ax.set_ylabel("Horas de parada")
    ax.set_title("Tiempo de inactividad acumulado por planta")
    fig.tight_layout()
    fig.savefig(FIGURAS / "paradas_por_planta.png", dpi=160)
    plt.close(fig)

    resumen = [
        "# Resultados del análisis",
        "",
        "> Datos 100 % sintéticos. No representan una empresa real.",
        "",
        "## Indicadores generales",
        "",
        "| Indicador | Resultado |",
        "|---|---:|",
        f"| Turnos analizados | {globales['turnos']:,} |",
        f"| Unidades buenas | {globales['unidades_buenas']:,} |",
        f"| Disponibilidad | {globales['disponibilidad']:.1%} |",
        f"| Rendimiento | {globales['rendimiento']:.1%} |",
        f"| Calidad | {globales['calidad']:.1%} |",
        f"| **OEE global** | **{globales['oee']:.1%}** |",
        f"| Cumplimiento del objetivo | {globales['cumplimiento_objetivo']:.1%} |",
        f"| Energía por unidad buena | {globales['energia_kwh_por_unidad_buena']:.3f} kWh |",
        "",
        "## Comparación entre plantas",
        "",
        "| Planta | OEE | Disponibilidad | Calidad | Horas de parada |",
        "|---|---:|---:|---:|---:|",
    ]
    for _, r in por_planta.iterrows():
        resumen.append(
            f"| {r['planta']} | {r['oee']:.1%} | {r['disponibilidad']:.1%} | "
            f"{r['calidad']:.1%} | {r['minutos_parada'] / 60:,.1f} |"
        )
    peor = por_planta.sort_values("oee").iloc[0]
    mejor = por_planta.sort_values("oee", ascending=False).iloc[0]
    resumen += [
        "", "## Hallazgos y acciones sugeridas", "",
        f"1. **Priorizar {peor['planta']}**: presenta el menor OEE ({peor['oee']:.1%}). "
        "Revisar causas de paradas, mantenimiento preventivo y estándares de producción.",
        f"2. **Tomar {mejor['planta']} como referencia interna**: su OEE es {mejor['oee']:.1%}. "
        "Evaluar qué prácticas podrían transferirse entre plantas.",
        "3. Segmentar pérdidas por turno y validar hipótesis con registros de causas de parada reales.",
        "4. No interpretar la mejora sintética de abril como efecto causal de una intervención.",
        "",
        "## Visualizaciones", "",
        "![OEE por planta](figures/oee_por_planta.png)",
        "![Tendencia OEE](figures/tendencia_oee.png)",
        "![Horas de parada](figures/paradas_por_planta.png)",
        "",
        "## Limitaciones", "",
        "El estudio es demostrativo y descriptivo, sin inferencia causal, sin incertidumbre estadística",
        "estimada y sin demanda observada del mundo real. La referencia de OEE de 85 % es ilustrativa;",
        "no debe usarse como meta universal sin conocer el proceso industrial.",
    ]
    (SALIDA / "resultados.md").write_text("\n".join(resumen) + "\n", encoding="utf-8")
    print(f"Análisis finalizado. OEE global: {globales['oee']:.1%}")
    print(f"Resultados: {SALIDA / 'resultados.md'}")


if __name__ == "__main__":
    ejecutar()
