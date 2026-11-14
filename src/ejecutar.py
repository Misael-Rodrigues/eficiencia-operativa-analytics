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

    # Diseño consistente para informes: azul ENPROL, sin referencias universales de OEE.
    AZUL = "#0D3755"
    plt.rcParams.update({
        "font.family": "DejaVu Sans",  # Alternativa libre si Sequel no está instalada
        "font.size": 11, "axes.spines.top": False,
        "axes.spines.right": False, "savefig.facecolor": "white",
    })

    fig, ax = plt.subplots(figsize=(9, 5.2))
    datos = por_planta.sort_values("oee", ascending=False)
    barras = ax.barh(datos["planta"], datos["oee"] * 100, color=AZUL, height=0.55)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("OEE (%)")
    ax.set_title("Eficiencia global por planta", loc="left", fontsize=16, pad=16)
    ax.bar_label(barras, fmt="%.1f %%", padding=6)
    ax.grid(axis="x", alpha=0.15)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=2)
    fig.savefig(FIGURAS / "oee_por_planta.png", dpi=220)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    x = range(len(por_mes))
    ax.plot(x, por_mes["oee"] * 100, color=AZUL, linewidth=2.8, marker="o", markersize=6)
    ax.set_xticks(list(x), por_mes["mes"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("OEE (%)")
    ax.set_title("Evolución mensual del OEE", loc="left", fontsize=16, pad=16)
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=2)
    fig.savefig(FIGURAS / "tendencia_oee.png", dpi=220)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    datos = por_planta.sort_values("minutos_parada", ascending=False)
    barras = ax.barh(datos["planta"], datos["minutos_parada"] / 60, color=AZUL, height=0.55)
    ax.invert_yaxis()
    ax.set_xlabel("Horas acumuladas")
    ax.set_title("Tiempo de parada por planta", loc="left", fontsize=16, pad=16)
    ax.bar_label(barras, fmt="%.0f h", padding=5)
    ax.margins(x=0.2)
    ax.grid(axis="x", alpha=0.15)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=2)
    fig.savefig(FIGURAS / "paradas_por_planta.png", dpi=220)
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
        "El estudio es demostrativo y descriptivo, sin inferencia causal ni datos observados",
        "del mundo real. No se utiliza un umbral universal de OEE.",
    ]
    (SALIDA / "resultados.md").write_text("\n".join(resumen) + "\n", encoding="utf-8")
    print(f"Análisis finalizado. OEE global: {globales['oee']:.1%}")
    print(f"Resultados: {SALIDA / 'resultados.md'}")


if __name__ == "__main__":
    ejecutar()
