import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def load_facts(json_path):

    # load data
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def embed_facts(facts, model_name = "all-MiniLM-L6-v2"): 

    # encode each fact into semantic embedding
    model = SentenceTransformer(model_name)
    texts = [fact['text'] for fact in facts]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    return embeddings

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  
    faiss.normalize_L2(embeddings)  # normalize embeddings for cosine similarity
    index.add(embeddings)
    return index


def save_index(index, index_path):
    faiss.write_index(index, index_path)


def save_metadata(facts, metadata_path):

    # save original facts for retrieval
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(facts, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":

    facts = load_facts("../data/leaders_facts.json")  
    embeddings = embed_facts(facts)
    index = build_faiss_index(embeddings)

    save_index(index, "../data/leaders_index.faiss")
    save_metadata(facts, "../data/leaders_metadata.json")



