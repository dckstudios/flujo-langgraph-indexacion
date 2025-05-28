import tiktoken

def chunk_text_by_tokens(text: str, max_tokens=1024, overlap=256, model="gpt-3.5-turbo"):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += max_tokens - overlap

    return chunks

def chunkear_textos(state):
    documentos = state.get("documentos_limpios", [])
    todos_los_chunks = []

    for doc in documentos:
        nombre = doc["nombre"]
        texto = doc["texto_limpio"]
        chunks = chunk_text_by_tokens(texto)

        document_id = doc.get("document_id")

        for i, c in enumerate(chunks):
            todos_los_chunks.append({
                "document_id": document_id,
                "nombre": nombre,
                "chunk_index": i,
                "chunk": c
        })

        print(f"📦 '{nombre}' dividido en {len(chunks)} chunks (tokens)")

    return {
        **state,
        "chunks": todos_los_chunks
    }