import gspread
from google.oauth2.service_account import Credentials

# Definimos el alcance (permisos que pedimos a Google)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Autenticamos con el archivo credentials.json
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

def buscar_cliente(nombre_buscar, url_hoja):
    """
    Busca un nombre dentro de una hoja de cálculo de Google Sheets.
    Devuelve las filas donde aparece o None si no lo encuentra.
    """
    hoja = client.open_by_url(url_hoja)
    ws = hoja.sheet1  # primera hoja del archivo

    celdas = ws.findall(nombre_buscar)
    if not celdas:
        return None

    resultados = []
    for celda in celdas:
        fila = ws.row_v_
