import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json, os, base64
from datetime import datetime, date

try:
    import requests
    _REQUESTS_OK = True
except ImportError:
    _REQUESTS_OK = False

st.set_page_config(page_title="SGI I+D+I - IIAD", page_icon="🔬", layout="wide")

# ── Secrets (100% seguro ante cualquier error) ───────────────────────────────
def _secret(key, default=""):
    try:
        return st.secrets[key]
    except Exception:
        return default

GH_TOKEN  = _secret("GITHUB_TOKEN")
GH_REPO   = _secret("GITHUB_REPO")
GH_PATH   = _secret("GITHUB_FILE_PATH", "sgi_state.json")
GH_BRANCH = _secret("GITHUB_BRANCH", "main")
GH_CONFIGURED = bool(GH_TOKEN and GH_REPO and _REQUESTS_OK)

def gh_load():
    if not GH_CONFIGURED:
        return None, None
    try:
        url = "https://api.github.com/repos/" + GH_REPO + "/contents/" + GH_PATH + "?ref=" + GH_BRANCH
        headers = {"Authorization": "token " + GH_TOKEN,
                   "Accept": "application/vnd.github.v3+json"}
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code == 200:
            data = r.json()
            return json.loads(base64.b64decode(data["content"]).decode("utf-8")), data["sha"]
    except Exception:
        pass
    return None, None

def gh_save(state, sha=None):
    if not GH_CONFIGURED:
        return False, "GitHub no configurado.", None
    try:
        b64 = base64.b64encode(
            json.dumps(state, ensure_ascii=False, indent=2).encode("utf-8")
        ).decode("utf-8")
        url = "https://api.github.com/repos/" + GH_REPO + "/contents/" + GH_PATH
        headers = {"Authorization": "token " + GH_TOKEN,
                   "Accept": "application/vnd.github.v3+json"}
        payload = {
            "message": "chore: estado SGI " + datetime.now().strftime("%Y-%m-%d %H:%M"),
            "content": b64,
            "branch": GH_BRANCH,
        }
        if sha:
            payload["sha"] = sha
        r = requests.put(url, headers=headers, json=payload, timeout=12)
        if r.status_code in (200, 201):
            return True, "Guardado en GitHub.", r.json()["content"]["sha"]
        return False, r.json().get("message", "HTTP " + str(r.status_code)), None
    except Exception as e:
        return False, str(e), None
