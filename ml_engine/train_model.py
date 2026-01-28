import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os
from pathlib import Path
from typing import Tuple, List
from feature_extractor import AudioFeatureExtractor


class VoiceClassifierTrainer:
    """Train a binary classifier for AI vs Human voice detection"""
    
    def __init__(self, model_save_path: str = "model_artifacts"):
        self.model_save_path = Path(model_save_path)
        self.model_save_path.mkdir(parents=True, exist_ok=True)
        
        self.feature_extractor = AudioFeatureExtractor()
        self.scaler = StandardScaler()
        self.classifier = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
    
    def load_audio_files(self, directory: Path, label: int) -> Tuple[List[np.ndarray], List[int]]:
        """Load all audio files from a directory and extract features"""
        features = []
        labels = []
        
        audio_extensions = ['.mp3', '.wav', '.flac', '.ogg']
        audio_files = []
        
        for ext in audio_extensions:
            audio_files.extend(directory.glob(f"**/*{ext}"))
        
        print(f"Found {len(audio_files)} audio files in {directory}")
        
        for audio_file in audio_files:
            try:
                with open(audio_file, 'rb') as f:
                    audio_bytes = f.read()
                
                feature_vector = self.feature_extractor.extract_all_features(audio_bytes)
                features.append(feature_vector)
                labels.append(label)
                
            except Exception as e:
                print(f"Error processing {audio_file}: {str(e)}")
                continue
        
        return features, labels
    
    def prepare_training_data(self, human_dir: str, ai_dir: str) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data from human and AI voice directories"""
        print("Loading human voice samples...")
        human_features, human_labels = self.load_audio_files(Path(human_dir), label=1)  # 1 = HUMAN
        
        print("Loading AI-generated voice samples...")
        ai_features, ai_labels = self.load_audio_files(Path(ai_dir), label=0)  # 0 = AI_GENERATED
        
        # Combine datasets
        X = np.array(human_features + ai_features)
        y = np.array(human_labels + ai_labels)
        
        print(f"\nTotal samples: {len(X)}")
        print(f"Human samples: {sum(y == 1)}")
        print(f"AI samples: {sum(y == 0)}")
        print(f"Feature dimension: {X.shape[1]}")
        
        return X, y
    
    def train(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2):
        """Train the classifier"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        print(f"\nTraining samples: {len(X_train)}")
        print(f"Testing samples: {len(X_test)}")
        
        # Scale features
        print("\nScaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train classifier
        print("Training Random Forest classifier...")
        self.classifier.fit(X_train_scaled, y_train)
        
        # Evaluate
        print("\nEvaluating model...")
        y_pred = self.classifier.predict(X_test_scaled)
        
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\nAccuracy: {accuracy:.4f}")
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['AI_GENERATED', 'HUMAN']))
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Feature importance
        feature_names = self.feature_extractor.get_feature_names()
        feature_importance = self.classifier.feature_importances_
        top_features_idx = np.argsort(feature_importance)[-10:]
        
        print("\nTop 10 Most Important Features:")
        for idx in reversed(top_features_idx):
            print(f"{feature_names[idx]}: {feature_importance[idx]:.4f}")
        
        return accuracy
    
    def save_model(self):
        """Save trained model and scaler"""
        model_path = self.model_save_path / "voice_classifier.pkl"
        scaler_path = self.model_save_path / "scaler.pkl"
        
        joblib.dump(self.classifier, model_path)
        joblib.dump(self.scaler, scaler_path)
        
        print(f"\nModel saved to: {model_path}")
        print(f"Scaler saved to: {scaler_path}")
    
    def train_and_save(self, human_dir: str, ai_dir: str):
        """Complete training pipeline"""
        print("=" * 60)
        print("BharatVox AI - Voice Classifier Training")
        print("=" * 60)
        
        # Prepare data
        X, y = self.prepare_training_data(human_dir, ai_dir)
        
        if len(X) < 10:
            print("\nWARNING: Very few training samples. Model may not perform well.")
            print("Please add more audio samples to the training directories.")
        
        # Train
        accuracy = self.train(X, y)
        
        # Save
        self.save_model()
        
        print("\n" + "=" * 60)
        print(f"Training completed! Final accuracy: {accuracy:.4f}")
        print("=" * 60)


if __name__ == "__main__":
    # Training script
    trainer = VoiceClassifierTrainer(model_save_path="model_artifacts")
    
    # Update these paths to your training data directories
    HUMAN_VOICE_DIR = "../data/training_data/human"
    AI_VOICE_DIR = "../data/training_data/ai_generated"
    
    trainer.train_and_save(HUMAN_VOICE_DIR, AI_VOICE_DIR)
