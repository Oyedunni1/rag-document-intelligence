import os
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()
client_ai = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
client_db = chromadb.PersistentClient(path="./chroma_db")


def retrieve_and_answer(query: str, collection_name: str = "documents") -> str:
    from embedder import embed_query

    collection = client_db.get_or_create_collection(name=collection_name)

    query_vector = embed_query(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )

    chunks = results["documents"][0]
    context = "\n\n---\n\n".join(chunks)

    prompt = f"""You are a helpful assistant. Answer the user's question 
using ONLY the context provided below. If the answer is not in the context, 
say "I couldn't find that in the document."

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:"""

    response = client_ai.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text