from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from datetime import datetime

# Importar los nodos
from nodes.start_node import start_node
from nodes.listar_documentos import listar_documentos
from nodes.descargar_documentos import descargar_documentos
from nodes.extraer_documentos import extraer_documentos
from nodes.limpiar_textos import limpiar_textos
from nodes.analizar_documento import analizar_documento
from nodes.generar_document_id import generar_document_id
from nodes.chunkear_textos import chunkear_textos
from nodes.formatear_chunks import formatear_chunks
from nodes.temas_clave_por_chunk import temas_clave_por_chunk
from nodes.indexar_en_supabase import indexar_en_supabase
from nodes.indexar_en_qdrant import indexar_en_qdrant



class EstadoIndexador(TypedDict):
    carpeta_drive: str
    tabla_supabase: str
    qdrant_collection: str
    documentos: List[dict]
    archivos_descargados: Optional[List[str]]
    documentos_con_texto: Optional[List[dict]]
    documentos_limpios: Optional[List[dict]]
    analisis_documento: Optional[List[dict]]
    tipo_contenido: str
    referencia_clave_documentos: str
    timestamp_indexacion: Optional[str]
    chunks: Optional[List[dict]]
    chunks_formateados: Optional[List[dict]]
    chunks_con_temas: Optional[List[dict]]
    archivo_chunks_guardado: Optional[str]



# Crear el grafo LangGraph
builder = StateGraph(EstadoIndexador)

# Añadir nodos
builder.add_node("start", RunnableLambda(start_node))
builder.add_node("listar_documentos", RunnableLambda(listar_documentos))
builder.add_node("descargar_documentos", RunnableLambda(descargar_documentos))
builder.add_node("extraer_documentos", RunnableLambda(extraer_documentos))
builder.add_node("limpiar_textos", RunnableLambda(limpiar_textos))
builder.add_node("analizar_documento", RunnableLambda(analizar_documento))
builder.add_node("generar_document_id", RunnableLambda(generar_document_id))
builder.add_node("chunkear_textos", RunnableLambda(chunkear_textos))
builder.add_node("formatear_chunks", RunnableLambda(formatear_chunks))
builder.add_node("temas_chunk", RunnableLambda(temas_clave_por_chunk))
builder.add_node("indexar_en_supabase", RunnableLambda(indexar_en_supabase))
builder.add_node("indexar_en_qdrant", RunnableLambda(indexar_en_qdrant))


# Definir flujo
builder.set_entry_point("start")
builder.add_edge("start", "listar_documentos")
builder.add_edge("listar_documentos", "descargar_documentos")
builder.add_edge("descargar_documentos", "extraer_documentos")
builder.add_edge("extraer_documentos", "limpiar_textos")
builder.add_edge("limpiar_textos", "analizar_documento")
builder.add_edge("analizar_documento", "generar_document_id")
builder.add_edge("generar_document_id", "chunkear_textos")
builder.add_edge("chunkear_textos", "formatear_chunks")
builder.add_edge("formatear_chunks", "temas_chunk")
builder.add_edge("temas_chunk", "indexar_en_supabase")
builder.add_edge("indexar_en_supabase", "indexar_en_qdrant")

# Compilar y correr
graph = builder.compile()
app = graph