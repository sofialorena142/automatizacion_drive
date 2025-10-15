from google.oauth2 import service_account
from googleapiclient.discovery import build
print("Google API client funcionando correctamente ✅")


# ID de la hoja
SHEET_ID = "18nYhrvYtm4qjj8J8kUUaEh7hirTLDjg6rym0F9XJ2zE"
RANGE_NAME = "Datos Personales!A:I"

# Cargar credenciales
creds = service_account.Credentials.from_service_account_file(
    "credentials.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

# Crear servicio
service = build("sheets", "v4", credentials=creds)

# Leer datos
result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range=RANGE_NAME
).execute()

values = result.get("values", [])
print(values)


