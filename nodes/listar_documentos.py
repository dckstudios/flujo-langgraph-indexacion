from utils.drive_auth import get_authenticated_drive
import os

def listar_documentos(state):
    drive = get_authenticated_drive()
    folder_id = state["carpeta_drive"]

    file_list = drive.ListFile({
        'q': f"'{folder_id}' in parents and trashed=false",
        'supportsAllDrives': True,
        'includeItemsFromAllDrives': True
    }).GetList()

    extensiones_validas = [".pdf"]
    documentos = []

    for file in file_list:
        name = file["title"]
        mime = file["mimeType"]
        ext = os.path.splitext(name)[-1].lower()

        if ext in extensiones_validas:
            documentos.append({
                "id": file["id"],
                "name": name,
                "mimeType": mime,
                "ext": ext,
                "version": file.get("version", None),
                "webViewLink": file.get("webViewLink", "")
            })

    print(f"📄 {len(documentos)} archivos encontrados en la carpeta")
    return {**state, "documentos": documentos}
