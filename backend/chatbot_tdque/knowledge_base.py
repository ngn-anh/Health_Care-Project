# knowledge_base.py
import json
import os
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Disease:
    name: str
    description: str
    common_symptoms: List[str]
    severity: str  # "mild", "moderate", "severe"
    recommended_tests: List[str]
    treatments: List[str]
    prevention: List[str]
    when_to_see_doctor: str
    contagious: bool
    duration: str

@dataclass
class Symptom:
    name: str
    description: str
    severity_levels: List[str]
    common_causes: List[str]

class MedicalKnowledgeBase:
    def __init__(self):
        self.diseases = self._load_diseases_from_json()
        self.symptoms = self._load_symptoms_from_json()
        self.symptom_to_index = {symptom: idx for idx, symptom in enumerate(self.get_all_symptoms())}
    
    def _load_diseases_from_json(self) -> Dict[str, Disease]:
        """Load diseases from JSON file, fallback to hardcoded data if file not found"""
        try:
            json_path = os.path.join(os.path.dirname(__file__), 'diseases_data.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            diseases = {}
            for key, disease_data in data['diseases'].items():
                diseases[key] = Disease(
                    name=disease_data['name'],
                    description=disease_data['description'],
                    common_symptoms=disease_data['common_symptoms'],
                    severity=disease_data['severity'],
                    recommended_tests=disease_data['recommended_tests'],
                    treatments=disease_data['treatments'],
                    prevention=disease_data['prevention'],
                    when_to_see_doctor=disease_data['when_to_see_doctor'],
                    contagious=disease_data['contagious'],
                    duration=disease_data['duration']
                )
            
            print(f"✅ Loaded {len(diseases)} diseases from JSON file")
            return diseases
            
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ Could not load diseases from JSON ({e}), using hardcoded data")
            return self._initialize_diseases()
    
    def _load_symptoms_from_json(self) -> Dict[str, Symptom]:
        """Load symptoms from JSON file, fallback to hardcoded data if file not found"""
        try:
            json_path = os.path.join(os.path.dirname(__file__), 'symptoms_data.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            symptoms = {}
            for key, symptom_data in data['symptoms'].items():
                symptoms[key] = Symptom(
                    name=symptom_data['name'],
                    description=symptom_data['description'],
                    severity_levels=symptom_data['severity_levels'],
                    common_causes=symptom_data['common_causes']
                )
            
            print(f"✅ Loaded {len(symptoms)} symptoms from JSON file")
            return symptoms
            
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ Could not load symptoms from JSON ({e}), using hardcoded data")
            return self._initialize_symptoms()
        
    def _initialize_diseases(self) -> Dict[str, Disease]:
        return {
            "Common_Cold": Disease(
                name="Common Cold",
                description="A viral infection of the upper respiratory tract",
                common_symptoms=["Runny Nose", "Sneezing", "Cough", "Sore Throat", "Mild Fatigue"],
                severity="mild",
                recommended_tests=["Clinical examination", "Throat swab if severe"],
                treatments=["Rest", "Fluids", "Paracetamol", "Throat lozenges"],
                prevention=["Hand washing", "Avoid close contact", "Healthy diet"],
                when_to_see_doctor="If symptoms persist >10 days or worsen",
                contagious=True,
                duration="7-10 days"
            ),
            "Influenza": Disease(
                name="Influenza (Flu)",
                description="A viral infection affecting the respiratory system",
                common_symptoms=["Fever", "Cough", "Body Aches", "Fatigue", "Headache", "Chills"],
                severity="moderate",
                recommended_tests=["Rapid flu test", "RT-PCR", "Throat swab"],
                treatments=["Oseltamivir (Tamiflu)", "Rest", "Fluids", "Paracetamol"],
                prevention=["Annual flu vaccine", "Hand hygiene", "Avoid crowds"],
                when_to_see_doctor="High fever >39°C, difficulty breathing",
                contagious=True,
                duration="5-7 days"
            ),
            "COVID19": Disease(
                name="COVID-19",
                description="Disease caused by SARS-CoV-2 coronavirus",
                common_symptoms=["Fever", "Cough", "Loss of Taste", "Loss of Smell", "Fatigue", "Shortness of Breath"],
                severity="moderate",
                recommended_tests=["RT-PCR test", "Rapid antigen test", "Chest X-ray"],
                treatments=["Isolation", "Paracetamol", "Rest", "Monitor oxygen levels"],
                prevention=["Vaccination", "Mask wearing", "Social distancing", "Hand hygiene"],
                when_to_see_doctor="Difficulty breathing, chest pain, oxygen <95%",
                contagious=True,
                duration="10-14 days"
            ),
            "Allergic_Rhinitis": Disease(
                name="Allergic Rhinitis",
                description="Allergic reaction causing nasal inflammation",
                common_symptoms=["Runny Nose", "Sneezing", "Itchy Eyes", "Nasal Congestion", "Watery Eyes"],
                severity="mild",
                recommended_tests=["Allergy skin test", "IgE blood test", "Nasal endoscopy"],
                treatments=["Antihistamines", "Nasal corticosteroids", "Avoid allergens"],
                prevention=["Identify and avoid triggers", "Air purifiers", "Regular cleaning"],
                when_to_see_doctor="Severe symptoms affecting daily life",
                contagious=False,
                duration="Seasonal or chronic"
            ),
            "Bronchitis": Disease(
                name="Bronchitis",
                description="Inflammation of the bronchial tubes",
                common_symptoms=["Persistent Cough", "Mucus Production", "Fatigue", "Shortness of Breath", "Chest Discomfort"],
                severity="moderate",
                recommended_tests=["Chest X-ray", "Sputum test", "Pulmonary function test"],
                treatments=["Bronchodilators", "Cough suppressants", "Antibiotics if bacterial"],
                prevention=["Avoid smoking", "Hand hygiene", "Avoid air pollution"],
                when_to_see_doctor="Cough with blood, high fever, breathing difficulty",
                contagious=False,
                duration="2-3 weeks"
            ),
            "Pneumonia": Disease(
                name="Pneumonia",
                description="Infection causing inflammation in lung air sacs",
                common_symptoms=["High Fever", "Persistent Cough", "Shortness of Breath", "Chest Pain", "Fatigue", "Chills"],
                severity="severe",
                recommended_tests=["Chest X-ray", "Blood tests", "Sputum culture", "CT scan"],
                treatments=["Antibiotics", "Rest", "Oxygen therapy", "Hospitalization if severe"],
                prevention=["Pneumonia vaccine", "Hand hygiene", "Healthy lifestyle"],
                when_to_see_doctor="Immediate medical attention required",
                contagious=True,
                duration="1-3 weeks with treatment"
            ),
            "Asthma": Disease(
                name="Asthma",
                description="Chronic respiratory condition with airway inflammation",
                common_symptoms=["Wheezing", "Shortness of Breath", "Chest Tightness", "Persistent Cough"],
                severity="moderate",
                recommended_tests=["Spirometry", "Peak flow test", "Chest X-ray", "Allergy tests"],
                treatments=["Inhaled corticosteroids", "Bronchodilators", "Avoid triggers"],
                prevention=["Identify triggers", "Take medications as prescribed", "Regular monitoring"],
                when_to_see_doctor="Severe breathing difficulty, blue lips/face",
                contagious=False,
                duration="Chronic condition"
            ),
            "Sinusitis": Disease(
                name="Sinusitis",
                description="Inflammation of the sinuses",
                common_symptoms=["Facial Pain", "Nasal Congestion", "Thick Nasal Discharge", "Headache", "Loss of Smell"],
                severity="mild",
                recommended_tests=["Clinical examination", "CT scan", "Nasal endoscopy"],
                treatments=["Nasal decongestants", "Saline rinses", "Antibiotics if bacterial"],
                prevention=["Humidify air", "Avoid allergens", "Hand hygiene"],
                when_to_see_doctor="Symptoms persist >10 days, severe headache",
                contagious=False,
                duration="1-2 weeks"
            ),
            "Migraine": Disease(
                name="Migraine",
                description="Neurological condition causing severe headaches",
                common_symptoms=["Severe Headache", "Nausea", "Light Sensitivity", "Sound Sensitivity", "Vomiting"],
                severity="moderate",
                recommended_tests=["Neurological exam", "MRI", "CT scan", "Blood tests"],
                treatments=["Pain relievers", "Triptans", "Anti-nausea medications", "Preventive medications"],
                prevention=["Identify triggers", "Regular sleep", "Stress management", "Stay hydrated"],
                when_to_see_doctor="Sudden severe headache, neurological symptoms",
                contagious=False,
                duration="4-72 hours per episode"
            ),
            "Food_Poisoning": Disease(
                name="Food Poisoning",
                description="Illness from consuming contaminated food",
                common_symptoms=["Nausea", "Vomiting", "Diarrhea", "Abdominal Pain", "Fever", "Fatigue"],
                severity="mild",
                recommended_tests=["Stool culture", "Blood tests if severe"],
                treatments=["Fluids", "Electrolyte replacement", "Rest", "Bland diet"],
                prevention=["Food safety", "Proper cooking", "Hand hygiene", "Safe water"],
                when_to_see_doctor="Severe dehydration, high fever, blood in stool",
                contagious=False,
                duration="1-7 days"
            )
        }
    
    def _initialize_symptoms(self) -> Dict[str, Symptom]:
        return {
            "Fever": Symptom(
                name="Fever",
                description="Elevated body temperature above 37.5°C",
                severity_levels=["Low grade (37.5-38°C)", "Moderate (38-39°C)", "High (>39°C)"],
                common_causes=["Viral infections", "Bacterial infections", "Inflammatory conditions"]
            ),
            "Cough": Symptom(
                name="Cough",
                description="Forceful expulsion of air from lungs",
                severity_levels=["Dry cough", "Productive cough", "Persistent cough"],
                common_causes=["Respiratory infections", "Allergies", "Asthma", "GERD"]
            ),
            "Runny Nose": Symptom(
                name="Runny Nose",
                description="Excess nasal discharge",
                severity_levels=["Clear discharge", "Thick discharge", "Colored discharge"],
                common_causes=["Viral infections", "Allergies", "Sinusitis"]
            ),
            "Sneezing": Symptom(
                name="Sneezing",
                description="Involuntary expulsion of air through nose",
                severity_levels=["Occasional", "Frequent", "Severe fits"],
                common_causes=["Allergies", "Viral infections", "Irritants"]
            ),
            "Sore Throat": Symptom(
                name="Sore Throat",
                description="Pain or irritation in the throat",
                severity_levels=["Mild discomfort", "Moderate pain", "Severe pain"],
                common_causes=["Viral infections", "Bacterial infections", "Allergies"]
            ),
            "Fatigue": Symptom(
                name="Fatigue",
                description="Extreme tiredness or exhaustion",
                severity_levels=["Mild tiredness", "Moderate fatigue", "Severe exhaustion"],
                common_causes=["Infections", "Sleep disorders", "Chronic conditions"]
            ),
            "Headache": Symptom(
                name="Headache",
                description="Pain in the head or neck region",
                severity_levels=["Mild", "Moderate", "Severe"],
                common_causes=["Tension", "Migraine", "Sinusitis", "Dehydration"]
            ),
            "Body Aches": Symptom(
                name="Body Aches",
                description="Muscle and joint pain throughout body",
                severity_levels=["Mild aches", "Moderate pain", "Severe pain"],
                common_causes=["Viral infections", "Overexertion", "Inflammatory conditions"]
            ),
            "Chills": Symptom(
                name="Chills",
                description="Feeling cold with shivering",
                severity_levels=["Mild chills", "Moderate shivering", "Severe rigors"],
                common_causes=["Fever", "Infections", "Hypothermia"]
            ),
            "Loss of Taste": Symptom(
                name="Loss of Taste",
                description="Reduced or complete loss of taste sensation",
                severity_levels=["Partial loss", "Complete loss", "Distorted taste"],
                common_causes=["Viral infections", "Nasal congestion", "Medications"]
            ),
            "Loss of Smell": Symptom(
                name="Loss of Smell",
                description="Reduced or complete loss of smell",
                severity_levels=["Partial loss", "Complete loss", "Distorted smell"],
                common_causes=["Viral infections", "Nasal congestion", "Sinusitis"]
            ),
            "Shortness of Breath": Symptom(
                name="Shortness of Breath",
                description="Difficulty breathing or feeling breathless",
                severity_levels=["Mild exertion", "Moderate activity", "At rest"],
                common_causes=["Respiratory infections", "Asthma", "Heart conditions"]
            ),
            "Chest Pain": Symptom(
                name="Chest Pain",
                description="Pain or discomfort in chest area",
                severity_levels=["Mild discomfort", "Moderate pain", "Severe pain"],
                common_causes=["Respiratory infections", "Muscle strain", "Heart conditions"]
            ),
            "Itchy Eyes": Symptom(
                name="Itchy Eyes",
                description="Irritation and urge to rub eyes",
                severity_levels=["Mild irritation", "Moderate itching", "Severe discomfort"],
                common_causes=["Allergies", "Dry eyes", "Infections"]
            ),
            "Watery Eyes": Symptom(
                name="Watery Eyes",
                description="Excessive tear production",
                severity_levels=["Mild tearing", "Moderate watering", "Severe tearing"],
                common_causes=["Allergies", "Infections", "Irritants"]
            ),
            "Nasal Congestion": Symptom(
                name="Nasal Congestion",
                description="Blocked or stuffy nose",
                severity_levels=["Mild stuffiness", "Moderate blockage", "Complete blockage"],
                common_causes=["Infections", "Allergies", "Sinusitis"]
            ),
            "Nausea": Symptom(
                name="Nausea",
                description="Feeling of sickness with urge to vomit",
                severity_levels=["Mild queasiness", "Moderate nausea", "Severe nausea"],
                common_causes=["Infections", "Food poisoning", "Medications"]
            ),
            "Vomiting": Symptom(
                name="Vomiting",
                description="Forceful emptying of stomach contents",
                severity_levels=["Occasional", "Frequent", "Persistent"],
                common_causes=["Infections", "Food poisoning", "Migraines"]
            ),
            "Diarrhea": Symptom(
                name="Diarrhea",
                description="Loose or watery bowel movements",
                severity_levels=["Mild", "Moderate", "Severe with dehydration"],
                common_causes=["Infections", "Food poisoning", "Medications"]
            ),
            "Abdominal Pain": Symptom(
                name="Abdominal Pain",
                description="Pain in the stomach or belly area",
                severity_levels=["Mild discomfort", "Moderate pain", "Severe cramping"],
                common_causes=["Infections", "Food issues", "Inflammatory conditions"]
            ),
            "Wheezing": Symptom(
                name="Wheezing",
                description="High-pitched whistling sound when breathing",
                severity_levels=["Mild wheeze", "Audible wheeze", "Severe wheeze"],
                common_causes=["Asthma", "Allergies", "Respiratory infections"]
            ),
            "Chest Tightness": Symptom(
                name="Chest Tightness",
                description="Feeling of pressure or constriction in chest",
                severity_levels=["Mild tightness", "Moderate pressure", "Severe constriction"],
                common_causes=["Asthma", "Anxiety", "Respiratory infections"]
            ),
            "Facial Pain": Symptom(
                name="Facial Pain",
                description="Pain in face, particularly around sinuses",
                severity_levels=["Mild discomfort", "Moderate pain", "Severe pressure"],
                common_causes=["Sinusitis", "Dental issues", "Nerve problems"]
            ),
            "Thick Nasal Discharge": Symptom(
                name="Thick Nasal Discharge",
                description="Thick, colored mucus from nose",
                severity_levels=["Slight thickness", "Moderately thick", "Very thick/colored"],
                common_causes=["Bacterial infections", "Sinusitis", "Chronic conditions"]
            ),
            "Light Sensitivity": Symptom(
                name="Light Sensitivity",
                description="Discomfort or pain from light exposure",
                severity_levels=["Mild sensitivity", "Moderate discomfort", "Severe photophobia"],
                common_causes=["Migraines", "Eye infections", "Neurological conditions"]
            ),
            "Sound Sensitivity": Symptom(
                name="Sound Sensitivity",
                description="Discomfort from normal sound levels",
                severity_levels=["Mild sensitivity", "Moderate discomfort", "Severe phonophobia"],
                common_causes=["Migraines", "Ear infections", "Neurological conditions"]
            ),
            "Mucus Production": Symptom(
                name="Mucus Production",
                description="Excessive production of respiratory mucus",
                severity_levels=["Small amounts", "Moderate production", "Excessive mucus"],
                common_causes=["Respiratory infections", "Chronic bronchitis", "Allergies"]
            ),
            "Chest Discomfort": Symptom(
                name="Chest Discomfort",
                description="General uneasiness or mild pain in chest",
                severity_levels=["Mild discomfort", "Moderate uneasiness", "Significant discomfort"],
                common_causes=["Respiratory infections", "Muscle strain", "Acid reflux"]
            ),
            "High Fever": Symptom(
                name="High Fever",
                description="Body temperature above 39°C (102.2°F)",
                severity_levels=["39-40°C", "40-41°C", ">41°C (emergency)"],
                common_causes=["Severe infections", "Pneumonia", "Sepsis"]
            ),
            "Persistent Cough": Symptom(
                name="Persistent Cough",
                description="Cough lasting more than 3 weeks",
                severity_levels=["3-8 weeks", "8+ weeks chronic", "Severe persistent"],
                common_causes=["Post-viral", "Asthma", "Chronic conditions"]
            )
        }
    
    def get_all_symptoms(self) -> List[str]:
        """Get list of all available symptoms"""
        return list(self.symptoms.keys())
    
    def get_all_diseases(self) -> List[str]:
        """Get list of all diseases"""
        return list(self.diseases.keys())
    
    def get_disease_info(self, disease_name: str) -> Disease:
        """Get detailed information about a specific disease"""
        return self.diseases.get(disease_name)
    
    def get_symptom_info(self, symptom_name: str) -> Symptom:
        """Get detailed information about a specific symptom"""
        return self.symptoms.get(symptom_name)
    
    def search_diseases_by_symptoms(self, symptoms: List[str]) -> Dict[str, float]:
        """Search diseases based on symptoms and return similarity scores"""
        scores = {}
        for disease_name, disease in self.diseases.items():
            common_symptoms = set(disease.common_symptoms)
            symptom_set = set(symptoms)
            
            # Calculate Jaccard similarity
            intersection = len(common_symptoms.intersection(symptom_set))
            union = len(common_symptoms.union(symptom_set))
            similarity = intersection / union if union > 0 else 0
            
            scores[disease_name] = similarity
        
        return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
    
    def save_to_json(self, diseases_file='diseases_data.json', symptoms_file='symptoms_data.json'):
        """Save current knowledge base to JSON files"""
        try:
            # Save diseases
            diseases_data = {
                "diseases": {}
            }
            
            for key, disease in self.diseases.items():
                diseases_data["diseases"][key] = {
                    "name": disease.name,
                    "description": disease.description,
                    "common_symptoms": disease.common_symptoms,
                    "severity": disease.severity,
                    "recommended_tests": disease.recommended_tests,
                    "treatments": disease.treatments,
                    "prevention": disease.prevention,
                    "when_to_see_doctor": disease.when_to_see_doctor,
                    "contagious": disease.contagious,
                    "duration": disease.duration
                }
            
            with open(diseases_file, 'w', encoding='utf-8') as f:
                json.dump(diseases_data, f, indent=2, ensure_ascii=False)
            
            # Save symptoms
            symptoms_data = {
                "symptoms": {}
            }
            
            for key, symptom in self.symptoms.items():
                symptoms_data["symptoms"][key] = {
                    "name": symptom.name,
                    "description": symptom.description,
                    "severity_levels": symptom.severity_levels,
                    "common_causes": symptom.common_causes
                }
            
            with open(symptoms_file, 'w', encoding='utf-8') as f:
                json.dump(symptoms_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Knowledge base saved to {diseases_file} and {symptoms_file}")
            
        except Exception as e:
            print(f"❌ Error saving knowledge base to JSON: {e}")
    
    def add_disease(self, key: str, disease: Disease):
        """Add a new disease to the knowledge base"""
        self.diseases[key] = disease
        print(f"✅ Added disease: {disease.name}")
    
    def add_symptom(self, key: str, symptom: Symptom):
        """Add a new symptom to the knowledge base"""
        self.symptoms[key] = symptom
        self.symptom_to_index = {symptom: idx for idx, symptom in enumerate(self.get_all_symptoms())}
        print(f"✅ Added symptom: {symptom.name}")
    
    def remove_disease(self, key: str):
        """Remove a disease from the knowledge base"""
        if key in self.diseases:
            disease_name = self.diseases[key].name
            del self.diseases[key]
            print(f"✅ Removed disease: {disease_name}")
        else:
            print(f"❌ Disease '{key}' not found")
    
    def remove_symptom(self, key: str):
        """Remove a symptom from the knowledge base"""
        if key in self.symptoms:
            symptom_name = self.symptoms[key].name
            del self.symptoms[key]
            self.symptom_to_index = {symptom: idx for idx, symptom in enumerate(self.get_all_symptoms())}
            print(f"✅ Removed symptom: {symptom_name}")
        else:
            print(f"❌ Symptom '{key}' not found") 