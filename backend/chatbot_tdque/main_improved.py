# main_improved.py
import numpy as np
import tensorflow as tf
import pyttsx3
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import logging
from improved_model import ImprovedHealthPredictor
from knowledge_base import MedicalKnowledgeBase

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the improved predictor
predictor = ImprovedHealthPredictor()
kb = MedicalKnowledgeBase()

# Try to load pre-trained model, otherwise train new one
if not predictor.load_model("improved_health_model"):
    print("🔄 No pre-trained model found. Training new model...")
    predictor.train_model(epochs=50)
    predictor.save_model("improved_health_model")

app = Flask(__name__)
CORS(app)

# Storage for consultation history
consultation_history = []

# Vietnamese to English symptom mapping
VIETNAMESE_SYMPTOMS = {
    "sốt": "Fever",
    "sot": "Fever",
    "ho": "Cough", 
    "đau đầu": "Headache",
    "dau dau": "Headache",
    "đau dầu": "Headache",
    "mệt mỏi": "Fatigue",
    "met moi": "Fatigue",
    "mệt": "Fatigue",
    "met": "Fatigue",
    "đau họng": "Sore Throat",
    "dau hong": "Sore Throat",
    "chảy nước mũi": "Runny Nose",
    "chay nuoc mui": "Runny Nose",
    "sổ mũi": "Runny Nose",
    "so mui": "Runny Nose",
    "buồn nôn": "Nausea",
    "buon non": "Nausea",
    "nôn": "Vomiting",
    "non": "Vomiting",
    "đau bụng": "Abdominal Pain",
    "dau bung": "Abdominal Pain",
    "khó thở": "Shortness of Breath",
    "kho tho": "Shortness of Breath",
    "đau ngực": "Chest Pain",
    "dau nguc": "Chest Pain",
    "đau cơ": "Muscle Pain",
    "dau co": "Muscle Pain",
    "mất vị giác": "Loss of Taste",
    "mat vi giac": "Loss of Taste",
    "mất vị": "Loss of Taste",
    "mat vi": "Loss of Taste",
    "mất khứu giác": "Loss of Smell",
    "mat khuu giac": "Loss of Smell",
    "mất mùi": "Loss of Smell",
    "mat mui": "Loss of Smell",
    "tiêu chảy": "Diarrhea",
    "tieu chay": "Diarrhea",
    "táo bón": "Constipation",
    "tao bon": "Constipation",
    "chóng mặt": "Dizziness",
    "chong mat": "Dizziness",
    "ngứa": "Itching",
    "ngua": "Itching",
    "phát ban": "Rash",
    "phat ban": "Rash",
    "sưng": "Swelling",
    "sung": "Swelling",
    "đau khớp": "Joint Pain",
    "dau khop": "Joint Pain",
    "thở khò khè": "Wheezing",
    "tho kho khe": "Wheezing",
    "khò khè": "Wheezing",
    "kho khe": "Wheezing",
    "hắt hơi": "Sneezing",
    "hat hoi": "Sneezing",
    "ngạt thở": "Shortness of Breath",
    "ngat tho": "Shortness of Breath",
    "sốt cao": "High Fever",
    "sot cao": "High Fever",
    "đau dữ dội": "Severe Pain",
    "dau du doi": "Severe Pain"
}

def map_vietnamese_symptoms(symptoms):
    """Convert Vietnamese symptoms to English"""
    mapped_symptoms = []
    
    for symptom_text in symptoms:
        # Split by common separators
        individual_symptoms = []
        
        # Split by commas, semicolons, and "và"
        for separator in [',', ';', ' và ', ' và', 'và ', ' va ', ' va', 'va ']:
            parts = symptom_text.split(separator)
            if len(parts) > 1:
                individual_symptoms.extend([s.strip() for s in parts if s.strip()])
                break
        
        # If no separator found, treat as single symptom
        if not individual_symptoms:
            individual_symptoms = [symptom_text.strip()]
        
        # Map each individual symptom
        for individual_symptom in individual_symptoms:
            if not individual_symptom:
                continue
                
            # Try exact match first
            mapped = VIETNAMESE_SYMPTOMS.get(individual_symptom.lower())
            if mapped:
                if mapped not in mapped_symptoms:  # Avoid duplicates
                    mapped_symptoms.append(mapped)
            else:
                # Try partial matching
                found = False
                for viet, eng in VIETNAMESE_SYMPTOMS.items():
                    if viet in individual_symptom.lower() or individual_symptom.lower() in viet:
                        if eng not in mapped_symptoms:  # Avoid duplicates
                            mapped_symptoms.append(eng)
                        found = True
                        break
                
                # If no mapping found, keep original (capitalize first letter)
                if not found:
                    original = individual_symptom.strip().title()
                    if original not in mapped_symptoms:
                        mapped_symptoms.append(original)
    
    return mapped_symptoms

def speak(text):
    """Text-to-speech function"""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logger.error(f"Speech synthesis error: {e}")

@app.route('/symptoms', methods=['GET'])
def get_symptoms():
    """Get all available symptoms"""
    symptoms = kb.get_all_symptoms()
    return jsonify({
        "symptoms": symptoms,
        "total": len(symptoms)
    })

@app.route('/diseases', methods=['GET'])
def get_diseases():
    """Get all available diseases"""
    diseases = kb.get_all_diseases()
    disease_info = {}
    
    for disease in diseases:
        info = kb.get_disease_info(disease)
        disease_info[disease] = {
            "name": info.name,
            "description": info.description,
            "severity": info.severity,
            "contagious": info.contagious,
            "duration": info.duration
        }
    
    return jsonify({
        "diseases": disease_info,
        "total": len(diseases)
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Enhanced prediction endpoint"""
    try:
        data = request.json
        
        # Handle different input formats
        if 'symptoms' in data:
            if isinstance(data['symptoms'], list):
                # List of symptom names
                if all(isinstance(s, str) for s in data['symptoms']):
                    raw_symptoms = data['symptoms']
                    # Map Vietnamese symptoms to English
                    symptoms = map_vietnamese_symptoms(raw_symptoms)
                    logger.info(f"Mapped symptoms: {raw_symptoms} -> {symptoms}")
                else:
                    # List of 0/1 values (legacy format)
                    symptom_names = kb.get_all_symptoms()
                    symptoms = [symptom_names[i] for i, val in enumerate(data['symptoms']) if val == 1]
            else:
                return jsonify({"error": "Invalid symptoms format"}), 400
        else:
            return jsonify({"error": "Missing symptoms"}), 400
        
        # Get detailed prediction
        result = predictor.get_detailed_prediction(symptoms)
        
        # Debug logging
        logger.info(f"Prediction result: {result['primary_diagnosis']}")
        logger.info(f"Confidence: {result['confidence']}")
        if result['disease_info']:
            logger.info(f"Disease info found: {result['disease_info'].name}")
        else:
            logger.info("No disease info found")
        
        # Check for emergency symptoms
        emergency_alert = None
        emergency_symptoms = ["Shortness of Breath", "Chest Pain", "High Fever", "Severe Headache", 
                            "đau ngực", "khó thở", "sốt cao", "đau đầu dữ dội"]
        if any(symptom.lower() in [s.lower() for s in emergency_symptoms] for symptom in symptoms):
            emergency_alert = "⚠️ TRIỆU CHỨNG KHẨN CẤP - HÃY ĐẾN BỆNH VIỆN NGAY LẬP TỨC!"
        
        # Format response to match chat interface expectations
        response = {
            "predicted_disease": result['primary_diagnosis'],
            "confidence": float(result['confidence']),
            "confidence_level": result['confidence_level'],
            "uncertainty": float(result['uncertainty']),
            "input_symptoms": symptoms,
            "emergency_alert": emergency_alert,
            "description": result['disease_info'].description if result['disease_info'] else None,
            "treatment": result['disease_info'].treatments[0] if result['disease_info'] and result['disease_info'].treatments else None,
            "when_to_see_doctor": result['disease_info'].when_to_see_doctor if result['disease_info'] else None,
            "prevention": result['disease_info'].prevention[0] if result['disease_info'] and result['disease_info'].prevention else None,
            "alternatives": [
                {
                    "disease": pred[0],
                    "probability": float(pred[1]['score']),
                    "ml_score": float(pred[1]['ml_score']),
                    "kb_score": float(pred[1]['kb_score'])
                }
                for pred in result['all_predictions'][:3]
            ],
            "recommendations": result['recommendations'],
            "timestamp": datetime.now().isoformat()
        }
        
        # Store in history
        consultation_history.append(response)
        
        # Keep only last 100 consultations
        if len(consultation_history) > 100:
            consultation_history.pop(0)
        
        logger.info(f"Prediction made for symptoms: {symptoms}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/disease/<disease_name>', methods=['GET'])
def get_disease_info(disease_name):
    """Get detailed information about a specific disease"""
    try:
        # Try different formatting
        disease_names_to_try = [
            disease_name,
            disease_name.replace('_', ' '),
            disease_name.replace(' ', '_'),
            disease_name.title(),
            disease_name.upper(),
            disease_name.lower()
        ]
        
        for name in disease_names_to_try:
            disease_info = kb.get_disease_info(name)
            if disease_info:
                return jsonify({
                    "name": disease_info.name,
                    "description": disease_info.description,
                    "common_symptoms": disease_info.common_symptoms,
                    "severity": disease_info.severity,
                    "recommended_tests": disease_info.recommended_tests,
                    "treatments": disease_info.treatments,
                    "prevention": disease_info.prevention,
                    "when_to_see_doctor": disease_info.when_to_see_doctor,
                    "contagious": disease_info.contagious,
                    "duration": disease_info.duration
                })
        
        return jsonify({"error": "Disease not found"}), 404
        
    except Exception as e:
        logger.error(f"Disease info error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/symptom/<symptom_name>', methods=['GET'])
def get_symptom_info(symptom_name):
    """Get detailed information about a specific symptom"""
    try:
        symptom_info = kb.get_symptom_info(symptom_name)
        if symptom_info:
            return jsonify({
                "name": symptom_info.name,
                "description": symptom_info.description,
                "severity_levels": symptom_info.severity_levels,
                "common_causes": symptom_info.common_causes
            })
        else:
            return jsonify({"error": "Symptom not found"}), 404
            
    except Exception as e:
        logger.error(f"Symptom info error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/search', methods=['POST'])
def search_by_symptoms():
    """Search diseases by symptoms using knowledge base only"""
    try:
        data = request.json
        symptoms = data.get('symptoms', [])
        
        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400
        
        # Search using knowledge base
        scores = kb.search_diseases_by_symptoms(symptoms)
        
        results = []
        for disease, score in list(scores.items())[:5]:  # Top 5
            disease_info = kb.get_disease_info(disease)
            results.append({
                "disease": disease,
                "similarity_score": score,
                "name": disease_info.name if disease_info else disease,
                "description": disease_info.description if disease_info else "",
                "severity": disease_info.severity if disease_info else "unknown"
            })
        
        return jsonify({
            "results": results,
            "query_symptoms": symptoms
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/history', methods=['GET'])
def get_consultation_history():
    """Get consultation history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = consultation_history[-limit:] if limit > 0 else consultation_history
        
        return jsonify({
            "history": history,
            "total": len(consultation_history)
        })
        
    except Exception as e:
        logger.error(f"History error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        # Calculate some basic stats
        total_consultations = len(consultation_history)
        
        if total_consultations > 0:
            # Most common diagnoses
            diagnoses = [h['predicted_disease'] for h in consultation_history]
            diagnosis_counts = {}
            for d in diagnoses:
                diagnosis_counts[d] = diagnosis_counts.get(d, 0) + 1
            
            most_common = sorted(diagnosis_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Average confidence
            confidences = [h['confidence'] for h in consultation_history]
            avg_confidence = sum(confidences) / len(confidences)
        else:
            most_common = []
            avg_confidence = 0
        
        return jsonify({
            "total_consultations": total_consultations,
            "total_diseases": len(kb.get_all_diseases()),
            "total_symptoms": len(kb.get_all_symptoms()),
            "most_common_diagnoses": most_common,
            "average_confidence": avg_confidence
        })
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": predictor.model is not None,
        "knowledge_base_loaded": len(kb.diseases) > 0,
        "timestamp": datetime.now().isoformat()
    })

def run_virtual_robot():
    """Enhanced virtual robot with improved predictions"""
    print("🤖 Welcome to the Advanced Health Assistant Robot!")
    print("=" * 60)
    print("This system uses advanced AI and medical knowledge base")
    print("to provide comprehensive health assessments.")
    print("=" * 60)
    
    # Display available symptoms
    symptoms = kb.get_all_symptoms()
    print(f"\n📋 Available symptoms ({len(symptoms)} total):")
    for i, symptom in enumerate(symptoms, 1):
        print(f"{i:2d}. {symptom}")
    
    print("\n" + "=" * 60)
    print("Please select your symptoms by entering their numbers")
    print("separated by commas (e.g., 1,5,8) or 'q' to quit:")
    
    user_input = input("Your selection: ").strip()
    
    if user_input.lower() == 'q':
        print("👋 Thank you for using the Health Assistant!")
        return
    
    try:
        # Parse user input
        selected_indices = [int(x.strip()) - 1 for x in user_input.split(',')]
        selected_symptoms = [symptoms[i] for i in selected_indices if 0 <= i < len(symptoms)]
        
        if not selected_symptoms:
            print("❌ No valid symptoms selected.")
            return
        
        print(f"\n🔍 Analyzing symptoms: {', '.join(selected_symptoms)}")
        print("Please wait...")
        
        # Get detailed prediction
        result = predictor.get_detailed_prediction(selected_symptoms)
        
        # Display results
        print("\n" + "=" * 60)
        print("🎯 DIAGNOSIS RESULTS")
        print("=" * 60)
        
        print(f"Primary Diagnosis: {result['primary_diagnosis']}")
        print(f"Confidence: {result['confidence']:.1%} ({result['confidence_level']})")
        print(f"Uncertainty: ±{result['uncertainty']:.3f}")
        
        if result['disease_info']:
            disease = result['disease_info']
            print(f"\n📄 Disease Information:")
            print(f"  Description: {disease.description}")
            print(f"  Severity: {disease.severity.title()}")
            print(f"  Duration: {disease.duration}")
            print(f"  Contagious: {'Yes' if disease.contagious else 'No'}")
        
        print(f"\n🔄 Alternative Diagnoses:")
        for pred in result['all_predictions'][:3]:
            print(f"  {pred[0]}: {pred[1]['score']:.1%}")
        
        print(f"\n💡 Recommendations:")
        recommendations = result['recommendations']
        
        print("  Immediate Actions:")
        for action in recommendations['immediate_actions']:
            print(f"    • {action}")
        
        print("  Recommended Tests:")
        for test in recommendations['tests']:
            print(f"    • {test}")
        
        print("  Possible Treatments:")
        for treatment in recommendations['treatments']:
            print(f"    • {treatment}")
        
        print(f"\n⚠️  When to see a doctor: {recommendations['when_to_see_doctor']}")
        
        # Text-to-speech
        speak_text = f"Based on your symptoms, you may have {result['primary_diagnosis']}. "
        speak_text += f"I recommend {recommendations['when_to_see_doctor']}"
        speak(speak_text)
        
        print("\n" + "=" * 60)
        
    except ValueError:
        print("❌ Invalid input format. Please enter numbers separated by commas.")
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == '__main__':
    print("🚀 Starting Advanced Health Assistant...")
    print("Choose mode:")
    print("1. Interactive Robot Mode")
    print("2. Web API Mode")
    
    choice = input("Enter choice (1/2): ").strip()
    
    if choice == '1':
        run_virtual_robot()
    else:
        print("🌐 Starting web server on http://127.0.0.1:8004")
        print("📚 API Documentation:")
        print("  GET  /symptoms          - Get all symptoms")
        print("  GET  /diseases          - Get all diseases")
        print("  POST /predict           - Make prediction")
        print("  GET  /disease/<name>    - Get disease info")
        print("  GET  /symptom/<name>    - Get symptom info")
        print("  POST /search            - Search by symptoms")
        print("  GET  /history           - Get consultation history")
        print("  GET  /stats             - Get system statistics")
        print("  GET  /health            - Health check")
        app.run(debug=True, host='0.0.0.0', port=8004) 