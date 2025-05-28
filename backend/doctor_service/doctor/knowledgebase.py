# knowledgebase.py
# Defining knowledge base for symptoms, diseases, and advice in English

SYMPTOM_LIST = [
    'fever', 'high_fever', 'mild_fever', 'cough', 'cough_with_phlegm', 'sore_throat', 'stuffy_nose',
    'fatigue', 'weight_loss', 'thirst', 'frequent_urination', 'shortness_breath', 'chest_pain',
    'stomach_pain', 'nausea', 'vomiting', 'heartburn', 'bloating', 'persistent_cough',
    'muscle_aches', 'chills', 'headache', 'dizziness', 'blurred_vision',
    'light_sensitivity', 'sound_sensitivity', 'yellow_skin', 'abdominal_pain',
    'loss_of_taste', 'loss_of_smell', 'dark_urine', 'wheezing', 'chest_tightness',
    'night_sweats', 'rash', 'joint_pain', 'bleeding_gums', 'sweating', 'cold_hands_feet', 'pale_skin'
]

ADVICE = {
    'cold': 'Rest, stay hydrated, and consider over-the-counter cold medication.',
    'diabetes': 'Consult a doctor for a blood sugar test and monitor your diet.',
    'pneumonia': 'Seek medical attention immediately for a chest X-ray and treatment.',
    'gastritis': 'Avoid spicy foods, use antacids, and consult a doctor.',
    'covid-19': 'Isolate, test for COVID-19, consult healthcare provider.',
    'flu': 'Get plenty of rest, drink fluids, and take antiviral medication if prescribed.',
    'hypertension': 'Monitor your blood pressure and reduce salt intake.',
    'migraine': 'Avoid triggers and rest in a quiet, dark room.',
    'hepatitis': 'Rest, avoid alcohol, and seek medical attention.',
    'asthma': 'Use inhalers as prescribed and avoid allergens.',
    'bronchitis': 'Rest, drink fluids, and avoid smoke.',
    'tuberculosis': 'Consult a doctor immediately. Requires long-term antibiotics.',
    'dengue': 'Stay hydrated and monitor for bleeding. Seek medical care.',
    'malaria': 'Use antimalarial drugs and stay hydrated.',
    'anemia': 'Eat iron-rich foods and consult a doctor for supplements.',
    'default': 'Consult a doctor for further evaluation.'
}

# Symptom co-occurrence mapping (simplified based on training data)
SYMPTOM_RELATIONSHIP = {
    'fever': ['cough', 'fatigue', 'headache', 'chills', 'muscle_aches'],
    'high_fever': ['chills', 'sweating', 'muscle_aches', 'rash', 'joint_pain'],
    'mild_fever': ['cough', 'sore_throat', 'stuffy_nose', 'fatigue'],
    'cough': ['fever', 'sore_throat', 'stuffy_nose', 'fatigue', 'cough_with_phlegm'],
    'cough_with_phlegm': ['chest_pain', 'shortness_breath', 'fever', 'fatigue'],
    'sore_throat': ['cough', 'stuffy_nose', 'mild_fever', 'fatigue'],
    'stuffy_nose': ['cough', 'sore_throat', 'mild_fever', 'loss_of_smell'],
    'fatigue': ['fever', 'cough', 'weight_loss', 'dizziness', 'pale_skin'],
    'weight_loss': ['fatigue', 'night_sweats', 'persistent_cough', 'fever'],
    'thirst': ['frequent_urination', 'weight_loss', 'blurred_vision', 'fatigue'],
    'frequent_urination': ['thirst', 'weight_loss', 'blurred_vision', 'dizziness'],
    'shortness_breath': ['cough_with_phlegm', 'chest_pain', 'wheezing', 'chest_tightness'],
    'chest_pain': ['cough_with_phlegm', 'shortness_breath', 'chest_tightness', 'dizziness'],
    'stomach_pain': ['nausea', 'vomiting', 'heartburn', 'bloating'],
    'nausea': ['stomach_pain', 'vomiting', 'heartburn', 'headache'],
    'vomiting': ['stomach_pain', 'nausea', 'heartburn', 'abdominal_pain'],
    'heartburn': ['stomach_pain', 'nausea', 'bloating', 'vomiting'],
    'bloating': ['stomach_pain', 'heartburn', 'nausea', 'abdominal_pain'],
    'persistent_cough': ['weight_loss', 'night_sweats', 'fever', 'fatigue'],
    'muscle_aches': ['fever', 'chills', 'high_fever', 'joint_pain'],
    'chills': ['fever', 'high_fever', 'muscle_aches', 'sweating'],
    'headache': ['fever', 'dizziness', 'light_sensitivity', 'sound_sensitivity'],
    'dizziness': ['headache', 'blurred_vision', 'chest_pain', 'fatigue'],
    'blurred_vision': ['thirst', 'frequent_urination', 'dizziness', 'headache'],
    'light_sensitivity': ['headache', 'sound_sensitivity', 'nausea', 'migraine'],
    'sound_sensitivity': ['headache', 'light_sensitivity', 'nausea', 'migraine'],
    'yellow_skin': ['abdominal_pain', 'dark_urine', 'fatigue', 'nausea'],
    'abdominal_pain': ['yellow_skin', 'dark_urine', 'stomach_pain', 'nausea'],
    'loss_of_taste': ['loss_of_smell', 'fever', 'cough', 'fatigue'],
    'loss_of_smell': ['loss_of_taste', 'fever', 'cough', 'stuffy_nose'],
    'dark_urine': ['yellow_skin', 'abdominal_pain', 'fatigue', 'nausea'],
    'wheezing': ['shortness_breath', 'chest_tightness', 'cough', 'fatigue'],
    'chest_tightness': ['shortness_breath', 'wheezing', 'cough', 'chest_pain'],
    'night_sweats': ['persistent_cough', 'weight_loss', 'fever', 'fatigue'],
    'rash': ['high_fever', 'joint_pain', 'muscle_aches', 'bleeding_gums'],
    'joint_pain': ['rash', 'high_fever', 'muscle_aches', 'fever'],
    'bleeding_gums': ['rash', 'high_fever', 'joint_pain', 'muscle_aches'],
    'sweating': ['high_fever', 'chills', 'fever', 'fatigue'],
    'cold_hands_feet': ['pale_skin', 'fatigue', 'dizziness', 'shortness_breath'],
    'pale_skin': ['fatigue', 'dizziness', 'cold_hands_feet', 'shortness_breath'],
}

def suggest_symptoms(user_symptoms):
    # Suggest symptoms that the user hasn't mentioned yet
    all_suggestions = set()
    for symptom in user_symptoms:
        if symptom in SYMPTOM_RELATIONSHIP:
            related_symptoms = SYMPTOM_RELATIONSHIP[symptom]
            all_suggestions.update(related_symptoms)
    # Remove already selected symptoms
    suggestions = [s for s in all_suggestions if s not in user_symptoms]
    # Limit to 5 most relevant symptoms
    return list(set(suggestions))[:5]