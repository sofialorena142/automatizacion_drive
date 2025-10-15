import sys
import os

# Agregar carpeta src al path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


from buscar_cliente import buscar_cliente
from buscar_plantilla import buscar_plantilla   # tu función para localizar plantilla (sigue válida)
from oauth_helper import get_credentials, build_drive_service
from copiar_plantilla_oauth import copiar_plantilla_con_creds

if __name__ == "__main__":
    # 1) datos: hoja y carpeta (actualizá con tus IDs)
    URL_HOJA = "https://docs.google.com/spreadsheets/d/18nYhrvYtm4qjj8J8kUUaEh7hirTLDjg6rym0F9XJ2zE/"
    ID_CARPETA_DESTINO = "11V6OEEst1pNG0Nv4yA6yxe9qAFXP1oev"   # ID puro, como ya venías usando

    # 2) obtener cliente
    resultado = buscar_cliente("Juan Perez", URL_HOJA)
    if not resultado:
        print("No se encontró el cliente.")
        raise SystemExit(1)
    cliente = resultado[0]  # primera coincidencia
    print("Resultado búsqueda cliente:", cliente)

    # 3) buscar plantilla (puede seguir usando tu buscar_plantilla que usa Service Account)
    # Si preferís, podés buscar la plantilla con Drive también usando OAuth; aquí uso tu función existente
    plantilla = buscar_plantilla("Demanda_TP+3")
    if not plantilla:
        print("No se encontró la plantilla.")
        raise SystemExit(1)
    id_plantilla = plantilla["id"]

    # 4) autenticación OAuth con TU cuenta para copiar (esto abrirá navegador la primera vez)
    creds = get_credentials()   # crea/usa token.json

    # 5) copiar la plantilla como TU usuario
    nuevo_nombre = f"Demanda_{cliente['data'].get('Demandado', 'SinNombre')}"
    copia = copiar_plantilla_con_creds(creds, id_plantilla, ID_CARPETA_DESTINO, nuevo_nombre)

    if copia:
        print("Flujo completado con éxito.")
    else:
        print("Falló la copia con OAuth.")
