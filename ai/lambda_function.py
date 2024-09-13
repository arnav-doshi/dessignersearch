import os
import json
import sys
sys.path.append("/mnt/access") #EFS
import base64
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg19 import preprocess_input
import faiss
import pickle
import boto3


# Initialize model and data (REMOVED FOR SECURITY PURPOSES)

# Load VGG19
model = load_model(model_path)

# Cache CSV and precomputed features (will change from CSV in future versions)
csv_df = pd.read_csv(csv_path)
with open(feature_path, 'rb') as f:
    dataset_features = pickle.load(f)

# FAISS index
dataset_features_list = list(dataset_features.values())
dataset_paths = list(dataset_features.keys())
d = len(dataset_features_list[0])
index = faiss.IndexFlatL2(d)
index.add(np.array(dataset_features_list))

# Image information dictionary
img_info = {os.path.join('downloaded_images', os.path.basename(row['image-link'])): row for _, row in csv_df.iterrows()}

def extract_features(image):
    img = tf.image.decode_image(image, channels=3)
    img = tf.image.resize(img, (224, 224))
    img = tf.cast(img, tf.float32)
    img = preprocess_input(img)
    img = tf.expand_dims(img, axis=0)
    features = model.predict(img)
    return features.flatten()

def compare_with_precomputed_features(user_features):
    k = 6
    distances, indices = index.search(np.expand_dims(user_features, axis=0), k=k)
    sorted_indices = indices[0][1:]
    sorted_paths = [dataset_paths[i] for i in sorted_indices]
    sorted_similarities = [1 - d for d in distances[0][1:]]
    return list(zip(sorted_paths, sorted_similarities))

def lambda_handler(event, context):
    image_data = base64.b64decode(event['body']) # Using base64 encoding. Will use a faster alternative in future versions
    image_name = event['headers']['image_name']
    
    user_features = extract_features(image_data)
    top_similar_images = compare_with_precomputed_features(user_features)
    
    results = []
    for img_path, similarity in top_similar_images[:5]:
        info = img_info.get(img_path)
        if info is not None:
            results.append({
                "Similarity": similarity,
                "Brand Name": info['brand-name'],
                "Product Name": info['product-name'],
                "Price": info['price'],
                "Product Link": info['product-link'],
                "Image Link": info['image-link']
            })
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
