# SGI I+D+I - IIAD
## Sistema de Gestion de la Investigacion, Desarrollo e Innovacion
**NTC 5801 / ISO 56002 | Laboratorio IIAD**
**Version 2.0 | Febrero 2026**

URL: https://implementacion-sg-idi-iiad-lania-v1.streamlit.app/

---

## INDICE

1. Descripcion general
2. Instalacion local
3. Paginas de la aplicacion
4. Como usar el checklist de actividades
5. Registro Documental y codigos SGC
6. Logo institucional
7. Exportar e importar el estado (JSON)
8. Flujo de trabajo recomendado con OneDrive / Teams
9. Despliegue en Streamlit Cloud
10. Preguntas frecuentes
11. Historial de versiones

---

## 1. DESCRIPCION GENERAL

Aplicacion web interactiva para el seguimiento de la implementacion del Sistema de
Gestion de I+D+I del Laboratorio IIAD, construida sobre Streamlit.

Cubre las 63 actividades distribuidas en 4 fases (12 meses), el inventario de
45 documentos base y 30 formatos operativos, y la exportacion de reportes CSV.

Normas de referencia: NTC 5801, ISO 56002, ISO 17034, ISO 17043.

Estructura del proyecto:

    sgi-iiad/
    |-- app.py              <- Codigo principal de la aplicacion
    |-- sgi_state.json      <- Estado del sistema (se crea automaticamente)
    |-- requirements.txt    <- Dependencias Python
    |-- README.txt          <- Este archivo

requirements.txt:

    streamlit>=1.32.0
    pandas>=2.0.0
    plotly>=5.18.0

---

## 2. INSTALACION LOCAL

    git clone https://github.com/tu-usuario/sgi-iiad.git
    cd sgi-iiad
    python -m venv venv
    source venv/bin/activate          # Mac / Linux
    venv\Scriptsctivate             # Windows
    pip install -r requirements.txt
    streamlit run app.py

La aplicacion abre en http://localhost:8501
En modo local el estado se guarda automaticamente en sgi_state.json.

---

## 3. PAGINAS DE LA APLICACION

Barra lateral izquierda -> menu de navegacion:

  Dashboard               Resumen ejecutivo: KPIs, graficas de avance y hitos por fase
  Fase 1 - Fundamentos    Checklist Meses 1-3: contexto, politica, estrategia (18 act.)
  Fase 2 - Apoyo          Checklist Meses 4-6: planificacion, recursos, docs (23 act.)
  Fase 3 - Operacion      Checklist Meses 7-9: procesos operativos, MinCiencias (16 act.)
  Fase 4 - Evaluacion     Checklist Meses 10-12: auditoria, revision, mejora (16 act.)
  Registro Documental     45 documentos base + 30 formatos con estado y codigos SGC
  Reportes y Exportar     Tablas de resumen, grafica mensual y exportacion a CSV
  Configuracion           Logo institucional, codigos SGC, informacion del sistema

La barra lateral siempre muestra el avance global actualizado, la barra de
progreso y los controles de guardar/cargar el archivo JSON.

---

## 4. COMO USAR EL CHECKLIST DE ACTIVIDADES

=== 4.1 Cambiar el estado ===

Cada actividad tiene un selector en la columna "Estado":

  Pendiente    La actividad no ha comenzado
  En proceso   La actividad esta en ejecucion
  Completo     La actividad esta terminada y tiene evidencia
  No aplica    La actividad no aplica al contexto del laboratorio

Al cambiar el estado el sistema guarda y recalcula los indicadores de avance.
Las actividades "No aplica" se excluyen del denominador del porcentaje.

=== 4.2 Registrar detalles de una actividad (NUEVO v2.0) ===

Haz clic en el expander que dice:
    "Detalles -- [ID]: [nombre de la actividad]..."

Se abre un panel con cinco campos:

  Fecha inicio        Selector de calendario (formato DD/MM/AAAA)
  Fecha fin/cierre    Selector de calendario (formato DD/MM/AAAA)
  Nombre responsable  Nombre completo de la persona asignada
  Rol / Cargo         Funcion institucional (ej: Lider SGI, Investigador Principal)
  Comentario /        Campo libre: pega la URL de SharePoint/Teams/OneDrive
  Enlace evidencia    o escribe observaciones del estado de la actividad

  -> Si el campo "Comentario" contiene una URL (empieza por http),
     aparece automaticamente un enlace clicable "Ver evidencia".

  -> La referencia normativa de la evidencia esperada segun NTC 5801
     se muestra en la parte inferior del panel como guia.

IMPORTANTE: Presiona el boton azul "Guardar detalles" para confirmar.
Sin este paso los campos no se persisten.

Una vez guardados, la fila principal muestra badges con el nombre del
responsable y las fechas de inicio y fin como resumen rapido.

=== 4.3 Filtros del checklist ===

En la parte superior de cada pagina de fase hay tres filtros:

  Estado       Muestra solo actividades con los estados seleccionados
  Buscar       Filtra por texto libre en el nombre de la actividad
  Responsable  Filtra por el responsable por defecto del sistema

---

## 5. REGISTRO DOCUMENTAL Y CODIGOS SGC

=== 5.1 Pestanas ===

  Documentos Base (45)      Procedimientos, manuales, planes, declaraciones formales
  Formatos Operativos (30)  Plantillas, fichas, actas y registros operativos

=== 5.2 Cambiar estado de un documento ===

Selector en la columna "Estado" de cada fila. Mismos cuatro valores que el checklist.

=== 5.3 Personalizar los codigos al SGC del laboratorio (NUEVO v2.0) ===

El sistema usa codigos por defecto: DOC-01...DOC-45 y FTO-01...FTO-30.
Para alinearlos a la codificacion de tu Sistema de Gestion de Calidad:

  1. Activa el toggle "Editar codigos SGC" en la parte superior de la pagina
  2. Aparece la columna "Cod. SGC" editable en cada fila
  3. Escribe el codigo personalizado (ej: LAB-IDI-001, IIAD-DOC-PRC-001)
  4. El cambio se guarda automaticamente al salir del campo de texto
  5. Desactiva el toggle para volver a la vista normal

Comportamiento visual:
  - Vista normal: codigos personalizados aparecen en NEGRITA
  - El codigo original DOC-XX permanece visible como referencia cruzada
  - Los CSV de exportacion incluyen ambas columnas: "Cod. Original" y "Cod. SGC"

Para restablecer todos los codigos al valor original:
  Configuracion -> "Codigos personalizados del SGC" -> "Restablecer todos los codigos"

---

## 6. LOGO INSTITUCIONAL (NUEVO v2.0)

=== 6.1 Subir el logo ===

  1. Ve a la pagina "Configuracion"
  2. Seccion "Logo institucional" -> clic en "Browse files" o arrastra el archivo
  3. Formatos aceptados: PNG, JPG
  4. El logo aparece inmediatamente en la parte superior del sidebar

Especificaciones recomendadas:
  - Formato: PNG con fondo transparente o blanco
  - Resolucion minima: 400 x 150 px (proporcion horizontal / apaisada)
  - Peso maximo recomendado: 500 KB

=== 6.2 Como se almacena ===

El logo se convierte a formato base64 y se guarda DENTRO del sgi_state.json.
Esto significa que el logo "viaja" junto al estado cuando compartes el archivo
JSON con tu equipo: quien lo cargue vera el logo automaticamente.

=== 6.3 Quitar el logo ===

Configuracion -> "Logo institucional" -> boton "Quitar logo".

---

## 7. EXPORTAR E IMPORTAR EL ESTADO (JSON)

El estado completo (avance, fechas, responsables, codigos SGC, logo) vive
en el archivo sgi_state.json. Trabaja siempre con este archivo.

=== 7.1 Descargar el estado actual ===

Sidebar -> seccion "Guardar progreso" -> "Descargar sgi_state.json"
El archivo se descarga con timestamp: sgi_state_20260219_1430.json

=== 7.2 Cargar un estado guardado ===

Sidebar -> seccion "Cargar progreso" -> cargador de archivos
Selecciona el archivo JSON. La app carga el estado y actualiza todo.

IMPORTANTE: Streamlit Cloud reinicia el servidor periodicamente y borra el
estado local de la sesion. Siempre descarga el JSON al terminar y cargalo
al inicio de la siguiente sesion.

=== 7.3 Exportar a CSV ===

Pagina "Reportes y Exportar" -> seccion "Exportar":

  Actividades CSV    Todas las actividades con: fase, ID, actividad, referencia
                     NTC, responsable asignado, rol, fechas, estado, evidencia
                     esperada, comentario/enlace.

  Documentos CSV     Todos los documentos y formatos con: codigo original,
                     codigo SGC personalizado, nombre, fase y estado.

Ambos archivos son abribles directamente en Excel.

---

## 8. FLUJO DE TRABAJO RECOMENDADO CON ONEDRIVE / TEAMS

=== Estructura de carpetas sugerida ===

  OneDrive - sitio del equipo IIAD
  |-- SGI-IIAD/
      |-- estados/
      |   |-- sgi_state_20260301_0900.json
      |   |-- sgi_state_20260315_1430.json
      |   |-- sgi_state_AAAAMMDD_HHMM.json   <- version mas reciente
      |-- evidencias/
      |   |-- Fase_1/  (DOC-01 al DOC-08, FTO-01 al FTO-05)
      |   |-- Fase_2/  (DOC-09 al DOC-24, FTO-06 al FTO-14)
      |   |-- Fase_3/  (DOC-25 al DOC-33, FTO-15 al FTO-24)
      |   |-- Fase_4/  (DOC-34 al DOC-45, FTO-25 al FTO-30)
      |-- README.txt

=== Antes de una reunion de seguimiento ===

  1. Abre: https://implementacion-sg-idi-iiad-lania-v1.streamlit.app/
  2. Sidebar -> cargador -> selecciona el JSON mas reciente de OneDrive
  3. Revisa el Dashboard para preparar el informe de avance
  4. Proyecta el Dashboard durante la reunion

=== Durante la reunion ===

  1. Para cada actividad revisada: cambia el estado en el selector
  2. Abre el expander de detalles y registra:
       - Fechas de inicio o cierre
       - Nombre del responsable asignado
       - Enlace al documento en SharePoint/OneDrive/Teams
  3. Usa el filtro "Estado: En proceso" para enfocarse en lo activo

=== Al terminar la reunion ===

  1. Sidebar -> "Descargar sgi_state.json"
  2. El archivo baja con fecha y hora: sgi_state_AAAAMMDD_HHMM.json
  3. Subelo a OneDrive/SGI-IIAD/estados/
  4. Comparte el enlace con el equipo si es necesario

=== Convencion para el campo "Comentario / Enlace evidencia" ===

Recomendado pegar la URL completa del archivo en SharePoint o Teams:

  https://tu-tenant.sharepoint.com/sites/IIAD/.../DOC-01_Analisis_contexto_v2.docx

Si el campo empieza por "http" la app lo convierte en enlace clicable.

---

## 9. DESPLIEGUE EN STREAMLIT CLOUD

=== Estructura minima del repositorio GitHub ===

  repo/
  |-- app.py
  |-- requirements.txt

=== Actualizar la aplicacion desplegada ===

  git add app.py
  git commit -m "feat: descripcion del cambio"
  git push origin main

Streamlit Cloud redespliega automaticamente en aproximadamente 1 minuto.

=== Secrets (opcional, para integraciones futuras) ===

Streamlit Cloud -> Settings -> Secrets (formato TOML):

  [general]
  institution_name = "Laboratorio IIAD"

---

## 10. PREGUNTAS FRECUENTES

P: Por que se pierde el progreso al recargar la pagina?
R: Streamlit Cloud reinicia el servidor periodicamente. El estado se mantiene
   en la sesion activa pero no persiste entre sesiones. Descarga el JSON al
   final de cada sesion y cargalo al inicio de la siguiente.

P: Puedo usar la app sin conexion a internet?
R: Si, ejecutando "streamlit run app.py" en tu maquina local. El estado se
   guarda automaticamente en sgi_state.json en la misma carpeta del proyecto.

P: Como adapto las actividades o documentos a mi proceso real?
R: Edita los diccionarios PHASES y la lista DOCUMENTS en app.py. Cada actividad
   es un dict con las claves: id, activity, ref, responsible, deadline, evidence.

P: El archivo JSON se puede abrir en Excel?
R: No directamente. Usa la funcion "Reportes -> Exportar CSV" para obtener
   archivos abribles en Excel con todos los campos incluyendo fechas y codigos SGC.

P: Como relaciono las actividades con MinCiencias?
R: Las actividades 3.13 a 3.16 de la Fase 3 cubren el registro en InstituLAC,
   GrupLAC y CvLAC. Usa el campo "Comentario / Enlace evidencia" para pegar
   la URL del perfil en la plataforma ScienTI de MinCiencias.

P: Que pasa si restablezco los codigos SGC?
R: Los codigos vuelven a DOC-01, FTO-01, etc. Los estados de los documentos
   se conservan intactos. Solo cambia la visualizacion del codigo.

P: Cuantas personas pueden usar la app al mismo tiempo?
R: La app en Streamlit Cloud es de usuario unico por sesion. Para trabajo
   colaborativo en tiempo real, cada persona trabaja en su sesion, descarga
   su JSON y se consolida al final. En el futuro se puede migrar a una base
   de datos compartida (SQLite, Airtable, SharePoint API).

---

## 11. HISTORIAL DE VERSIONES

  Version  Fecha          Cambios
  -------  -------------  ---------------------------------------------------------
  1.0      Feb 2026       Version inicial: checklist 4 fases, registro documental,
                          dashboard con KPIs y graficas, persistencia JSON
  2.0      Feb 2026       + Fechas inicio/fin por actividad
                          + Nombre responsable asignado y rol/cargo por actividad
                          + Campo comentario/enlace evidencia con link clicable
                          + Logo institucional (upload, base64 en JSON, sidebar)
                          + Codigos SGC editables en Registro Documental
                          + Pagina de Configuracion
                          + CSV de exportacion enriquecido (fechas, responsables,
                            codigos SGC, enlace evidencia)

---

Sistema desarrollado para el area IIAD del Laboratorio de Referencia.
Implementacion: NTC 5801:2018 / ISO 56002:2019
Para soporte: abre un Issue en el repositorio GitHub o contacta al Lider SGI.
