import librosa
import numpy as np
import soundfile

def extract_audio_features(file_path):
    y, sr = librosa.load(file_path, sr=None)

    # Energy (RMS)
    rms = librosa.feature.rms(y=y)[0]
    energy = np.mean(rms)

    # Danceability (Onset strength normalized by std deviation)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    danceability = np.mean(onset_env) / (np.std(onset_env) + 1e-6)

    # Loudness in dB
    loudness_db = 20 * np.log10(np.mean(rms) + 1e-6)

    # Normalize loudness (scale from -60 dB to 0 dB → 0 to 1)
    min_db = -60
    max_db = 0
    normalized_loudness = (loudness_db - min_db) / (max_db - min_db)
    normalized_loudness = min(max(normalized_loudness, 0), 1)  # Clamp to [0, 1]

    # 🔍 Print debug info
    print(f"\n🔊 Loudness (dB): {loudness_db:.2f}")
    print(f"🎚️  Loudness (normalized): {normalized_loudness:.4f}\n")

    return {
        "energy": round(float(energy), 4),
        "danceability": round(float(danceability), 4),
        "loudness": round(float(normalized_loudness), 4)
    }
