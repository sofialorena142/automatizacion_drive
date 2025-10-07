from src.buscar_cliente import buscar_cliente
from google.auth.exceptions import DefaultCredentialsError

# mi URL
url_hoja = "https://docs.google.com/spreadsheets/d/1Gb9V0Zau6c9WzNFmxHd9goBv-hikVLjz/edit?copiedFromTrash=&gid=1674203574#gid=1674203574"

print("Probando conexión con Google Sheets...")

try:
    resultado = buscar_cliente("Juan Perez", url_hoja)
    if resultado:
        print("Coincidencias encontradas:")
        for fila in resultado:
            print(fila)
    else:
        print("No se encontró el nombre en la hoja.")
except Exception as e:
    print("Algo falló:", e)
