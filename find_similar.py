import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Load the embeddings
with open("node_embeddings.pkl", "rb") as f:
    node_embeddings = pickle.load(f)

print(f"Loaded embeddings for {len(node_embeddings)} nodes.")

# Load the data
df = pd.read_csv("dbpedia_music_data_2010_2025.csv")

def get_node_embedding(node, embeddings, dimensions=64):
    if node in embeddings:
        return embeddings[node]
    return np.zeros(dimensions)  # Default embedding for unknown nodes

def preprocess_input_song(title, artist, genre, embeddings, dimensions=64):
    artist_embedding = get_node_embedding(artist, embeddings, dimensions)
    genre_embedding = get_node_embedding(genre, embeddings, dimensions)
    return artist_embedding + genre_embedding

def analyze_feature_contributions(input_embedding, compared_embedding, feature_names):
    dot_product = input_embedding * compared_embedding
    contributions = dot_product / np.sum(dot_product)  # Normalize contributions
    return {feature: contribution for feature, contribution in zip(feature_names, contributions)}

def find_similar_songs(input_title, input_artist, input_genre, df, embeddings, top_n=5, dimensions=64):
    # Get the input song's embedding
    input_embedding = preprocess_input_song(input_title, input_artist, input_genre, embeddings, dimensions)

    # Compute similarity and feature contributions for each song
    similarities = []
    feature_contributions = []
    feature_names = ["artist", "genre"]  # Features contributing to the embedding

    for _, row in df.iterrows():
        # Skip exact matches
        if row["title"] == input_title and row["artist"] == input_artist:
            similarities.append(-1)  # Assign a low similarity score for exact matches
            feature_contributions.append({feature: 0 for feature in feature_names})
            continue

        song_embedding = preprocess_input_song(row["title"], row["artist"], row["genre"], embeddings, dimensions)
        similarity = cosine_similarity([input_embedding], [song_embedding])[0][0]
        similarities.append(similarity)

        # Analyze feature contributions
        contributions = analyze_feature_contributions(input_embedding, song_embedding, feature_names)
        feature_contributions.append(contributions)

    # Add similarities and contributions to the DataFrame
    df["similarity"] = similarities
    df["contributions"] = feature_contributions

    # Remove duplicates by grouping by title and keeping the highest similarity
    unique_songs = df[df["similarity"] > 0].sort_values(by="similarity", ascending=False)
    unique_songs = unique_songs.groupby("title").first().reset_index()

    # Prepare the result DataFrame
    result = unique_songs.sort_values(by="similarity", ascending=False).head(top_n)
    result["influence"] = result["contributions"].apply(
        lambda x: ", ".join([f"{feature}: {contribution:.2%}" for feature, contribution in x.items()])
    )
    return result

# Example usage
title = "Pumpy"
artist = "Cadet (rapper)"
genre = "Afroswing"


similar_songs = find_similar_songs(title, artist, genre, df, node_embeddings, top_n=10)
print(similar_songs[["title", "artist", "genre", "releaseDate", "similarity", "influence"]])
