# src/oauth_helper.py
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes que necesitamos
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

OAUTH_FILE = "oauth_credentials.json"  # el JSON que descargaste para OAuth
TOKEN_FILE = "token.json"              # donde guardaremos el token tras consent

def get_credentials(oauth_file: str = OAUTH_FILE, token_file: str = TOKEN_FILE):
    """
    Devuelve credenciales OAuth válidas para usar con googleapiclient.
    Si no existe token.json, abre el flujo interactivo (navegador).
    """
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # Si no hay credenciales válidas, iniciar el flujo
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(oauth_file, SCOPES)
            # Abre un servidor local y el navegador para autorizar
            creds = flow.run_local_server(port=0)
        # Guardar el token para la próxima vez
        with open(token_file, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return creds

def build_drive_service(creds):
    return build("drive", "v3", credentials=creds)

def build_sheets_service(creds):
    return build("sheets", "v4", credentials=creds)
