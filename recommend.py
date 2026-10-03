import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_songs(predicted_genre, features, prioritize_new_artists=True):
    # ✅ Load the updated dataset
    df = pd.read_csv("data/music_features.csv")

    # ✅ Filter by predicted genre
    genre_df = df[df["genre"] == predicted_genre]

    # ✅ Optionally prioritize new artists
    if prioritize_new_artists:
        new_artist_df = genre_df[genre_df["is_new_artist"] == True]
        if not new_artist_df.empty:
            genre_df = new_artist_df  # Use only new artists if available

    # ✅ Define feature columns used for similarity
    feature_cols = ["energy", "danceability", "loudness"]

    if genre_df.empty:
        return []

    # ✅ Prepare vectors for similarity comparison
    song_features = genre_df[feature_cols].values
    input_vector = [[features["energy"], features["danceability"], features["loudness"]]]

    # ✅ Calculate cosine similarity
    similarities = cosine_similarity(input_vector, song_features)[0]
    genre_df = genre_df.copy()
    genre_df["similarity"] = similarities

    # ✅ Get top 5 similar songs
    top_songs = genre_df.sort_values(by="similarity", ascending=False).head(5)

    return top_songs[["song", "artist", "genre"]].to_dict(orient="records")
