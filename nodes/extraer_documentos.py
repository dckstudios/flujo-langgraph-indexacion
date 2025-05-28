import os
import fitz  # PyMuPDF

def extraer_documentos(state):
    nombres = state.get("archivos_descargados", [])
    textos = []

    for file_name in nombres:
        local_path = f"/tmp/{file_name}"
        texto = ""

        with fitz.open(local_path) as doc:
            for page in doc:
                texto += page.get_text()

        print(f"📝 Extraído de {file_name}: {len(texto)} caracteres")
        textos.append({
            "nombre": file_name,
            "texto": texto
        })

    return {
        **state,
        "documentos_con_texto": textos
    }