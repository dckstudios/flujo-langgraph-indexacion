import json
import requests
from io import BytesIO

def indexar_en_qdrant(state):
    chunks = state.get("chunks_con_temas", [])
    collection = state.get("qdrant_collection", "KEXP_Empresa_Proyecto")

    # Serializar los chunks como archivo en memoria
    archivo_json = BytesIO()
    archivo_json.write(json.dumps(chunks, ensure_ascii=False).encode("utf-8"))
    archivo_json.seek(0)

    files = {
        "json_file": ("chunks.json", archivo_json, "application/json"),
    }
    data = {
        "collection_name": collection
    }

    try:
        print("🚀 El proceso de indexación en Qdrant ha empezado")
        response = requests.post(
            "http://144.202.109.147:5000/index",
            files=files,
            data=data
        )

        if response.status_code == 200:
            print("✅ Chunks indexados correctamente a Qdrant.")
        else:
            print(f"❌ Error al enviar a Qdrant: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"❌ Error de conexión al enviar a Qdrant: {str(e)}")

    return state
