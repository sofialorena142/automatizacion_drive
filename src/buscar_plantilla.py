from google.oauth2 import service_account
from googleapiclient.discovery import build

def buscar_plantilla(nombre_plantilla):
    """
    Busca un archivo en Google Drive por su nombre y devuelve su ID y nombre.
    """
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
    SERVICE_ACCOUNT_FILE = "credentials.json"

    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("drive", "v3", credentials=creds)

        # Filtramos por nombre exacto
        query = f"name = '{nombre_plantilla}' and trashed = false"
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType)"
        ).execute()

        archivos = results.get("files", [])

        if not archivos:
            print(f"⚠️ No se encontró ninguna plantilla llamada '{nombre_plantilla}'")
            return None

        archivo = archivos[0]
        print(f"✅ Plantilla encontrada: {archivo['name']} (ID: {archivo['id']})")
        return archivo

    except Exception as e:
        print(f"❌ Error al buscar la plantilla: {e}")
        return None
