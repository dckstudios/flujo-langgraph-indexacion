import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    
    return (
        text
        .replace("---", "-")
        .replace("___", "_")
        .replace("...", "…")
        .replace("\r\n", " ")
        .replace("\n", " ")
        .replace("\r", " ")
        .strip()
    )

def limpiar_textos(state):
    documentos = state.get("documentos_con_texto", [])
    documentos_limpios = []

    for doc in documentos:
        nombre = doc.get("nombre", "sin_nombre")
        texto_original = doc.get("texto", "")
        texto_limpio = clean_text(texto_original)

        chars_original = len(texto_original)
        chars_limpio = len(texto_limpio)
        eliminados = chars_original - chars_limpio

        print(f"🧼 Limpieza de '{nombre}': {chars_original} → {chars_limpio} caracteres ({eliminados} eliminados)")

        documentos_limpios.append({
            "nombre": nombre,
            "texto_limpio": texto_limpio
        })

    return {
        **state,
        "documentos_limpios": documentos_limpios
    }