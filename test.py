# test_recommend.py
from recommend import recommend_songs

features = {
    "energy": 0.3513,
    "danceability": 0.5174,
    "loudness": 0.8485
}
recommendations = recommend_songs("Rock", features)

for song in recommendations:
    print(song)
