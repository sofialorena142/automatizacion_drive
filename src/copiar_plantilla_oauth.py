# src/copiar_plantilla.py
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def copiar_plantilla_con_creds(creds, id_plantilla: str, id_carpeta_destino: str, nuevo_nombre: str):
    """
    Copia el archivo 'id_plantilla' dentro de la carpeta destino usando las credenciales pasadas (OAuth).
    `creds` es un objeto google.oauth2.credentials.Credentials.
    """
    try:
        service = build("drive", "v3", credentials=creds)
        body = {"name": nuevo_nombre, "parents": [id_carpeta_destino]}
        copia = service.files().copy(fileId=id_plantilla, body=body).execute()
        print(f"✅ Plantilla copiada por usuario: {copia['name']} (ID: {copia['id']})")
        return copia
    except Exception as e:
        print(f"❌ Error al copiar la plantilla con OAuth: {e}")
        return None

