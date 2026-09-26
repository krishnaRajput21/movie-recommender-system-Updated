import pickle
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import os

# 1. load data from old .pkl file 
movies_dict_path = os.path.join(os.path.dirname(__file__), '../movies_dict.pkl')
with open(movies_dict_path, 'rb') as f:
    movies_dict = pickle.load(f)

movies_df = pd.DataFrame(movies_dict)

# Identify columns
text_column = 'tags' if 'tags' in movies_df.columns else movies_df.columns[-1]
id_column = 'movie_id' if 'movie_id' in movies_df.columns else movies_df.columns[0]
title_column = 'title' if 'title' in movies_df.columns else movies_df.columns[1]

# --- FIX: Remove duplicate id ---
print(f"Original Dataset Size: {len(movies_df)}")
movies_df = movies_df.drop_duplicates(subset=[id_column])
print(f"Dataset Size after removing duplicates: {len(movies_df)}")
# -----------------------------------------------------------

# 2. ChromaDB Setup
db_path = os.path.join(os.path.dirname(__file__), '../data/chroma_db')
chroma_client = chromadb.PersistentClient(path=db_path)

try:
    chroma_client.delete_collection(name="movies_collection")
except Exception:
    pass
collection = chroma_client.create_collection(name="movies_collection")

# 3. Model Load
print("Loading AI Model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 4. Generate & Save
print(f"Generating embeddings for column: {text_column}...")

docs = movies_df[text_column].tolist()
ids = movies_df[id_column].astype(str).tolist()
titles = movies_df[title_column].tolist()

metadatas = [{"title": title, "movie_id": m_id} for title, m_id in zip(titles, ids)]

embeddings = model.encode(docs, show_progress_bar=True).tolist()

print("Saving to Vector Database...")
collection.add(
    ids=ids,
    embeddings=embeddings,
    metadatas=metadatas,
    documents=docs
)

print("✅ Vector Database Successfully Created in 'data/chroma_db' folder!")