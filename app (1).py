import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="SGI I+D+I – IIAD",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DATA
# ============================================================

PHASES = {
    "Fase 1": {
        "name": "Fundamentos y Diagnóstico",
        "months": "Meses 1–3",
        "chapters": "Cap. 4 y 5  ·  NTC 5801 / ISO 56002",
        "color": "#1565C0",
        "hito": "Política de I+D+I aprobada y comunicada",
        "items": [
            {"id": "1.1",  "activity": "Equipo de implementación conformado y designado formalmente",           "ref": "§5.3",    "responsible": "Dirección",          "deadline": "Mes 1", "evidence": "Acta de designación"},
            {"id": "1.2",  "activity": "Capacitación del equipo en NTC 5801 / ISO 56002",                      "ref": "§7.2",    "responsible": "Líder SGI",          "deadline": "Mes 1", "evidence": "Registro de asistencia"},
            {"id": "1.3",  "activity": "Análisis PESTEL elaborado",                                            "ref": "§4.1.2",  "responsible": "Líder SGI",          "deadline": "Mes 1", "evidence": "DOC-01"},
            {"id": "1.4",  "activity": "Auditoría de capacidades internas realizada",                          "ref": "§4.1.3",  "responsible": "Líder SGI",          "deadline": "Mes 2", "evidence": "DOC-01"},
            {"id": "1.5",  "activity": "Análisis de contexto externo e interno documentado (DOC-01)",          "ref": "§4.1",    "responsible": "Líder SGI",          "deadline": "Mes 2", "evidence": "DOC-01 aprobado"},
            {"id": "1.6",  "activity": "Partes interesadas identificadas y clasificadas",                      "ref": "§4.2",    "responsible": "Equipo",             "deadline": "Mes 2", "evidence": "DOC-02"},
            {"id": "1.7",  "activity": "Necesidades y expectativas de partes interesadas documentadas",        "ref": "§4.2.1",  "responsible": "Equipo",             "deadline": "Mes 2", "evidence": "DOC-02"},
            {"id": "1.8",  "activity": "Mecanismos de interacción con partes interesadas definidos",           "ref": "§4.2.1c", "responsible": "Equipo",             "deadline": "Mes 2", "evidence": "DOC-02"},
            {"id": "1.9",  "activity": "Alcance del SGI determinado y documentado (DOC-03)",                   "ref": "§4.3",    "responsible": "Dirección",          "deadline": "Mes 2", "evidence": "DOC-03 aprobado"},
            {"id": "1.10", "activity": "Interacciones con ISO 17034/17043 documentadas en el alcance",         "ref": "§4.3c",   "responsible": "Líder SGI",          "deadline": "Mes 2", "evidence": "DOC-03"},
            {"id": "1.11", "activity": "DOFA elaborado con insumos de análisis externo e interno",             "ref": "§4.1",    "responsible": "Equipo",             "deadline": "Mes 3", "evidence": "DOC-04"},
            {"id": "1.12", "activity": "DOFA cruzado (FO/FA/DO/DA) construido",                                "ref": "§4.1",    "responsible": "Equipo",             "deadline": "Mes 3", "evidence": "DOC-04"},
            {"id": "1.13", "activity": "Visión de innovación redactada y validada por la dirección",           "ref": "§5.1.3",  "responsible": "Dirección",          "deadline": "Mes 3", "evidence": "DOC-05"},
            {"id": "1.14", "activity": "Política de I+D+I redactada, aprobada y firmada",                      "ref": "§5.2.1",  "responsible": "Alta dirección",     "deadline": "Mes 3", "evidence": "DOC-06 firmado"},
            {"id": "1.15", "activity": "Política comunicada a todo el personal",                               "ref": "§5.2.2",  "responsible": "Comunicaciones",     "deadline": "Mes 3", "evidence": "Registro difusión"},
            {"id": "1.16", "activity": "Estrategia de innovación documentada",                                 "ref": "§5.1.4",  "responsible": "Dirección",          "deadline": "Mes 3", "evidence": "DOC-07"},
            {"id": "1.17", "activity": "Roles y responsabilidades del SGI definidos (Matriz RACI)",            "ref": "§5.3",    "responsible": "Dirección",          "deadline": "Mes 3", "evidence": "DOC-08"},
            {"id": "1.18", "activity": "FTO-01 al FTO-05 diseñados y aprobados",                               "ref": "§7.5",    "responsible": "Líder SGI",          "deadline": "Mes 3", "evidence": "Formatos en listado maestro"},
        ],
    },
    "Fase 2": {
        "name": "Documentación Estratégica y de Apoyo",
        "months": "Meses 4–6",
        "chapters": "Cap. 6 y 7  ·  NTC 5801 / ISO 56002",
        "color": "#2E7D32",
        "hito": "Sistema documental base aprobado + personal capacitado",
        "items": [
            {"id": "2.1",  "activity": "Riesgos y oportunidades del SGI identificados",                        "ref": "§6.1",    "responsible": "Líder SGI",          "deadline": "Mes 4", "evidence": "DOC-09"},
            {"id": "2.2",  "activity": "Matriz de riesgos con valoración (probabilidad × impacto) elaborada",  "ref": "§6.1",    "responsible": "Equipo",             "deadline": "Mes 4", "evidence": "DOC-09"},
            {"id": "2.3",  "activity": "Planes de tratamiento de riesgos definidos",                           "ref": "§6.1",    "responsible": "Equipo",             "deadline": "Mes 4", "evidence": "DOC-09"},
            {"id": "2.4",  "activity": "Objetivos de innovación SMART definidos (mín. 3)",                     "ref": "§6.2.1",  "responsible": "Dirección",          "deadline": "Mes 4", "evidence": "DOC-10"},
            {"id": "2.5",  "activity": "Planes de acción para cada objetivo elaborados",                       "ref": "§6.2.2",  "responsible": "Líder SGI",          "deadline": "Mes 4", "evidence": "DOC-10"},
            {"id": "2.6",  "activity": "Estructura organizacional para I+D+I definida",                        "ref": "§6.3",    "responsible": "Dirección",          "deadline": "Mes 4", "evidence": "DOC-11"},
            {"id": "2.7",  "activity": "Portafolio inicial de proyectos estructurado (horizontes 1/2/3)",      "ref": "§6.4",    "responsible": "Líder SGI",          "deadline": "Mes 5", "evidence": "DOC-12"},
            {"id": "2.8",  "activity": "Procedimiento de gestión de recursos aprobado",                        "ref": "§7.1",    "responsible": "Líder SGI",          "deadline": "Mes 5", "evidence": "DOC-13"},
            {"id": "2.9",  "activity": "Presupuesto anual de I+D+I elaborado y aprobado",                      "ref": "§7.1.5",  "responsible": "Finanzas",           "deadline": "Mes 5", "evidence": "DOC-14"},
            {"id": "2.10", "activity": "Inventario de infraestructura habilitadora realizado",                  "ref": "§7.1.6",  "responsible": "Líder SGI",          "deadline": "Mes 5", "evidence": "DOC-15"},
            {"id": "2.11", "activity": "Plan de gestión del conocimiento elaborado",                           "ref": "§7.1.4",  "responsible": "Líder SGI",          "deadline": "Mes 5", "evidence": "DOC-16"},
            {"id": "2.12", "activity": "Matriz de competencias del personal diligenciada",                     "ref": "§7.2",    "responsible": "RRHH",               "deadline": "Mes 5", "evidence": "DOC-17"},
            {"id": "2.13", "activity": "Brechas de competencia identificadas",                                 "ref": "§7.2",    "responsible": "RRHH",               "deadline": "Mes 5", "evidence": "DOC-17"},
            {"id": "2.14", "activity": "Plan de capacitación elaborado para cubrir brechas",                   "ref": "§7.2",    "responsible": "RRHH",               "deadline": "Mes 5", "evidence": "DOC-18"},
            {"id": "2.15", "activity": "Plan de comunicación del SGI aprobado",                                "ref": "§7.4",    "responsible": "Comunicaciones",     "deadline": "Mes 6", "evidence": "DOC-19"},
            {"id": "2.16", "activity": "Procedimiento de control de documentos aprobado",                      "ref": "§7.5",    "responsible": "Líder SGI",          "deadline": "Mes 6", "evidence": "DOC-20"},
            {"id": "2.17", "activity": "Sistema de codificación documental definido",                          "ref": "§7.5",    "responsible": "Líder SGI",          "deadline": "Mes 6", "evidence": "DOC-21"},
            {"id": "2.18", "activity": "Listado maestro de documentos creado y en uso",                        "ref": "§7.5.3",  "responsible": "Líder SGI",          "deadline": "Mes 6", "evidence": "DOC-21 en Notion"},
            {"id": "2.19", "activity": "Catálogo de herramientas de innovación elaborado",                     "ref": "§7.6",    "responsible": "Equipo",             "deadline": "Mes 6", "evidence": "DOC-22"},
            {"id": "2.20", "activity": "Procedimiento de vigilancia tecnológica aprobado",                     "ref": "§7.7",    "responsible": "Líder SGI",          "deadline": "Mes 6", "evidence": "DOC-23"},
            {"id": "2.21", "activity": "Primera vigilancia tecnológica ejecutada y documentada",               "ref": "§7.7",    "responsible": "Líder SGI",          "deadline": "Mes 6", "evidence": "Informe VT-001"},
            {"id": "2.22", "activity": "Procedimiento de propiedad intelectual aprobado",                      "ref": "§7.8",    "responsible": "Asesor jurídico",    "deadline": "Mes 6", "evidence": "DOC-24"},
            {"id": "2.23", "activity": "FTO-06 al FTO-14 diseñados y aprobados",                               "ref": "§7.5",    "responsible": "Líder SGI",          "deadline": "Mes 6", "evidence": "Formatos en listado"},
        ],
    },
    "Fase 3": {
        "name": "Documentación Operativa e Implementación",
        "months": "Meses 7–9",
        "chapters": "Cap. 8  ·  NTC 5801 / ISO 56002 + MinCiencias",
        "color": "#E65100",
        "hito": "Proyecto piloto de I+D+I en ejecución",
        "items": [
            {"id": "3.1",  "activity": "Manual de planificación y control operacional aprobado",               "ref": "§8.1",      "responsible": "Líder SGI",           "deadline": "Mes 7", "evidence": "DOC-25"},
            {"id": "3.2",  "activity": "Procedimiento de gestión de iniciativas aprobado",                     "ref": "§8.2",      "responsible": "Líder SGI",           "deadline": "Mes 7", "evidence": "DOC-26"},
            {"id": "3.3",  "activity": "Procedimiento de identificación de oportunidades aprobado",            "ref": "§8.3.2",    "responsible": "Líder SGI",           "deadline": "Mes 7", "evidence": "DOC-27"},
            {"id": "3.4",  "activity": "Procedimiento de creación de conceptos aprobado",                      "ref": "§8.3.3",    "responsible": "Líder SGI",           "deadline": "Mes 7", "evidence": "DOC-28"},
            {"id": "3.5",  "activity": "Procedimiento de validación de conceptos aprobado",                    "ref": "§8.3.4",    "responsible": "Líder SGI",           "deadline": "Mes 8", "evidence": "DOC-29"},
            {"id": "3.6",  "activity": "Procedimiento de desarrollo de soluciones aprobado",                   "ref": "§8.3.5",    "responsible": "Líder SGI",           "deadline": "Mes 8", "evidence": "DOC-30"},
            {"id": "3.7",  "activity": "Procedimiento de despliegue de soluciones aprobado",                   "ref": "§8.3.6",    "responsible": "Líder SGI",           "deadline": "Mes 8", "evidence": "DOC-31"},
            {"id": "3.8",  "activity": "Manual de gestión de proyectos NTC 5802 aprobado",                     "ref": "NTC 5802",  "responsible": "Líder SGI",           "deadline": "Mes 8", "evidence": "DOC-32"},
            {"id": "3.9",  "activity": "Formato de formulación de proyecto elaborado y probado",               "ref": "NTC 5802",  "responsible": "Líder SGI",           "deadline": "Mes 8", "evidence": "FTO-19 validado"},
            {"id": "3.10", "activity": "Al menos 1 proyecto piloto formulado y en ejecución",                  "ref": "§8.3",      "responsible": "Investigador",        "deadline": "Mes 9", "evidence": "Ficha de proyecto"},
            {"id": "3.11", "activity": "Primera acta de comité de innovación realizada",                       "ref": "§8.2",      "responsible": "Líder SGI",           "deadline": "Mes 9", "evidence": "FTO-23 diligenciado"},
            {"id": "3.12", "activity": "FTO-15 al FTO-24 diseñados y aprobados",                               "ref": "§7.5",      "responsible": "Líder SGI",           "deadline": "Mes 9", "evidence": "Formatos en listado"},
            {"id": "3.13", "activity": "Laboratorio registrado en InstituLAC (MinCiencias)",                   "ref": "Ext.",       "responsible": "Dirección",           "deadline": "Mes 7", "evidence": "Constancia de registro"},
            {"id": "3.14", "activity": "Grupo(s) de investigación registrados en GrupLAC",                     "ref": "Ext.",       "responsible": "Investigador líder",  "deadline": "Mes 8", "evidence": "Ficha GrupLAC"},
            {"id": "3.15", "activity": "CvLAC de todo el personal investigador actualizado",                   "ref": "Ext.",       "responsible": "Investigadores",      "deadline": "Mes 8", "evidence": "Perfiles activos"},
            {"id": "3.16", "activity": "Productos de investigación clasificados (tipologías MinCiencias)",     "ref": "Ext.",       "responsible": "Líder SGI",           "deadline": "Mes 9", "evidence": "Listado clasificado"},
        ],
    },
    "Fase 4": {
        "name": "Evaluación, Auditoría y Mejora",
        "months": "Meses 10–12",
        "chapters": "Cap. 9 y 10  ·  NTC 5801 / ISO 56002",
        "color": "#6A1B9A",
        "hito": "Primera auditoría interna + revisión por la dirección",
        "items": [
            {"id": "4.1",  "activity": "Procedimiento de seguimiento y medición aprobado",                     "ref": "§9.1.1",  "responsible": "Líder SGI",       "deadline": "Mes 10", "evidence": "DOC-34"},
            {"id": "4.2",  "activity": "Indicadores de I+D+I definidos (entrada, proceso, salida, impacto)",   "ref": "§9.1.2",  "responsible": "Líder SGI",       "deadline": "Mes 10", "evidence": "DOC-35 (mín. 6 KPIs)"},
            {"id": "4.3",  "activity": "Línea base de indicadores establecida",                                "ref": "§9.1.2",  "responsible": "Líder SGI",       "deadline": "Mes 10", "evidence": "Registro inicial"},
            {"id": "4.4",  "activity": "Dashboard de seguimiento en Notion implementado",                      "ref": "§9.1",    "responsible": "Líder SGI",       "deadline": "Mes 10", "evidence": "Base de datos activa"},
            {"id": "4.5",  "activity": "Programa anual de auditorías elaborado",                               "ref": "§9.2",    "responsible": "Auditor interno", "deadline": "Mes 10", "evidence": "DOC-38"},
            {"id": "4.6",  "activity": "Auditor interno capacitado en NTC 5801",                               "ref": "§9.2",    "responsible": "Dirección",       "deadline": "Mes 10", "evidence": "Certificado o registro"},
            {"id": "4.7",  "activity": "Lista de verificación de auditoría interna elaborada (por capítulo)",  "ref": "§9.2",    "responsible": "Auditor interno", "deadline": "Mes 10", "evidence": "DOC-39"},
            {"id": "4.8",  "activity": "Primera auditoría interna realizada",                                  "ref": "§9.2",    "responsible": "Auditor interno", "deadline": "Mes 11", "evidence": "DOC-40 (informe)"},
            {"id": "4.9",  "activity": "No conformidades identificadas y registradas",                         "ref": "§10.2",   "responsible": "Auditor interno", "deadline": "Mes 11", "evidence": "FTO-26"},
            {"id": "4.10", "activity": "Planes de acción correctiva para NC elaborados",                       "ref": "§10.2",   "responsible": "Responsables",    "deadline": "Mes 11", "evidence": "FTO-27"},
            {"id": "4.11", "activity": "Procedimiento de revisión por la dirección aprobado",                  "ref": "§9.3",    "responsible": "Dirección",       "deadline": "Mes 11", "evidence": "DOC-41"},
            {"id": "4.12", "activity": "Primera revisión por la dirección realizada",                          "ref": "§9.3",    "responsible": "Alta dirección",  "deadline": "Mes 12", "evidence": "DOC-42 (acta)"},
            {"id": "4.13", "activity": "Informe anual de desempeño del SGI elaborado",                         "ref": "§9.1.2",  "responsible": "Líder SGI",       "deadline": "Mes 12", "evidence": "DOC-36"},
            {"id": "4.14", "activity": "Plan de mejora continua del SGI para el año 2 elaborado",              "ref": "§10.3",   "responsible": "Equipo",          "deadline": "Mes 12", "evidence": "DOC-45"},
            {"id": "4.15", "activity": "FTO-25 al FTO-30 diseñados y en uso",                                  "ref": "§7.5",    "responsible": "Líder SGI",       "deadline": "Mes 12", "evidence": "Formatos en listado"},
            {"id": "4.16", "activity": "Sistema completo listo para evaluación ICONTEC",                       "ref": "§4–10",   "responsible": "Líder SGI",       "deadline": "Mes 12", "evidence": "45 documentos base"},
        ],
    },
}

DOCUMENTS = [
    {"code": "DOC-01", "name": "Análisis de cuestiones externas e internas",           "phase": "Fase 1", "chapter": "§4.1",    "type": "Procedimiento + Registro"},
    {"code": "DOC-02", "name": "Matriz de partes interesadas y sus necesidades",       "phase": "Fase 1", "chapter": "§4.2",    "type": "Registro vivo"},
    {"code": "DOC-03", "name": "Documento de alcance del SGI",                         "phase": "Fase 1", "chapter": "§4.3",    "type": "Declaración formal"},
    {"code": "DOC-04", "name": "Análisis DOFA del laboratorio",                        "phase": "Fase 1", "chapter": "§4.1",    "type": "Registro interno"},
    {"code": "DOC-05", "name": "Visión de innovación",                                 "phase": "Fase 1", "chapter": "§5.1.3",  "type": "Declaración estratégica"},
    {"code": "DOC-06", "name": "Política de I+D+I",                                    "phase": "Fase 1", "chapter": "§5.2.1",  "type": "Documento oficial"},
    {"code": "DOC-07", "name": "Estrategia de innovación",                             "phase": "Fase 1", "chapter": "§5.1.4",  "type": "Documento estratégico"},
    {"code": "DOC-08", "name": "Matriz de roles, responsabilidades y autoridades",     "phase": "Fase 1", "chapter": "§5.3",    "type": "Organigrama + RACI"},
    {"code": "DOC-09", "name": "Matriz de riesgos y oportunidades del SGI",            "phase": "Fase 2", "chapter": "§6.1",    "type": "Registro vivo"},
    {"code": "DOC-10", "name": "Objetivos de innovación SMART y planes de acción",     "phase": "Fase 2", "chapter": "§6.2",    "type": "Plan formal"},
    {"code": "DOC-11", "name": "Estructura organizacional para I+D+I",                 "phase": "Fase 2", "chapter": "§6.3",    "type": "Organigrama + descripción"},
    {"code": "DOC-12", "name": "Portafolio inicial de iniciativas de innovación",      "phase": "Fase 2", "chapter": "§6.4",    "type": "Base de datos"},
    {"code": "DOC-13", "name": "Procedimiento de gestión de recursos para I+D+I",      "phase": "Fase 2", "chapter": "§7.1",    "type": "Procedimiento"},
    {"code": "DOC-14", "name": "Presupuesto anual de I+D+I",                           "phase": "Fase 2", "chapter": "§7.1.5",  "type": "Plan financiero"},
    {"code": "DOC-15", "name": "Inventario de infraestructura habilitadora de I+D+I",  "phase": "Fase 2", "chapter": "§7.1.6",  "type": "Registro"},
    {"code": "DOC-16", "name": "Plan de gestión del conocimiento",                     "phase": "Fase 2", "chapter": "§7.1.4",  "type": "Plan"},
    {"code": "DOC-17", "name": "Matriz de competencias del personal en I+D+I",         "phase": "Fase 2", "chapter": "§7.2",    "type": "Registro"},
    {"code": "DOC-18", "name": "Plan anual de capacitación y toma de conciencia",      "phase": "Fase 2", "chapter": "§7.2/7.3","type": "Plan"},
    {"code": "DOC-19", "name": "Plan de comunicación interna y externa del SGI",       "phase": "Fase 2", "chapter": "§7.4",    "type": "Plan"},
    {"code": "DOC-20", "name": "Procedimiento de control de documentos y registros",   "phase": "Fase 2", "chapter": "§7.5",    "type": "Procedimiento maestro"},
    {"code": "DOC-21", "name": "Listado maestro de documentos",                        "phase": "Fase 2", "chapter": "§7.5.3",  "type": "Registro vivo"},
    {"code": "DOC-22", "name": "Catálogo de herramientas y métodos de innovación",     "phase": "Fase 2", "chapter": "§7.6",    "type": "Catálogo"},
    {"code": "DOC-23", "name": "Procedimiento de vigilancia tecnológica",              "phase": "Fase 2", "chapter": "§7.7",    "type": "Procedimiento"},
    {"code": "DOC-24", "name": "Procedimiento de gestión de propiedad intelectual",    "phase": "Fase 2", "chapter": "§7.8",    "type": "Procedimiento"},
    {"code": "DOC-25", "name": "Manual de planificación y control operacional del SGI","phase": "Fase 3", "chapter": "§8.1",    "type": "Manual"},
    {"code": "DOC-26", "name": "Procedimiento de gestión de iniciativas de innovación","phase": "Fase 3", "chapter": "§8.2",    "type": "Procedimiento"},
    {"code": "DOC-27", "name": "Procedimiento para identificación de oportunidades",   "phase": "Fase 3", "chapter": "§8.3.2",  "type": "Procedimiento"},
    {"code": "DOC-28", "name": "Procedimiento para creación de conceptos",             "phase": "Fase 3", "chapter": "§8.3.3",  "type": "Procedimiento"},
    {"code": "DOC-29", "name": "Procedimiento para validación de conceptos",           "phase": "Fase 3", "chapter": "§8.3.4",  "type": "Procedimiento"},
    {"code": "DOC-30", "name": "Procedimiento para desarrollo de soluciones",          "phase": "Fase 3", "chapter": "§8.3.5",  "type": "Procedimiento"},
    {"code": "DOC-31", "name": "Procedimiento para despliegue de soluciones",          "phase": "Fase 3", "chapter": "§8.3.6",  "type": "Procedimiento"},
    {"code": "DOC-32", "name": "Manual de gestión de proyectos de I+D+I (NTC 5802)",  "phase": "Fase 3", "chapter": "§8+5802", "type": "Manual"},
    {"code": "DOC-33", "name": "Formato de formulación de proyecto MinCiencias/SGR",  "phase": "Fase 3", "chapter": "NTC 5802","type": "Formato estándar"},
    {"code": "DOC-34", "name": "Procedimiento de seguimiento, medición y evaluación",  "phase": "Fase 4", "chapter": "§9.1.1",  "type": "Procedimiento"},
    {"code": "DOC-35", "name": "Tablero de indicadores de I+D+I (KPIs)",               "phase": "Fase 4", "chapter": "§9.1.2",  "type": "Dashboard"},
    {"code": "DOC-36", "name": "Informe anual de desempeño del SGI",                   "phase": "Fase 4", "chapter": "§9.1.2",  "type": "Informe"},
    {"code": "DOC-37", "name": "Procedimiento de auditoría interna del SGI",           "phase": "Fase 4", "chapter": "§9.2",    "type": "Procedimiento"},
    {"code": "DOC-38", "name": "Programa anual de auditorías internas",                "phase": "Fase 4", "chapter": "§9.2",    "type": "Plan"},
    {"code": "DOC-39", "name": "Lista de verificación de auditoría interna",           "phase": "Fase 4", "chapter": "§9.2",    "type": "Instrumento"},
    {"code": "DOC-40", "name": "Informe de auditoría interna",                         "phase": "Fase 4", "chapter": "§9.2",    "type": "Registro"},
    {"code": "DOC-41", "name": "Procedimiento de revisión por la dirección",           "phase": "Fase 4", "chapter": "§9.3",    "type": "Procedimiento"},
    {"code": "DOC-42", "name": "Informe de revisión por la dirección",                 "phase": "Fase 4", "chapter": "§9.3",    "type": "Registro"},
    {"code": "DOC-43", "name": "Procedimiento de no conformidades y acciones correctivas","phase":"Fase 4","chapter": "§10.2",  "type": "Procedimiento"},
    {"code": "DOC-44", "name": "Registro de no conformidades y acciones de mejora",   "phase": "Fase 4", "chapter": "§10.2",   "type": "Registro vivo"},
    {"code": "DOC-45", "name": "Plan de mejora continua del SGI",                      "phase": "Fase 4", "chapter": "§10.3",   "type": "Plan anual"},
]

FORMATS = [
    {"code": "FTO-01", "name": "Formato de análisis PESTEL",                            "phase": "Fase 1"},
    {"code": "FTO-02", "name": "Plantilla de matriz de partes interesadas",             "phase": "Fase 1"},
    {"code": "FTO-03", "name": "Plantilla DOFA cruzada (FO/FA/DO/DA)",                  "phase": "Fase 1"},
    {"code": "FTO-04", "name": "Acta de reunión de la alta dirección",                  "phase": "Fase 1"},
    {"code": "FTO-05", "name": "Acta de conformación del equipo de implementación",     "phase": "Fase 1"},
    {"code": "FTO-06", "name": "Formato de identificación y evaluación de riesgos",     "phase": "Fase 2"},
    {"code": "FTO-07", "name": "Ficha de objetivo de innovación",                       "phase": "Fase 2"},
    {"code": "FTO-08", "name": "Formato de solicitud y asignación de recursos",         "phase": "Fase 2"},
    {"code": "FTO-09", "name": "Perfil de competencias en innovación por cargo",        "phase": "Fase 2"},
    {"code": "FTO-10", "name": "Formato de evaluación de competencias",                 "phase": "Fase 2"},
    {"code": "FTO-11", "name": "Formato de solicitud de capacitación",                  "phase": "Fase 2"},
    {"code": "FTO-12", "name": "Registro de asistencia a capacitaciones",               "phase": "Fase 2"},
    {"code": "FTO-13", "name": "Solicitud de protección de propiedad intelectual",      "phase": "Fase 2"},
    {"code": "FTO-14", "name": "Boletín / informe de vigilancia tecnológica",           "phase": "Fase 2"},
    {"code": "FTO-15", "name": "Formato de captación de ideas / oportunidades",         "phase": "Fase 3"},
    {"code": "FTO-16", "name": "Ficha de evaluación preliminar de ideas",               "phase": "Fase 3"},
    {"code": "FTO-17", "name": "Formato de desarrollo de concepto",                     "phase": "Fase 3"},
    {"code": "FTO-18", "name": "Protocolo de prueba o validación experimental",         "phase": "Fase 3"},
    {"code": "FTO-19", "name": "Ficha de proyecto de I+D+I",                            "phase": "Fase 3"},
    {"code": "FTO-20", "name": "Cronograma de proyecto (Gantt)",                        "phase": "Fase 3"},
    {"code": "FTO-21", "name": "Informe de avance de proyecto",                         "phase": "Fase 3"},
    {"code": "FTO-22", "name": "Informe final de proyecto",                             "phase": "Fase 3"},
    {"code": "FTO-23", "name": "Acta de comité de innovación / portafolio",             "phase": "Fase 3"},
    {"code": "FTO-24", "name": "Registro de lecciones aprendidas de proyectos",         "phase": "Fase 3"},
    {"code": "FTO-25", "name": "Ficha de indicador (KPI)",                              "phase": "Fase 4"},
    {"code": "FTO-26", "name": "Formato de reporte de no conformidad",                  "phase": "Fase 4"},
    {"code": "FTO-27", "name": "Formato de plan de acción correctiva / preventiva",     "phase": "Fase 4"},
    {"code": "FTO-28", "name": "Lista de chequeo de auditoría interna",                 "phase": "Fase 4"},
    {"code": "FTO-29", "name": "Acta de revisión por la dirección",                     "phase": "Fase 4"},
    {"code": "FTO-30", "name": "Encuesta de satisfacción de partes interesadas",        "phase": "Fase 4"},
]

STATUS_OPTIONS = ["⬜ Pendiente", "🔄 En proceso", "✅ Completo", "⛔ No aplica"]
STATE_FILE = "sgi_state.json"

# ============================================================
# STATE MANAGEMENT
# ============================================================

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def item_key(phase_key, item_id):
    return f"chk_{phase_key}_{item_id}"

def doc_key(code):
    return f"doc_{code}"

if "state" not in st.session_state:
    st.session_state.state = load_state()

# ============================================================
# CALCULATIONS
# ============================================================

def phase_progress(phase_key):
    items = PHASES[phase_key]["items"]
    total = len(items)
    done = sum(1 for i in items if st.session_state.state.get(item_key(phase_key, i["id"]), "⬜ Pendiente") == "✅ Completo")
    wip  = sum(1 for i in items if st.session_state.state.get(item_key(phase_key, i["id"]), "⬜ Pendiente") == "🔄 En proceso")
    na   = sum(1 for i in items if st.session_state.state.get(item_key(phase_key, i["id"]), "⬜ Pendiente") == "⛔ No aplica")
    applicable = total - na
    pct = round(done / applicable * 100) if applicable > 0 else 0
    return total, done, wip, na, pct

def overall_progress():
    all_items = sum(len(PHASES[pk]["items"]) for pk in PHASES)
    all_done  = sum(phase_progress(pk)[1] for pk in PHASES)
    all_na    = sum(phase_progress(pk)[3] for pk in PHASES)
    applicable = all_items - all_na
    pct = round(all_done / applicable * 100) if applicable > 0 else 0
    return all_items, all_done, applicable, pct

def doc_progress():
    all_items = DOCUMENTS + FORMATS
    total = len(all_items)
    done  = sum(1 for d in all_items if st.session_state.state.get(doc_key(d["code"]), "⬜ Pendiente") == "✅ Completo")
    return total, done, round(done / total * 100) if total > 0 else 0

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0D1B2A; }
    [data-testid="stSidebar"] * { color: #E8EDF3 !important; }
    .card {
        background: white; border-radius: 12px; padding: 18px 20px;
        border-left: 5px solid; box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 12px;
    }
    .card-title { font-weight: 700; font-size: 1.05rem; color: #1a1a2e; }
    .card-sub   { font-size: 0.8rem; color: #777; margin-top: 3px; }
    .card-pct   { font-size: 2rem; font-weight: 800; margin: 6px 0 2px 0; }
    .tag {
        display: inline-block; padding: 2px 10px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600; margin-right: 4px;
    }
    .tip-box {
        background: #E3F2FD; border-left: 4px solid #1565C0;
        border-radius: 8px; padding: 10px 14px; font-size: 0.82rem;
        color: #0D47A1; margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR — con Export/Import JSON
# ============================================================

with st.sidebar:
    st.markdown("## 🔬 SGI I+D+I")
    st.markdown("**Laboratorio IIAD**")
    st.markdown("*NTC 5801 / ISO 56002*")
    st.markdown("---")

    page = st.radio("", [
        "🏠 Dashboard",
        "📋 Fase 1 — Fundamentos",
        "📋 Fase 2 — Apoyo Estratégico",
        "📋 Fase 3 — Operación",
        "📋 Fase 4 — Evaluación y Mejora",
        "📄 Registro Documental",
        "📊 Reportes y Exportar",
    ], label_visibility="collapsed")

    st.markdown("---")
    _, done_all, applicable_all, pct_all = overall_progress()
    st.markdown(f"### Avance Global: **{pct_all}%**")
    st.progress(pct_all / 100)
    st.caption(f"{done_all} de {applicable_all} actividades completadas")
    st.markdown("---")

    # ── EXPORTAR ESTADO ───────────────────────────────
    st.markdown("##### 💾 Guardar progreso")
    st.caption("Descarga el archivo al finalizar cada sesión.")
    state_bytes = json.dumps(
        st.session_state.state, ensure_ascii=False, indent=2
    ).encode("utf-8")
    st.download_button(
        label="⬇️ Descargar sgi_state.json",
        data=state_bytes,
        file_name=f"sgi_state_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
        use_container_width=True,
    )

    st.markdown("---")

    # ── IMPORTAR ESTADO ───────────────────────────────
    st.markdown("##### 📂 Cargar progreso")
    st.caption("Sube el archivo guardado para restaurar el avance.")
    uploaded_file = st.file_uploader(
        "Sube sgi_state.json",
        type=["json"],
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        try:
            loaded_state = json.load(uploaded_file)
            st.session_state.state = loaded_state
            save_state(loaded_state)
            st.success("✅ Progreso cargado correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error al cargar: {e}")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem; color:#90A4AE; line-height:1.6">
    💡 <b>Flujo de trabajo:</b><br>
    1. Abre la app<br>
    2. Carga el <code>sgi_state.json</code><br>
    3. Actualiza estados en la reunión<br>
    4. Descarga el JSON al terminar<br>
    5. Guarda en OneDrive / Teams
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PAGE: DASHBOARD
# ============================================================

if page == "🏠 Dashboard":
    st.title("🔬 Sistema de Gestión I+D+I")
    st.markdown(f"**Laboratorio IIAD** · NTC 5801 / ISO 56002 · *{datetime.now().strftime('%d/%m/%Y')}*")
    st.divider()

    total_all, done_all, appl_all, pct_all = overall_progress()
    tot_docs, done_docs, pct_docs = doc_progress()
    phases_done = sum(1 for pk in PHASES if phase_progress(pk)[4] == 100)
    wip_all = sum(phase_progress(pk)[2] for pk in PHASES)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📊 Avance General",    f"{pct_all}%",   f"{done_all}/{appl_all} actividades")
    k2.metric("📄 Documentos",        f"{pct_docs}%",  f"{done_docs}/{tot_docs} elaborados")
    k3.metric("✅ Fases completadas",  f"{phases_done}/4")
    k4.metric("🔄 En proceso",         f"{wip_all}",    "actividades activas")
    st.divider()

    st.markdown("### 📈 Progreso por Fase")
    cols = st.columns(4)
    for i, pk in enumerate(PHASES):
        ph = PHASES[pk]
        total, done, wip, na, pct = phase_progress(pk)
        with cols[i]:
            st.markdown(f"""
            <div class="card" style="border-left-color:{ph['color']}">
                <div class="card-title">{pk}</div>
                <div class="card-sub">{ph['name']}</div>
                <div class="card-pct" style="color:{ph['color']}">{pct}%</div>
                <div class="card-sub">{ph['months']}</div>
                <div style="margin-top:8px;font-size:0.82rem;">
                    ✅ {done}&nbsp;&nbsp;🔄 {wip}&nbsp;&nbsp;⬜ {total-done-wip-na}&nbsp;&nbsp;⛔ {na}
                </div>
            </div>""", unsafe_allow_html=True)
            st.progress(pct / 100)

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Estado de actividades por fase")
        chart_rows = []
        for pk in PHASES:
            total, done, wip, na, pct = phase_progress(pk)
            pending = total - done - wip - na
            chart_rows += [
                {"Fase": pk, "Estado": "✅ Completo",   "n": done},
                {"Fase": pk, "Estado": "🔄 En proceso", "n": wip},
                {"Fase": pk, "Estado": "⬜ Pendiente",  "n": pending},
                {"Fase": pk, "Estado": "⛔ No aplica",  "n": na},
            ]
        df_bar = pd.DataFrame(chart_rows)
        fig_bar = px.bar(df_bar, x="Fase", y="n", color="Estado",
                         color_discrete_map={
                             "✅ Completo": "#4CAF50", "🔄 En proceso": "#2196F3",
                             "⬜ Pendiente": "#CFD8DC", "⛔ No aplica": "#FF7043"},
                         barmode="stack", height=320)
        fig_bar.update_layout(plot_bgcolor="white", yaxis_title="N° actividades",
                              legend=dict(orientation="h", y=-0.3))
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.markdown("#### Radar de avance por fase")
        labels = [f"F{i+1}: {PHASES[pk]['name'][:18]}" for i, pk in enumerate(PHASES)]
        values = [phase_progress(pk)[4] for pk in PHASES]
        fig_r = go.Figure(go.Scatterpolar(
            r=values + [values[0]], theta=labels + [labels[0]],
            fill="toself", fillcolor="rgba(21,101,192,0.15)",
            line=dict(color="#1565C0", width=2),
        ))
        fig_r.update_layout(polar=dict(radialaxis=dict(range=[0, 100])),
                             height=320, margin=dict(t=30, b=30, l=30, r=30))
        st.plotly_chart(fig_r, use_container_width=True)

    st.divider()
    st.markdown("### 🗓️ Hitos de Cierre por Fase")
    mes_hito = {"Fase 1": "Mes 3", "Fase 2": "Mes 6", "Fase 3": "Mes 9", "Fase 4": "Mes 12"}
    m_cols = st.columns(4)
    for i, pk in enumerate(PHASES):
        ph = PHASES[pk]
        _, done, _, na, pct = phase_progress(pk)
        icon = "✅" if pct == 100 else ("🔄" if done > 0 else "⏳")
        with m_cols[i]:
            st.markdown(f"""
            <div style="background:{ph['color']}12;border:1px solid {ph['color']}40;
                        border-radius:10px;padding:14px;text-align:center;">
                <div style="color:{ph['color']};font-weight:700;font-size:1.1rem">{mes_hito[pk]}</div>
                <div style="font-size:1.5rem;margin:6px 0">{icon}</div>
                <div style="font-size:0.8rem;color:#444">{ph['hito']}</div>
            </div>""", unsafe_allow_html=True)

# ============================================================
# PAGE: PHASE CHECKLIST
# ============================================================

elif page.startswith("📋 Fase"):
    phase_map = {
        "📋 Fase 1 — Fundamentos":        "Fase 1",
        "📋 Fase 2 — Apoyo Estratégico":   "Fase 2",
        "📋 Fase 3 — Operación":           "Fase 3",
        "📋 Fase 4 — Evaluación y Mejora": "Fase 4",
    }
    pk = phase_map[page]
    ph = PHASES[pk]
    total, done, wip, na, pct = phase_progress(pk)

    st.title(f"{pk}: {ph['name']}")
    st.markdown(f"**{ph['months']}** · {ph['chapters']}")
    st.divider()

    kc1, kc2, kc3, kc4, kc5 = st.columns(5)
    kc1.metric("Avance",        f"{pct}%")
    kc2.metric("✅ Completas",   done)
    kc3.metric("🔄 En proceso", wip)
    kc4.metric("⬜ Pendientes", total - done - wip - na)
    kc5.metric("⛔ No aplica",  na)
    st.progress(pct / 100)
    st.divider()

    fc1, fc2, fc3 = st.columns([2, 2, 2])
    with fc1:
        f_status = st.multiselect("Estado:", STATUS_OPTIONS, default=STATUS_OPTIONS, key=f"fs_{pk}")
    with fc2:
        f_text = st.text_input("Buscar actividad:", key=f"ft_{pk}")
    with fc3:
        responsables = sorted(set(i["responsible"] for i in ph["items"]))
        f_resp = st.multiselect("Responsable:", responsables, default=responsables, key=f"fr_{pk}")

    st.divider()
    hdr = st.columns([0.4, 0.7, 3.8, 0.9, 1.8, 1.0, 1.8])
    for col, label in zip(hdr, ["**#**","**Ref.**","**Actividad / Entregable**","**Plazo**","**Estado**","**Resp.**","**Evidencia**"]):
        col.markdown(label)
    st.markdown("<hr style='margin:4px 0'>", unsafe_allow_html=True)

    for item in ph["items"]:
        k = item_key(pk, item["id"])
        current = st.session_state.state.get(k, "⬜ Pendiente")
        if current not in f_status: continue
        if f_text and f_text.lower() not in item["activity"].lower(): continue
        if item["responsible"] not in f_resp: continue

        row = st.columns([0.4, 0.7, 3.8, 0.9, 1.8, 1.0, 1.8])
        row[0].markdown(f"**{item['id']}**")
        row[1].markdown(f"`{item['ref']}`")
        row[2].markdown(item["activity"])
        row[3].markdown(f"<small>{item['deadline']}</small>", unsafe_allow_html=True)
        new_status = row[4].selectbox("", STATUS_OPTIONS,
                                      index=STATUS_OPTIONS.index(current),
                                      key=f"sel_{pk}_{item['id']}",
                                      label_visibility="collapsed")
        row[5].markdown(f"<small>{item['responsible']}</small>", unsafe_allow_html=True)
        row[6].markdown(f"<small>{item['evidence']}</small>", unsafe_allow_html=True)

        if new_status != current:
            st.session_state.state[k] = new_status
            save_state(st.session_state.state)
            st.rerun()
        st.markdown("<hr style='margin:3px 0;opacity:0.25'>", unsafe_allow_html=True)

# ============================================================
# PAGE: DOCUMENT REGISTRY
# ============================================================

elif page == "📄 Registro Documental":
    st.title("📄 Registro Documental del SGI")
    st.markdown("Inventario de los **45 documentos base** y **30 formatos operativos**.")
    st.divider()

    tab_docs, tab_fmts = st.tabs(["📁 Documentos Base (45)", "📋 Formatos Operativos (30)"])

    for tab, items_list in [(tab_docs, DOCUMENTS), (tab_fmts, FORMATS)]:
        with tab:
            phase_filter = st.multiselect(
                "Filtrar por fase:", ["Fase 1","Fase 2","Fase 3","Fase 4"],
                default=["Fase 1","Fase 2","Fase 3","Fase 4"],
                key=f"df_{id(items_list)}")

            hdr = st.columns([0.6, 0.7, 1.0, 4.0, 1.8])
            for col, lbl in zip(hdr, ["**Fase**","**Código**","**Ref.**","**Nombre**","**Estado**"]):
                col.markdown(lbl)
            st.markdown("<hr style='margin:4px 0'>", unsafe_allow_html=True)

            for d in items_list:
                if d["phase"] not in phase_filter: continue
                k = doc_key(d["code"])
                current = st.session_state.state.get(k, "⬜ Pendiente")
                color = PHASES[d["phase"]]["color"]

                row = st.columns([0.6, 0.7, 1.0, 4.0, 1.8])
                row[0].markdown(f"<span class='tag' style='background:{color}20;color:{color}'>{d['phase']}</span>", unsafe_allow_html=True)
                row[1].markdown(f"**`{d['code']}`**")
                row[2].markdown(f"<small>`{d.get('chapter','—')}`</small>", unsafe_allow_html=True)
                row[3].markdown(f"{d['name']}<br><small style='color:#999'>{d.get('type','—')}</small>", unsafe_allow_html=True)
                new_s = row[4].selectbox("", STATUS_OPTIONS, index=STATUS_OPTIONS.index(current),
                                         key=f"dsel_{d['code']}", label_visibility="collapsed")
                if new_s != current:
                    st.session_state.state[k] = new_s
                    save_state(st.session_state.state)
                    st.rerun()
                st.markdown("<hr style='margin:3px 0;opacity:0.2'>", unsafe_allow_html=True)

# ============================================================
# PAGE: REPORTS & EXPORT
# ============================================================

elif page == "📊 Reportes y Exportar":
    st.title("📊 Reportes de Avance")
    st.divider()

    rows = []
    for pk, ph in PHASES.items():
        for item in ph["items"]:
            k = item_key(pk, item["id"])
            rows.append({
                "Fase": pk, "Nombre Fase": ph["name"],
                "ID": item["id"], "Actividad": item["activity"],
                "Referencia NTC": item["ref"], "Responsable": item["responsible"],
                "Plazo": item["deadline"],
                "Estado": st.session_state.state.get(k, "⬜ Pendiente"),
                "Evidencia": item["evidence"],
            })
    df_all = pd.DataFrame(rows)

    st.markdown("### 📋 Resumen por Fase")
    summary = []
    for pk in PHASES:
        total, done, wip, na, pct = phase_progress(pk)
        summary.append({
            "Fase": f"{pk}: {PHASES[pk]['name']}",
            "Total": total, "✅ Completas": done,
            "🔄 En proceso": wip, "⬜ Pendientes": total-done-wip-na,
            "⛔ No aplica": na, "% Avance": f"{pct}%"
        })
    st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)
    st.divider()

    st.markdown("### 📅 Actividades por mes")
    month_order = [f"Mes {i}" for i in range(1, 13)]
    df_all["Mes_num"] = df_all["Plazo"].str.extract(r"(\d+)").astype(float)
    monthly = df_all.groupby(["Plazo", "Estado", "Mes_num"]).size().reset_index(name="n")
    monthly = monthly.sort_values("Mes_num")
    fig_m = px.bar(monthly, x="Plazo", y="n", color="Estado",
                   color_discrete_map={
                       "✅ Completo": "#4CAF50", "🔄 En proceso": "#2196F3",
                       "⬜ Pendiente": "#CFD8DC", "⛔ No aplica": "#FF7043"},
                   barmode="stack", height=320,
                   category_orders={"Plazo": month_order})
    fig_m.update_layout(plot_bgcolor="white", xaxis_title="Mes",
                        yaxis_title="N° actividades",
                        legend=dict(orientation="h", y=-0.3))
    st.plotly_chart(fig_m, use_container_width=True)
    st.divider()

    st.markdown("### 🔄 Actividades Pendientes / En Proceso")
    df_pending = df_all[df_all["Estado"].isin(["🔄 En proceso", "⬜ Pendiente"])][
        ["Fase","ID","Actividad","Referencia NTC","Responsable","Plazo","Estado"]]
    if df_pending.empty:
        st.success("🎉 ¡Todas las actividades están completas!")
    else:
        st.dataframe(df_pending, use_container_width=True, hide_index=True)
    st.divider()

    st.markdown("### ⬇️ Exportar")
    e1, e2 = st.columns(2)
    with e1:
        csv = df_all.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Actividades CSV",  csv,
                           f"SGI_actividades_{datetime.now().strftime('%Y%m%d')}.csv",
                           "text/csv", use_container_width=True)
    with e2:
        doc_rows = [{"Código": d["code"], "Nombre": d["name"], "Fase": d["phase"],
                     "Estado": st.session_state.state.get(doc_key(d["code"]), "⬜ Pendiente")}
                    for d in DOCUMENTS + FORMATS]
        csv_docs = pd.DataFrame(doc_rows).to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Documentos CSV", csv_docs,
                           f"SGI_documentos_{datetime.now().strftime('%Y%m%d')}.csv",
                           "text/csv", use_container_width=True)
