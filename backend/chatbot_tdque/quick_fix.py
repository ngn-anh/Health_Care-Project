#!/usr/bin/env python3
# quick_fix.py - Fix the "always Asthma" issue

import os
import numpy as np
from improved_model import ImprovedHealthPredictor

def delete_old_model():
    """Delete old model files to force retraining"""
    files_to_delete = [
        "improved_health_model_model.keras",
        "improved_health_model_data.pkl"
    ]
    
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Deleted {file}")

def retrain_model():
    """Retrain model with better parameters"""
    print("🔄 Retraining model with improved parameters...")
    
    # Delete old model
    delete_old_model()
    
    # Create new predictor
    predictor = ImprovedHealthPredictor()
    
    # Train with more epochs and better parameters
    print("🚀 Training new model...")
    history = predictor.train_model(epochs=100)
    
    # Save model
    predictor.save_model("improved_health_model")
    
    # Test different symptoms
    test_cases = [
        ["Fever", "Cough"],           # Should be Flu/Cold
        ["Runny Nose", "Sneezing"],   # Should be Cold/Allergy
        ["Wheezing", "Shortness of Breath"],  # Should be Asthma
        ["Nausea", "Vomiting"],       # Should be Food Poisoning
        ["Headache", "Light Sensitivity"],  # Should be Migraine
    ]
    
    print("\n🧪 Testing predictions:")
    print("-" * 50)
    
    for symptoms in test_cases:
        result = predictor.get_detailed_prediction(symptoms)
        print(f"Symptoms: {symptoms}")
        print(f"Predicted: {result['primary_diagnosis']}")
        print(f"Confidence: {result['confidence']:.3f}")
        print("-" * 30)

if __name__ == "__main__":
    retrain_model() 