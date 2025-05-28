from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from main import app  # esto importa tu LangGraph ya compilado
import uvicorn

class IndexacionInput(BaseModel):
    carpeta_drive: str
    tabla_supabase: str
    qdrant_collection: str
    tipo_contenido: str
    referencia_clave_documentos: str

api = FastAPI()

@api.post("/indexar")
def indexar_documentos(input: IndexacionInput):
    resultado = app.invoke({
        "carpeta_drive": input.carpeta_drive,
        "tabla_supabase": input.tabla_supabase,
        "qdrant_collection": input.qdrant_collection,
        "tipo_contenido": input.tipo_contenido,
        "referencia_clave_documentos": input.referencia_clave_documentos,
        "timestamp_indexacion": datetime.utcnow().isoformat()
    })
    return {
        "mensaje": "📚 Proceso de indexación completado",
        "chunks_indexados": len(resultado.get("chunks_con_temas", []))
    }

if __name__ == "__main__":
    uvicorn.run("api:api", host="0.0.0.0", port=6060, reload=True)
