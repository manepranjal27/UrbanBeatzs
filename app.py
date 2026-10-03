from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, flash
import os
from werkzeug.utils import secure_filename
import subprocess
from pymongo import MongoClient
from datetime import datetime

from utils.file_utils import allowed_file, load_and_preprocess_audio, get_album_art_for_song
from utils.model_utils import predict_genre
from extract_features import extract_audio_features
from recommend import recommend_songs

UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")  # Change if your port or host is different
db = client["musicAppDB"]
contacts_collection = db["contacts"]


# Welcome page
@app.route("/", methods=["GET"])
def welcome():
    return render_template("welcome.html")

@app.route("/about")
def about():
    return render_template("about.html")

#-----------------------------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        contact_data = {
            "name": name,
            "email": email,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

        try:
            contacts_collection.insert_one(contact_data)
            flash("✅ Thank you for reaching out! We'll get back to you soon.", "success")
        except Exception as e:
            print("MongoDB Error:", e)
            flash("❌ Something went wrong. Please try again.", "danger")

        return redirect(url_for("contact"))

    return render_template("contact.html")
#-----------------------------

# Home page – handles analyze requests
@app.route("/index", methods=["GET", "POST"])
def index():
    # Get all allowed audio files from the upload folder
    song_list = os.listdir(app.config["UPLOAD_FOLDER"])
    song_files = [f for f in song_list if allowed_file(f)]
    
    # Get file info with modification times
    song_info = []
    for song in song_files:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], song)
        mod_time = os.path.getmtime(file_path)
        # Add album art URL for each song
        album_art = get_album_art_for_song(song)
        song_info.append({
            "name": song, 
            "modified": mod_time,
            "album_art": album_art
        })
    
    # Sort by modification time (newest first)
    song_info.sort(key=lambda x: x["modified"], reverse=True)
    
    # Extract just the filenames for the template
    sorted_song_files = song_info

    if request.method == "POST":
        filename = request.form.get("filename")  # 
        if filename and allowed_file(filename):
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            # Extract features & predict
            audio_features = extract_audio_features(path)
            audio_input = load_and_preprocess_audio(path)
            predicted_genre, prediction = predict_genre(audio_input)
            recommendations = recommend_songs(predicted_genre, audio_features)

            # Load genre facts and pick a random one for the predicted genre
            genre_facts_path = os.path.join(os.path.dirname(__file__), 'genre_facts.json')
            genre_fact = None
            try:
                with open(genre_facts_path, 'r', encoding='utf-8') as f:
                    all_facts = json.load(f)
                    facts_list = all_facts.get(predicted_genre, [])
                    if facts_list:
                        import random
                        genre_fact = random.choice(facts_list)
            except Exception as e:
                genre_fact = None

            return render_template("result.html",
                                   genre=predicted_genre,
                                   confidence=prediction,
                                   features=audio_features,
                                   recommendations=recommendations,
                                   genre_fact=genre_fact)

    return render_template("index.html", song_files=sorted_song_files)

import json

def escapejs_filter(value):
    # Use json.dumps to escape characters and then strip the surrounding quotes
    return json.dumps(value)[1:-1]

app.jinja_env.filters['escapejs'] = escapejs_filter


# Serve uploaded audio files
from urllib.parse import unquote

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    decoded_filename = unquote(filename)
    return send_from_directory(app.config["UPLOAD_FOLDER"], decoded_filename)



# Handle music download from YouTube
@app.route("/download", methods=["POST"])
def download_song():
    data = request.get_json()
    query = data.get("query")
    output_path = app.config["UPLOAD_FOLDER"]

    if not query:
        return jsonify({"message": "❌ No search query provided."}), 400

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Build yt-dlp command
    command = [
        "python", "-m", "yt_dlp",
        "-x", "--audio-format", "mp3",
        f"ytsearch1:{query}",
        "-o", os.path.join(output_path, "%(title)s.%(ext)s")
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("✅ Download success:", result.stdout)
        return jsonify({"message": "✅ Song downloaded successfully!",               
    "redirect": "/index"})
    except subprocess.CalledProcessError as e:
        print("❌ Download failed:", e.stderr)
        return jsonify({"message": "❌ Download failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
