# File: scripts/image_retrieval.py
import os
import torch
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from transformers import CLIPProcessor, CLIPModel

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def extract_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        embedding = model.get_image_features(**inputs)
    return embedding.cpu().numpy().flatten()

def load_feature_store():
    paths = [
        "features/train_embeddings.parquet",
        "features/test_embeddings.parquet",
        "features/val_embeddings.parquet"
    ]
    dfs = [pd.read_parquet(p) for p in paths if os.path.exists(p)]
    return pd.concat(dfs, ignore_index=True)

def retrieve_similar_images(query_image_path, top_k=5):
    print(f"🔍 Extracting embedding for query image: {query_image_path}")
    query_embedding = extract_embedding(query_image_path).reshape(1, -1)

    print("📦 Loading feature store...")
    feature_store = load_feature_store()
    embeddings = np.stack(feature_store["embedding"].to_numpy())
    image_paths = feature_store["image_path"].to_list()

    print("📈 Computing similarity scores...")
    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = scores.argsort()[-top_k:][::-1]

    print("\n✅ Top similar images:")
    for idx in top_indices:
        print(f"{image_paths[idx]} (score: {scores[idx]:.4f})")

if __name__ == "__main__":
    # Replace with any image path from your dataset or new image
    query_image = "data/images/test/000123.jpg"
    retrieve_similar_images(query_image, top_k=5)
