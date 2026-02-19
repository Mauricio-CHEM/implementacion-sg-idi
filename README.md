# 🔬 Dashboard SGI I+D+I — NTC 5801 / ISO 56002

Dashboard de seguimiento para la implementación del Sistema de Gestión de I+D+I del **Laboratorio IIAD**, alineado con **NTC 5801** e **ISO 56002**.

## Funcionalidades

- **Dashboard general** con KPIs, gráficas de progreso y radar por fase
- **Lista de verificación** por fase (73 actividades en 4 fases)
- **Registro documental** (45 documentos base + 30 formatos)
- **Reportes** con gráfica mensual y exportación a CSV
- **Persistencia automática** en archivo `sgi_state.json`

## Instalación

```bash
git clone https://github.com/tu-usuario/sgi-iadi.git
cd sgi-iadi
pip install -r requirements.txt
```

## Uso

```bash
streamlit run app.py
```

Abre el navegador en `http://localhost:8501`

## Estructura del proyecto

```
sgi-iadi/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias
├── README.md           # Este archivo
└── sgi_state.json      # Estado guardado (auto-generado)
```

## Actualizar el estado

1. Abre cualquier fase en el menú lateral
2. Cambia el estado de cada actividad con el selector
3. El estado se **guarda automáticamente** al cambiar cualquier ítem
4. También puedes presionar **💾 Guardar estado** en la barra lateral

## Licencia

Uso interno — Laboratorio IIAD
