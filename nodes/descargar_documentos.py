import os
from utils.drive_auth import get_authenticated_drive

def descargar_documentos(state):
    documentos = state.get("documentos", [])
    if not documentos:
        raise ValueError("No hay documentos en el estado.")

    drive = get_authenticated_drive()
    nombres_descargados = []

    for documento in documentos:
        file_id = documento["id"]
        file_name = documento["name"]
        local_path = f"/tmp/{file_name}"

        print(f"⬇️ Descargando: {file_name}")
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile(local_path)
        nombres_descargados.append(file_name)

    return {
        **state,
        "archivos_descargados": nombres_descargados
    }