<<<<<<< HEAD
# 🎵 Music Recommender

A web application that predicts music genres, extracts audio features, and recommends similar songs based on machine learning.

## 🚀 Features

- **Genre Prediction**: Analyzes audio files to predict music genre using a TensorFlow/Keras model
- **Audio Feature Extraction**: Extracts energy, danceability, and loudness features from songs
- **Song Recommendations**: Suggests similar songs based on genre and audio features
- **YouTube Integration**: Downloads songs directly from YouTube for analysis
- **Audio Playback**: Built-in player for uploaded/downloaded songs
- **Genre Fun Facts**: Displays a random fun fact, tip, and icon for each predicted genre
- **MongoBD Compass**: To stored contact information on MongoDB compass 

## 🧠 Machine Learning Model


The application uses a Convolutional Neural Network (CNN) built with TensorFlow and Keras to classify songs into 10 music genres.  
The model was trained on extracted audio features (MFCCs and spectral features) and achieved:

- **Training Accuracy:** 99.56%
- **Validation Accuracy:** 92.65%

These results demonstrate strong feature learning and effective generalization on unseen audio data.
### Supported Genres
- Blues
- Classical
- Country
- Disco
- Hip-Hop
- Jazz
- Metal
- Pop
- Reggae
- Rock

## 🛠️ Technical Stack

- **Backend**: Python, Flask, MongoDB
- **Machine Learning**: TensorFlow, Keras
- **Audio Processing**: librosa, soundfile
- **Data Analysis**: pandas, scikit-learn
- **Frontend**: HTML, CSS, JavaScript
- **External Tools**: yt-dlp for YouTube downloads

## 📁 Project Structure

```
MusicRecommender/
├── app.py                 # Main Flask application
├── extract_features.py    # Audio feature extraction
├── recommend.py           # Song recommendation system
├── requirements.txt       # Python dependencies
├── data/                  # Dataset for recommendations
├── model/                 # Trained ML model
├── static/                # CSS and static assets
├── templates/             # HTML templates
│   ├── index.html         # Main page with player and song list
│   └── result.html        # Results page with predictions
├── uploads/               # Uploaded and downloaded audio files
├── utils/                 # Helper functions
│   ├── file_utils.py      # File handling utilities
│   └── model_utils.py     # Model prediction utilities
├── genre_facts.json        # Fun facts, tips, and icons for each genre
└── ...
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip
- yt-dlp (for YouTube downloads)
- pip install pymongo

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/MusicRecommender.git
   cd MusicRecommender
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv env
   # On Windows
   tf-env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install yt-dlp for YouTube downloads:
   ```
   pip install yt-dlp
   ```

### Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 📊 Web Interface

### Main Page
- Music player with controls
- List of uploaded songs
- YouTube search and download functionality
- Song analysis button

### Results Page
- Displays predicted genre with confidence scores
- Shows extracted audio features
- Lists song recommendations based on genre and features
- Displays a random fun fact, tip, and icon for the predicted genre

## 🎤 Genre Fun Facts

- The results page now displays a random fun fact, tip, and icon for each predicted genre, loaded from a dedicated `genre_facts.json` file.
- Each genre has at least 10 unique facts/tips, making the results more engaging and educational.
- The backend randomly selects a fact for the predicted genre and passes it to the UI.

### Customizing Genre Facts

- To add or edit facts, tips, or icons for any genre, open `genre_facts.json` and add entries to the relevant genre’s list.
- Each entry is an object with:
  - `icon`: an emoji or icon string
  - `desc`: a short genre description
  - `fact`: an interesting fact or trivia
  - `tip`: a listening or engagement tip

**Example Entry:**
```json
"Jazz": [
  {
    "icon": "🎷",
    "desc": "Improvisational, expressive, and smooth with rich harmonies.",
    "fact": "Jazz originated in New Orleans in the early 20th century.",
    "tip": "Great for relaxing evenings."
  }
]
```

## 🖌️ Modern UI Enhancements
- Animated confidence bars, genre icons, and a visually engaging, rhythm-inspired layout.
- Responsive design for desktop and mobile.

## 🛣️ Ready for React (Optional)
- The backend is API-ready and can be connected to a React frontend in the future for even more interactivity and scalability.

## 🧩 How It Works

1. **Upload or Download**: Add songs to the application by uploading files or downloading from YouTube
2. **Select and Play**: Choose a song from the list to play it in the built-in player
3. **Analyze**: Click the "Analyze Song" button to process the selected song
4. **View Results**: See the predicted genre, audio features, and recommended similar songs

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [librosa](https://librosa.org/) for audio processing
- [TensorFlow](https://www.tensorflow.org/) for machine learning
- [Flask](https://flask.palletsprojects.com/) for web framework
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube downloads
=======
# Music-Recommendation-System
>>>>>>> 45eeaee098eb7e6b4e14b1abf405e58fc2d99188
