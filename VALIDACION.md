# Validación local del proyecto

Ejecutar desde la raíz:

```bash
python -m pip install -r requirements-dev.txt
python -m src.generar_datos
python -m src.ejecutar
python -m pytest -q
```

Se verifican: reproducibilidad, rangos de KPIs, coherencia de sumas, entradas inválidas, agregaciones y generación de informes PNG/CSV/JSON.

Los datos son sintéticos. La ejecución de GitHub Actions debe comprobarse también en el repositorio remoto.

**Nota de actualización:** si el README del repositorio ya fue editado manualmente, consérvalo; el README incluido en este ZIP es la versión original con pequeños ajustes de enlace y estado.
