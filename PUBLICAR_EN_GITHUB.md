# Guía rápida para publicar en GitHub

1. Crea un repositorio **público** en GitHub con nombre `eficiencia-operativa-analytics`. No marques la opción de inicializar con README, .gitignore o licencia: ya están incluidos.
2. Descomprime el ZIP y abre una terminal dentro de la carpeta `eficiencia-operativa-analytics`.
3. Ejecuta (reemplaza `TU_USUARIO` por tu identificador de GitHub):

```bash
git init
git add .
git commit -m "feat: análisis reproducible de eficiencia operativa"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/eficiencia-operativa-analytics.git
git push -u origin main
```

Si Git solicita autenticarte, utiliza tu método de autenticación admitido (por ejemplo, Git Credential Manager o clave SSH). GitHub no acepta contraseñas normales para operaciones Git por HTTPS.

## Configuración recomendada

**Descripción del repositorio:**
> Análisis de eficiencia operativa con Python: OEE, productividad, paradas, calidad y visualizaciones con datos sintéticos reproducibles.

**Topics (etiquetas):** `python`, `data-analysis`, `pandas`, `operational-efficiency`, `oee`, `manufacturing`, `data-visualization`, `portfolio`, `spanish`

**Vista previa para LinkedIn (texto en español):**
> 📊 Nuevo proyecto de análisis de datos: Eficiencia Operativa con Python.
>
> Analicé 1.086 registros sintéticos de turnos de producción en tres plantas, calculé KPIs de disponibilidad, rendimiento, calidad y OEE, y construí gráficos para detectar oportunidades de mejora.
>
> Resultado del ejercicio: OEE global de 78,1 %, con una diferencia relevante entre la planta Centro (70,6 %) y Sur (84,3 %). Incluí datos reproducibles, código modular, pruebas automáticas y documentación en español.
>
> 🔗 https://github.com/TU_USUARIO/eficiencia-operativa-analytics
>
> #DataAnalytics #Python #Pandas #BusinessIntelligence #EficienciaOperativa

**Importante:** Señala siempre que los datos son simulados. No presentes hallazgos ficticios como una experiencia empresarial real.
