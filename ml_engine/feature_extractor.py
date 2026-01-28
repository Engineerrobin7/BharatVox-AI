import librosa
import numpy as np
from typing import Dict, Tuple
import io
import soundfile as sf


class AudioFeatureExtractor:
    """Extract audio features for ML classification"""
    
    def __init__(self, sample_rate: int = 22050, n_mfcc: int = 13):
        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
    
    def load_audio_from_bytes(self, audio_bytes: bytes) -> Tuple[np.ndarray, int]:
        """Load audio from bytes"""
        try:
            audio_io = io.BytesIO(audio_bytes)
            y, sr = librosa.load(audio_io, sr=self.sample_rate, mono=True)
            return y, sr
        except Exception as e:
            raise ValueError(f"Failed to load audio: {str(e)}")
    
    def extract_mfcc_features(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Extract MFCC features"""
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)
        mfcc_mean = np.mean(mfccs, axis=1)
        mfcc_std = np.std(mfccs, axis=1)
        return np.concatenate([mfcc_mean, mfcc_std])
    
    def extract_spectral_features(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Extract spectral features"""
        # Spectral centroid
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_centroid_mean = np.mean(spectral_centroids)
        spectral_centroid_std = np.std(spectral_centroids)
        
        # Spectral rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        spectral_rolloff_mean = np.mean(spectral_rolloff)
        spectral_rolloff_std = np.std(spectral_rolloff)
        
        # Spectral bandwidth
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        spectral_bandwidth_mean = np.mean(spectral_bandwidth)
        spectral_bandwidth_std = np.std(spectral_bandwidth)
        
        return np.array([
            spectral_centroid_mean, spectral_centroid_std,
            spectral_rolloff_mean, spectral_rolloff_std,
            spectral_bandwidth_mean, spectral_bandwidth_std
        ])
    
    def extract_zero_crossing_rate(self, y: np.ndarray) -> np.ndarray:
        """Extract zero crossing rate features"""
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        zcr_mean = np.mean(zcr)
        zcr_std = np.std(zcr)
        return np.array([zcr_mean, zcr_std])
    
    def extract_pitch_features(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Extract pitch-related features"""
        # Fundamental frequency estimation
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        
        # Get pitch values where magnitude is high
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        
        if len(pitch_values) > 0:
            pitch_mean = np.mean(pitch_values)
            pitch_std = np.std(pitch_values)
            pitch_variance = np.var(pitch_values)
        else:
            pitch_mean = pitch_std = pitch_variance = 0.0
        
        return np.array([pitch_mean, pitch_std, pitch_variance])
    
    def extract_harmonic_features(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Extract harmonic and percussive features"""
        # Separate harmonic and percussive components
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        
        # Calculate harmonic-to-noise ratio approximation
        harmonic_energy = np.sum(y_harmonic ** 2)
        percussive_energy = np.sum(y_percussive ** 2)
        
        if percussive_energy > 0:
            hnr = harmonic_energy / percussive_energy
        else:
            hnr = harmonic_energy
        
        harmonic_mean = np.mean(np.abs(y_harmonic))
        percussive_mean = np.mean(np.abs(y_percussive))
        
        return np.array([hnr, harmonic_mean, percussive_mean])
    
    def extract_all_features(self, audio_bytes: bytes) -> Dict[str, float]:
        """Extract all features from audio bytes and return as a dictionary"""
        # Load audio
        y, sr = self.load_audio_from_bytes(audio_bytes)
        
        # Extract all feature sets
        mfcc_features = self.extract_mfcc_features(y, sr)
        spectral_features = self.extract_spectral_features(y, sr)
        zcr_features = self.extract_zero_crossing_rate(y)
        pitch_features = self.extract_pitch_features(y, sr)
        harmonic_features = self.extract_harmonic_features(y, sr)
        
        # Concatenate all features into a single array to maintain order for scaler
        all_features_array = np.concatenate([
            mfcc_features,
            spectral_features,
            zcr_features,
            pitch_features,
            harmonic_features
        ])

        # Create a dictionary of features
        feature_names = self.get_feature_names()
        all_features_dict = dict(zip(feature_names, all_features_array))
        
        return all_features_dict
    
    def get_feature_names(self) -> list:
        """Get names of all features"""
        names = []
        
        # MFCC features
        for i in range(self.n_mfcc):
            names.append(f"mfcc_{i}_mean")
        for i in range(self.n_mfcc):
            names.append(f"mfcc_{i}_std")
        
        # Spectral features
        names.extend([
            "spectral_centroid_mean", "spectral_centroid_std",
            "spectral_rolloff_mean", "spectral_rolloff_std",
            "spectral_bandwidth_mean", "spectral_bandwidth_std"
        ])
        
        # ZCR features
        names.extend(["zcr_mean", "zcr_std"])
        
        # Pitch features
        names.extend(["pitch_mean", "pitch_std", "pitch_variance"])
        
        # Harmonic features
        names.extend(["hnr", "harmonic_mean", "percussive_mean"])
        
        return names
