import json

def formatear_chunks(state):
    documentos = state.get("documentos", [])
    analisis = state.get("analisis_documento", [])
    chunks = state.get("chunks", [])

    tipo_contenido = state.get("tipo_contenido")
    referencia_clave = state.get("referencia_clave_documentos")
    timestamp = state.get("timestamp_indexacion")

    # Índices por nombre
    index_drive = {d["name"]: d for d in documentos}
    index_analisis = {}

    for a in analisis:
        nombre = a.get("nombre")
        contenido = a.get("analisis_documento", "").strip()

        if not contenido:
            continue  # salta si está vacío

        try:
            parsed = json.loads(contenido)
            index_analisis[nombre] = parsed
        except json.JSONDecodeError:
            print(f"⚠️ Error al parsear JSON para '{nombre}'")
            continue


    formateados = []

    for chunk in chunks:
        nombre = chunk["nombre"]
        drive_info = index_drive.get(nombre, {})

        analisis_info = index_analisis.get(nombre, {})

        formateados.append({
            "id_documento": chunk.get("document_id"),
            "nombre_documento": nombre,
            "version_documento": "1",
            "tipo_documento": analisis_info.get("tipo_de_documento"),
            "tipo_contenido": tipo_contenido,
            "temas_clave_documento": analisis_info.get("temas_clave_documento"),
            "timestamp_indexacion": timestamp,
            "referencia_clave_documentos": referencia_clave,
            "categoria_documento": analisis_info.get("categoria_documento"),
            "url_documento": "None",
            "fragmento_texto": chunk.get("chunk")
        })

    print(f"✅ Chunks formateados: {len(formateados)} chunks")

    return {
        **state,
        "chunks_formateados": formateados
    }
