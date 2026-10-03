import os
import numpy as np
import pandas as pd
import librosa
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


# ==============================
# SETTINGS
# ==============================

CSV_PATH = "data/music_features.csv"
AUDIO_FOLDER = "uploads"
MODEL_FOLDER = "model"
MODEL_PATH = os.path.join(MODEL_FOLDER, "Trained_model.h5")

IMG_SIZE = 210


# ==============================
# LOAD DATASET
# ==============================

print("Loading dataset...")

df = pd.read_csv(CSV_PATH)

print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())

print("\nGenres:")
print(df["genre"].value_counts())


# ==============================
# AUDIO PREPROCESSING
# ==============================

def load_audio(file_path):

    y, sr = librosa.load(file_path, sr=None)

    mel_spec = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_mels=210
    )

    mel_spec = librosa.power_to_db(
        mel_spec,
        ref=np.max
    )

    # Normalize
    minimum = np.min(mel_spec)
    maximum = np.max(mel_spec)

    if maximum - minimum != 0:
        mel_spec = (
            (mel_spec - minimum)
            / (maximum - minimum)
        )

    # Make exactly 210 time frames
    if mel_spec.shape[1] < 210:

        mel_spec = np.pad(
            mel_spec,
            (
                (0, 0),
                (0, 210 - mel_spec.shape[1])
            ),
            mode="constant"
        )

    else:

        mel_spec = mel_spec[:, :210]

    # CNN input
    mel_spec = mel_spec.reshape(
        210,
        210,
        1
    )

    return mel_spec


# ==============================
# FIND AUDIO FILE
# ==============================

def find_audio(song_name):

    # Direct path
    direct_path = os.path.join(
        AUDIO_FOLDER,
        song_name
    )

    if os.path.exists(direct_path):
        return direct_path

    # Search recursively
    for root, dirs, files in os.walk(AUDIO_FOLDER):

        for file in files:

            if file.lower() == song_name.lower():

                return os.path.join(
                    root,
                    file
                )

    return None


# ==============================
# PREPARE DATA
# ==============================

X = []
y = []

print("\nPreparing audio data...")

total = len(df)

for index, row in df.iterrows():

    song = str(row["song"])
    genre = str(row["genre"])

    audio_path = find_audio(song)

    if audio_path is None:

        if index % 100 == 0:
            print(
                f"Audio not found: {song}"
            )

        continue

    try:

        mel = load_audio(audio_path)

        X.append(mel)
        y.append(genre)

        if len(X) % 10 == 0:

            print(
                f"Processed {len(X)} audio files"
            )

    except Exception as e:

        print(
            f"Error processing {song}: {e}"
        )


print("\n==============================")
print("Audio processing completed")
print("==============================")

print("Usable audio files:", len(X))


if len(X) == 0:

    raise RuntimeError(
        "No matching audio files were found in uploads folder."
    )


# Convert to NumPy
X = np.array(X, dtype=np.float32)

y = np.array(y)


# ==============================
# ENCODE GENRES
# ==============================

encoder = LabelEncoder()

y_encoded = encoder.fit_transform(y)

num_classes = len(
    encoder.classes_
)

print("\nClasses:")
print(encoder.classes_)

print("Number of classes:", num_classes)


# ==============================
# TRAIN / TEST SPLIT
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==============================
# CNN MODEL
# ==============================

model = tf.keras.Sequential([

    tf.keras.layers.Input(
        shape=(210, 210, 1)
    ),

    tf.keras.layers.Conv2D(
        32,
        (3, 3),
        activation="relu"
    ),

    tf.keras.layers.MaxPooling2D(
        (2, 2)
    ),

    tf.keras.layers.Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),

    tf.keras.layers.MaxPooling2D(
        (2, 2)
    ),

    tf.keras.layers.Conv2D(
        128,
        (3, 3),
        activation="relu"
    ),

    tf.keras.layers.MaxPooling2D(
        (2, 2)
    ),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(
        128,
        activation="relu"
    ),

    tf.keras.layers.Dropout(
        0.5
    ),

    tf.keras.layers.Dense(
        num_classes,
        activation="softmax"
    )
])


# ==============================
# COMPILE
# ==============================

model.compile(

    optimizer="adam",

    loss="sparse_categorical_crossentropy",

    metrics=["accuracy"]
)


model.summary()


# ==============================
# TRAIN
# ==============================

print("\n==============================")
print("Starting CNN training...")
print("==============================")

history = model.fit(

    X_train,
    y_train,

    validation_data=(
        X_test,
        y_test
    ),

    epochs=15,

    batch_size=16,

    verbose=1
)


# ==============================
# EVALUATE
# ==============================

loss, accuracy = model.evaluate(
    X_test,
    y_test,
    verbose=0
)

print("\n==============================")
print("Training completed")
print("==============================")

print(
    f"Test Accuracy: {accuracy * 100:.2f}%"
)


# ==============================
# SAVE MODEL
# ==============================

os.makedirs(
    MODEL_FOLDER,
    exist_ok=True
)

model.save(
    MODEL_PATH
)

print("\nModel saved successfully!")

print(
    f"Location: {MODEL_PATH}"
)