# Dashboard: Conectividad y Demografía en la Región de Aysén

Dashboard interactivo construido con **Python y Dash** que analiza la
relación entre el crecimiento de las conexiones de internet fijo y la
evolución demográfica en las 10 comunas de la Región de Aysén.

Proyecto realizado para la asignatura **IF1022-1 - Visualización de
Datos**, Universidad de Aysén.

## Integrantes

- [Nombre integrante 1] — conectividad
- [Nombre integrante 2] — población

## Fuentes de datos

- **SUBTEL** - Series de Conexiones de Internet Fija (2007-2026), nivel
  comunal. Descarga: https://www.subtel.gob.cl/
- **INE** - Estimaciones y Proyecciones de Población por Comuna
  2002-2035, base 2017. Descarga: https://www.ine.gob.cl/

Ambas fuentes son de acceso público y libre uso. Los archivos
originales se encuentran en `data/raw/`.

## Estructura del proyecto

```
dashboard-conectividad-aysen/
├── data/
│   ├── raw/          # archivos originales descargados (SUBTEL, INE)
│   └── processed/    # datasets limpios generados por loaders.py
├── app/
│   ├── app.py        # punto de entrada de la app Dash
│   ├── loaders.py    # carga y limpieza de datos (merge/join/groupby)
│   ├── charts/        # un módulo por gráfico/pestaña
│   └── assets/        # logo, hoja de estilos
├── notebooks/         # exploración de datos (opcional)
└── requirements.txt
```

## Cómo ejecutar

1. Crear y activar un entorno virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # En Windows: .venv\Scripts\activate
   ```

2. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar la aplicación:

   ```bash
   cd app
   python app.py
   ```

4. Abrir en el navegador: http://127.0.0.1:8050

## Notas

- Reemplazar `app/assets/logo_uaysen.png` con el logo oficial de la
  Universidad de Aysén antes de la entrega final.
- Los TODOs en `loaders.py` y en cada módulo de `charts/` indican el
  trabajo pendiente de cada integrante.
