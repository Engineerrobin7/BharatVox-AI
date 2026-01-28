import numpy as np
import joblib
from pathlib import Path
from typing import Tuple, Dict
from .feature_extractor import AudioFeatureExtractor
import os


class VoiceClassifier:
    """Inference engine for voice classification"""

    # Constants for explanation thresholds
    _EXPLANATION_THRESHOLDS = {
        "mfcc_std_mean_ai": 10.0,
        "pitch_variance_ai": 1000.0,
        "hnr_ai": 5.0,
        "mfcc_std_mean_human": 10.0,
        "pitch_variance_human": 1000.0,
        "zcr_std_human": 0.01,
    }
    
    def __init__(self, model_path: str = None, scaler_path: str = None):
        self.feature_extractor = AudioFeatureExtractor()
        self.feature_names = self.feature_extractor.get_feature_names()
        
        # Load model and scaler
        if model_path is None:
            model_path = os.getenv("MODEL_PATH", "ml_engine/model_artifacts/voice_classifier.pkl")
        if scaler_path is None:
            scaler_path = os.getenv("SCALER_PATH", "ml_engine/model_artifacts/scaler.pkl")
        
        try:
            self.classifier = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            print(f"Model loaded from: {model_path}")
            print(f"Scaler loaded from: {scaler_path}")
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Model files not found. Please train the model first using train_model.py. Error: {str(e)}"
            )
    
    def predict(self, audio_bytes: bytes) -> Tuple[str, float, str]:
        """
        Predict if voice is AI-generated or human
        
        Returns:
            classification: "AI_GENERATED" or "HUMAN"
            confidence_score: Probability score (0-1)
            explanation: Human-readable explanation
        """
        # Extract features as a dictionary
        features_dict = self.feature_extractor.extract_all_features(audio_bytes)
        
        # Convert feature dictionary to numpy array in the correct order for the scaler
        features = np.array([features_dict[name] for name in self.feature_names])
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Predict
        prediction = self.classifier.predict(features_scaled)[0]
        probabilities = self.classifier.predict_proba(features_scaled)[0]
        
        # Map prediction to classification
        if prediction == 0:
            classification = "AI_GENERATED"
            confidence_score = probabilities[0]
            explanation = self._generate_ai_explanation(features_dict, confidence_score)
        else:
            classification = "HUMAN"
            confidence_score = probabilities[1]
            explanation = self._generate_human_explanation(features_dict, confidence_score)
        
        return classification, float(confidence_score), explanation
    
    def _generate_ai_explanation(self, features: Dict[str, float], confidence: float) -> str:
        """Generate explanation for AI-generated classification"""
        explanations = []
        
        # Analyze MFCC variance (AI voices often have lower variance)
        # Assuming mfcc_0_std to mfcc_12_std are the standard deviation features for MFCCs
        mfcc_std_values = [features[f"mfcc_{i}_std"] for i in range(self.feature_extractor.n_mfcc)]
        mfcc_std_mean = np.mean(mfcc_std_values)
        if mfcc_std_mean < self._EXPLANATION_THRESHOLDS["mfcc_std_mean_ai"]:
            explanations.append("consistent spectral patterns")
        
        # Analyze pitch variance
        pitch_variance = features["pitch_variance"]
        if pitch_variance < self._EXPLANATION_THRESHOLDS["pitch_variance_ai"]:
            explanations.append("uniform pitch characteristics")
        
        # Analyze harmonic-to-noise ratio
        hnr = features["hnr"]
        if hnr > self._EXPLANATION_THRESHOLDS["hnr_ai"]:
            explanations.append("high harmonic clarity")
        
        if not explanations:
            explanations.append("synthetic voice characteristics detected")
        
        base_msg = "Detected AI-generated voice with "
        return base_msg + ", ".join(explanations) + f" (confidence: {confidence:.2%})"
    
    def _generate_human_explanation(self, features: Dict[str, float], confidence: float) -> str:
        """Generate explanation for human classification"""
        explanations = []
        
        # Analyze MFCC variance (human voices have higher variance)
        mfcc_std_values = [features[f"mfcc_{i}_std"] for i in range(self.feature_extractor.n_mfcc)]
        mfcc_std_mean = np.mean(mfcc_std_values)
        if mfcc_std_mean > self._EXPLANATION_THRESHOLDS["mfcc_std_mean_human"]:
            explanations.append("natural spectral variation")
        
        # Analyze pitch variance
        pitch_variance = features["pitch_variance"]
        if pitch_variance > self._EXPLANATION_THRESHOLDS["pitch_variance_human"]:
            explanations.append("organic pitch fluctuations")
        
        # Analyze zero-crossing rate variation
        zcr_std = features["zcr_std"]
        if zcr_std > self._EXPLANATION_THRESHOLDS["zcr_std_human"]:
            explanations.append("natural voice modulation")
        
        if not explanations:
            explanations.append("human voice characteristics detected")
        
        base_msg = "Detected human voice with "
        return base_msg + ", ".join(explanations) + f" (confidence: {confidence:.2%})"


# Singleton instance for reuse
_classifier_instance = None


def get_classifier() -> VoiceClassifier:
    """Get or create classifier instance (singleton pattern)"""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = VoiceClassifier()
    return _classifier_instance
