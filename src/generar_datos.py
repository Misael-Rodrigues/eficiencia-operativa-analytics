"""Genera datos sintéticos reproducibles por turno y planta."""
from pathlib import Path

import numpy as np
import pandas as pd

RUTA_DATOS = Path(__file__).resolve().parents[1] / "data" / "operaciones.csv"


def generar_datos(semilla: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)
    registros = []
    fechas = pd.date_range("2025-01-01", "2025-06-30", freq="D")
    perfiles = {
        "Norte": {"parada": 37, "rendimiento": 0.90, "defectos": 0.034},
        "Centro": {"parada": 57, "rendimiento": 0.84, "defectos": 0.055},
        "Sur": {"parada": 28, "rendimiento": 0.93, "defectos": 0.025},
    }
    for fecha in fechas:
        for planta, perfil in perfiles.items():
            for turno in ("Mañana", "Tarde"):
                minutos_planificados = 480
                factor_turno = 1.15 if turno == "Tarde" else 1.0
                # Cambios operativos sintéticos desde abril: mejora parcial en Centro.
                mejora = 0.76 if (planta == "Centro" and fecha.month >= 4) else 1.0
                parada = int(np.clip(rng.normal(perfil["parada"] * factor_turno * mejora, 14), 5, 130))
                minutos_operativos = minutos_planificados - parada
                velocidad_ideal = 1.0  # unidades por minuto
                rendimiento = float(np.clip(rng.normal(perfil["rendimiento"], 0.045), 0.65, 0.99))
                unidades = int(np.floor(minutos_operativos * velocidad_ideal * rendimiento))
                proporcion_defectos = float(np.clip(rng.normal(perfil["defectos"], 0.012), 0.004, 0.11))
                defectos = int(rng.binomial(unidades, proporcion_defectos))
                buenas = unidades - defectos
                # Objetivo de producción para comparar cumplimiento, no la capacidad teórica.
                objetivo = 390
                energia_kwh = round(90 + 0.16 * unidades + 0.3 * parada + rng.normal(0, 9), 2)
                costo_mantenimiento = round(max(0, 30 + parada * 2.4 + rng.normal(0, 25)), 2)
                registros.append({
                    "fecha": fecha.strftime("%Y-%m-%d"),
                    "planta": planta,
                    "turno": turno,
                    "minutos_planificados": minutos_planificados,
                    "minutos_parada": parada,
                    "minutos_operativos": minutos_operativos,
                    "velocidad_ideal_u_min": velocidad_ideal,
                    "unidades_producidas": unidades,
                    "unidades_defectuosas": defectos,
                    "unidades_buenas": buenas,
                    "objetivo_unidades_buenas": objetivo,
                    "energia_kwh": energia_kwh,
                    "costo_mantenimiento_usd": costo_mantenimiento,
                })
    return pd.DataFrame(registros)


if __name__ == "__main__":
    RUTA_DATOS.parent.mkdir(parents=True, exist_ok=True)
    df = generar_datos()
    df.to_csv(RUTA_DATOS, index=False)
    print(f"Datos sintéticos guardados: {RUTA_DATOS} ({len(df)} filas)")
