#!/usr/bin/env python3
# debug_model.py
import sys
from improved_model import ImprovedHealthPredictor
from knowledge_base import MedicalKnowledgeBase

def test_prediction():
    """Test the prediction model to debug issues"""
    print("🔧 DEBUG: Testing Model Predictions")
    print("=" * 50)
    
    # Initialize
    predictor = ImprovedHealthPredictor()
    kb = MedicalKnowledgeBase()
    
    # Check if model exists
    if not predictor.load_model("improved_health_model"):
        print("❌ No model found, training new one...")
        predictor.train_model(epochs=20)
        predictor.save_model("improved_health_model")
    
    # Test different symptom combinations
    test_cases = [
        ["Fever", "Cough"],
        ["Headache", "Fatigue"],
        ["Runny Nose", "Sneezing"],
        ["Sore Throat", "Fever"],
        ["Shortness of Breath", "Wheezing"],
        ["Nausea", "Vomiting"],
    ]
    
    print("🧪 Testing various symptom combinations:")
    print("-" * 50)
    
    for i, symptoms in enumerate(test_cases, 1):
        print(f"\n{i}. Testing symptoms: {symptoms}")
        
        try:
            # Get prediction
            result = predictor.get_detailed_prediction(symptoms)
            
            print(f"   Predicted: {result['primary_diagnosis']}")
            print(f"   Confidence: {result['confidence']:.3f}")
            print(f"   Uncertainty: {result['uncertainty']:.3f}")
            
            # Show top 3 predictions
            print("   Top 3 predictions:")
            for j, pred in enumerate(result['all_predictions'][:3]):
                print(f"     {j+1}. {pred[0]}: {pred[1]['score']:.3f}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test knowledge base search
    print("\n" + "=" * 50)
    print("🔍 Testing Knowledge Base Search:")
    print("-" * 50)
    
    for symptoms in test_cases[:3]:
        print(f"\nSymptoms: {symptoms}")
        scores = kb.search_diseases_by_symptoms(symptoms)
        
        # Show top 3 KB results
        top_kb = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        for disease, score in top_kb:
            print(f"  {disease}: {score:.3f}")
    
    # Check available diseases and symptoms
    print("\n" + "=" * 50)
    print("📊 System Information:")
    print(f"Available diseases: {len(predictor.diseases)}")
    print(f"Available symptoms: {len(predictor.symptoms)}")
    print(f"Disease list: {predictor.diseases}")
    print(f"First 10 symptoms: {predictor.symptoms[:10]}")

if __name__ == "__main__":
    test_prediction() 