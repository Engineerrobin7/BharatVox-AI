"""
Demo Model Generator for BharatVox AI
This creates a basic pre-trained model for testing purposes when you don't have training data yet.
WARNING: This is for DEMO/TESTING only. Train with real data for production use.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
import sys

def create_demo_model():
    """Create a demo model with synthetic data for testing"""
    
    print("=" * 60)
    print("BharatVox AI - Demo Model Generator")
    print("=" * 60)
    print("\nWARNING: This creates a DEMO model for testing only!")
    print("For production use, train with real audio data.\n")
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    # Create model artifacts directory inside the script's directory
    model_dir = script_dir / "model_artifacts"
    model_dir.mkdir(exist_ok=True)
    
    # Generate synthetic training data
    # 40 features (matching our feature extractor)
    n_samples = 200
    n_features = 40
    
    print(f"Generating {n_samples} synthetic samples with {n_features} features...")
    
    # Create synthetic AI-generated voice features
    # AI voices typically have:
    # - Lower MFCC variance
    # - More consistent pitch
    # - Higher harmonic-to-noise ratio
    ai_features = np.random.randn(n_samples // 2, n_features)
    ai_features[:, 13:26] *= 0.5  # Lower MFCC std
    ai_features[:, -6] *= 0.3     # Lower pitch variance
    ai_features[:, -3] += 2       # Higher HNR
    
    # Create synthetic human voice features
    # Human voices typically have:
    # - Higher MFCC variance
    # - More pitch variation
    # - Natural fluctuations
    human_features = np.random.randn(n_samples // 2, n_features)
    human_features[:, 13:26] *= 1.5  # Higher MFCC std
    human_features[:, -6] *= 2.0     # Higher pitch variance
    human_features[:, -9] *= 1.5     # Higher ZCR variation
    
    # Combine datasets
    X = np.vstack([ai_features, human_features])
    y = np.array([0] * (n_samples // 2) + [1] * (n_samples // 2))  # 0=AI, 1=Human
    
    # Shuffle
    indices = np.random.permutation(n_samples)
    X = X[indices]
    y = y[indices]
    
    print(f"Total samples: {len(X)}")
    print(f"AI samples: {sum(y == 0)}")
    print(f"Human samples: {sum(y == 1)}")
    
    # Create and train scaler
    print("\nTraining scaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Create and train classifier
    print("Training Random Forest classifier...")
    classifier = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    classifier.fit(X_scaled, y)
    
    # Calculate training accuracy
    train_accuracy = classifier.score(X_scaled, y)
    print(f"\nTraining accuracy: {train_accuracy:.4f}")
    
    # Save model and scaler
    model_path = model_dir / "voice_classifier.pkl"
    scaler_path = model_dir / "scaler.pkl"
    
    joblib.dump(classifier, model_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"\nDemo model saved to: {model_path}")
    print(f"Demo scaler saved to: {scaler_path}")
    
    print("\n" + "=" * 60)
    print("Demo model created successfully!")
    print("=" * 60)
    print("\nYou can now test the API with this demo model.")
    print("Remember: Train with real audio data for production use!")
    print("\nTo train with real data:")
    print("1. Add audio files to data/training_data/human/ and data/training_data/ai_generated/")
    print("2. Run: python train_model.py")
    print("=" * 60)


if __name__ == "__main__":
    create_demo_model()
