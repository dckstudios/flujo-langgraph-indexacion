from datetime import datetime
import re

def generar_document_id(state):
    documentos = state.get("documentos_limpios", [])
    documentos_con_id = []

    for doc in documentos:
        nombre = doc.get("nombre", "sin_nombre")
        texto_limpio = doc.get("texto_limpio", "")

        nombre_sanitizado = re.sub(r'\W+', '_', nombre.lower())[:50]
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        document_id = f"{nombre_sanitizado}_{timestamp}"

        documentos_con_id.append({
            **doc,
            "document_id": document_id
        })

        print(f"🆔 ID generado para '{nombre}': {document_id}")

    return {
        **state,
        "documentos_limpios": documentos_con_id
    }
