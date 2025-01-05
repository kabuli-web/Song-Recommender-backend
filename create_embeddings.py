import networkx as nx
import pandas as pd
from node2vec import Node2Vec
import numpy as np
import pickle

# Load the data
df = pd.read_csv("dbpedia_music_data_2010_2025.csv")
# Initialize a graph
G = nx.Graph()

# Add nodes and edges for artists, genres, and related artists
for _, row in df.iterrows():
    # Add nodes
    G.add_node(row["artist"], node_type="artist")
    G.add_node(row["genre"], node_type="genre")
    if row["relatedArtist"] != "Unknown":
        G.add_node(row["relatedArtist"], node_type="artist")

    # Add edges
    G.add_edge(row["artist"], row["genre"], relation="belongs_to")
    if row["relatedArtist"] != "Unknown":
        G.add_edge(row["artist"], row["relatedArtist"], relation=row["relation"])

print(f"Graph created with {len(G.nodes())} nodes and {len(G.edges())} edges.")

# Generate embeddings using Node2Vec
node2vec = Node2Vec(G, dimensions=64, walk_length=30, num_walks=200, workers=4)
model = node2vec.fit(window=10, min_count=1, batch_words=4)

# Save embeddings for each node
node_embeddings = {node: model.wv[node] for node in G.nodes()}

# Save the embeddings to a file
with open("node_embeddings.pkl", "wb") as f:
    pickle.dump(node_embeddings, f)

print("Embeddings saved to 'node_embeddings.pkl'")
