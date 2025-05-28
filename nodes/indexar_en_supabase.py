import os
from supabase import create_client, Client
from datetime import datetime

def indexar_en_supabase(state):
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    tabla = state.get("tabla_supabase")

    supabase: Client = create_client(supabase_url, supabase_key)

    registros = []

    for chunk in state.get("chunks_con_temas", []):
        registros.append({
            "id_documento": chunk.get("id_documento"),
            "nombre_documento": chunk.get("nombre_documento"),
            "version_documento": chunk.get("version_documento"),
            "tipo_documento": chunk.get("tipo_documento"),
            "tipo_contenido": chunk.get("tipo_contenido"),
            "temas_clave_documento": chunk.get("temas_clave_documento"),
            "timestamp_indexacion": chunk.get("timestamp_indexacion"),
            "referencia_clave_documentos": chunk.get("referencia_clave_documentos"),
            "categoria_documento": chunk.get("categoria_documento"),
            "url_documento": chunk.get("url_documento"),
            "fragmento_texto": chunk.get("fragmento_texto"),
            "temas_clave_fragmento": chunk.get("temas_clave_chunk"),
            "indexed": 1
        })
        print("🛢️ Chunk insertado en Supabase")

    try:
        data, count = supabase.table(tabla).insert(registros).execute()
        print(f"✅ {len(registros)} registros insertados en Supabase.")
    except Exception as e:
        print(f"❌ Error al insertar en Supabase: {str(e)}")

    return state
