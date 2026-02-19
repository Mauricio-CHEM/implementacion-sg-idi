# 🔬 SGI I+D+I — IIAD
### Sistema de Gestión de la Investigación, Desarrollo e Innovación
**NTC 5801 / ISO 56002 | Laboratorio IIAD | Versión 2.0**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://implementacion-sg-idi-iiad-lania-v1.streamlit.app/)

---

## Índice

- [Descripción general](#1-descripción-general)
- [Instalación local](#2-instalación-local)
- [Páginas de la aplicación](#3-páginas-de-la-aplicación)
- [Checklist de actividades](#4-cómo-usar-el-checklist-de-actividades)
- [Registro Documental y códigos SGC](#5-registro-documental-y-códigos-sgc)
- [Logo institucional](#6-logo-institucional)
- [Exportar e importar el estado JSON](#7-exportar-e-importar-el-estado-json)
- [Flujo de trabajo con OneDrive / Teams](#8-flujo-de-trabajo-recomendado-con-onedrive--teams)
- [Despliegue en Streamlit Cloud](#9-despliegue-en-streamlit-cloud)
- [Preguntas frecuentes](#10-preguntas-frecuentes)
- [Historial de versiones](#11-historial-de-versiones)

---

## 1. Descripción General

Aplicación web interactiva para el seguimiento de la implementación del **Sistema de Gestión de I+D+I** del Laboratorio IIAD, construida con [Streamlit](https://streamlit.io/).

Cubre las **63 actividades** distribuidas en 4 fases de implementación (12 meses), el inventario de **45 documentos base** y **30 formatos operativos**, y la exportación de reportes CSV.

**Normas de referencia:** NTC 5801 · ISO 56002 · ISO 17034 · ISO 17043

### Estructura del proyecto

```
sgi-iiad/
├── app.py              # Código principal de la aplicación
├── sgi_state.json      # Estado del sistema (se genera automáticamente)
├── requirements.txt    # Dependencias Python
└── README.md           # Este archivo
```

### `requirements.txt`

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
```

---

## 2. Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/sgi-iiad.git
cd sgi-iiad

# Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
streamlit run app.py
```

La aplicación abre en **http://localhost:8501**.
En modo local el estado se guarda automáticamente en `sgi_state.json`.

---

## 3. Páginas de la Aplicación

La barra lateral izquierda contiene el menú de navegación principal:

| Página | Descripción |
|--------|-------------|
| **Dashboard** | Resumen ejecutivo: KPIs, gráficas de avance y hitos por fase |
| **Fase 1 — Fundamentos** | Checklist Meses 1–3: contexto, política, estrategia (18 act.) |
| **Fase 2 — Apoyo Estratégico** | Checklist Meses 4–6: planificación, recursos, documentación (23 act.) |
| **Fase 3 — Operación** | Checklist Meses 7–9: procesos operativos + MinCiencias (16 act.) |
| **Fase 4 — Evaluación y Mejora** | Checklist Meses 10–12: auditoría, revisión, mejora (16 act.) |
| **Registro Documental** | 45 documentos base + 30 formatos con estado y códigos SGC |
| **Reportes y Exportar** | Tablas de resumen, gráfica mensual y exportación a CSV |
| **Configuración** | Logo institucional, códigos SGC personalizados, info del sistema |

> La barra lateral siempre muestra el **avance global actualizado**, la barra de progreso y los controles de guardar/cargar el JSON.

---

## 4. Cómo Usar el Checklist de Actividades

### 4.1 Cambiar el estado de una actividad

Cada actividad muestra en su fila principal un selector con cuatro opciones:

| Estado | Significado |
|--------|-------------|
| ⬜ Pendiente | La actividad no ha comenzado |
| 🔄 En proceso | La actividad está en ejecución |
| ✅ Completo | La actividad está terminada y tiene evidencia |
| ⛔ No aplica | La actividad no aplica al contexto del laboratorio |

> Al cambiar el estado, el sistema guarda y recalcula los indicadores de avance automáticamente.
> Las actividades **"No aplica"** se excluyen del denominador del porcentaje de avance.

### 4.2 Registrar detalles de una actividad *(nuevo en v2.0)*

Haz clic en el expander **`📝 Detalles — [ID]: [nombre de la actividad]...`**

Se abre un panel con cinco campos:

```
┌─────────────────┬──────────────────┬───────────────────────┬──────────────────┐
│  Fecha inicio   │  Fecha fin/cierre │  Nombre responsable   │   Rol / Cargo    │
├─────────────────┴──────────────────┴───────────────────────┴──────────────────┤
│  Comentario / Enlace de evidencia (SharePoint, Teams, OneDrive...)             │
├────────────────────────────────────────────────────────────────────────────────┤
│  📌 Evidencia esperada según NTC 5801: [referencia]                            │
└────────────────────────────────────────────────────────────────────────────────┘
```

**Descripción de cada campo:**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Fecha inicio** | Selector de calendario — formato DD/MM/AAAA | `01/03/2026` |
| **Fecha fin/cierre** | Fecha real de cierre o entrega del entregable | `15/03/2026` |
| **Nombre responsable** | Nombre completo de la persona asignada | `María Torres` |
| **Rol / Cargo** | Función institucional de la persona | `Líder SGI` |
| **Comentario / Enlace** | URL de SharePoint/Teams/OneDrive o texto libre | `https://...` |

> ⚠️ **Importante:** Presiona el botón azul **"Guardar detalles"** para confirmar los cambios.

**Comportamiento adicional:**
- Si el campo "Comentario" contiene una URL (`http...`), aparece automáticamente un enlace **"Ver evidencia →"** clicable.
- Una vez guardados, la fila principal muestra **badges** con el nombre del responsable y las fechas como resumen rápido.
- La evidencia esperada según NTC 5801 aparece al pie del panel como referencia normativa.

### 4.3 Filtros del checklist

| Filtro | Función |
|--------|---------|
| **Estado** | Muestra solo actividades con los estados seleccionados |
| **Buscar** | Filtra por texto libre en el nombre de la actividad |
| **Responsable** | Filtra por el responsable por defecto definido en el sistema |

---

## 5. Registro Documental y Códigos SGC

### 5.1 Pestañas disponibles

| Pestaña | Contenido |
|---------|-----------|
| **Documentos Base (45)** | Procedimientos, manuales, planes y declaraciones formales |
| **Formatos Operativos (30)** | Plantillas, fichas, actas y registros operativos |

### 5.2 Cambiar el estado de un documento

Selector en la columna **"Estado"** de cada fila. Mismos cuatro valores que el checklist.

### 5.3 Personalizar los códigos al SGC del laboratorio *(nuevo en v2.0)*

El sistema incluye códigos por defecto (`DOC-01…DOC-45`, `FTO-01…FTO-30`). Para alinearlos a la codificación de tu SGC:

1. Activa el toggle **"✏️ Editar códigos SGC"** en la parte superior de la página
2. Aparece la columna **"Cod. SGC"** editable en cada fila
3. Escribe el código personalizado (ej: `LAB-IDI-001`, `IIAD-DOC-PRC-001`)
4. El cambio se guarda automáticamente al salir del campo
5. Desactiva el toggle para volver a la vista normal

**Comportamiento visual:**
- En vista normal los códigos personalizados se muestran en **negrita**
- El código original `DOC-XX` permanece visible como referencia cruzada
- El CSV de exportación incluye ambas columnas: `Cod. Original` y `Cod. SGC`

> Para restablecer todos los códigos: **Configuración → "Códigos personalizados del SGC" → "Restablecer todos los códigos"**

---

## 6. Logo Institucional *(nuevo en v2.0)*

### Subir el logo

1. Ve a la página **Configuración**
2. Sección **"Logo institucional"** → clic en *Browse files* o arrastra el archivo
3. Formatos aceptados: `PNG`, `JPG`
4. El logo aparece inmediatamente en la parte superior del sidebar

**Especificaciones recomendadas:**

| Parámetro | Recomendación |
|-----------|---------------|
| Formato | PNG con fondo transparente o blanco |
| Resolución mínima | 400 × 150 px |
| Proporción | Horizontal / apaisada |
| Peso máximo | 500 KB |

### Cómo se almacena

El logo se convierte a **base64** y se guarda dentro del `sgi_state.json`. Esto significa que el logo *viaja junto al estado* cuando compartes el archivo JSON con tu equipo — quien lo cargue verá el logo automáticamente.

### Quitar el logo

**Configuración → "Logo institucional" → "Quitar logo"**

---

## 7. Exportar e Importar el Estado JSON

Todo el estado del sistema (avance, fechas, responsables, códigos SGC y logo) vive en un único archivo `sgi_state.json`.

### 7.1 Descargar el estado actual

**Sidebar → "Guardar progreso" → "Descargar sgi_state.json"**

El archivo se descarga con timestamp: `sgi_state_20260219_1430.json`

### 7.2 Cargar un estado guardado

**Sidebar → "Cargar progreso" → cargador de archivos**

Selecciona el archivo JSON. La app carga el estado y actualiza todos los indicadores.

> ⚠️ Streamlit Cloud reinicia el servidor periódicamente. **Siempre descarga el JSON al terminar la sesión** y cárgalo al inicio de la siguiente.

### 7.3 Exportar a CSV

En **Reportes y Exportar → sección "Exportar"**:

| Archivo | Columnas incluidas |
|---------|-------------------|
| **Actividades CSV** | Fase, ID, actividad, ref. NTC, responsable sistema, responsable asignado, rol, plazo, fecha inicio, fecha fin, estado, evidencia esperada, comentario/enlace |
| **Documentos CSV** | Código original, código SGC, nombre, fase, estado |

Ambos archivos son abribles directamente en **Excel**.

---

## 8. Flujo de Trabajo Recomendado con OneDrive / Teams

### Estructura de carpetas sugerida

```
OneDrive — sitio del equipo IIAD
└── SGI-IIAD/
    ├── estados/
    │   ├── sgi_state_20260301_0900.json
    │   ├── sgi_state_20260315_1430.json
    │   └── sgi_state_AAAAMMDD_HHMM.json   ← versión más reciente
    ├── evidencias/
    │   ├── Fase_1/   (DOC-01 al DOC-08, FTO-01 al FTO-05)
    │   ├── Fase_2/   (DOC-09 al DOC-24, FTO-06 al FTO-14)
    │   ├── Fase_3/   (DOC-25 al DOC-33, FTO-15 al FTO-24)
    │   └── Fase_4/   (DOC-34 al DOC-45, FTO-25 al FTO-30)
    └── README.md
```

### Flujo por reunión de seguimiento

**Antes:**
1. Abre la app en el navegador
2. Sidebar → carga el JSON más reciente desde OneDrive
3. Revisa el Dashboard para preparar el informe de avance

**Durante:**
1. Cambia el estado de las actividades revisadas
2. Abre el expander de detalles y registra fechas, responsable y enlace de evidencia
3. Usa el filtro **"Estado: En proceso"** para enfocarse en lo activo

**Al terminar:**
1. Sidebar → **"Descargar sgi_state.json"**
2. Sube el archivo a `OneDrive/SGI-IIAD/estados/`
3. Comparte el enlace con el equipo si es necesario

### Convención para el campo "Comentario / Enlace evidencia"

```
https://tu-tenant.sharepoint.com/sites/IIAD/.../DOC-01_Analisis_contexto_v2.docx
```
> Si el campo empieza por `http`, la app lo convierte automáticamente en enlace clicable.

---

## 9. Despliegue en Streamlit Cloud

### Estructura mínima del repositorio

```
repo/
├── app.py
└── requirements.txt
```

### Actualizar la aplicación desplegada

```bash
git add app.py
git commit -m "feat: descripcion del cambio"
git push origin main
# Streamlit Cloud redespliega automáticamente en ~1 minuto
```

### Secrets (para integraciones futuras)

*Streamlit Cloud → Settings → Secrets* (formato TOML):

```toml
[general]
institution_name = "Laboratorio IIAD"
```

---

## 10. Preguntas Frecuentes

**¿Por qué se pierde el progreso al recargar la página?**
Streamlit Cloud reinicia el servidor periódicamente. El estado se mantiene en la sesión activa pero no persiste entre sesiones. Descarga el JSON al terminar y cárgalo al inicio de la siguiente sesión.

**¿Puedo usar la app sin conexión a internet?**
Sí, ejecutando `streamlit run app.py` en tu máquina local. El estado se guarda automáticamente en `sgi_state.json` en la carpeta del proyecto.

**¿Cómo adapto las actividades o documentos a mi proceso real?**
Edita el diccionario `PHASES` y la lista `DOCUMENTS` en `app.py`. Cada actividad es un `dict` con las claves: `id`, `activity`, `ref`, `responsible`, `deadline`, `evidence`.

**¿El archivo JSON se puede abrir en Excel?**
No directamente. Usa **Reportes → Exportar CSV** para obtener archivos abribles en Excel con todos los campos incluyendo fechas, responsables y códigos SGC.

**¿Cómo relaciono las actividades con MinCiencias?**
Las actividades **3.13 a 3.16** de la Fase 3 cubren el registro en InstituLAC, GrupLAC y CvLAC. Usa el campo "Comentario / Enlace evidencia" para pegar la URL del perfil en la plataforma ScienTI.

**¿Qué pasa si restablezco los códigos SGC?**
Los códigos vuelven a `DOC-01`, `FTO-01`, etc. Los estados de los documentos se conservan intactos — solo cambia la visualización del código.

**¿Cuántas personas pueden usar la app al mismo tiempo?**
La app en Streamlit Cloud es de usuario único por sesión. Para trabajo colaborativo cada persona trabaja en su sesión, descarga su JSON y se consolida al final. En el futuro se puede migrar a una base de datos compartida (SQLite, SharePoint API, etc.).

---

## 11. Historial de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| **1.0** | Feb 2026 | Versión inicial: checklist 4 fases, registro documental, dashboard con KPIs y gráficas, persistencia JSON |
| **2.0** | Feb 2026 | ✅ Fechas inicio/fin por actividad · ✅ Nombre responsable asignado y rol/cargo · ✅ Campo comentario/enlace evidencia con link clicable · ✅ Logo institucional (upload, base64 en JSON, sidebar) · ✅ Códigos SGC editables en Registro Documental · ✅ Página de Configuración · ✅ CSV enriquecido con todos los campos nuevos |

---

<div align="center">
  <sub>Sistema desarrollado para el área IIAD · Implementación NTC 5801:2018 / ISO 56002:2019</sub>
</div>
