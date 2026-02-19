# 🔬 SGI I+D+I — IIAD
### Sistema de Gestión de la Investigación, Desarrollo e Innovación
**NTC 5801 / ISO 56002 | Laboratorio IIAD | Versión 3.0**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://implementacion-sg-idi-iiad-lania-v1.streamlit.app/)

---

## Índice
- [Descripción general](#1-descripción-general)
- [Instalación local](#2-instalación-local)
- [GitHub Sync — configuración](#3-github-sync--auto-carga-del-estado)
- [Páginas de la aplicación](#4-páginas-de-la-aplicación)
- [Checklist de actividades](#5-cómo-usar-el-checklist-de-actividades)
- [Registro Documental y códigos SGC](#6-registro-documental-y-códigos-sgc)
- [Logo institucional](#7-logo-institucional)
- [Flujo de trabajo con OneDrive / Teams](#8-flujo-de-trabajo-recomendado)
- [Preguntas frecuentes](#9-preguntas-frecuentes)
- [Historial de versiones](#10-historial-de-versiones)

---

## 1. Descripción General

Aplicación web interactiva para el seguimiento de la implementación del **Sistema de Gestión de I+D+I** del Laboratorio IIAD, construida con [Streamlit](https://streamlit.io/).

Cubre las **63 actividades** distribuidas en 4 fases de implementación (12 meses), el inventario de **45 documentos base** y **30 formatos operativos**, y la exportación de reportes CSV.

**Normas de referencia:** NTC 5801 · ISO 56002 · ISO 17034 · ISO 17043

### Estructura del proyecto

```
sgi-iiad/
├── app.py              # Código principal de la aplicación
├── sgi_state.json      # Estado del sistema (versionado en GitHub)
├── requirements.txt    # Dependencias Python
└── README.md           # Este archivo
```

### `requirements.txt`

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
requests>=2.31.0
```

---

## 2. Instalación Local

```bash
git clone https://github.com/tu-usuario/sgi-iiad.git
cd sgi-iiad
python -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
streamlit run app.py
```

La app abre en **http://localhost:8501**.

---

## 3. GitHub Sync — Auto-carga del Estado

### Cómo funciona

Con GitHub Sync activo, la app **carga el JSON automáticamente al abrir** sin buscar ni subir ningún archivo. Todo el historial queda en los commits del repo.

```
Abrir app  →  ☁️ Carga automática desde GitHub  →  Trabajar
Terminar   →  💾 "Guardar"  →  Commit automático al repo
```

### Paso 1 — Crear el Personal Access Token (PAT)

1. GitHub → tu avatar → **Settings** → **Developer settings**
2. **Personal access tokens** → **Tokens (classic)** → **Generate new token**
3. Nombre sugerido: `sgi-iiad-streamlit`
4. Scope requerido: ✅ **`repo`** (solo este)
5. Expiration: 1 año recomendado
6. Copiar el token (`ghp_xxxxxxxxxxxx`) — solo se muestra una vez

### Paso 2 — Agregar Secrets en Streamlit Cloud

1. Streamlit Cloud → tu app → **Settings** → **Secrets**
2. Pegar y completar:

```toml
GITHUB_TOKEN     = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GITHUB_REPO      = "tu-usuario/sgi-iiad"
GITHUB_FILE_PATH = "sgi_state.json"
GITHUB_BRANCH    = "main"
```

3. Clic en **Save** → la app se reinicia automáticamente

### Paso 3 — Inicializar el archivo en el repo

Si `sgi_state.json` aún no existe en el repo:

```bash
echo "{}" > sgi_state.json
git add sgi_state.json
git commit -m "chore: inicializar estado SGI"
git push origin main
```

### Controles en el Sidebar

| Control | Descripción |
|---------|-------------|
| **☁️ GitHub activo** (badge verde) | Sesión sincronizada con el repo |
| **⚠️ Sin sincronizar** (badge gris) | Hay cambios locales pendientes de guardar |
| **🔄 Recargar** | Trae el estado más reciente del repo (descarta cambios locales) |
| **💾 Guardar** | Crea un commit en GitHub con el estado actual |
| **⬇️ Descargar sgi_state.json** | Respaldo local siempre disponible |

> **Sin GitHub configurado:** la app funciona en modo local — descarga manual del JSON y carga con el file uploader del sidebar.

---

## 4. Páginas de la Aplicación

| Página | Descripción |
|--------|-------------|
| **Dashboard** | KPIs globales, gráficas de avance por fase, hitos |
| **Fase 1 — Fundamentos** | Checklist Meses 1–3 (18 actividades) |
| **Fase 2 — Apoyo Estratégico** | Checklist Meses 4–6 (23 actividades) |
| **Fase 3 — Operación** | Checklist Meses 7–9 (16 actividades) |
| **Fase 4 — Evaluación y Mejora** | Checklist Meses 10–12 (16 actividades) |
| **Registro Documental** | 45 documentos + 30 formatos con estado y códigos SGC |
| **Reportes y Exportar** | Resúmenes y exportación CSV |
| **Configuración** | Logo, códigos SGC, estado GitHub Sync |

---

## 5. Cómo Usar el Checklist de Actividades

### 5.1 Cambiar el estado

| Estado | Significado |
|--------|-------------|
| ⬜ Pendiente | No ha comenzado |
| 🔄 En proceso | En ejecución |
| ✅ Completo | Terminada con evidencia |
| ⛔ No aplica | Excluida del cálculo de avance |

### 5.2 Registrar detalles *(v2.0)*

Clic en el expander **`📝 Detalles — [ID]: [actividad]...`**

```
┌──────────────┬──────────────────┬──────────────────────┬──────────────┐
│ Fecha inicio │ Fecha fin/cierre │  Nombre responsable  │  Rol/Cargo   │
├──────────────┴──────────────────┴──────────────────────┴──────────────┤
│  Comentario / Enlace de evidencia (SharePoint, Teams, OneDrive...)     │
└────────────────────────────────────────────────────────────────────────┘
```

> Si el campo "Comentario" contiene una URL, aparece automáticamente como enlace clicable.
> Presiona **"Guardar detalles"** para confirmar los cambios.

---

## 6. Registro Documental y Códigos SGC

Activa el toggle **"✏️ Editar códigos SGC"** para personalizar los códigos a tu SGC:

1. Se revela la columna **"Cod. SGC"** editable en cada fila
2. Escribe el código (ej: `LAB-IDI-001`) — se guarda al salir del campo
3. En vista normal los códigos personalizados aparecen en **negrita**
4. El CSV de exportación incluye `Cod. Original` y `Cod. SGC`

> Restablecer: **Configuración → "Restablecer todos los códigos"**

---

## 7. Logo Institucional

1. **Configuración → Logo institucional → Browse files**
2. Formatos: `PNG`, `JPG` | Recomendado: fondo blanco, mínimo 400 × 150 px, máx 500 KB
3. El logo se almacena en base64 dentro del `sgi_state.json` → viaja con el estado al compartir el JSON

---

## 8. Flujo de Trabajo Recomendado

### Con GitHub Sync activo *(recomendado)*

```
Abrir app  →  Estado cargado automáticamente
Trabajar   →  Actualizar estados, detalles, responsables
Terminar   →  💾 "Guardar" en el sidebar  →  Commit al repo
```

### Sin GitHub Sync (modo manual)

```
Abrir app  →  Cargar JSON desde el sidebar
Trabajar   →  Actualizar estados y detalles
Terminar   →  ⬇️ Descargar JSON  →  Guardar en OneDrive/Teams
```

### Estructura de carpetas OneDrive (modo manual)

```
OneDrive — IIAD
└── SGI-IIAD/
    ├── estados/
    │   ├── sgi_state_20260301_0900.json
    │   └── sgi_state_AAAAMMDD_HHMM.json   ← más reciente
    └── evidencias/
        ├── Fase_1/
        ├── Fase_2/
        ├── Fase_3/
        └── Fase_4/
```

---

## 9. Preguntas Frecuentes

**¿Por qué se pierde el progreso al recargar?**
Con GitHub Sync activo, no se pierde — se recarga desde el repo. Sin GitHub, descarga el JSON al terminar y cárgalo al inicio.

**¿El JSON en GitHub es público?**
Si el repo es público, sí. Para datos sensibles usa un repo **privado** — GitHub permite repos privados gratuitos.

**¿Puedo usar la app sin conexión?**
Sí con `streamlit run app.py` en tu máquina local. El estado se guarda en `sgi_state.json` automáticamente.

**¿El JSON se puede abrir en Excel?**
No directamente. Usa **Reportes → Exportar CSV** para obtener archivos con todos los campos.

**¿Qué pasa si dos personas guardan al mismo tiempo?**
El último en guardar sobreescribe. Para equipos grandes se recomienda definir un "responsable del dashboard" que gestione los guardados.

---

## 10. Historial de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| **1.0** | Feb 2026 | Versión inicial: checklist 4 fases, registro documental, dashboard, JSON local |
| **2.0** | Feb 2026 | + Fechas/responsable/rol/evidencia · + Logo institucional · + Códigos SGC editables · + Página Configuración |
| **3.0** | Feb 2026 | + **GitHub Sync**: auto-carga al abrir, botones 🔄 Recargar / 💾 Guardar, badge de estado, secrets TOML, `requests` añadido a dependencias |

---

<div align="center">
  <sub>Sistema desarrollado para el área IIAD · Implementación NTC 5801:2018 / ISO 56002:2019</sub>
</div>
