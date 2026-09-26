from fastapi import FastAPI, HTTPException
import chromadb
from sentence_transformers import SentenceTransformer
import os

app = FastAPI(
    title="Movie Recommender API",
    description="Vector Search & LLM Embedding-based Movie Recommendation System"
)

# 1. ChromaDB Client and Model initialization 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../data/chroma_db')

print("Loading ChromaDB persistent client...")
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_collection(name="movies_collection")

print("Loading Embedding Model...")
model = SentenceTransformer('all-MiniLM-L6-v2')


@app.get("/")
def home():
    return {"message": "Movie Recommender API is up and running!"}


@app.get("/recommend")
def get_recommendations(query: str, top_k: int = 5):
    """
    User query/text/movie-name accept karega aur top_k similar movies return karega.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query string cannot be empty")

    try:
        # Converting user input into vector embedding 
        query_embedding = model.encode([query]).tolist()

        # Search nearest neighbors in ChromaDB
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )

        recommendations = []
        if results and 'metadatas' in results and len(results['metadatas']) > 0:
            for metadata in results['metadatas'][0]:
                recommendations.append({
                    "title": metadata.get("title"),
                    "movie_id": metadata.get("movie_id")
                })

        return {
            "query": query,
            "total_results": len(recommendations),
            "recommendations": recommendations
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))