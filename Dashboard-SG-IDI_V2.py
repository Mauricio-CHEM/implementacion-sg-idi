import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json, os, base64, requests
from datetime import datetime, date

st.set_page_config(page_title='SGI I+D+I - IIAD', page_icon='🔬', layout='wide')

# ── GitHub Sync config (Streamlit Secrets) ───────────────────────────────
GH_TOKEN  = st.secrets.get('GITHUB_TOKEN',     '')
GH_REPO   = st.secrets.get('GITHUB_REPO',      '')  # 'owner/repo'
GH_PATH   = st.secrets.get('GITHUB_FILE_PATH', 'sgi_state.json')
GH_BRANCH = st.secrets.get('GITHUB_BRANCH',    'main')
GH_CONFIGURED = bool(GH_TOKEN and GH_REPO)

def _gh_headers():
    return {'Authorization': f'token {GH_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'}

def gh_load():
    if not GH_CONFIGURED:
        return None, None
    try:
        url = f'https://api.github.com/repos/{GH_REPO}/contents/{GH_PATH}?ref={GH_BRANCH}'
        r = requests.get(url, headers=_gh_headers(), timeout=8)
        if r.status_code == 200:
            d = r.json()
            return json.loads(base64.b64decode(d['content']).decode('utf-8')), d['sha']
    except Exception:
        pass
    return None, None

def gh_save(state, sha=None):
    if not GH_CONFIGURED:
        return False, 'GitHub no configurado. Usa descarga local.', None
    try:
        b64 = base64.b64encode(
            json.dumps(state, ensure_ascii=False, indent=2).encode('utf-8')
        ).decode('utf-8')
        url = f'https://api.github.com/repos/{GH_REPO}/contents/{GH_PATH}'
        payload = {
            'message': f"chore: estado SGI {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            'content': b64, 'branch': GH_BRANCH
        }
        if sha:
            payload['sha'] = sha
        r = requests.put(url, headers=_gh_headers(), json=payload, timeout=12)
        if r.status_code in (200, 201):
            new_sha = r.json()['content']['sha']
            return True, 'Guardado en GitHub correctamente.', new_sha
        return False, r.json().get('message', f'Error HTTP {r.status_code}'), None
    except Exception as e:
        return False, str(e), None
