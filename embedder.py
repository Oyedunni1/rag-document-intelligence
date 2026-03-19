import os
import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

try:
    import streamlit as st
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    api_key = os.getenv("GOOGLE_API_KEY")

client_ai = genai.Client(api_key=api_key)

# Use in-memory on cloud, persistent locally
try:
    import streamlit as st
    st.secrets["GOOGLE_API_KEY"]
    client_db = chromadb.EphemeralClient()
except Exception:
    client_db = chromadb.PersistentClient(path="./chroma_db")


def embed_and_store(chunks: list[str], collection_name: str = "documents"):
    # Delete old collection if it exists so we start fresh
    try:
        client_db.delete_collection(name=collection_name)
    except Exception:
        pass

    collection = client_db.get_or_create_collection(name=collection_name)

    for i, chunk in enumerate(chunks):
        result = client_ai.models.embed_content(
            model="models/gemini-embedding-2-preview",
            contents=chunk,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
        )
        collection.add(
            documents=[chunk],
            embeddings=[result.embeddings[0].values],
            ids=[f"chunk_{i}"]
        )
        print(f"Stored chunk {i + 1} of {len(chunks)}")

    print(f"\nDone! {len(chunks)} chunks stored in ChromaDB.")


def embed_query(query: str) -> list[float]:
    result = client_ai.models.embed_content(
        model="models/gemini-embedding-2-preview",
        contents=query,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )
    return result.embeddings[0].values