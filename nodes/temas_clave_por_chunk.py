from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
import time

load_dotenv()

modelo = ChatOpenAI(
    model="qwen/qwen-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
    temperature=0.3
)

PROMPT_ZH = """请阅读下面的文本，并根据其内容提取关键主题词或短语。保持原文语言，避免翻译或添加解释。仅返回关键主题的逗号分隔列表。

文本：
"""

def temas_clave_por_chunk(state):
    chunks = state.get("chunks_formateados", [])
    resultado = []
    total = len(chunks)

    for i, chunk in enumerate(chunks, start=1):
        fragmento = chunk.get("fragmento_texto", "").strip()
        prompt = PROMPT_ZH + fragmento

        try:
            respuesta = modelo.invoke([HumanMessage(content=prompt)])
            temas = respuesta.content.strip()

            chunk_actualizado = {**chunk, "temas_clave_fragmento": temas}
            resultado.append(chunk_actualizado)
            print(f"✅ Temas clave generados {i}/{total} chunks del documento: '{chunk['nombre_documento']}'")
        except Exception as e:
            print(f"❌ Error en chunk {i}/{total} de '{chunk['nombre_documento']}': {str(e)}")
            continue

        time.sleep(0.5)  # para evitar saturar la API

    return {
        **state,
        "chunks_con_temas": resultado
    }