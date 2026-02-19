import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json, os, base64
from datetime import datetime, date

st.set_page_config(page_title="SGI I+D+I - IIAD", page_icon="🔬", layout="wide")


# ---- DATA ----
PHASES = {
    "Fase 1": {
        "name": "Fundamentos y Diagnostico",
        "months": "Meses 1-3", "chapters": "Cap. 4 y 5 | NTC 5801 / ISO 56002",
        "color": "#1565C0", "hito": "Politica de I+D+I aprobada y comunicada",
        "items": [
            {"id":"1.1", "activity":"Equipo de implementacion conformado y designado", "ref":"S5.3", "responsible":"Direccion", "deadline":"Mes 1", "evidence":"Acta de designacion"},
            {"id":"1.2", "activity":"Capacitacion del equipo en NTC 5801 / ISO 56002", "ref":"S7.2", "responsible":"Lider SGI", "deadline":"Mes 1", "evidence":"Registro de asistencia"},
            {"id":"1.3", "activity":"Analisis PESTEL elaborado", "ref":"S4.1.2", "responsible":"Lider SGI", "deadline":"Mes 1", "evidence":"DOC-01"},
            {"id":"1.4", "activity":"Auditoria de capacidades internas realizada", "ref":"S4.1.3", "responsible":"Lider SGI", "deadline":"Mes 2", "evidence":"DOC-01"},
            {"id":"1.5", "activity":"Analisis de contexto externo e interno documentado (DOC-01)", "ref":"S4.1", "responsible":"Lider SGI", "deadline":"Mes 2", "evidence":"DOC-01 aprobado"},
            {"id":"1.6", "activity":"Partes interesadas identificadas y clasificadas", "ref":"S4.2", "responsible":"Equipo", "deadline":"Mes 2", "evidence":"DOC-02"},
            {"id":"1.7", "activity":"Necesidades y expectativas de partes interesadas documentadas", "ref":"S4.2.1", "responsible":"Equipo", "deadline":"Mes 2", "evidence":"DOC-02"},
            {"id":"1.8", "activity":"Mecanismos de interaccion con partes interesadas definidos", "ref":"S4.2.1c", "responsible":"Equipo", "deadline":"Mes 2", "evidence":"DOC-02"},
            {"id":"1.9", "activity":"Alcance del SGI determinado y documentado (DOC-03)", "ref":"S4.3", "responsible":"Direccion", "deadline":"Mes 2", "evidence":"DOC-03 aprobado"},
            {"id":"1.10","activity":"Interacciones con ISO 17034/17043 documentadas en el alcance", "ref":"S4.3c", "responsible":"Lider SGI", "deadline":"Mes 2", "evidence":"DOC-03"},
            {"id":"1.11","activity":"DOFA elaborado con insumos de analisis externo e interno", "ref":"S4.1", "responsible":"Equipo", "deadline":"Mes 3", "evidence":"DOC-04"},
            {"id":"1.12","activity":"DOFA cruzado (FO/FA/DO/DA) construido", "ref":"S4.1", "responsible":"Equipo", "deadline":"Mes 3", "evidence":"DOC-04"},
            {"id":"1.13","activity":"Vision de innovacion redactada y validada por la direccion", "ref":"S5.1.3", "responsible":"Direccion", "deadline":"Mes 3", "evidence":"DOC-05"},
            {"id":"1.14","activity":"Politica de I+D+I redactada, aprobada y firmada", "ref":"S5.2.1", "responsible":"Alta direccion", "deadline":"Mes 3", "evidence":"DOC-06 firmado"},
            {"id":"1.15","activity":"Politica comunicada a todo el personal", "ref":"S5.2.2", "responsible":"Comunicaciones", "deadline":"Mes 3", "evidence":"Registro difusion"},
            {"id":"1.16","activity":"Estrategia de innovacion documentada", "ref":"S5.1.4", "responsible":"Direccion", "deadline":"Mes 3", "evidence":"DOC-07"},
            {"id":"1.17","activity":"Roles y responsabilidades del SGI definidos (Matriz RACI)", "ref":"S5.3", "responsible":"Direccion", "deadline":"Mes 3", "evidence":"DOC-08"},
            {"id":"1.18","activity":"FTO-01 al FTO-05 disenados y aprobados", "ref":"S7.5", "responsible":"Lider SGI", "deadline":"Mes 3", "evidence":"Formatos en listado maestro"},
        ],
    },
    "Fase 2": {
        "name": "Documentacion Estrategica y de Apoyo",
        "months": "Meses 4-6", "chapters": "Cap. 6 y 7 | NTC 5801 / ISO 56002",
        "color": "#2E7D32", "hito": "Sistema documental base aprobado + personal capacitado",
        "items": [
            {"id":"2.1", "activity":"Riesgos y oportunidades del SGI identificados", "ref":"S6.1", "responsible":"Lider SGI", "deadline":"Mes 4", "evidence":"DOC-09"},
            {"id":"2.2", "activity":"Matriz de riesgos con valoracion (probabilidad x impacto) elaborada", "ref":"S6.1", "responsible":"Equipo", "deadline":"Mes 4", "evidence":"DOC-09"},
            {"id":"2.3", "activity":"Planes de tratamiento de riesgos definidos", "ref":"S6.1", "responsible":"Equipo", "deadline":"Mes 4", "evidence":"DOC-09"},
            {"id":"2.4", "activity":"Objetivos de innovacion SMART definidos (min. 3)", "ref":"S6.2.1", "responsible":"Direccion", "deadline":"Mes 4", "evidence":"DOC-10"},
            {"id":"2.5", "activity":"Planes de accion para cada objetivo elaborados", "ref":"S6.2.2", "responsible":"Lider SGI", "deadline":"Mes 4", "evidence":"DOC-10"},
            {"id":"2.6", "activity":"Estructura organizacional para I+D+I definida", "ref":"S6.3", "responsible":"Direccion", "deadline":"Mes 4", "evidence":"DOC-11"},
            {"id":"2.7", "activity":"Portafolio inicial de proyectos estructurado (horizontes 1/2/3)", "ref":"S6.4", "responsible":"Lider SGI", "deadline":"Mes 5", "evidence":"DOC-12"},
            {"id":"2.8", "activity":"Procedimiento de gestion de recursos aprobado", "ref":"S7.1", "responsible":"Lider SGI", "deadline":"Mes 5", "evidence":"DOC-13"},
            {"id":"2.9", "activity":"Presupuesto anual de I+D+I elaborado y aprobado", "ref":"S7.1.5", "responsible":"Finanzas", "deadline":"Mes 5", "evidence":"DOC-14"},
            {"id":"2.10","activity":"Inventario de infraestructura habilitadora realizado", "ref":"S7.1.6", "responsible":"Lider SGI", "deadline":"Mes 5", "evidence":"DOC-15"},
            {"id":"2.11","activity":"Plan de gestion del conocimiento elaborado", "ref":"S7.1.4", "responsible":"Lider SGI", "deadline":"Mes 5", "evidence":"DOC-16"},
            {"id":"2.12","activity":"Matriz de competencias del personal diligenciada", "ref":"S7.2", "responsible":"RRHH", "deadline":"Mes 5", "evidence":"DOC-17"},
            {"id":"2.13","activity":"Brechas de competencia identificadas", "ref":"S7.2", "responsible":"RRHH", "deadline":"Mes 5", "evidence":"DOC-17"},
            {"id":"2.14","activity":"Plan de capacitacion elaborado para cubrir brechas", "ref":"S7.2", "responsible":"RRHH", "deadline":"Mes 5", "evidence":"DOC-18"},
            {"id":"2.15","activity":"Plan de comunicacion del SGI aprobado", "ref":"S7.4", "responsible":"Comunicaciones", "deadline":"Mes 6", "evidence":"DOC-19"},
            {"id":"2.16","activity":"Procedimiento de control de documentos aprobado", "ref":"S7.5", "responsible":"Lider SGI", "deadline":"Mes 6", "evidence":"DOC-20"},
            {"id":"2.17","activity":"Sistema de codificacion documental definido", "ref":"S7.5", "responsible":"Lider SGI", "deadline":"Mes 6", "evidence":"DOC-21"},
            {"id":"2.18","activity":"Listado maestro de documentos creado y en uso", "ref":"S7.5.3", "responsible":"Lider SGI", "deadline":"Mes 6", "evidence":"DOC-21 en Notion"},
            {"id":"2.19","activity":"Catalogo de herramientas de innovacion elaborado", "ref":"S7.6", "responsible":"Equipo", "deadline":"Mes 6", "evidence":"DOC-22"},
            {"id":"2.20","activity":"Procedimiento de vigilancia tecnologica aprobado", "ref":"S7.7", "responsible":"Lider SGI", "deadline":"Mes 6", "evidence":"DOC-23"},
            {"id":"2.21","activity":"Primera vigilancia tecnologica ejecutada y documentada", "ref":"S7.7", "responsible":"Lider SGI", "deadline":"Mes 6", "evidence":"Informe VT-001"},
            {"id":"2.22","activity":"Procedimiento de propiedad intelectual aprobado", "ref":"S7.8", "responsible":"Asesor juridico", "deadline":"Mes 6", "evidence":"DOC-24"},
            {"id":"2.23","activity":"FTO-06 al FTO-14 disenados y aprobados", "ref":"S7.5", "responsible":"Lider SGI", "deadline":"Mes 6", "evidence":"Formatos en listado"},
        ],
    },
    "Fase 3": {
        "name": "Documentacion Operativa e Implementacion",
        "months": "Meses 7-9", "chapters": "Cap. 8 | NTC 5801 / ISO 56002 + MinCiencias",
        "color": "#E65100", "hito": "Proyecto piloto de I+D+I en ejecucion",
        "items": [
            {"id":"3.1", "activity":"Manual de planificacion y control operacional aprobado", "ref":"S8.1", "responsible":"Lider SGI", "deadline":"Mes 7", "evidence":"DOC-25"},
            {"id":"3.2", "activity":"Procedimiento de gestion de iniciativas aprobado", "ref":"S8.2", "responsible":"Lider SGI", "deadline":"Mes 7", "evidence":"DOC-26"},
            {"id":"3.3", "activity":"Procedimiento de identificacion de oportunidades aprobado", "ref":"S8.3.2", "responsible":"Lider SGI", "deadline":"Mes 7", "evidence":"DOC-27"},
            {"id":"3.4", "activity":"Procedimiento de creacion de conceptos aprobado", "ref":"S8.3.3", "responsible":"Lider SGI", "deadline":"Mes 7", "evidence":"DOC-28"},
            {"id":"3.5", "activity":"Procedimiento de validacion de conceptos aprobado", "ref":"S8.3.4", "responsible":"Lider SGI", "deadline":"Mes 8", "evidence":"DOC-29"},
            {"id":"3.6", "activity":"Procedimiento de desarrollo de soluciones aprobado", "ref":"S8.3.5", "responsible":"Lider SGI", "deadline":"Mes 8", "evidence":"DOC-30"},
            {"id":"3.7", "activity":"Procedimiento de despliegue de soluciones aprobado", "ref":"S8.3.6", "responsible":"Lider SGI", "deadline":"Mes 8", "evidence":"DOC-31"},
            {"id":"3.8", "activity":"Manual de gestion de proyectos NTC 5802 aprobado", "ref":"NTC5802", "responsible":"Lider SGI", "deadline":"Mes 8", "evidence":"DOC-32"},
            {"id":"3.9", "activity":"Formato de formulacion de proyecto elaborado y probado", "ref":"NTC5802", "responsible":"Lider SGI", "deadline":"Mes 8", "evidence":"FTO-19 validado"},
            {"id":"3.10","activity":"Al menos 1 proyecto piloto formulado y en ejecucion", "ref":"S8.3", "responsible":"Investigador", "deadline":"Mes 9", "evidence":"Ficha de proyecto"},
            {"id":"3.11","activity":"Primera acta de comite de innovacion realizada", "ref":"S8.2", "responsible":"Lider SGI", "deadline":"Mes 9", "evidence":"FTO-23 diligenciado"},
            {"id":"3.12","activity":"FTO-15 al FTO-24 disenados y aprobados", "ref":"S7.5", "responsible":"Lider SGI", "deadline":"Mes 9", "evidence":"Formatos en listado"},
            {"id":"3.13","activity":"Laboratorio registrado en InstituLAC (MinCiencias)", "ref":"Ext.", "responsible":"Direccion", "deadline":"Mes 7", "evidence":"Constancia de registro"},
            {"id":"3.14","activity":"Grupo(s) de investigacion registrados en GrupLAC", "ref":"Ext.", "responsible":"Investigador lider", "deadline":"Mes 8", "evidence":"Ficha GrupLAC"},
            {"id":"3.15","activity":"CvLAC de todo el personal investigador actualizado", "ref":"Ext.", "responsible":"Investigadores", "deadline":"Mes 8", "evidence":"Perfiles activos"},
            {"id":"3.16","activity":"Productos de investigacion clasificados (tipologias MinCiencias)", "ref":"Ext.", "responsible":"Lider SGI", "deadline":"Mes 9", "evidence":"Listado clasificado"},
        ],
    },
    "Fase 4": {
        "name": "Evaluacion, Auditoria y Mejora",
        "months": "Meses 10-12", "chapters": "Cap. 9 y 10 | NTC 5801 / ISO 56002",
        "color": "#6A1B9A", "hito": "Primera auditoria interna + revision por la direccion",
        "items": [
            {"id":"4.1", "activity":"Procedimiento de seguimiento y medicion aprobado", "ref":"S9.1.1", "responsible":"Lider SGI", "deadline":"Mes 10", "evidence":"DOC-34"},
            {"id":"4.2", "activity":"Indicadores de I+D+I definidos (entrada, proceso, salida, impacto)", "ref":"S9.1.2", "responsible":"Lider SGI", "deadline":"Mes 10", "evidence":"DOC-35"},
            {"id":"4.3", "activity":"Linea base de indicadores establecida", "ref":"S9.1.2", "responsible":"Lider SGI", "deadline":"Mes 10", "evidence":"Registro inicial"},
            {"id":"4.4", "activity":"Dashboard de seguimiento en Notion implementado", "ref":"S9.1", "responsible":"Lider SGI", "deadline":"Mes 10", "evidence":"Base de datos activa"},
            {"id":"4.5", "activity":"Programa anual de auditorias elaborado", "ref":"S9.2", "responsible":"Auditor interno", "deadline":"Mes 10", "evidence":"DOC-38"},
            {"id":"4.6", "activity":"Auditor interno capacitado en NTC 5801", "ref":"S9.2", "responsible":"Direccion", "deadline":"Mes 10", "evidence":"Certificado o registro"},
            {"id":"4.7", "activity":"Lista de verificacion de auditoria interna elaborada (por capitulo)", "ref":"S9.2", "responsible":"Auditor interno", "deadline":"Mes 10", "evidence":"DOC-39"},
            {"id":"4.8", "activity":"Primera auditoria interna realizada", "ref":"S9.2", "responsible":"Auditor interno", "deadline":"Mes 11", "evidence":"DOC-40 (informe)"},
            {"id":"4.9", "activity":"No conformidades identificadas y registradas", "ref":"S10.2", "responsible":"Auditor interno", "deadline":"Mes 11", "evidence":"FTO-26"},
            {"id":"4.10","activity":"Planes de accion correctiva para NC elaborados", "ref":"S10.2", "responsible":"Responsables", "deadline":"Mes 11", "evidence":"FTO-27"},
            {"id":"4.11","activity":"Procedimiento de revision por la direccion aprobado", "ref":"S9.3", "responsible":"Direccion", "deadline":"Mes 11", "evidence":"DOC-41"},
            {"id":"4.12","activity":"Primera revision por la direccion realizada", "ref":"S9.3", "responsible":"Alta direccion", "deadline":"Mes 12", "evidence":"DOC-42 (acta)"},
            {"id":"4.13","activity":"Informe anual de desempeno del SGI elaborado", "ref":"S9.1.2", "responsible":"Lider SGI", "deadline":"Mes 12", "evidence":"DOC-36"},
            {"id":"4.14","activity":"Plan de mejora continua del SGI para el anio 2 elaborado", "ref":"S10.3", "responsible":"Equipo", "deadline":"Mes 12", "evidence":"DOC-45"},
            {"id":"4.15","activity":"FTO-25 al FTO-30 disenados y en uso", "ref":"S7.5", "responsible":"Lider SGI", "deadline":"Mes 12", "evidence":"Formatos en listado"},
            {"id":"4.16","activity":"Sistema completo listo para evaluacion ICONTEC", "ref":"S4-10", "responsible":"Lider SGI", "deadline":"Mes 12", "evidence":"45 documentos base"},
        ],
    },
}


DOCUMENTS = [
    {"code":"DOC-01","name":"Analisis de cuestiones externas e internas","phase":"Fase 1","chapter":"S4.1","type":"Procedimiento + Registro"},
    {"code":"DOC-02","name":"Matriz de partes interesadas y sus necesidades","phase":"Fase 1","chapter":"S4.2","type":"Registro vivo"},
    {"code":"DOC-03","name":"Documento de alcance del SGI","phase":"Fase 1","chapter":"S4.3","type":"Declaracion formal"},
    {"code":"DOC-04","name":"Analisis DOFA del laboratorio","phase":"Fase 1","chapter":"S4.1","type":"Registro interno"},
    {"code":"DOC-05","name":"Vision de innovacion","phase":"Fase 1","chapter":"S5.1.3","type":"Declaracion estrategica"},
    {"code":"DOC-06","name":"Politica de I+D+I","phase":"Fase 1","chapter":"S5.2.1","type":"Documento oficial"},
    {"code":"DOC-07","name":"Estrategia de innovacion","phase":"Fase 1","chapter":"S5.1.4","type":"Documento estrategico"},
    {"code":"DOC-08","name":"Matriz de roles, responsabilidades y autoridades","phase":"Fase 1","chapter":"S5.3","type":"Organigrama + RACI"},
    {"code":"DOC-09","name":"Matriz de riesgos y oportunidades del SGI","phase":"Fase 2","chapter":"S6.1","type":"Registro vivo"},
    {"code":"DOC-10","name":"Objetivos de innovacion SMART y planes de accion","phase":"Fase 2","chapter":"S6.2","type":"Plan formal"},
    {"code":"DOC-11","name":"Estructura organizacional para I+D+I","phase":"Fase 2","chapter":"S6.3","type":"Organigrama"},
    {"code":"DOC-12","name":"Portafolio inicial de iniciativas de innovacion","phase":"Fase 2","chapter":"S6.4","type":"Base de datos"},
    {"code":"DOC-13","name":"Procedimiento de gestion de recursos para I+D+I","phase":"Fase 2","chapter":"S7.1","type":"Procedimiento"},
    {"code":"DOC-14","name":"Presupuesto anual de I+D+I","phase":"Fase 2","chapter":"S7.1.5","type":"Plan financiero"},
    {"code":"DOC-15","name":"Inventario de infraestructura habilitadora de I+D+I","phase":"Fase 2","chapter":"S7.1.6","type":"Registro"},
    {"code":"DOC-16","name":"Plan de gestion del conocimiento","phase":"Fase 2","chapter":"S7.1.4","type":"Plan"},
    {"code":"DOC-17","name":"Matriz de competencias del personal en I+D+I","phase":"Fase 2","chapter":"S7.2","type":"Registro"},
    {"code":"DOC-18","name":"Plan anual de capacitacion y toma de conciencia","phase":"Fase 2","chapter":"S7.2","type":"Plan"},
    {"code":"DOC-19","name":"Plan de comunicacion interna y externa del SGI","phase":"Fase 2","chapter":"S7.4","type":"Plan"},
    {"code":"DOC-20","name":"Procedimiento de control de documentos y registros","phase":"Fase 2","chapter":"S7.5","type":"Procedimiento maestro"},
    {"code":"DOC-21","name":"Listado maestro de documentos","phase":"Fase 2","chapter":"S7.5.3","type":"Registro vivo"},
    {"code":"DOC-22","name":"Catalogo de herramientas y metodos de innovacion","phase":"Fase 2","chapter":"S7.6","type":"Catalogo"},
    {"code":"DOC-23","name":"Procedimiento de vigilancia tecnologica","phase":"Fase 2","chapter":"S7.7","type":"Procedimiento"},
    {"code":"DOC-24","name":"Procedimiento de gestion de propiedad intelectual","phase":"Fase 2","chapter":"S7.8","type":"Procedimiento"},
    {"code":"DOC-25","name":"Manual de planificacion y control operacional del SGI","phase":"Fase 3","chapter":"S8.1","type":"Manual"},
    {"code":"DOC-26","name":"Procedimiento de gestion de iniciativas de innovacion","phase":"Fase 3","chapter":"S8.2","type":"Procedimiento"},
    {"code":"DOC-27","name":"Procedimiento para identificacion de oportunidades","phase":"Fase 3","chapter":"S8.3.2","type":"Procedimiento"},
    {"code":"DOC-28","name":"Procedimiento para creacion de conceptos","phase":"Fase 3","chapter":"S8.3.3","type":"Procedimiento"},
    {"code":"DOC-29","name":"Procedimiento para validacion de conceptos","phase":"Fase 3","chapter":"S8.3.4","type":"Procedimiento"},
    {"code":"DOC-30","name":"Procedimiento para desarrollo de soluciones","phase":"Fase 3","chapter":"S8.3.5","type":"Procedimiento"},
    {"code":"DOC-31","name":"Procedimiento para despliegue de soluciones","phase":"Fase 3","chapter":"S8.3.6","type":"Procedimiento"},
    {"code":"DOC-32","name":"Manual de gestion de proyectos de I+D+I (NTC 5802)","phase":"Fase 3","chapter":"S8+5802","type":"Manual"},
    {"code":"DOC-33","name":"Formato de formulacion de proyecto MinCiencias/SGR","phase":"Fase 3","chapter":"NTC5802","type":"Formato estandar"},
    {"code":"DOC-34","name":"Procedimiento de seguimiento, medicion y evaluacion","phase":"Fase 4","chapter":"S9.1.1","type":"Procedimiento"},
    {"code":"DOC-35","name":"Tablero de indicadores de I+D+I (KPIs)","phase":"Fase 4","chapter":"S9.1.2","type":"Dashboard"},
    {"code":"DOC-36","name":"Informe anual de desempeno del SGI","phase":"Fase 4","chapter":"S9.1.2","type":"Informe"},
    {"code":"DOC-37","name":"Procedimiento de auditoria interna del SGI","phase":"Fase 4","chapter":"S9.2","type":"Procedimiento"},
    {"code":"DOC-38","name":"Programa anual de auditorias internas","phase":"Fase 4","chapter":"S9.2","type":"Plan"},
    {"code":"DOC-39","name":"Lista de verificacion de auditoria interna","phase":"Fase 4","chapter":"S9.2","type":"Instrumento"},
    {"code":"DOC-40","name":"Informe de auditoria interna","phase":"Fase 4","chapter":"S9.2","type":"Registro"},
    {"code":"DOC-41","name":"Procedimiento de revision por la direccion","phase":"Fase 4","chapter":"S9.3","type":"Procedimiento"},
    {"code":"DOC-42","name":"Informe de revision por la direccion","phase":"Fase 4","chapter":"S9.3","type":"Registro"},
    {"code":"DOC-43","name":"Procedimiento de no conformidades y acciones correctivas","phase":"Fase 4","chapter":"S10.2","type":"Procedimiento"},
    {"code":"DOC-44","name":"Registro de no conformidades y acciones de mejora","phase":"Fase 4","chapter":"S10.2","type":"Registro vivo"},
    {"code":"DOC-45","name":"Plan de mejora continua del SGI","phase":"Fase 4","chapter":"S10.3","type":"Plan anual"},
]
FORMATS = [
    {"code":"FTO-01","name":"Formato de analisis PESTEL","phase":"Fase 1"},
    {"code":"FTO-02","name":"Plantilla de matriz de partes interesadas","phase":"Fase 1"},
    {"code":"FTO-03","name":"Plantilla DOFA cruzada","phase":"Fase 1"},
    {"code":"FTO-04","name":"Acta de reunion de la alta direccion","phase":"Fase 1"},
    {"code":"FTO-05","name":"Acta de conformacion del equipo de implementacion","phase":"Fase 1"},
    {"code":"FTO-06","name":"Formato de identificacion y evaluacion de riesgos","phase":"Fase 2"},
    {"code":"FTO-07","name":"Ficha de objetivo de innovacion","phase":"Fase 2"},
    {"code":"FTO-08","name":"Formato de solicitud y asignacion de recursos","phase":"Fase 2"},
    {"code":"FTO-09","name":"Perfil de competencias en innovacion por cargo","phase":"Fase 2"},
    {"code":"FTO-10","name":"Formato de evaluacion de competencias","phase":"Fase 2"},
    {"code":"FTO-11","name":"Formato de solicitud de capacitacion","phase":"Fase 2"},
    {"code":"FTO-12","name":"Registro de asistencia a capacitaciones","phase":"Fase 2"},
    {"code":"FTO-13","name":"Solicitud de proteccion de propiedad intelectual","phase":"Fase 2"},
    {"code":"FTO-14","name":"Boletin / informe de vigilancia tecnologica","phase":"Fase 2"},
    {"code":"FTO-15","name":"Formato de captacion de ideas / oportunidades","phase":"Fase 3"},
    {"code":"FTO-16","name":"Ficha de evaluacion preliminar de ideas","phase":"Fase 3"},
    {"code":"FTO-17","name":"Formato de desarrollo de concepto","phase":"Fase 3"},
    {"code":"FTO-18","name":"Protocolo de prueba o validacion experimental","phase":"Fase 3"},
    {"code":"FTO-19","name":"Ficha de proyecto de I+D+I","phase":"Fase 3"},
    {"code":"FTO-20","name":"Cronograma de proyecto (Gantt)","phase":"Fase 3"},
    {"code":"FTO-21","name":"Informe de avance de proyecto","phase":"Fase 3"},
    {"code":"FTO-22","name":"Informe final de proyecto","phase":"Fase 3"},
    {"code":"FTO-23","name":"Acta de comite de innovacion / portafolio","phase":"Fase 3"},
    {"code":"FTO-24","name":"Registro de lecciones aprendidas de proyectos","phase":"Fase 3"},
    {"code":"FTO-25","name":"Ficha de indicador (KPI)","phase":"Fase 4"},
    {"code":"FTO-26","name":"Formato de reporte de no conformidad","phase":"Fase 4"},
    {"code":"FTO-27","name":"Formato de plan de accion correctiva / preventiva","phase":"Fase 4"},
    {"code":"FTO-28","name":"Lista de chequeo de auditoria interna","phase":"Fase 4"},
    {"code":"FTO-29","name":"Acta de revision por la direccion","phase":"Fase 4"},
    {"code":"FTO-30","name":"Encuesta de satisfaccion de partes interesadas","phase":"Fase 4"},
]
STATUS_OPTIONS = ["Pendiente", "En proceso", "Completo", "No aplica"]
STATUS_EMOJI   = {"Pendiente":"X", "En proceso":"~", "Completo":"OK", "No aplica":"N/A"}
STATE_FILE = "sgi_state.json"


# ---- STATE MANAGEMENT ----
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE,"r",encoding="utf-8") as f: return json.load(f)
    return {}

def save_state(s):
    with open(STATE_FILE,"w",encoding="utf-8") as f: json.dump(s,f,ensure_ascii=False,indent=2)

def ikey(pk,iid): return f"chk_{pk}_{iid}"
def dkey(code): return f"doc_{code}"

def get_istate(key):
    v = st.session_state.state.get(key, {})
    if isinstance(v,str): v={"status":v}
    return {"status":v.get("status","Pendiente"),"fecha_inicio":v.get("fecha_inicio",""),
            "fecha_fin":v.get("fecha_fin",""),"responsable_nombre":v.get("responsable_nombre",""),
            "rol":v.get("rol",""),"comentario":v.get("comentario","")}

def save_istate(key,data):
    st.session_state.state[key]=data
    save_state(st.session_state.state)

def get_custom_code(orig):
    return st.session_state.state.get("custom_codes",{}).get(orig,orig)

def set_custom_code(orig,new):
    if "custom_codes" not in st.session_state.state: st.session_state.state["custom_codes"]={}
    st.session_state.state["custom_codes"][orig]=new.strip() or orig
    save_state(st.session_state.state)

def get_doc_status(code):
    v=st.session_state.state.get(dkey(code),"Pendiente")
    return v if isinstance(v,str) else v.get("status","Pendiente")

def set_doc_status(code,status):
    v=st.session_state.state.get(dkey(code),{})
    if isinstance(v,str): v={"status":v}
    v["status"]=status
    st.session_state.state[dkey(code)]=v
    save_state(st.session_state.state)

if "state" not in st.session_state:
    st.session_state.state = load_state()


# ---- CALCULATIONS ----
def phase_progress(pk):
    items=PHASES[pk]["items"]
    total=len(items)
    done=sum(1 for i in items if get_istate(ikey(pk,i["id"]))["status"]=="Completo")
    wip =sum(1 for i in items if get_istate(ikey(pk,i["id"]))["status"]=="En proceso")
    na  =sum(1 for i in items if get_istate(ikey(pk,i["id"]))["status"]=="No aplica")
    app=total-na
    pct=round(done/app*100) if app>0 else 0
    return total,done,wip,na,pct

def overall_progress():
    ai=sum(len(PHASES[pk]["items"]) for pk in PHASES)
    ad=sum(phase_progress(pk)[1] for pk in PHASES)
    an=sum(phase_progress(pk)[3] for pk in PHASES)
    app=ai-an
    pct=round(ad/app*100) if app>0 else 0
    return ai,ad,app,pct

def doc_progress():
    all_items=DOCUMENTS+FORMATS
    total=len(all_items)
    done=sum(1 for d in all_items if get_doc_status(d["code"])=="Completo")
    return total,done,round(done/total*100) if total>0 else 0


# ---- CSS ----
st.markdown("""
<style>
[data-testid="stSidebar"]{background-color:#0D1B2A;}
[data-testid="stSidebar"] *{color:#E8EDF3 !important;}
[data-testid="stSidebar"] hr{border-color:#2a3f5a !important;}
.card{background:white;border-radius:12px;padding:18px;border-left:5px solid;
      box-shadow:0 2px 10px rgba(0,0,0,0.08);margin-bottom:12px;}
.card-pct{font-size:2rem;font-weight:800;margin:6px 0 2px 0;}
.tag{display:inline-block;padding:2px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;}
.detail-box{background:#F8FAFF;border:1px solid #E3EAF8;border-radius:10px;padding:14px 16px;margin:4px 0 8px 0;}
</style>""", unsafe_allow_html=True)


# ---- SIDEBAR ----
with st.sidebar:
    logo_b64 = st.session_state.state.get("logo_b64",None)
    if logo_b64:
        st.markdown(f'<img src="{logo_b64}" style="width:100%;border-radius:8px;margin-bottom:10px">',
                    unsafe_allow_html=True)
    st.markdown("## SGI I+D+I")
    st.markdown("**Laboratorio Nacional de Insumos Agrícolas - LANIA - Área IIAD**")
    st.markdown("*Implementación NTC 5801 / ISO 56002*")
    st.markdown("---")
    page = st.radio("", [
        "Dashboard","Fase 1 - Fundamentos","Fase 2 - Apoyo Estrategico",
        "Fase 3 - Operacion","Fase 4 - Evaluacion y Mejora",
        "Registro Documental","Reportes y Exportar","Configuracion"
    ], label_visibility="collapsed")
    st.markdown("---")
    _,done_all,appl_all,pct_all = overall_progress()
    st.markdown(f"### Avance: **{pct_all}%**")
    st.progress(pct_all/100)
    st.caption(f"{done_all} de {appl_all} completadas")
    st.markdown("---")
    st.markdown("##### Guardar progreso")
    state_bytes=json.dumps(st.session_state.state,ensure_ascii=False,indent=2).encode("utf-8")
    st.download_button("Descargar sgi_state.json", data=state_bytes,
        file_name=f"sgi_state_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json", use_container_width=True)
    st.markdown("---")
    st.markdown("##### Cargar progreso")
    uploaded_file = st.file_uploader("sgi_state.json", type=["json"], label_visibility="collapsed")
    if uploaded_file is not None:
        try:
            loaded=json.load(uploaded_file)
            st.session_state.state=loaded
            save_state(loaded)
            st.success("Progreso cargado correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
    st.markdown("---")
    st.caption("Flujo: 1) Carga JSON | 2) Actualiza | 3) Descarga | 4) Guarda en OneDrive")


# ---- PAGE: DASHBOARD ----
if page == "Dashboard":
    st.title("Seguimiento de implementación del sistema de Gestión I+D+I")
    st.markdown(f"**Área de Investigación e Innovación Analítica y Diagnóstica (IIAD)** | NTC 5801 / ISO 56002 | *{datetime.now().strftime('%d/%m/%Y')}*")
    st.divider()
    total_all,done_all,appl_all,pct_all=overall_progress()
    tot_docs,done_docs,pct_docs=doc_progress()
    phases_done=sum(1 for pk in PHASES if phase_progress(pk)[4]==100)
    wip_all=sum(phase_progress(pk)[2] for pk in PHASES)
    k1,k2,k3,k4=st.columns(4)
    k1.metric("Avance General",f"{pct_all}%",f"{done_all}/{appl_all} actividades")
    k2.metric("Documentos",f"{pct_docs}%",f"{done_docs}/{tot_docs} elaborados")
    k3.metric("Fases completadas",f"{phases_done}/4")
    k4.metric("En proceso",f"{wip_all}","actividades activas")
    st.divider()
    st.markdown("### Progreso por Fase")
    cols=st.columns(4)
    for i,pk in enumerate(PHASES):
        ph=PHASES[pk]; total,done,wip,na,pct=phase_progress(pk)
        with cols[i]:
            st.markdown(f"""<div class="card" style="border-left-color:{ph['color']}">
                <div style="font-weight:700">{pk}</div>
                <div style="font-size:0.8rem;color:#777">{ph['name']}</div>
                <div class="card-pct" style="color:{ph['color']}">{pct}%</div>
                <div style="font-size:0.8rem;color:#777">{ph['months']}</div>
                <div style="margin-top:8px;font-size:0.82rem;">OK {done} | ~ {wip} | X {total-done-wip-na} | N/A {na}</div>
            </div>""", unsafe_allow_html=True)
            st.progress(pct/100)
    st.divider()
    c1,c2=st.columns(2)
    with c1:
        st.markdown("#### Estado por fase")
        cr=[]
        for pk in PHASES:
            total,done,wip,na,pct=phase_progress(pk)
            cr+=[{"Fase":pk,"Estado":"Completo","n":done},{"Fase":pk,"Estado":"En proceso","n":wip},
                 {"Fase":pk,"Estado":"Pendiente","n":total-done-wip-na},{"Fase":pk,"Estado":"No aplica","n":na}]
        fig=px.bar(pd.DataFrame(cr),x="Fase",y="n",color="Estado",
                   color_discrete_map={"Completo":"#4CAF50","En proceso":"#2196F3","Pendiente":"#CFD8DC","No aplica":"#FF7043"},
                   barmode="stack",height=300)
        fig.update_layout(plot_bgcolor="white",yaxis_title="N actividades",legend=dict(orientation="h",y=-0.3))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown("#### Radar de avance")
        labels=[f"F{i+1}: {PHASES[pk]['name'][:15]}" for i,pk in enumerate(PHASES)]
        values=[phase_progress(pk)[4] for pk in PHASES]
        fig_r=go.Figure(go.Scatterpolar(r=values+[values[0]],theta=labels+[labels[0]],
            fill="toself",fillcolor="rgba(21,101,192,0.15)",line=dict(color="#1565C0",width=2)))
        fig_r.update_layout(polar=dict(radialaxis=dict(range=[0,100])),height=300,margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig_r,use_container_width=True)
    st.divider()
    st.markdown("### Hitos de Cierre")
    mes_hito={"Fase 1":"Mes 3","Fase 2":"Mes 6","Fase 3":"Mes 9","Fase 4":"Mes 12"}
    m_cols=st.columns(4)
    for i,pk in enumerate(PHASES):
        ph=PHASES[pk]; _,done,_,na,pct=phase_progress(pk)
        icon="OK" if pct==100 else ("~" if done>0 else "...")
        with m_cols[i]:
            st.markdown(f"""<div style="background:{ph['color']}12;border:1px solid {ph['color']}40;
                border-radius:10px;padding:14px;text-align:center;">
                <div style="color:{ph['color']};font-weight:700">{mes_hito[pk]}</div>
                <div style="font-size:1.3rem;margin:6px 0">{icon}</div>
                <div style="font-size:0.8rem;color:#444">{ph['hito']}</div>
            </div>""", unsafe_allow_html=True)


# ---- PAGE: PHASE CHECKLIST ----
elif page in ["Fase 1 - Fundamentos","Fase 2 - Apoyo Estrategico","Fase 3 - Operacion","Fase 4 - Evaluacion y Mejora"]:
    phase_map={"Fase 1 - Fundamentos":"Fase 1","Fase 2 - Apoyo Estrategico":"Fase 2",
               "Fase 3 - Operacion":"Fase 3","Fase 4 - Evaluacion y Mejora":"Fase 4"}
    pk=phase_map[page]; ph=PHASES[pk]
    total,done,wip,na,pct=phase_progress(pk)
    st.title(f"{pk}: {ph['name']}")
    st.markdown(f"**{ph['months']}** | {ph['chapters']}")
    st.divider()
    kc1,kc2,kc3,kc4,kc5=st.columns(5)
    kc1.metric("Avance",f"{pct}%")
    kc2.metric("Completas",done)
    kc3.metric("En proceso",wip)
    kc4.metric("Pendientes",total-done-wip-na)
    kc5.metric("No aplica",na)
    st.progress(pct/100)
    st.divider()
    fc1,fc2,fc3=st.columns(3)
    with fc1: f_status=st.multiselect("Estado:",STATUS_OPTIONS,default=STATUS_OPTIONS,key=f"fs_{pk}")
    with fc2: f_text=st.text_input("Buscar:",key=f"ft_{pk}")
    with fc3:
        resps=sorted(set(i["responsible"] for i in ph["items"]))
        f_resp=st.multiselect("Responsable:",resps,default=resps,key=f"fr_{pk}")
    st.divider()
    hdr=st.columns([0.4,0.6,4.2,0.9,1.6])
    for col,lbl in zip(hdr,["**#**","**Ref.**","**Actividad / Entregable**","**Plazo**","**Estado**"]): col.markdown(lbl)
    st.markdown("<hr style='margin:4px 0'>",unsafe_allow_html=True)
    for item in ph["items"]:
        k=ikey(pk,item["id"]); ist=get_istate(k); cur=ist["status"]
        if cur not in f_status: continue
        if f_text and f_text.lower() not in item["activity"].lower(): continue
        if item["responsible"] not in f_resp: continue
        row=st.columns([0.4,0.6,4.2,0.9,1.6])
        row[0].markdown(f"**{item['id']}**")
        row[1].markdown(f"`{item['ref']}`")
        badges=""
        if ist["responsable_nombre"]: badges+=f" | {ist['responsable_nombre']}"
        if ist["fecha_inicio"]: badges+=f" | Ini: {ist['fecha_inicio']}"
        if ist["fecha_fin"]: badges+=f" -> {ist['fecha_fin']}"
        row[2].markdown(f"{item['activity']}<br><small style='color:#888'>{badges}</small>",unsafe_allow_html=True)
        row[3].markdown(f"<small>{item['deadline']}</small>",unsafe_allow_html=True)
        new_status=row[4].selectbox("",STATUS_OPTIONS,index=STATUS_OPTIONS.index(cur),
                                    key=f"sel_{pk}_{item['id']}",label_visibility="collapsed")
        if new_status!=cur:
            ist["status"]=new_status; save_istate(k,ist); st.rerun()
        with st.expander(f"Detalles -- {item['id']}: {item['activity'][:55]}..."):
            st.markdown('<div class="detail-box">',unsafe_allow_html=True)
            d1,d2,d3,d4=st.columns(4)
            try: fi_val=date.fromisoformat(ist["fecha_inicio"]) if ist["fecha_inicio"] else None
            except: fi_val=None
            try: ff_val=date.fromisoformat(ist["fecha_fin"]) if ist["fecha_fin"] else None
            except: ff_val=None
            new_fi=d1.date_input("Fecha inicio",value=fi_val,key=f"fi_{pk}_{item['id']}",format="DD/MM/YYYY")
            new_ff=d2.date_input("Fecha fin/cierre",value=ff_val,key=f"ff_{pk}_{item['id']}",format="DD/MM/YYYY")
            new_resp=d3.text_input("Nombre responsable",value=ist["responsable_nombre"],
                                   key=f"resp_{pk}_{item['id']}",placeholder="Ej. Ana Garcia")
            new_rol=d4.text_input("Rol / Cargo",value=ist["rol"],
                                  key=f"rol_{pk}_{item['id']}",placeholder="Ej. Lider SGI")
            new_cmt=st.text_area("Comentario / Enlace evidencia",value=ist["comentario"],
                                 key=f"cmt_{pk}_{item['id']}",height=75,
                                 placeholder="Enlace SharePoint/Teams o comentario...")
            if ist["comentario"] and ist["comentario"].startswith("http"):
                st.markdown(f'<a href="{ist['comentario']}" target="_blank" style="font-size:0.8rem">Ver evidencia</a>',
                            unsafe_allow_html=True)
            st.caption(f"Evidencia esperada (NTC 5801): {item['evidence']}")
            st.markdown('</div>',unsafe_allow_html=True)
            if st.button("Guardar detalles",key=f"save_{pk}_{item['id']}",type="primary"):
                save_istate(k,{"status":cur,
                    "fecha_inicio":str(new_fi) if new_fi else "",
                    "fecha_fin":str(new_ff) if new_ff else "",
                    "responsable_nombre":new_resp,"rol":new_rol,"comentario":new_cmt})
                st.success("Detalles guardados.")
        st.markdown("<hr style='margin:3px 0;opacity:0.2'>",unsafe_allow_html=True)


# ---- PAGE: DOCUMENT REGISTRY ----
elif page == "Registro Documental":
    st.title("Registro Documental del SGI")
    st.markdown("Inventario de los **45 documentos base** y **30 formatos operativos**.")
    c_t,c_h=st.columns([1,3])
    with c_t: edit_codes=st.toggle("Editar codigos SGC",value=False,help="Personaliza los codigos a tu SGC")
    with c_h:
        if edit_codes: st.info("Modo edicion activo: modifica los codigos directamente en cada fila.")
    st.divider()
    tab_docs,tab_fmts=st.tabs(["Documentos Base (45)","Formatos Operativos (30)"])
    for tab,items_list in [(tab_docs,DOCUMENTS),(tab_fmts,FORMATS)]:
        with tab:
            pf=st.multiselect("Fase:",["Fase 1","Fase 2","Fase 3","Fase 4"],
                              default=["Fase 1","Fase 2","Fase 3","Fase 4"],key=f"df_{id(items_list)}")
            if edit_codes:
                hdr=st.columns([0.5,1.0,1.2,3.8,1.6])
                for col,lbl in zip(hdr,["**Fase**","**Cod. orig.**","**Cod. SGC**","**Nombre**","**Estado**"]): col.markdown(lbl)
            else:
                hdr=st.columns([0.5,1.0,0.9,4.1,1.6])
                for col,lbl in zip(hdr,["**Fase**","**Codigo**","**Ref.**","**Nombre**","**Estado**"]): col.markdown(lbl)
            st.markdown("<hr style='margin:4px 0'>",unsafe_allow_html=True)
            for d in items_list:
                if d["phase"] not in pf: continue
                cur_s=get_doc_status(d["code"]); cc=get_custom_code(d["code"]); color=PHASES[d["phase"]]["color"]
                if edit_codes:
                    row=st.columns([0.5,1.0,1.2,3.8,1.6])
                    row[0].markdown(f'<span class="tag" style="background:{color}20;color:{color}">{d["phase"]}</span>',unsafe_allow_html=True)
                    row[1].markdown(f"<small style='color:#999'>`{d['code']}`</small>",unsafe_allow_html=True)
                    new_code=row[2].text_input("",value=cc,key=f"cedit_{d['code']}",
                                               label_visibility="collapsed",placeholder=d["code"])
                    row[3].markdown(f"{d['name']}<br><small style='color:#999'>{d.get('type','-')}</small>",unsafe_allow_html=True)
                    if new_code!=cc: set_custom_code(d["code"],new_code)
                else:
                    row=st.columns([0.5,1.0,0.9,4.1,1.6])
                    row[0].markdown(f'<span class="tag" style="background:{color}20;color:{color}">{d["phase"]}</span>',unsafe_allow_html=True)
                    disp=f"**`{cc}`**" if cc!=d["code"] else f"`{cc}`"
                    row[1].markdown(disp)
                    row[2].markdown(f"<small>`{d.get('chapter','-')}`</small>",unsafe_allow_html=True)
                    row[3].markdown(f"{d['name']}<br><small style='color:#999'>{d.get('type','-')}</small>",unsafe_allow_html=True)
                new_s=row[4].selectbox("",STATUS_OPTIONS,index=STATUS_OPTIONS.index(cur_s),
                                       key=f"dsel_{d['code']}",label_visibility="collapsed")
                if new_s!=cur_s: set_doc_status(d["code"],new_s); st.rerun()
                st.markdown("<hr style='margin:3px 0;opacity:0.18'>",unsafe_allow_html=True)


# ---- PAGE: REPORTS ----
elif page == "Reportes y Exportar":
    st.title("Reportes de Avance")
    st.divider()
    rows=[]
    for pk,ph in PHASES.items():
        for item in ph["items"]:
            k=ikey(pk,item["id"]); ist=get_istate(k)
            rows.append({"Fase":pk,"Nombre Fase":ph["name"],"ID":item["id"],
                "Actividad":item["activity"],"Ref. NTC":item["ref"],
                "Resp. sistema":item["responsible"],"Resp. asignado":ist["responsable_nombre"],
                "Rol":ist["rol"],"Plazo":item["deadline"],
                "Fecha Inicio":ist["fecha_inicio"],"Fecha Fin":ist["fecha_fin"],
                "Estado":ist["status"],"Evidencia esperada":item["evidence"],
                "Comentario/Enlace":ist["comentario"]})
    df_all=pd.DataFrame(rows)
    st.markdown("### Resumen por Fase")
    summary=[]
    for pk in PHASES:
        total,done,wip,na,pct=phase_progress(pk)
        summary.append({"Fase":f"{pk}: {PHASES[pk]['name']}","Total":total,
            "Completas":done,"En proceso":wip,"Pendientes":total-done-wip-na,
            "No aplica":na,"% Avance":f"{pct}%"})
    st.dataframe(pd.DataFrame(summary),use_container_width=True,hide_index=True)
    st.divider()
    st.markdown("### Actividades por mes")
    mo=[f"Mes {i}" for i in range(1,13)]
    df_all["Mes_num"]=df_all["Plazo"].str.extract(r"(\d+)").astype(float)
    monthly=df_all.groupby(["Plazo","Estado","Mes_num"]).size().reset_index(name="n").sort_values("Mes_num")
    fig=px.bar(monthly,x="Plazo",y="n",color="Estado",
               color_discrete_map={"Completo":"#4CAF50","En proceso":"#2196F3","Pendiente":"#CFD8DC","No aplica":"#FF7043"},
               barmode="stack",height=300,category_orders={"Plazo":mo})
    fig.update_layout(plot_bgcolor="white",xaxis_title="Mes",yaxis_title="N actividades",legend=dict(orientation="h",y=-0.3))
    st.plotly_chart(fig,use_container_width=True)
    st.divider()
    st.markdown("### Actividades Pendientes / En Proceso")
    dfp=df_all[df_all["Estado"].isin(["En proceso","Pendiente"])][
        ["Fase","ID","Actividad","Ref. NTC","Resp. asignado","Plazo","Estado"]]
    st.dataframe(dfp if not dfp.empty else pd.DataFrame({"Mensaje":["Todas las actividades completadas"]}),
                 use_container_width=True,hide_index=True)
    st.divider()
    st.markdown("### Exportar")
    e1,e2=st.columns(2)
    with e1:
        csv=df_all.to_csv(index=False).encode("utf-8")
        st.download_button("Actividades CSV (con fechas y responsables)",csv,
                           f"SGI_actividades_{datetime.now().strftime('%Y%m%d')}.csv","text/csv",use_container_width=True)
    with e2:
        doc_rows=[{"Cod. Original":d["code"],"Cod. SGC":get_custom_code(d["code"]),
                   "Nombre":d["name"],"Fase":d["phase"],"Estado":get_doc_status(d["code"])}
                  for d in DOCUMENTS+FORMATS]
        csv2=pd.DataFrame(doc_rows).to_csv(index=False).encode("utf-8")
        st.download_button("Documentos CSV (con codigos SGC)",csv2,
                           f"SGI_documentos_{datetime.now().strftime('%Y%m%d')}.csv","text/csv",use_container_width=True)


# ---- PAGE: CONFIG ----
elif page == "Configuracion":
    st.title("Configuracion del Dashboard")
    st.divider()
    st.markdown("### Logo institucional")
    st.markdown("El logo se almacena dentro del `sgi_state.json` y aparece en la barra lateral.")
    logo_b64=st.session_state.state.get("logo_b64",None)
    c1,c2=st.columns([1,2])
    with c1:
        if logo_b64:
            st.markdown(f'<img src="{logo_b64}" style="width:100%;border-radius:10px;border:1px solid #e0e0e0;padding:8px">',unsafe_allow_html=True)
            st.caption("Logo actual")
        else:
            st.info("No hay logo cargado aun.")
    with c2:
        logo_file=st.file_uploader("Subir logo (PNG, JPG — fondo blanco recomendado)",
                                    type=["png","jpg","jpeg"],key="logo_upload")
        if logo_file:
            raw=logo_file.read(); ext=logo_file.name.rsplit(".",1)[-1].lower()
            mime=f"image/{ext}"; b64_str=base64.b64encode(raw).decode()
            st.session_state.state["logo_b64"]=f"data:{mime};base64,{b64_str}"
            save_state(st.session_state.state)
            st.success("Logo guardado. Aparecera en el sidebar."); st.rerun()
        if logo_b64:
            if st.button("Quitar logo"):
                st.session_state.state.pop("logo_b64",None)
                save_state(st.session_state.state); st.rerun()
    st.divider()
    st.markdown("### Codigos personalizados del SGC")
    custom_codes=st.session_state.state.get("custom_codes",{})
    modified={o:c for o,c in custom_codes.items() if o!=c}
    if modified:
        st.dataframe(pd.DataFrame([{"Cod. original":o,"Cod. SGC":c} for o,c in modified.items()]),
                     use_container_width=True,hide_index=True)
        if st.button("Restablecer todos los codigos"):
            st.session_state.state.pop("custom_codes",None)
            save_state(st.session_state.state); st.success("Codigos restablecidos."); st.rerun()
    else:
        st.info("No hay codigos personalizados aun. Ve a Registro Documental y activa 'Editar codigos SGC'.")
    st.divider()
    st.markdown("### Informacion del sistema")
    total_items=sum(len(PHASES[pk]["items"]) for pk in PHASES)
    st.markdown(f"""| Parametro | Valor |
|---|---|
| Fases | 4 |
| Total actividades | {total_items} |
| Documentos base | 45 |
| Formatos | 30 |
| Normas | NTC 5801, ISO 56002, ISO 17034, ISO 17043 |
| Version | 2.0 |""")
