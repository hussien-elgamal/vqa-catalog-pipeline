import os
import torch
from PIL import Image
from tqdm import tqdm
import pandas as pd
from transformers import CLIPProcessor, CLIPModel

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def extract_embeddings(split_dir, split_name, output_path):
    image_paths = [os.path.join(split_dir, fname)
                   for fname in os.listdir(split_dir) if fname.endswith((".jpg", ".png"))]

    features = []

    for img_path in tqdm(image_paths, desc=f"Processing {split_name}"):
        try:
            image = Image.open(img_path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt").to(device)

            with torch.no_grad():
                embedding = model.get_image_features(**inputs)

            embedding = embedding.cpu().numpy().flatten()
            features.append({
                "image_path": img_path,
                "embedding": embedding
            })
        except Exception as e:
            print(f"Error in {img_path}: {e}")

    df = pd.DataFrame(features)
    df.to_parquet(output_path, index=False)
    print(f"✅ Saved {split_name} features to {output_path}")

if __name__ == "__main__":
    extract_embeddings("data/train/train", "train", "features/train_embeddings.parquet")
    extract_embeddings("data/test", "test", "features/test_embeddings.parquet")
    extract_embeddings("data/val", "val", "features/val_embeddings.parquet")
