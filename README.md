# Análisis de Eficiencia Operativa

**Análisis de datos de producción industrial con Python y Pandas**

Este proyecto analiza la eficiencia operativa de tres plantas industriales a partir de datos sintéticos de producción correspondientes al período de enero a junio de 2025.

El análisis se centra en la construcción de indicadores de desempeño, la comparación de resultados entre plantas y turnos y la identificación de posibles oportunidades de mejora en los procesos productivos.

El proyecto incluye generación de datos reproducibles, procesamiento automatizado, visualización de indicadores y pruebas de validación.

## 1. Contexto del proyecto

En operaciones industriales, el seguimiento de la producción no siempre permite comprender las causas de las pérdidas de eficiencia. Una planta puede presentar un volumen elevado de producción y, al mismo tiempo, registrar problemas relacionados con paradas, rendimiento o calidad.

Para explorar estas diferencias, se construyó un escenario simulado con tres plantas manufactureras y registros operacionales de seis meses.

El análisis busca responder las siguientes preguntas:

- ¿Existen diferencias significativas de eficiencia entre las plantas?
- ¿Qué impacto tienen las paradas operacionales sobre la disponibilidad?
- ¿Cómo se comportan los indicadores de rendimiento y calidad?
- ¿Qué variaciones se observan entre turnos y períodos?
- ¿Qué aspectos deberían investigarse para orientar iniciativas de mejora?

## 2. Herramientas utilizadas

| Herramienta | Aplicación |
|---|---|
| Python 3.11+ | Procesamiento y automatización |
| Pandas | Manipulación y análisis de datos |
| NumPy | Cálculos y operaciones numéricas |
| Matplotlib | Visualización de resultados |
| Pytest | Validación automatizada |
| GitHub Actions | Ejecución de pruebas mediante integración continua |

## 3. Datos

La base de datos contiene registros sintéticos de producción generados mediante Python.

Los datos representan operaciones de tres plantas industriales durante el primer semestre de 2025.

El conjunto incluye variables relacionadas con tiempos de producción, paradas operacionales, unidades producidas, defectos, objetivos de producción y consumo energético.

La generación utiliza una semilla fija para permitir la reproducción de los resultados.

El archivo principal se encuentra en:

`data/operaciones.csv`

Las definiciones de las variables, las reglas de cálculo y las consideraciones sobre los datos están documentadas en [DICCIONARIO.md](data/DICCIONARIO.md).

## 4. Metodología

El análisis se desarrolló mediante un proceso de generación, preparación, cálculo y visualización de datos.

### Preparación de datos

Se utilizaron Pandas y NumPy para organizar los registros, verificar su consistencia y preparar las variables necesarias para el cálculo de los indicadores.

### Cálculo de indicadores

Los principales indicadores considerados fueron:

| Indicador | Definición |
|---|---|
| Disponibilidad | Tiempo operativo / Tiempo planificado |
| Rendimiento | Producción real / Capacidad ideal operativa |
| Calidad | Unidades conformes / Unidades producidas |
| OEE | Disponibilidad × Rendimiento × Calidad |
| Cumplimiento | Unidades conformes / Objetivo de producción |
| Consumo específico de energía | Energía consumida / Unidades conformes |

El OEE (Overall Equipment Effectiveness) se utiliza como indicador principal para evaluar la eficiencia de los equipos, considerando disponibilidad, rendimiento y calidad.

Los indicadores se consolidan por planta, turno y período de análisis.

### Visualización

Se desarrollaron gráficos con Matplotlib para facilitar la comparación de los resultados y la identificación de variaciones operacionales.

Los archivos generados se almacenan en el directorio `reports`.

## 5. Resultados

Los resultados se presentan mediante indicadores consolidados y visualizaciones de desempeño.

### OEE por planta

![OEE por planta](reports/figures/oee_por_planta.png)

Comparación de la eficiencia global entre las tres plantas industriales.

### Evolución mensual del OEE

![Evolución mensual del OEE](reports/figures/tendencia_oee.png)

Comportamiento del indicador durante los seis meses analizados.

### Paradas operacionales

![Paradas operacionales por planta](reports/figures/paradas_por_planta.png)

Comparación del tiempo acumulado de paradas entre las unidades productivas.

Los resultados detallados y los indicadores calculados están disponibles en [reports/resultados.md](reports/resultados.md).

## 6. Consideraciones del análisis

La metodología permite identificar diferencias de desempeño y establecer prioridades para investigaciones operacionales.

Entre las posibles líneas de análisis se encuentran:

- Investigar las plantas con menor OEE, diferenciando las pérdidas de disponibilidad, rendimiento y calidad.
- Comparar indicadores entre turnos para identificar variaciones operacionales.
- Incorporar registros de causas de parada para profundizar el diagnóstico.
- Evaluar las prácticas operativas de las plantas con mejores indicadores.
- Definir objetivos de desempeño considerando las características de cada proceso productivo.

Los resultados permiten describir patrones y diferencias en los datos simulados, pero no demuestran relaciones causales entre las variables.

## 7. Estructura del repositorio

```text
eficiencia-operativa-analytics/
├── .github/
│   └── workflows/
│       └── tests.yml
├── data/
│   ├── DICCIONARIO.md
│   └── operaciones.csv
├── reports/
│   ├── figures/
│   ├── indicadores.json
│   ├── kpis_por_mes.csv
│   ├── kpis_por_planta.csv
│   ├── kpis_por_turno.csv
│   └── resultados.md
├── src/
│   ├── __init__.py
│   ├── analisis.py
│   ├── ejecutar.py
│   └── generar_datos.py
├── tests/
│   └── test_analisis.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

## 8. Ejecución del proyecto

**Requisitos:** Python 3.11 o superior y Git.

Clonar el repositorio:

```bash
git clone https://github.com/Misael-Rodrigues/eficiencia-operativa-analytics.git
cd eficiencia-operativa-analytics
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno virtual en Windows:

```powershell
.venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
source .venv/bin/activate
```

Instalar las dependencias:

```bash
python -m pip install -r requirements-dev.txt
```

Generar los datos y ejecutar el análisis:

```bash
python -m src.generar_datos
python -m src.ejecutar
```

Ejecutar las pruebas:

```bash
python -m pytest -q
```

El conjunto de datos original está incluido en el repositorio. No es necesario regenerarlo para consultar los resultados existentes.

## 9. Limitaciones

El proyecto utiliza exclusivamente datos sintéticos y no representa operaciones de una empresa real.

Los registros fueron construidos con fines de análisis y demostración, por lo que las conclusiones no deben interpretarse como resultados de una intervención empresarial.

El análisis tiene carácter descriptivo. Los valores económicos y energéticos son simulados y no constituyen una base para decisiones de inversión.

Para aplicar la metodología en un entorno industrial real, sería necesario revisar la disponibilidad y calidad de los registros, las velocidades ideales de cada línea y los criterios de consolidación de indicadores.

## 10. Posibles desarrollos

El proyecto puede ampliarse mediante:

- Análisis de Pareto de causas de parada.
- Desarrollo de un dashboard interactivo en Power BI.
- Seguimiento de metas de producción por planta y turno.
- Incorporación de alertas para desviaciones operacionales.
- Evaluación de resultados antes y después de intervenciones de mejora.

## Autor

**Misael Rodrigues**

Proyecto independiente de análisis de datos, desarrollado como parte de un portafolio profesional enfocado en Data Analytics, Business Intelligence y eficiencia operacional.

[GitHub](https://github.com/Misael-Rodrigues)

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Los datos utilizados fueron generados sintéticamente con fines de demostración.
