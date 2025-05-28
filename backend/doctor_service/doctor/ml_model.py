# doctor_service/ml_model.py

import os
import joblib
import numpy as np
from .knowledgebase import SYMPTOM_LIST, ADVICE, suggest_symptoms

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Load model, scaler, mlb once
model = joblib.load(os.path.join(BASE_DIR, "disease_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
mlb = joblib.load(os.path.join(BASE_DIR, "mlb.pkl"))

def diagnose_with_ai(symptoms):
    if not symptoms:
        return {
            "message": "Please provide symptoms.",
            "finished": False,
            "suggested_symptoms": SYMPTOM_LIST[:5]
        }

    valid_symptoms = [s for s in symptoms if s in SYMPTOM_LIST]

    symptom_features = mlb.transform([valid_symptoms])
    symptom_features = scaler.transform(symptom_features)
    prediction = model.predict(symptom_features)[0]
    probability = model.predict_proba(symptom_features)[0]
    confidence = float(np.max(probability))

    if confidence >= 0.7 or len(valid_symptoms) >= 5:
        advice = ADVICE.get(prediction, ADVICE['default'])
        return {
            "message": f"Diagnosis: {prediction} (Confidence: {confidence * 100:.2f}%)\nAdvice: {advice}",
            "finished": True
        }

    suggested_symptoms = suggest_symptoms(valid_symptoms)

    return {
        "message": f"I'm not confident to diagnose yet. Do you have any of these?",
        "suggested_symptoms": suggested_symptoms,
        "finished": False
    }
