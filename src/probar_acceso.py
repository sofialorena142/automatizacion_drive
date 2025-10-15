from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "credentials.json"
ID_CARPETA = "1O8JFgkXWFjVEyR--z5DQDajk8rewcUG-"

def verificar_acceso_carpeta():
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("drive", "v3", credentials=creds)

        # Listar archivos en la carpeta para comprobar acceso
        results = service.files().list(
            q=f"'{ID_CARPETA}' in parents",
            pageSize=10,
            fields="files(id, name)"
        ).execute()
        archivos = results.get('files', [])

        if not archivos:
            print("📂 Carpeta vacía o no accesible por el Service Account")
            return False
        else:
            print("📂 Archivos visibles por el Service Account:")
            for f in archivos:
                print(f" - {f['name']} (ID: {f['id']})")
            return True

    except Exception as e:
        print(f"❌ Error al acceder a la carpeta: {e}")
        return False

if __name__ == "__main__":
    acceso = verificar_acceso_carpeta()
    if acceso:
        print("✅ El Service Account tiene acceso a la carpeta")
    else:
        print("❌ El Service Account NO tiene acceso a la carpeta")
