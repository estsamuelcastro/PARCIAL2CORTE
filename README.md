# Sistema logístico de monedas inteligentes — entrega final

Este paquete organiza la entrega de la etapa solicitada en cuatro objetivos: arquitectura, diseño mecánico/electrónico, simulación PyBullet e integración ESP32 + Streamlit. La moneda de trabajo es el peso colombiano (COP).

## Qué contiene

- `urdf/maqueta_base_original.urdf`: copia de la base entregada para el proyecto.
- `urdf/maqueta_proyecto.urdf`: adaptación ampliada para cinco denominaciones colombianas ($50, $100, $200, $500 y $1.000), compuertas, recipientes, sensores/electrónica representados, carro recolector, 3 obstáculos y meta.
- `simulation/main.py`: simulación funcional en PyBullet que carga el URDF, clasifica monedas, actualiza métricas y ejecuta la ruta con tres obstáculos.
- `dashboard/app.py`: dashboard Streamlit con cantidad, peso, valor, estado, distribución por denominación, ruta y asistente de datos.
- `firmware/`: programas Arduino para el ESP32 actuador y ESP32-CAM.
- `mechanical/cad/coin_sorter.scad`: CAD paramétrico de referencia en OpenSCAD para tolva, banda, estaciones y compuertas.
- `mechanical/drawings/`: plano conceptual con cotas principales.
- `electrical/`: diagrama de conexiones y alimentación.
- `docs/`: arquitectura, requisitos, materiales, integración y plan de validación.
- `data/`: CSV de demostración y archivo de telemetría que la simulación genera.

## Instalación

En VS Code, abrir esta carpeta y usar el terminal de la carpeta raíz:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Ejecutar PyBullet

```powershell
.\.venv\Scripts\python.exe simulation\main.py
```

Controles durante la simulación: `1`=$50, `2`=$100, `3`=$200, `4`=$500, `5`=$1.000; `R` reinicia, `SPACE` pausa/continúa y `ESC` cierra.

Al finalizar, se actualizan:

- `data/live_telemetry.csv`
- `data/live_summary.json`

## Ejecutar Streamlit

```powershell
.\.venv\Scripts\python.exe -m streamlit run dashboard\app.py
```

En el panel lateral se puede introducir la IP del ESP32. El botón de consulta usa `GET /status` y los comandos de clasificación utilizan `GET /sort?value=...`.

## Integración física prevista

La primera integración inalámbrica usa Wi-Fi y HTTP/JSON porque permite probar rápidamente el enlace ESP32 ↔ PC. La cámara ESP32-CAM queda preparada para captura local y evolución posterior hacia clasificación por visión en el PC.

## Alcance y honestidad de la evidencia

Este paquete deja implementada y documentada la parte de diseño, simulación, software de supervisión y firmware de integración. La construcción física, calibración real de sensores y pruebas con monedas reales requieren el montaje y las mediciones en laboratorio; no se presenta este archivo como evidencia de una prueba física que no se haya realizado.
