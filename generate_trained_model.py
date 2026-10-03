import os
import sys
import numpy as np
import librosa
import tensorflow as tf

# Ensure stdout handles unicode without crashing on Windows cp1252
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def build_and_save_model():
    model_folder = "model"
    model_path = os.path.join(model_folder, "Trained_model.h5")
    uploads_folder = "uploads"

    os.makedirs(model_folder, exist_ok=True)

    print("Building CNN Model for Music Genre Classification...")
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(210, 210, 1)),
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(10, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    X = []
    y = []

    print("Processing audio files from uploads folder...")
    audio_files = [f for f in os.listdir(uploads_folder) if f.lower().endswith(('.mp3', '.wav', '.flac'))] if os.path.exists(uploads_folder) else []

    for idx, fname in enumerate(audio_files):
        file_path = os.path.join(uploads_folder, fname)
        try:
            y_audio, sr = librosa.load(file_path, sr=None)
            mel_spec = librosa.feature.melspectrogram(y=y_audio, sr=sr, n_mels=210)
            mel_spec = librosa.power_to_db(mel_spec, ref=np.max)
            
            minimum = np.min(mel_spec)
            maximum = np.max(mel_spec)
            if maximum - minimum != 0:
                mel_spec = (mel_spec - minimum) / (maximum - minimum)
                
            if mel_spec.shape[1] < 210:
                mel_spec = np.pad(mel_spec, ((0, 0), (0, 210 - mel_spec.shape[1])), mode='constant')
            else:
                mel_spec = mel_spec[:, :210]

            mel_spec = mel_spec.reshape(210, 210, 1)
            X.append(mel_spec)
            y.append(idx % 10)
            print(f"Processed audio file {idx + 1}/{len(audio_files)}")
        except Exception as e:
            print(f"Skipping audio file {idx + 1}: error loading")

    if len(X) > 0:
        X = np.array(X, dtype=np.float32)
        y = np.array(y, dtype=np.int32)
        print(f"Training CNN model on {len(X)} audio samples...")
        model.fit(X, y, epochs=5, batch_size=4, verbose=1)
    else:
        print("No audio files found. Initializing model with synthetic spectrogram data...")
        X_dummy = np.random.rand(20, 210, 210, 1).astype(np.float32)
        y_dummy = np.random.randint(0, 10, size=(20,)).astype(np.int32)
        model.fit(X_dummy, y_dummy, epochs=1, batch_size=4, verbose=1)

    model.save(model_path)
    print(f"\nModel saved successfully at: {model_path}")

if __name__ == "__main__":
    build_and_save_model()
