import streamlit as st

st.set_page_config(page_title='SGI I+D+I - IIAD', page_icon=':microscope:', layout='wide')

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json, os, base64
from datetime import datetime, date

try:
    import requests
    _REQ = True
except ImportError:
    _REQ = False

def _s(k, d=''):
    try: return st.secrets[k]
    except: return d

GH_TOKEN  = _s('GITHUB_TOKEN')
GH_REPO   = _s('GITHUB_REPO')
GH_PATH   = _s('GITHUB_FILE_PATH', 'sgi_state.json')
GH_BRANCH = _s('GITHUB_BRANCH', 'main')
GH_ON     = bool(GH_TOKEN and GH_REPO and _REQ)

def gh_load():
    if not GH_ON: return None, None
    try:
        url = 'https://api.github.com/repos/' + GH_REPO + '/contents/' + GH_PATH + '?ref=' + GH_BRANCH
        h = {'Authorization': 'token ' + GH_TOKEN, 'Accept': 'application/vnd.github.v3+json'}
        r = requests.get(url, headers=h, timeout=8)
        if r.status_code == 200:
            d = r.json()
            raw = base64.b64decode(d['content']).decode().strip()
            return (json.loads(raw) if raw else {}), d['sha']
    except: pass
    return None, None

def gh_save(state, sha=None):
    if not GH_ON: return False, 'GitHub no configurado.', None
    try:
        b64 = base64.b64encode(json.dumps(state, ensure_ascii=False, indent=2).encode()).decode()
        url = 'https://api.github.com/repos/' + GH_REPO + '/contents/' + GH_PATH
        h   = {'Authorization': 'token ' + GH_TOKEN, 'Accept': 'application/vnd.github.v3+json'}
        p   = {'message': 'chore: SGI ' + datetime.now().strftime('%Y-%m-%d %H:%M'),
               'content': b64, 'branch': GH_BRANCH}
        if sha: p['sha'] = sha
        r = requests.put(url, headers=h, json=p, timeout=12)
        if r.status_code in (200, 201): return True, 'Guardado en GitHub.', r.json()['content']['sha']
        return False, r.json().get('message', 'HTTP ' + str(r.status_code)), None
    except Exception as e: return False, str(e), None

PHASES = {
    'Fase 1': {
        'name': 'Fundamentos y Diagnostico', 'months': 'Meses 1-3',
        'chapters': 'Cap. 4-5 NTC 5801', 'color': '#1565C0',
        'hito': 'Politica de I+D+I aprobada',
        'items': [
            {'id':'1.1','activity':'Equipo de implementacion conformado','ref':'S5.3','responsible':'Direccion','deadline':'Mes 1','evidence':'Acta designacion'},
            {'id':'1.2','activity':'Capacitacion equipo NTC 5801 e ISO 56002','ref':'S7.2','responsible':'Lider SGI','deadline':'Mes 1','evidence':'Registro asistencia'},
            {'id':'1.3','activity':'Analisis PESTEL elaborado','ref':'S4.1.2','responsible':'Lider SGI','deadline':'Mes 1','evidence':'DOC-01'},
            {'id':'1.4','activity':'Auditoria de capacidades internas','ref':'S4.1.3','responsible':'Lider SGI','deadline':'Mes 2','evidence':'DOC-01'},
            {'id':'1.5','activity':'Analisis de contexto documentado','ref':'S4.1','responsible':'Lider SGI','deadline':'Mes 2','evidence':'DOC-01 aprobado'},
            {'id':'1.6','activity':'Partes interesadas identificadas','ref':'S4.2','responsible':'Equipo','deadline':'Mes 2','evidence':'DOC-02'},
            {'id':'1.7','activity':'Necesidades y expectativas documentadas','ref':'S4.2.1','responsible':'Equipo','deadline':'Mes 2','evidence':'DOC-02'},
            {'id':'1.8','activity':'Mecanismos de interaccion definidos','ref':'S4.2.1c','responsible':'Equipo','deadline':'Mes 2','evidence':'DOC-02'},
            {'id':'1.9','activity':'Alcance del SGI documentado','ref':'S4.3','responsible':'Direccion','deadline':'Mes 2','evidence':'DOC-03'},
            {'id':'1.10','activity':'Interacciones ISO 17034 y 17043 en alcance','ref':'S4.3c','responsible':'Lider SGI','deadline':'Mes 2','evidence':'DOC-03'},
            {'id':'1.11','activity':'DOFA elaborado','ref':'S4.1','responsible':'Equipo','deadline':'Mes 3','evidence':'DOC-04'},
            {'id':'1.12','activity':'DOFA cruzado construido','ref':'S4.1','responsible':'Equipo','deadline':'Mes 3','evidence':'DOC-04'},
            {'id':'1.13','activity':'Vision de innovacion redactada','ref':'S5.1.3','responsible':'Direccion','deadline':'Mes 3','evidence':'DOC-05'},
            {'id':'1.14','activity':'Politica de I+D+I firmada','ref':'S5.2.1','responsible':'Alta direccion','deadline':'Mes 3','evidence':'DOC-06'},
            {'id':'1.15','activity':'Politica comunicada al personal','ref':'S5.2.2','responsible':'Comunicaciones','deadline':'Mes 3','evidence':'Registro difusion'},
            {'id':'1.16','activity':'Estrategia de innovacion documentada','ref':'S5.1.4','responsible':'Direccion','deadline':'Mes 3','evidence':'DOC-07'},
            {'id':'1.17','activity':'Roles y responsabilidades RACI definidos','ref':'S5.3','responsible':'Direccion','deadline':'Mes 3','evidence':'DOC-08'},
            {'id':'1.18','activity':'FTO-01 al FTO-05 aprobados','ref':'S7.5','responsible':'Lider SGI','deadline':'Mes 3','evidence':'Listado maestro'},
        ],
    },
    'Fase 2': {
        'name': 'Doc Estrategica y Apoyo', 'months': 'Meses 4-6',
        'chapters': 'Cap. 6-7 NTC 5801', 'color': '#2E7D32',
        'hito': 'Sistema documental base aprobado',
        'items': [
            {'id':'2.1','activity':'Riesgos y oportunidades identificados','ref':'S6.1','responsible':'Lider SGI','deadline':'Mes 4','evidence':'DOC-09'},
            {'id':'2.2','activity':'Matriz de riesgos valorada','ref':'S6.1','responsible':'Equipo','deadline':'Mes 4','evidence':'DOC-09'},
            {'id':'2.3','activity':'Planes de tratamiento de riesgos','ref':'S6.1','responsible':'Equipo','deadline':'Mes 4','evidence':'DOC-09'},
            {'id':'2.4','activity':'Objetivos de innovacion SMART definidos','ref':'S6.2.1','responsible':'Direccion','deadline':'Mes 4','evidence':'DOC-10'},
            {'id':'2.5','activity':'Planes de accion por objetivo','ref':'S6.2.2','responsible':'Lider SGI','deadline':'Mes 4','evidence':'DOC-10'},
            {'id':'2.6','activity':'Estructura organizacional I+D+I definida','ref':'S6.3','responsible':'Direccion','deadline':'Mes 4','evidence':'DOC-11'},
            {'id':'2.7','activity':'Portafolio inicial de proyectos','ref':'S6.4','responsible':'Lider SGI','deadline':'Mes 5','evidence':'DOC-12'},
            {'id':'2.8','activity':'Procedimiento gestion de recursos','ref':'S7.1','responsible':'Lider SGI','deadline':'Mes 5','evidence':'DOC-13'},
            {'id':'2.9','activity':'Presupuesto anual I+D+I aprobado','ref':'S7.1.5','responsible':'Finanzas','deadline':'Mes 5','evidence':'DOC-14'},
            {'id':'2.10','activity':'Inventario infraestructura habilitadora','ref':'S7.1.6','responsible':'Lider SGI','deadline':'Mes 5','evidence':'DOC-15'},
            {'id':'2.11','activity':'Plan gestion del conocimiento','ref':'S7.1.4','responsible':'Lider SGI','deadline':'Mes 5','evidence':'DOC-16'},
            {'id':'2.12','activity':'Matriz de competencias diligenciada','ref':'S7.2','responsible':'RRHH','deadline':'Mes 5','evidence':'DOC-17'},
            {'id':'2.13','activity':'Brechas de competencia identificadas','ref':'S7.2','responsible':'RRHH','deadline':'Mes 5','evidence':'DOC-17'},
            {'id':'2.14','activity':'Plan de capacitacion elaborado','ref':'S7.2','responsible':'RRHH','deadline':'Mes 5','evidence':'DOC-18'},
            {'id':'2.15','activity':'Plan de comunicacion aprobado','ref':'S7.4','responsible':'Comunicaciones','deadline':'Mes 6','evidence':'DOC-19'},
            {'id':'2.16','activity':'Procedimiento control de documentos','ref':'S7.5','responsible':'Lider SGI','deadline':'Mes 6','evidence':'DOC-20'},
            {'id':'2.17','activity':'Sistema de codificacion documental','ref':'S7.5','responsible':'Lider SGI','deadline':'Mes 6','evidence':'DOC-21'},
            {'id':'2.18','activity':'Listado maestro de documentos','ref':'S7.5.3','responsible':'Lider SGI','deadline':'Mes 6','evidence':'DOC-21'},
            {'id':'2.19','activity':'Catalogo de herramientas de innovacion','ref':'S7.6','responsible':'Equipo','deadline':'Mes 6','evidence':'DOC-22'},
            {'id':'2.20','activity':'Procedimiento vigilancia tecnologica','ref':'S7.7','responsible':'Lider SGI','deadline':'Mes 6','evidence':'DOC-23'},
            {'id':'2.21','activity':'Primera vigilancia tecnologica ejecutada','ref':'S7.7','responsible':'Lider SGI','deadline':'Mes 6','evidence':'VT-001'},
            {'id':'2.22','activity':'Procedimiento propiedad intelectual','ref':'S7.8','responsible':'Asesor juridico','deadline':'Mes 6','evidence':'DOC-24'},
            {'id':'2.23','activity':'FTO-06 al FTO-14 aprobados','ref':'S7.5','responsible':'Lider SGI','deadline':'Mes 6','evidence':'Listado maestro'},
        ],
    },
    'Fase 3': {
        'name': 'Doc Operativa e Implementacion', 'months': 'Meses 7-9',
        'chapters': 'Cap. 8 NTC 5801', 'color': '#E65100',
        'hito': 'Proyecto piloto en ejecucion',
        'items': [
            {'id':'3.1','activity':'Manual planificacion y control operacional','ref':'S8.1','responsible':'Lider SGI','deadline':'Mes 7','evidence':'DOC-25'},
            {'id':'3.2','activity':'Procedimiento gestion de iniciativas','ref':'S8.2','responsible':'Lider SGI','deadline':'Mes 7','evidence':'DOC-26'},
            {'id':'3.3','activity':'Procedimiento identificacion oportunidades','ref':'S8.3.2','responsible':'Lider SGI','deadline':'Mes 7','evidence':'DOC-27'},
            {'id':'3.4','activity':'Procedimiento creacion de conceptos','ref':'S8.3.3','responsible':'Lider SGI','deadline':'Mes 7','evidence':'DOC-28'},
            {'id':'3.5','activity':'Procedimiento validacion de conceptos','ref':'S8.3.4','responsible':'Lider SGI','deadline':'Mes 8','evidence':'DOC-29'},
            {'id':'3.6','activity':'Procedimiento desarrollo de soluciones','ref':'S8.3.5','responsible':'Lider SGI','deadline':'Mes 8','evidence':'DOC-30'},
            {'id':'3.7','activity':'Procedimiento despliegue de soluciones','ref':'S8.3.6','responsible':'Lider SGI','deadline':'Mes 8','evidence':'DOC-31'},
            {'id':'3.8','activity':'Manual gestion proyectos NTC 5802','ref':'NTC5802','responsible':'Lider SGI','deadline':'Mes 8','evidence':'DOC-32'},
            {'id':'3.9','activity':'Formato formulacion de proyecto MinCiencias','ref':'NTC5802','responsible':'Lider SGI','deadline':'Mes 8','evidence':'FTO-19'},
            {'id':'3.10','activity':'Al menos 1 proyecto piloto en ejecucion','ref':'S8.3','responsible':'Investigador','deadline':'Mes 9','evidence':'Ficha proyecto'},
            {'id':'3.11','activity':'Primera acta comite de innovacion','ref':'S8.2','responsible':'Lider SGI','deadline':'Mes 9','evidence':'FTO-23'},
            {'id':'3.12','activity':'FTO-15 al FTO-24 aprobados','ref':'S7.5','responsible':'Lider SGI','deadline':'Mes 9','evidence':'Listado maestro'},
            {'id':'3.13','activity':'Laboratorio en InstituLAC MinCiencias','ref':'Ext.','responsible':'Direccion','deadline':'Mes 7','evidence':'Constancia registro'},
            {'id':'3.14','activity':'Grupos registrados en GrupLAC','ref':'Ext.','responsible':'Investigador lider','deadline':'Mes 8','evidence':'Ficha GrupLAC'},
            {'id':'3.15','activity':'CvLAC del personal actualizado','ref':'Ext.','responsible':'Investigadores','deadline':'Mes 8','evidence':'Perfiles activos'},
            {'id':'3.16','activity':'Productos de investigacion clasificados','ref':'Ext.','responsible':'Lider SGI','deadline':'Mes 9','evidence':'Listado clasificado'},
        ],
    },
    'Fase 4': {
        'name': 'Evaluacion Auditoria y Mejora', 'months': 'Meses 10-12',
        'chapters': 'Cap. 9-10 NTC 5801', 'color': '#6A1B9A',
        'hito': 'Primera auditoria interna realizada',
        'items': [
            {'id':'4.1','activity':'Procedimiento seguimiento y medicion','ref':'S9.1.1','responsible':'Lider SGI','deadline':'Mes 10','evidence':'DOC-34'},
            {'id':'4.2','activity':'Indicadores de I+D+I definidos','ref':'S9.1.2','responsible':'Lider SGI','deadline':'Mes 10','evidence':'DOC-35'},
            {'id':'4.3','activity':'Linea base de indicadores establecida','ref':'S9.1.2','responsible':'Lider SGI','deadline':'Mes 10','evidence':'Registro inicial'},
            {'id':'4.4','activity':'Dashboard de seguimiento implementado','ref':'S9.1','responsible':'Lider SGI','deadline':'Mes 10','evidence':'Base datos activa'},
            {'id':'4.5','activity':'Programa anual de auditorias','ref':'S9.2','responsible':'Auditor interno','deadline':'Mes 10','evidence':'DOC-38'},
            {'id':'4.6','activity':'Auditor interno capacitado NTC 5801','ref':'S9.2','responsible':'Direccion','deadline':'Mes 10','evidence':'Certificado'},
            {'id':'4.7','activity':'Lista verificacion auditoria elaborada','ref':'S9.2','responsible':'Auditor interno','deadline':'Mes 10','evidence':'DOC-39'},
            {'id':'4.8','activity':'Primera auditoria interna realizada','ref':'S9.2','responsible':'Auditor interno','deadline':'Mes 11','evidence':'DOC-40'},
            {'id':'4.9','activity':'No conformidades identificadas','ref':'S10.2','responsible':'Auditor interno','deadline':'Mes 11','evidence':'FTO-26'},
            {'id':'4.10','activity':'Planes de accion correctiva elaborados','ref':'S10.2','responsible':'Responsables','deadline':'Mes 11','evidence':'FTO-27'},
            {'id':'4.11','activity':'Procedimiento revision por la direccion','ref':'S9.3','responsible':'Direccion','deadline':'Mes 11','evidence':'DOC-41'},
            {'id':'4.12','activity':'Primera revision por la direccion realizada','ref':'S9.3','responsible':'Alta direccion','deadline':'Mes 12','evidence':'DOC-42'},
            {'id':'4.13','activity':'Informe anual desempeno del SGI','ref':'S9.1.2','responsible':'Lider SGI','deadline':'Mes 12','evidence':'DOC-36'},
            {'id':'4.14','activity':'Plan mejora continua anio 2','ref':'S10.3','responsible':'Equipo','deadline':'Mes 12','evidence':'DOC-45'},
            {'id':'4.15','activity':'FTO-25 al FTO-30 en uso','ref':'S7.5','responsible':'Lider SGI','deadline':'Mes 12','evidence':'Listado maestro'},
            {'id':'4.16','activity':'Sistema listo para evaluacion ICONTEC','ref':'S4-10','responsible':'Lider SGI','deadline':'Mes 12','evidence':'45 documentos base'},
        ],
    },
}

DOCUMENTS = [
    {'code':'DOC-01','name':'Analisis cuestiones externas e internas','phase':'Fase 1','chapter':'S4.1','type':'Procedimiento + Registro'},
    {'code':'DOC-02','name':'Matriz de partes interesadas','phase':'Fase 1','chapter':'S4.2','type':'Registro vivo'},
    {'code':'DOC-03','name':'Alcance del SGI','phase':'Fase 1','chapter':'S4.3','type':'Declaracion formal'},
    {'code':'DOC-04','name':'Analisis DOFA del laboratorio','phase':'Fase 1','chapter':'S4.1','type':'Registro interno'},
    {'code':'DOC-05','name':'Vision de innovacion','phase':'Fase 1','chapter':'S5.1.3','type':'Declaracion estrategica'},
    {'code':'DOC-06','name':'Politica de I+D+I','phase':'Fase 1','chapter':'S5.2.1','type':'Documento oficial'},
    {'code':'DOC-07','name':'Estrategia de innovacion','phase':'Fase 1','chapter':'S5.1.4','type':'Documento estrategico'},
    {'code':'DOC-08','name':'Matriz RACI roles y responsabilidades','phase':'Fase 1','chapter':'S5.3','type':'Organigrama + RACI'},
    {'code':'DOC-09','name':'Matriz de riesgos y oportunidades','phase':'Fase 2','chapter':'S6.1','type':'Registro vivo'},
    {'code':'DOC-10','name':'Objetivos SMART y planes de accion','phase':'Fase 2','chapter':'S6.2','type':'Plan formal'},
    {'code':'DOC-11','name':'Estructura organizacional I+D+I','phase':'Fase 2','chapter':'S6.3','type':'Organigrama'},
    {'code':'DOC-12','name':'Portafolio de iniciativas','phase':'Fase 2','chapter':'S6.4','type':'Base de datos'},
    {'code':'DOC-13','name':'Procedimiento gestion de recursos','phase':'Fase 2','chapter':'S7.1','type':'Procedimiento'},
    {'code':'DOC-14','name':'Presupuesto anual I+D+I','phase':'Fase 2','chapter':'S7.1.5','type':'Plan financiero'},
    {'code':'DOC-15','name':'Inventario infraestructura habilitadora','phase':'Fase 2','chapter':'S7.1.6','type':'Registro'},
    {'code':'DOC-16','name':'Plan gestion del conocimiento','phase':'Fase 2','chapter':'S7.1.4','type':'Plan'},
    {'code':'DOC-17','name':'Matriz de competencias del personal','phase':'Fase 2','chapter':'S7.2','type':'Registro'},
    {'code':'DOC-18','name':'Plan anual de capacitacion','phase':'Fase 2','chapter':'S7.2','type':'Plan'},
    {'code':'DOC-19','name':'Plan de comunicacion del SGI','phase':'Fase 2','chapter':'S7.4','type':'Plan'},
    {'code':'DOC-20','name':'Procedimiento control de documentos','phase':'Fase 2','chapter':'S7.5','type':'Procedimiento maestro'},
    {'code':'DOC-21','name':'Listado maestro de documentos','phase':'Fase 2','chapter':'S7.5.3','type':'Registro vivo'},
    {'code':'DOC-22','name':'Catalogo herramientas de innovacion','phase':'Fase 2','chapter':'S7.6','type':'Catalogo'},
    {'code':'DOC-23','name':'Procedimiento vigilancia tecnologica','phase':'Fase 2','chapter':'S7.7','type':'Procedimiento'},
    {'code':'DOC-24','name':'Procedimiento propiedad intelectual','phase':'Fase 2','chapter':'S7.8','type':'Procedimiento'},
    {'code':'DOC-25','name':'Manual planificacion y control operacional','phase':'Fase 3','chapter':'S8.1','type':'Manual'},
    {'code':'DOC-26','name':'Procedimiento gestion de iniciativas','phase':'Fase 3','chapter':'S8.2','type':'Procedimiento'},
    {'code':'DOC-27','name':'Procedimiento identificacion oportunidades','phase':'Fase 3','chapter':'S8.3.2','type':'Procedimiento'},
    {'code':'DOC-28','name':'Procedimiento creacion de conceptos','phase':'Fase 3','chapter':'S8.3.3','type':'Procedimiento'},
    {'code':'DOC-29','name':'Procedimiento validacion de conceptos','phase':'Fase 3','chapter':'S8.3.4','type':'Procedimiento'},
    {'code':'DOC-30','name':'Procedimiento desarrollo de soluciones','phase':'Fase 3','chapter':'S8.3.5','type':'Procedimiento'},
    {'code':'DOC-31','name':'Procedimiento despliegue de soluciones','phase':'Fase 3','chapter':'S8.3.6','type':'Procedimiento'},
    {'code':'DOC-32','name':'Manual gestion proyectos NTC 5802','phase':'Fase 3','chapter':'S8+5802','type':'Manual'},
    {'code':'DOC-33','name':'Formato formulacion proyecto MinCiencias','phase':'Fase 3','chapter':'NTC5802','type':'Formato estandar'},
    {'code':'DOC-34','name':'Procedimiento seguimiento y medicion','phase':'Fase 4','chapter':'S9.1.1','type':'Procedimiento'},
    {'code':'DOC-35','name':'Tablero de indicadores KPIs','phase':'Fase 4','chapter':'S9.1.2','type':'Dashboard'},
    {'code':'DOC-36','name':'Informe anual desempeno SGI','phase':'Fase 4','chapter':'S9.1.2','type':'Informe'},
    {'code':'DOC-37','name':'Procedimiento auditoria interna','phase':'Fase 4','chapter':'S9.2','type':'Procedimiento'},
    {'code':'DOC-38','name':'Programa anual de auditorias','phase':'Fase 4','chapter':'S9.2','type':'Plan'},
    {'code':'DOC-39','name':'Lista verificacion auditoria','phase':'Fase 4','chapter':'S9.2','type':'Instrumento'},
    {'code':'DOC-40','name':'Informe de auditoria interna','phase':'Fase 4','chapter':'S9.2','type':'Registro'},
    {'code':'DOC-41','name':'Procedimiento revision por la direccion','phase':'Fase 4','chapter':'S9.3','type':'Procedimiento'},
    {'code':'DOC-42','name':'Informe revision por la direccion','phase':'Fase 4','chapter':'S9.3','type':'Registro'},
    {'code':'DOC-43','name':'Procedimiento no conformidades','phase':'Fase 4','chapter':'S10.2','type':'Procedimiento'},
    {'code':'DOC-44','name':'Registro no conformidades y mejoras','phase':'Fase 4','chapter':'S10.2','type':'Registro vivo'},
    {'code':'DOC-45','name':'Plan de mejora continua del SGI','phase':'Fase 4','chapter':'S10.3','type':'Plan anual'},
]

FORMATS = [
    {'code':'FTO-01','name':'Formato analisis PESTEL','phase':'Fase 1'},
    {'code':'FTO-02','name':'Plantilla matriz partes interesadas','phase':'Fase 1'},
    {'code':'FTO-03','name':'Plantilla DOFA cruzada','phase':'Fase 1'},
    {'code':'FTO-04','name':'Acta reunion alta direccion','phase':'Fase 1'},
    {'code':'FTO-05','name':'Acta conformacion equipo implementacion','phase':'Fase 1'},
    {'code':'FTO-06','name':'Formato identificacion y evaluacion riesgos','phase':'Fase 2'},
    {'code':'FTO-07','name':'Ficha objetivo de innovacion','phase':'Fase 2'},
    {'code':'FTO-08','name':'Formato solicitud y asignacion recursos','phase':'Fase 2'},
    {'code':'FTO-09','name':'Perfil competencias por cargo','phase':'Fase 2'},
    {'code':'FTO-10','name':'Formato evaluacion de competencias','phase':'Fase 2'},
    {'code':'FTO-11','name':'Formato solicitud de capacitacion','phase':'Fase 2'},
    {'code':'FTO-12','name':'Registro asistencia capacitaciones','phase':'Fase 2'},
    {'code':'FTO-13','name':'Solicitud proteccion propiedad intelectual','phase':'Fase 2'},
    {'code':'FTO-14','name':'Informe vigilancia tecnologica','phase':'Fase 2'},
    {'code':'FTO-15','name':'Formato captacion ideas y oportunidades','phase':'Fase 3'},
    {'code':'FTO-16','name':'Ficha evaluacion preliminar de ideas','phase':'Fase 3'},
    {'code':'FTO-17','name':'Formato desarrollo de concepto','phase':'Fase 3'},
    {'code':'FTO-18','name':'Protocolo prueba o validacion experimental','phase':'Fase 3'},
    {'code':'FTO-19','name':'Ficha de proyecto I+D+I','phase':'Fase 3'},
    {'code':'FTO-20','name':'Cronograma de proyecto Gantt','phase':'Fase 3'},
    {'code':'FTO-21','name':'Informe de avance de proyecto','phase':'Fase 3'},
    {'code':'FTO-22','name':'Informe final de proyecto','phase':'Fase 3'},
    {'code':'FTO-23','name':'Acta comite de innovacion','phase':'Fase 3'},
    {'code':'FTO-24','name':'Registro lecciones aprendidas','phase':'Fase 3'},
    {'code':'FTO-25','name':'Ficha de indicador KPI','phase':'Fase 4'},
    {'code':'FTO-26','name':'Formato reporte no conformidad','phase':'Fase 4'},
    {'code':'FTO-27','name':'Formato accion correctiva y preventiva','phase':'Fase 4'},
    {'code':'FTO-28','name':'Lista chequeo auditoria interna','phase':'Fase 4'},
    {'code':'FTO-29','name':'Acta revision por la direccion','phase':'Fase 4'},
    {'code':'FTO-30','name':'Encuesta satisfaccion partes interesadas','phase':'Fase 4'},
]

STATUS_OPTIONS = ['Pendiente', 'En proceso', 'Completo', 'No aplica']
STATE_FILE     = 'sgi_state.json'
PHASE_PAGES    = {'Fase 1 - Fundamentos': 'Fase 1', 'Fase 2 - Apoyo Estrategico': 'Fase 2',
                  'Fase 3 - Operacion': 'Fase 3', 'Fase 4 - Evaluacion y Mejora': 'Fase 4'}
MES_HITO       = {'Fase 1':'Mes 3','Fase 2':'Mes 6','Fase 3':'Mes 9','Fase 4':'Mes 12'}

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                txt = f.read().strip()
            return json.loads(txt) if txt else {}
        except Exception:
            return {}
    return {}

def save_state(s):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(s, f, ensure_ascii=False, indent=2)

def ikey(pk, iid): return 'chk_' + pk + '_' + iid
def dkey(code):    return 'doc_' + code

def get_istate(key):
    v = st.session_state.state.get(key, {})
    if isinstance(v, str): v = {'status': v}
    return {'status': v.get('status','Pendiente'), 'fecha_inicio': v.get('fecha_inicio',''),
            'fecha_fin': v.get('fecha_fin',''), 'responsable_nombre': v.get('responsable_nombre',''),
            'rol': v.get('rol',''), 'comentario': v.get('comentario','')}

def save_istate(key, data):
    st.session_state.state[key] = data
    save_state(st.session_state.state)

def get_custom_code(orig):
    return st.session_state.state.get('custom_codes', {}).get(orig, orig)

def set_custom_code(orig, new):
    st.session_state.state.setdefault('custom_codes', {})[orig] = new.strip() or orig
    save_state(st.session_state.state)

def get_doc_status(code):
    v = st.session_state.state.get(dkey(code), 'Pendiente')
    return v if isinstance(v, str) else v.get('status', 'Pendiente')

def set_doc_status(code, status):
    v = st.session_state.state.get(dkey(code), {})
    if isinstance(v, str): v = {'status': v}
    v['status'] = status
    st.session_state.state[dkey(code)] = v
    save_state(st.session_state.state)

if 'state' not in st.session_state:
    st.session_state.state     = load_state()
    st.session_state.gh_sha    = None
    st.session_state.gh_source = 'local'
    st.session_state.gh_loaded = False

def phase_progress(pk):
    items = PHASES[pk]['items']
    total = len(items)
    done  = sum(1 for i in items if get_istate(ikey(pk, i['id']))['status'] == 'Completo')
    wip   = sum(1 for i in items if get_istate(ikey(pk, i['id']))['status'] == 'En proceso')
    na    = sum(1 for i in items if get_istate(ikey(pk, i['id']))['status'] == 'No aplica')
    appl  = total - na
    return total, done, wip, na, (round(done / appl * 100) if appl > 0 else 0)

def overall_progress():
    ai = sum(len(PHASES[pk]['items']) for pk in PHASES)
    ad = sum(phase_progress(pk)[1] for pk in PHASES)
    an = sum(phase_progress(pk)[3] for pk in PHASES)
    ap = ai - an
    return ai, ad, ap, (round(ad / ap * 100) if ap > 0 else 0)

def doc_progress():
    all_d = DOCUMENTS + FORMATS
    tot   = len(all_d)
    done  = sum(1 for d in all_d if get_doc_status(d['code']) == 'Completo')
    return tot, done, (round(done / tot * 100) if tot > 0 else 0)

st.markdown('''<style>
[data-testid="stSidebar"]{background-color:#0D1B2A}
[data-testid="stSidebar"] *{color:#E8EDF3!important}
[data-testid="stSidebar"] hr{border-color:#2a3f5a!important}
.kcard{background:white;border-radius:12px;padding:16px;border-left:5px solid;
       box-shadow:0 2px 8px rgba(0,0,0,.07);margin-bottom:10px}
.kpct{font-size:2rem;font-weight:800;margin:4px 0}
.tag{display:inline-block;padding:2px 9px;border-radius:20px;font-size:.74rem;font-weight:600}
</style>''', unsafe_allow_html=True)

with st.sidebar:
    lb = st.session_state.state.get('logo_b64')
    if lb:
        st.markdown('<img src="' + lb + '" style="width:100%;border-radius:8px;margin-bottom:10px">',
                    unsafe_allow_html=True)
    st.markdown('## Seguimiento de implementación sistema de gestión de la investigación')
    st.markdown('### Laboratorio Nacional de Insumo Agrícolas - LANIA - Área IIAD')
    st.markdown('*basado en las normas NTC 5801 / ISO 56002*')
    if GH_ON and not st.session_state.gh_loaded:
        st.session_state.gh_loaded = True
        with st.spinner('Sincronizando...'):
            gh_state, gh_sha = gh_load()
        if gh_state is not None:
            st.session_state.state     = gh_state
            st.session_state.gh_sha    = gh_sha
            st.session_state.gh_source = 'github'
            save_state(gh_state)
            st.rerun()
    if GH_ON:
        src   = st.session_state.get('gh_source', 'local')
        color = '#238636' if src == 'github' else '#6e7681'
        label = 'GitHub activo' if src == 'github' else 'Sin sincronizar'
        st.markdown('<span style="background:' + color + ';color:white;padding:3px 10px;'
                    'border-radius:10px;font-size:.74rem;font-weight:600">' + label + '</span>',
                    unsafe_allow_html=True)
    st.markdown('---')
    page = st.radio('', ['Dashboard','Fase 1 - Fundamentos','Fase 2 - Apoyo Estrategico',
                          'Fase 3 - Operacion','Fase 4 - Evaluacion y Mejora',
                          'Registro Documental','Reportes y Exportar','Configuracion'],
                     label_visibility='collapsed')
    st.markdown('---')
    _, done_all, appl_all, pct_all = overall_progress()
    st.markdown('### Avance: **' + str(pct_all) + '%**')
    st.progress(pct_all / 100)
    st.caption(str(done_all) + ' de ' + str(appl_all) + ' completadas')
    st.markdown('---')
    if GH_ON:
        st.markdown('##### Sync GitHub')
        c1, c2 = st.columns(2)
        with c1:
            if st.button('Recargar', use_container_width=True):
                with st.spinner('...'): s, sha = gh_load()
                if s:
                    st.session_state.state = s; st.session_state.gh_sha = sha
                    st.session_state.gh_source = 'github'; save_state(s); st.rerun()
                else: st.error('Error al conectar.')
        with c2:
            if st.button('Guardar', use_container_width=True, type='primary'):
                with st.spinner('...'): ok, msg, sha2 = gh_save(st.session_state.state, st.session_state.gh_sha)
                if ok: st.session_state.gh_sha = sha2; st.session_state.gh_source = 'github'; st.success(msg)
                else: st.error(msg)
        st.markdown('---')
    st.download_button('Descargar JSON',
        data=json.dumps(st.session_state.state, ensure_ascii=False, indent=2).encode(),
        file_name='sgi_' + datetime.now().strftime('%Y%m%d_%H%M') + '.json',
        mime='application/json', use_container_width=True)
    if not GH_ON:
        st.markdown('---')
        uf = st.file_uploader('Cargar sgi_state.json', type=['json'])
        if uf:
            try:
                loaded = json.load(uf); st.session_state.state = loaded
                save_state(loaded); st.rerun()
            except Exception as e: st.error(str(e))

if page == 'Dashboard':
    st.title('Sistema de Gestion I+D+I - Área de Investigación e Innovación Analítica y Diagnóstica')
    st.markdown('**Laboratorio LANIA* | NTC 5801 / ISO 56002 | ' + datetime.now().strftime('%d/%m/%Y'))
    if GH_ON:
        src = st.session_state.get('gh_source','local')
        sha_s = (st.session_state.gh_sha or '')[:7]
        if src == 'github': st.info('Sincronizado con GitHub  SHA: ' + sha_s)
        else: st.warning('Estado local. Presiona Guardar para sincronizar.')
    st.divider()
    _, done_all, appl_all, pct_all = overall_progress()
    tot_docs, done_docs, pct_docs  = doc_progress()
    phases_done = sum(1 for pk in PHASES if phase_progress(pk)[4] == 100)
    wip_all     = sum(phase_progress(pk)[2] for pk in PHASES)
    k1,k2,k3,k4 = st.columns(4)
    k1.metric('Avance General', str(pct_all)+'%', str(done_all)+'/'+str(appl_all)+' actividades')
    k2.metric('Documentos', str(pct_docs)+'%', str(done_docs)+'/'+str(tot_docs)+' elaborados')
    k3.metric('Fases completadas', str(phases_done)+'/4')
    k4.metric('En proceso', wip_all, 'actividades activas')
    st.divider()
    st.markdown('### Progreso por Fase')
    cols = st.columns(4)
    for i, pk in enumerate(PHASES):
        ph = PHASES[pk]
        total,done,wip,na,pct = phase_progress(pk)
        pend = total-done-wip-na
        card = ('<div class="kcard" style="border-left-color:'+ph['color']+'">'
                '<div style="font-weight:700">'+pk+'</div>'
                '<div style="font-size:.8rem;color:#777">'+ph['name']+'</div>'
                '<div class="kpct" style="color:'+ph['color']+'">'+str(pct)+'%</div>'
                '<div style="font-size:.8rem;color:#777">'+ph['months']+'</div>'
                '<div style="margin-top:8px;font-size:.82rem">'
                'OK '+str(done)+' | ~ '+str(wip)+' | P '+str(pend)+' | N/A '+str(na)
                +'</div></div>')
        with cols[i]: st.markdown(card, unsafe_allow_html=True); st.progress(pct/100)
    st.divider()
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('#### Estado por fase')
        cr = []
        for pk in PHASES:
            total,done,wip,na,_ = phase_progress(pk)
            cr += [{'Fase':pk,'Estado':'Completo','n':done},
                   {'Fase':pk,'Estado':'En proceso','n':wip},
                   {'Fase':pk,'Estado':'Pendiente','n':total-done-wip-na},
                   {'Fase':pk,'Estado':'No aplica','n':na}]
        fig = px.bar(pd.DataFrame(cr),x='Fase',y='n',color='Estado',barmode='stack',height=300,
                     color_discrete_map={'Completo':'#4CAF50','En proceso':'#2196F3','Pendiente':'#CFD8DC','No aplica':'#FF7043'})
        fig.update_layout(plot_bgcolor='white',legend=dict(orientation='h',y=-0.3))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('#### Radar de avance')
        lbls=['F'+str(i+1)+': '+PHASES[pk]['name'][:14] for i,pk in enumerate(PHASES)]
        vals=[phase_progress(pk)[4] for pk in PHASES]
        fig_r=go.Figure(go.Scatterpolar(r=vals+[vals[0]],theta=lbls+[lbls[0]],
            fill='toself',fillcolor='rgba(21,101,192,0.15)',line=dict(color='#1565C0',width=2)))
        fig_r.update_layout(polar=dict(radialaxis=dict(range=[0,100])),height=300,margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig_r,use_container_width=True)
    st.divider()
    st.markdown('### Hitos de Cierre')
    mc = st.columns(4)
    for i,pk in enumerate(PHASES):
        ph=PHASES[pk]; _,done,_,_,pct=phase_progress(pk)
        ico='OK' if pct==100 else ('~' if done>0 else '...')
        hito=('<div style="background:'+ph['color']+'12;border:1px solid '+ph['color']+'40;'
              'border-radius:10px;padding:14px;text-align:center">'
              '<div style="color:'+ph['color']+';font-weight:700">'+MES_HITO[pk]+'</div>'
              '<div style="font-size:1.3rem;margin:6px 0">'+ico+'</div>'
              '<div style="font-size:.8rem;color:#444">'+ph['hito']+'</div></div>')
        with mc[i]: st.markdown(hito,unsafe_allow_html=True)

elif page in PHASE_PAGES:
    pk=PHASE_PAGES[page]; ph=PHASES[pk]
    total,done,wip,na,pct=phase_progress(pk)
    st.title(pk+': '+ph['name'])
    st.markdown('**'+ph['months']+'** | '+ph['chapters'])
    st.divider()
    kc=st.columns(5)
    kc[0].metric('Avance',str(pct)+'%'); kc[1].metric('Completas',done)
    kc[2].metric('En proceso',wip); kc[3].metric('Pendientes',total-done-wip-na); kc[4].metric('No aplica',na)
    st.progress(pct/100); st.divider()
    fc1,fc2,fc3=st.columns(3)
    with fc1: f_st=st.multiselect('Estado:',STATUS_OPTIONS,default=STATUS_OPTIONS,key='fs_'+pk)
    with fc2: f_tx=st.text_input('Buscar:',key='ft_'+pk)
    with fc3:
        resps=sorted(set(i['responsible'] for i in ph['items']))
        f_rp=st.multiselect('Responsable:',resps,default=resps,key='fr_'+pk)
    st.divider()
    hdr=st.columns([0.4,0.6,4.2,0.9,1.6])
    for col,lbl in zip(hdr,['**#**','**Ref.**','**Actividad**','**Plazo**','**Estado**']): col.markdown(lbl)
    st.markdown('<hr style="margin:4px 0">',unsafe_allow_html=True)
    for item in ph['items']:
        k=ikey(pk,item['id']); ist=get_istate(k); cur=ist['status']
        if cur not in f_st: continue
        if f_tx and f_tx.lower() not in item['activity'].lower(): continue
        if item['responsible'] not in f_rp: continue
        row=st.columns([0.4,0.6,4.2,0.9,1.6])
        row[0].markdown('**'+item['id']+'**')
        row[1].markdown('`'+item['ref']+'`')
        badges=''
        if ist['responsable_nombre']: badges+=' | '+ist['responsable_nombre']
        if ist['fecha_inicio']:       badges+=' | '+ist['fecha_inicio']
        if ist['fecha_fin']:          badges+=' -> '+ist['fecha_fin']
        row[2].markdown(item['activity']+'<br><small style="color:#888">'+badges+'</small>',unsafe_allow_html=True)
        row[3].markdown('<small>'+item['deadline']+'</small>',unsafe_allow_html=True)
        new_st=row[4].selectbox('',STATUS_OPTIONS,index=STATUS_OPTIONS.index(cur),
                                 key='sel_'+pk+'_'+item['id'],label_visibility='collapsed')
        if new_st!=cur: ist['status']=new_st; save_istate(k,ist); st.rerun()
        with st.expander('Detalles  '+item['id']+': '+item['activity'][:55]):
            d1,d2,d3,d4=st.columns(4)
            try:    fi_v=date.fromisoformat(ist['fecha_inicio']) if ist['fecha_inicio'] else None
            except: fi_v=None
            try:    ff_v=date.fromisoformat(ist['fecha_fin']) if ist['fecha_fin'] else None
            except: ff_v=None
            new_fi  =d1.date_input('Fecha inicio',value=fi_v,key='fi_'+pk+'_'+item['id'])
            new_ff  =d2.date_input('Fecha fin',value=ff_v,key='ff_'+pk+'_'+item['id'])
            new_resp=d3.text_input('Responsable',value=ist['responsable_nombre'],key='rn_'+pk+'_'+item['id'])
            new_rol =d4.text_input('Rol',value=ist['rol'],key='rl_'+pk+'_'+item['id'])
            new_cmt =st.text_area('Comentario / Enlace',value=ist['comentario'],key='cm_'+pk+'_'+item['id'],height=70)
            if ist['comentario'] and ist['comentario'].startswith('http'):
                st.markdown('<a href="'+ist['comentario']+'" target="_blank">Ver evidencia</a>',unsafe_allow_html=True)
            st.caption('Evidencia esperada: '+item['evidence'])
            if st.button('Guardar',key='sv_'+pk+'_'+item['id'],type='primary'):
                save_istate(k,{'status':cur,'fecha_inicio':str(new_fi) if new_fi else '',
                    'fecha_fin':str(new_ff) if new_ff else '','responsable_nombre':new_resp,
                    'rol':new_rol,'comentario':new_cmt})
                st.success('Guardado.')
        st.markdown('<hr style="margin:3px 0;opacity:.2">',unsafe_allow_html=True)

elif page == 'Registro Documental':
    st.title('Registro Documental del SGI')
    st.markdown('**45 documentos base** y **30 formatos operativos**.')
    edit_codes=st.checkbox('Editar codigos SGC',value=False)
    st.divider()
    t1,t2=st.tabs(['Documentos Base (45)','Formatos (30)'])
    for tab,items_list,tid in [(t1,DOCUMENTS,'docs'),(t2,FORMATS,'fmts')]:
        with tab:
            pf=st.multiselect('Fase:',['Fase 1','Fase 2','Fase 3','Fase 4'],
                               default=['Fase 1','Fase 2','Fase 3','Fase 4'],key='df_'+tid)
            hdr=st.columns([0.5,1.0,0.9,4.1,1.6])
            for col,lbl in zip(hdr,['**Fase**','**Codigo**','**Ref.**','**Nombre**','**Estado**']): col.markdown(lbl)
            st.markdown('<hr style="margin:4px 0">',unsafe_allow_html=True)
            for d in items_list:
                if d['phase'] not in pf: continue
                cur_s=get_doc_status(d['code']); cc=get_custom_code(d['code'])
                color=PHASES[d['phase']]['color']
                tag='<span class="tag" style="background:'+color+'20;color:'+color+'">'+d['phase']+'</span>'
                row=st.columns([0.5,1.0,0.9,4.1,1.6])
                row[0].markdown(tag,unsafe_allow_html=True)
                if edit_codes:
                    nc=row[1].text_input('',value=cc,key='cedit_'+d['code'],label_visibility='collapsed')
                    if nc!=cc: set_custom_code(d['code'],nc)
                else:
                    row[1].markdown('**`'+cc+'`**' if cc!=d['code'] else '`'+cc+'`')
                row[2].markdown('<small>`'+d.get('chapter','-')+'`</small>',unsafe_allow_html=True)
                row[3].markdown(d['name']+'<br><small style="color:#999">'+d.get('type','-')+'</small>',unsafe_allow_html=True)
                new_s=row[4].selectbox('',STATUS_OPTIONS,index=STATUS_OPTIONS.index(cur_s),
                                        key='dsel_'+d['code'],label_visibility='collapsed')
                if new_s!=cur_s: set_doc_status(d['code'],new_s); st.rerun()
                st.markdown('<hr style="margin:3px 0;opacity:.18">',unsafe_allow_html=True)

elif page == 'Reportes y Exportar':
    st.title('Reportes de Avance'); st.divider()
    rows=[]
    for pk,ph in PHASES.items():
        for item in ph['items']:
            ist=get_istate(ikey(pk,item['id']))
            rows.append({'Fase':pk,'ID':item['id'],'Actividad':item['activity'],
                         'Ref. NTC':item['ref'],'Plazo':item['deadline'],
                         'Responsable':ist['responsable_nombre'],'Estado':ist['status'],'Comentario':ist['comentario']})
    df=pd.DataFrame(rows)
    st.markdown('### Resumen por Fase')
    summary=[]
    for pk in PHASES:
        total,done,wip,na,pct=phase_progress(pk)
        summary.append({'Fase':pk+': '+PHASES[pk]['name'],'Total':total,'Completas':done,
                         'En proceso':wip,'Pendientes':total-done-wip-na,'N/A':na,'% Avance':str(pct)+'%'})
    st.dataframe(pd.DataFrame(summary),use_container_width=True,hide_index=True)
    st.divider()
    dfp=df[df['Estado'].isin(['En proceso','Pendiente'])]
    st.markdown('### Pendientes / En proceso ('+str(len(dfp))+')')
    if dfp.empty: st.success('Todas completadas.')
    else: st.dataframe(dfp,use_container_width=True,hide_index=True)
    st.divider()
    st.download_button('Descargar CSV',data=df.to_csv(index=False).encode(),
        file_name='SGI_'+datetime.now().strftime('%Y%m%d')+'.csv',mime='text/csv',use_container_width=True)

elif page == 'Configuracion':
    st.title('Configuracion'); st.divider()
    st.markdown('### GitHub Sync')
    if GH_ON:
        st.success('Repo: '+GH_REPO+' | '+GH_PATH+' | '+GH_BRANCH)
        st.caption('SHA: '+(st.session_state.gh_sha or 'no cargado')[:7]+' | '+st.session_state.get('gh_source','local'))
    else:
        st.warning('GitHub Sync no configurado. Agrega estos Secrets en Streamlit Cloud:')
        st.code('GITHUB_TOKEN     = ghp_xxxx')
        st.code('GITHUB_REPO      = usuario/repo')
        st.code('GITHUB_FILE_PATH = sgi_state.json')
        st.code('GITHUB_BRANCH    = main')
    st.divider()
    st.markdown('### Logo institucional')
    lb=st.session_state.state.get('logo_b64')
    c1,c2=st.columns([1,2])
    with c1:
        if lb: st.markdown('<img src="'+lb+'" style="width:100%">',unsafe_allow_html=True)
        else: st.info('Sin logo.')
    with c2:
        lf=st.file_uploader('Subir logo',type=['png','jpg','jpeg'])
        if lf:
            raw=lf.read(); ext=lf.name.rsplit('.',1)[-1].lower()
            st.session_state.state['logo_b64']='data:image/'+ext+';base64,'+base64.b64encode(raw).decode()
            save_state(st.session_state.state); st.rerun()
        if lb and st.button('Quitar logo'):
            st.session_state.state.pop('logo_b64',None); save_state(st.session_state.state); st.rerun()
    st.divider()
    n=sum(len(PHASES[pk]['items']) for pk in PHASES)
    st.markdown('**Version:** 4.2 | **Actividades:** '+str(n)+' | **Docs:** 45 | **Formatos:** 30')
