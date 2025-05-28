from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os, re, json

load_dotenv()

modelo = ChatOpenAI(
    temperature=0,
    model="google/gemini-2.0-flash-001",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE")
)

def limpiar_json_marcado(respuesta: str) -> str:
    # Elimina envoltorios tipo ```json ... ```
    limpio = re.sub(r"^```json\s*|\s*```$", "", respuesta.strip(), flags=re.IGNORECASE)
    return limpio.strip()

def analizar_documento(state):
    documentos = state.get("documentos_limpios", [])
    resultados = []

    for doc in documentos:
        texto = doc["texto_limpio"]
        nombre = doc["nombre"]

        prompt = f"""
                    Eres un experto en análisis de texto. Devuelve SOLO un JSON con esta estructura:

                    {{
                    "temas_clave_documento": "...",
                    "tipo_de_documento": "texto",
                    "categoria_documento": "..."
                    }}

                    No agregues ningún texto adicional, aqui el texto a analizar: 
                    
                    {texto}
                    """

        try:
            respuesta = modelo.invoke([HumanMessage(content=prompt)])
            contenido = limpiar_json_marcado(respuesta.content)

            parsed = json.loads(contenido)
            resultados.append({
                "nombre": nombre,
                "analisis_documento": json.dumps(parsed, ensure_ascii=False)
            })
            print(f"✅ Documento '{nombre}' ha generado los temas clave correctamente.")

        except json.JSONDecodeError:
            print(f"⚠️ JSON inválido para '{nombre}':\n{contenido[:120]}")
        except Exception as e:
            print(f"❌ Error general en '{nombre}': {e}")

    return {
        **state,
        "analisis_documento": resultados
    }