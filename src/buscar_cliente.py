# src/buscar_cliente.py
import os
from typing import List, Dict, Optional
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def _get_creds(credentials_path: Optional[str] = None) -> Credentials:
    """
    Obtiene credenciales desde el archivo indicado o desde la variable de entorno
    GOOGLE_APPLICATION_CREDENTIALS. Por defecto busca 'credentials.json' en la raíz.
    """
    path = credentials_path or os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Archivo de credenciales no encontrado en: {path}")
    return Credentials.from_service_account_file(path, scopes=SCOPES)

def _get_client(credentials_path: Optional[str] = None) -> gspread.Client:
    creds = _get_creds(credentials_path)
    return gspread.authorize(creds)

def abrir_hoja_por_url(url: str, credentials_path: Optional[str] = None) -> gspread.Spreadsheet:
    """
    Abre y devuelve el objeto Spreadsheet dado su URL (completa).
    """
    client = _get_client(credentials_path)
    return client.open_by_url(url)

def buscar_cliente(
    nombre: str,
    url_hoja: str,
    sheet_name: Optional[str] = None,
    column_name: str = "Demandado",
    exact_match: bool = True,
    credentials_path: Optional[str] = None
) -> Optional[List[Dict]]:
    """
    Busca filas en la hoja donde la columna `column_name` coincide (o contiene) `nombre`.
    Devuelve una lista de diccionarios con: {"row": numero_de_fila, "data": {header: valor, ...}}
    Retorna None si no encuentra nada.
    """
    if not nombre:
        raise ValueError("El parámetro 'nombre' no puede estar vacío.")

    # Abrir spreadsheet
    ss = abrir_hoja_por_url(url_hoja, credentials_path)

    # Seleccionar hoja/pestaña
    if sheet_name:
        try:
            ws = ss.worksheet(sheet_name)
        except Exception as e:
            raise ValueError(f"No se encontró la pestaña '{sheet_name}' en el documento. Detalle: {e}")
    else:
        ws = ss.sheet1

    # Traer todos los valores (incluye encabezado)
    valores = ws.get_all_values()
    if not valores or len(valores) == 0:
        return None

    headers = valores[0]
    lower_headers = [h.strip().lower() for h in headers]

    # Buscar índice de la columna a usar para buscar el nombre
    target = column_name.strip().lower()
    col_idx = None
    if target in lower_headers:
        col_idx = lower_headers.index(target)
    else:
        # Intentos alternativos comunes
        for alt in ("nombre", "name", "cliente", "apellido"):
            if alt in lower_headers:
                col_idx = lower_headers.index(alt)
                break

    if col_idx is None:
        raise ValueError(f"No se encontró la columna '{column_name}' (ni alternativas) en el encabezado: {headers}")

    # Buscar coincidencias
    results = []
    for i, fila in enumerate(valores[1:], start=2):  # start=2 porque row 1 es header
        cell = fila[col_idx] if col_idx < len(fila) else ""
        if exact_match:
            match = cell.strip().lower() == nombre.strip().lower()
        else:
            match = nombre.strip().lower() in cell.strip().lower()

        if match:
            data = {headers[j]: (fila[j] if j < len(fila) else "") for j in range(len(headers))}
            results.append({"row": i, "data": data})

    return results if results else None



