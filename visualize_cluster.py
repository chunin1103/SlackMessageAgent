import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client["SEO_keywords"]
collection = db["branding"]

docs_cursor = collection.find(
    {"text_embedding_hf": {"$exists": True, "$ne": None}},
    {"text_embedding_hf": 1, "branding": 1}
)
docs = list(docs_cursor)

embeddings = []
brandings = []
for doc in docs:
    embedding_val = doc["text_embedding_hf"]
    if isinstance(embedding_val[0], list):
        embeddings.append(embedding_val[0])
    else:
        embeddings.append(embedding_val)
    brandings.append(doc.get("branding", ""))

X = np.array(embeddings)
print("Embeddings shape:", X.shape)

num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
labels = kmeans.fit_predict(X)

pca = PCA(n_components=3, random_state=42)
X_pca_3d = pca.fit_transform(X)
print("PCA 3D shape:", X_pca_3d.shape)

# Plotly 3D
fig = px.scatter_3d(
    x=X_pca_3d[:, 0],
    y=X_pca_3d[:, 1],
    z=X_pca_3d[:, 2],
    color=labels.astype(str),
    hover_name=[b[:30] for b in brandings],
    title="3D Embedding Clusters with Plotly"
)
fig.show(renderer="browser")
