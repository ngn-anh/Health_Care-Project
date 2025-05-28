# train_model.py
# Script to train and save a new AI model for disease prediction

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from sklearn.model_selection import StratifiedKFold, cross_val_score
import joblib

# Symptom list from knowledgebase
SYMPTOM_LIST = [
    'fever', 'high_fever', 'mild_fever', 'cough', 'cough_with_phlegm', 'sore_throat', 'stuffy_nose',
    'fatigue', 'weight_loss', 'thirst', 'frequent_urination', 'shortness_breath', 'chest_pain',
    'stomach_pain', 'nausea', 'vomiting', 'heartburn', 'bloating', 'persistent_cough',
    'muscle_aches', 'chills', 'headache', 'dizziness', 'blurred_vision',
    'light_sensitivity', 'sound_sensitivity', 'yellow_skin', 'abdominal_pain',
    'loss_of_taste', 'loss_of_smell', 'dark_urine', 'wheezing', 'chest_tightness',
    'night_sweats', 'rash', 'joint_pain', 'bleeding_gums', 'sweating', 'cold_hands_feet', 'pale_skin'
]

# Expanded dataset: more samples for each disease to improve model accuracy
data = {
    'symptoms': [
        # Cold (5 samples)
        ['cough', 'sore_throat', 'stuffy_nose', 'mild_fever', 'fatigue'],
        ['cough', 'stuffy_nose', 'mild_fever', 'headache'],
        ['sore_throat', 'stuffy_nose', 'fatigue', 'mild_fever'],
        ['cough', 'sore_throat', 'fatigue', 'stuffy_nose'],
        ['mild_fever', 'cough', 'headache', 'fatigue'],
        # Flu (5 samples)
        ['high_fever', 'chills', 'muscle_aches', 'fatigue', 'cough'],
        ['high_fever', 'muscle_aches', 'cough', 'sore_throat', 'fatigue'],
        ['high_fever', 'chills', 'headache', 'cough', 'fatigue'],
        ['chills', 'high_fever', 'muscle_aches', 'cough'],
        ['high_fever', 'fatigue', 'cough', 'chills'],
        # Pneumonia (5 samples)
        ['high_fever', 'cough_with_phlegm', 'chest_pain', 'shortness_breath'],
        ['high_fever', 'cough_with_phlegm', 'fatigue', 'chest_pain'],
        ['shortness_breath', 'cough_with_phlegm', 'fever', 'chest_tightness'],
        ['cough_with_phlegm', 'chest_pain', 'shortness_breath', 'fever'],
        ['chest_pain', 'shortness_breath', 'cough_with_phlegm'],
        # COVID-19 (5 samples)
        ['fever', 'cough', 'loss_of_taste', 'loss_of_smell', 'fatigue'],
        ['fever', 'cough', 'fatigue', 'shortness_breath', 'loss_of_smell'],
        ['loss_of_taste', 'loss_of_smell', 'fever', 'cough', 'headache'],
        ['cough', 'fever', 'loss_of_smell', 'fatigue'],
        ['loss_of_taste', 'fever', 'cough', 'shortness_breath'],
        # Diabetes (5 samples)
        ['thirst', 'frequent_urination', 'weight_loss', 'blurred_vision'],
        ['thirst', 'frequent_urination', 'fatigue', 'blurred_vision'],
        ['weight_loss', 'frequent_urination', 'thirst', 'dizziness'],
        ['thirst', 'blurred_vision', 'frequent_urination', 'fatigue'],
        ['weight_loss', 'thirst', 'frequent_urination'],
        # Gastritis (5 samples)
        ['stomach_pain', 'nausea', 'bloating', 'heartburn', 'vomiting'],
        ['stomach_pain', 'heartburn', 'nausea', 'bloating'],
        ['vomiting', 'stomach_pain', 'heartburn', 'abdominal_pain'],
        ['nausea', 'stomach_pain', 'bloating', 'heartburn'],
        ['stomach_pain', 'vomiting', 'heartburn'],
        # Hypertension (5 samples)
        ['headache', 'dizziness', 'blurred_vision', 'chest_pain'],
        ['dizziness', 'chest_pain', 'headache', 'blurred_vision'],
        ['headache', 'dizziness', 'chest_tightness', 'sweating'],
        ['chest_pain', 'headache', 'dizziness', 'blurred_vision'],
        ['dizziness', 'headache', 'chest_pain'],
        # Migraine (5 samples)
        ['headache', 'nausea', 'light_sensitivity', 'sound_sensitivity'],
        ['headache', 'light_sensitivity', 'nausea', 'dizziness'],
        ['sound_sensitivity', 'headache', 'light_sensitivity', 'fatigue'],
        ['headache', 'nausea', 'sound_sensitivity', 'light_sensitivity'],
        ['light_sensitivity', 'headache', 'nausea'],
        # Hepatitis (5 samples)
        ['yellow_skin', 'abdominal_pain', 'fatigue', 'dark_urine'],
        ['yellow_skin', 'fatigue', 'dark_urine', 'nausea'],
        ['abdominal_pain', 'yellow_skin', 'dark_urine', 'fever'],
        ['dark_urine', 'yellow_skin', 'abdominal_pain', 'fatigue'],
        ['yellow_skin', 'nausea', 'dark_urine'],
        # Asthma (5 samples)
        ['shortness_breath', 'wheezing', 'chest_tightness', 'cough'],
        ['wheezing', 'shortness_breath', 'chest_tightness', 'cough'],
        ['cough', 'wheezing', 'shortness_breath', 'fatigue'],
        ['shortness_breath', 'chest_tightness', 'wheezing'],
        ['wheezing', 'shortness_breath', 'cough'],
        # Bronchitis (5 samples)
        ['cough_with_phlegm', 'chest_pain', 'fatigue', 'mild_fever'],
        ['cough_with_phlegm', 'fatigue', 'mild_fever', 'sore_throat'],
        ['cough_with_phlegm', 'chest_pain', 'mild_fever', 'fatigue'],
        ['mild_fever', 'cough_with_phlegm', 'chest_pain'],
        ['fatigue', 'cough_with_phlegm', 'mild_fever'],
        # Tuberculosis (5 samples)
        ['persistent_cough', 'weight_loss', 'night_sweats', 'fever'],
        ['persistent_cough', 'night_sweats', 'weight_loss', 'fatigue'],
        ['fever', 'persistent_cough', 'weight_loss', 'night_sweats'],
        ['night_sweats', 'persistent_cough', 'fever', 'fatigue'],
        ['weight_loss', 'persistent_cough', 'night_sweats'],
        # Dengue (5 samples)
        ['high_fever', 'rash', 'joint_pain', 'muscle_aches', 'bleeding_gums'],
        ['high_fever', 'rash', 'joint_pain', 'headache'],
        ['muscle_aches', 'high_fever', 'rash', 'bleeding_gums'],
        ['joint_pain', 'high_fever', 'rash', 'muscle_aches'],
        ['rash', 'high_fever', 'bleeding_gums'],
        # Malaria (5 samples)
        ['high_fever', 'chills', 'sweating', 'headache', 'nausea'],
        ['high_fever', 'chills', 'sweating', 'fatigue', 'headache'],
        ['nausea', 'high_fever', 'chills', 'muscle_aches'],
        ['chills', 'high_fever', 'sweating', 'headache'],
        ['high_fever', 'nausea', 'chills'],
        # Anemia (5 samples)
        ['fatigue', 'pale_skin', 'shortness_breath', 'dizziness', 'cold_hands_feet'],
        ['pale_skin', 'fatigue', 'dizziness', 'cold_hands_feet'],
        ['shortness_breath', 'fatigue', 'pale_skin', 'dizziness'],
        ['fatigue', 'cold_hands_feet', 'pale_skin', 'shortness_breath'],
        ['dizziness', 'pale_skin', 'fatigue'],
    ],
    'disease': [
        # Cold
        'cold', 'cold', 'cold', 'cold', 'cold',
        # Flu
        'flu', 'flu', 'flu', 'flu', 'flu',
        # Pneumonia
        'pneumonia', 'pneumonia', 'pneumonia', 'pneumonia', 'pneumonia',
        # COVID-19
        'covid-19', 'covid-19', 'covid-19', 'covid-19', 'covid-19',
        # Diabetes
        'diabetes', 'diabetes', 'diabetes', 'diabetes', 'diabetes',
        # Gastritis
        'gastritis', 'gastritis', 'gastritis', 'gastritis', 'gastritis',
        # Hypertension
        'hypertension', 'hypertension', 'hypertension', 'hypertension', 'hypertension',
        # Migraine
        'migraine', 'migraine', 'migraine', 'migraine', 'migraine',
        # Hepatitis
        'hepatitis', 'hepatitis', 'hepatitis', 'hepatitis', 'hepatitis',
        # Asthma
        'asthma', 'asthma', 'asthma', 'asthma', 'asthma',
        # Bronchitis
        'bronchitis', 'bronchitis', 'bronchitis', 'bronchitis', 'bronchitis',
        # Tuberculosis
        'tuberculosis', 'tuberculosis', 'tuberculosis', 'tuberculosis', 'tuberculosis',
        # Dengue
        'dengue', 'dengue', 'dengue', 'dengue', 'dengue',
        # Malaria
        'malaria', 'malaria', 'malaria', 'malaria', 'malaria',
        # Anemia
        'anemia', 'anemia', 'anemia', 'anemia', 'anemia',
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Transform symptoms into binary features using MultiLabelBinarizer
mlb = MultiLabelBinarizer(classes=SYMPTOM_LIST)
X = mlb.fit_transform(df['symptoms'])
y = df['disease']

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train a Random Forest model with optimized parameters
model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_scaled, y)

# Perform cross-validation with StratifiedKFold to ensure class balance
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)  # Reduced to 3 folds
scores = cross_val_score(model, X_scaled, y, cv=cv)
print(f"Cross-validation accuracy: {scores.mean():.2f} (+/- {scores.std() * 2:.2f})")

# Save the model, scaler, and mlb
joblib.dump(model, 'disease_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(mlb, 'mlb.pkl')

print("Model, scaler, and mlb saved successfully!")