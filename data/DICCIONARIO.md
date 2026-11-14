# Diccionario de datos

Una fila corresponde a **una planta, una fecha y un turno**.

| Campo | Definición | Unidad |
|---|---|---|
| fecha | Fecha del turno | AAAA-MM-DD |
| planta | Identificador ficticio: Norte, Centro o Sur | Categoría |
| turno | Mañana o Tarde | Categoría |
| minutos_planificados | Tiempo planificado para producción | min |
| minutos_parada | Interrupciones del proceso | min |
| minutos_operativos | Tiempo planificado menos paradas | min |
| velocidad_ideal_u_min | Velocidad ideal declarada del equipo | unidades/min |
| unidades_producidas | Total producido, incluyendo defectos | unidades |
| unidades_defectuosas | Producción con defectos | unidades |
| unidades_buenas | Total producido menos defectos | unidades |
| objetivo_unidades_buenas | Meta ficticia de producción útil | unidades |
| energia_kwh | Energía consumida por turno | kWh |
| costo_mantenimiento_usd | Coste estimado de mantenimiento por turno | USD |

## Fórmulas

- **Disponibilidad** = Σ minutos operativos / Σ minutos planificados.
- **Rendimiento** = Σ unidades producidas / Σ (minutos operativos × velocidad ideal).
- **Calidad** = Σ unidades buenas / Σ unidades producidas.
- **OEE** = disponibilidad × rendimiento × calidad, cuando la velocidad ideal es homogénea.
- **Cumplimiento** = Σ unidades buenas / Σ objetivo de unidades buenas.
- **Intensidad energética** = Σ kWh / Σ unidades buenas.

La agregación por sumas evita promediar porcentajes de turnos con pesos distintos.
En este proyecto la velocidad ideal es constante (1 unidad/min), por eso la identidad de OEE es exacta.
Los costes y los volúmenes son simulados y no son presupuestos ni cotizaciones reales.
