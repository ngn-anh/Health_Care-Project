# improved_model.py
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import json
from knowledge_base import MedicalKnowledgeBase

class ImprovedHealthPredictor:
    def __init__(self):
        self.kb = MedicalKnowledgeBase()
        self.symptoms = self.kb.get_all_symptoms()
        self.diseases = self.kb.get_all_diseases()
        self.scaler = StandardScaler()
        self.model = None
        self.symptom_to_index = {symptom: idx for idx, symptom in enumerate(self.symptoms)}
        self.disease_to_index = {disease: idx for idx, disease in enumerate(self.diseases)}
        self.index_to_disease = {idx: disease for disease, idx in self.disease_to_index.items()}
        
    def _generate_training_data(self):
        """Generate comprehensive training data based on knowledge base"""
        X, y = [], []
        
        # Generate multiple samples for each disease with variations
        for disease_name, disease in self.kb.diseases.items():
            disease_idx = self.disease_to_index[disease_name]
            
            # Create base symptom vector for this disease
            base_symptoms = disease.common_symptoms
            
            # Generate multiple variations of symptom combinations  
            samples_per_disease = 100  # Increase samples
            for _ in range(samples_per_disease):
                symptom_vector = np.zeros(len(self.symptoms))
                
                # Always include some core symptoms
                core_symptom_count = min(len(base_symptoms), np.random.randint(2, len(base_symptoms) + 1))
                selected_core = np.random.choice(base_symptoms, core_symptom_count, replace=False)
                
                for symptom in selected_core:
                    if symptom in self.symptom_to_index:
                        symptom_vector[self.symptom_to_index[symptom]] = 1
                
                # Randomly add some noise (other symptoms with low probability)
                for i, symptom in enumerate(self.symptoms):
                    if symptom not in selected_core and np.random.random() < 0.1:
                        symptom_vector[i] = 1
                
                # Add some intensity variation (0.5 to 1.0 for present symptoms)
                for i in range(len(symptom_vector)):
                    if symptom_vector[i] == 1:
                        symptom_vector[i] = np.random.uniform(0.6, 1.0)
                
                X.append(symptom_vector)
                y.append(disease_idx)
        
        # Add negative samples (random symptom combinations not matching any disease)
        for _ in range(100):
            symptom_vector = np.random.randint(0, 2, len(self.symptoms)) * np.random.uniform(0.3, 1.0, len(self.symptoms))
            # Make sure it doesn't strongly match any known disease
            if not self._matches_known_disease(symptom_vector):
                X.append(symptom_vector)
                y.append(-1)  # Unknown disease class
        
        return np.array(X, dtype=np.float32), np.array(y)
    
    def _matches_known_disease(self, symptom_vector, threshold=0.5):
        """Check if symptom vector strongly matches any known disease"""
        for disease_name, disease in self.kb.diseases.items():
            symptom_names = [self.symptoms[i] for i, val in enumerate(symptom_vector) if val > 0.5]
            common_symptoms = set(disease.common_symptoms)
            symptom_set = set(symptom_names)
            
            if len(common_symptoms.intersection(symptom_set)) / len(common_symptoms) > threshold:
                return True
        return False
    
    def build_model(self):
        """Build an improved neural network model"""
        inputs = tf.keras.Input(shape=(len(self.symptoms),), name='symptoms')
        
        # Feature extraction layers
        x = tf.keras.layers.Dense(128, activation='relu', name='dense1')(inputs)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.3)(x)
        
        x = tf.keras.layers.Dense(64, activation='relu', name='dense2')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.3)(x)
        
        x = tf.keras.layers.Dense(32, activation='relu', name='dense3')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        
        # Output layer (including unknown disease class)
        outputs = tf.keras.layers.Dense(len(self.diseases) + 1, activation='softmax', name='predictions')(x)
        
        model = tf.keras.Model(inputs, outputs)
        
        # Use a more sophisticated optimizer
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        model.compile(
            optimizer=optimizer,
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_model(self, epochs=200, validation_split=0.2):
        """Train the model with improved data and validation"""
        print("🔬 Generating training data...")
        X, y = self._generate_training_data()
        
        # Handle unknown disease class
        y[y == -1] = len(self.diseases)  # Unknown class gets highest index
        
        print(f"📊 Training data: {X.shape[0]} samples, {X.shape[1]} features")
        print(f"🎯 Classes: {len(np.unique(y))}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Build model
        self.model = self.build_model()
        
        # Callbacks for better training
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss', patience=20, restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss', factor=0.5, patience=10, min_lr=1e-6
            )
        ]
        
        print("🚀 Training model...")
        history = self.model.fit(
            X_train_scaled, y_train,
            epochs=epochs,
            batch_size=32,
            validation_split=validation_split,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate model
        print("\n📈 Evaluating model...")
        test_loss, test_acc = self.model.evaluate(X_test_scaled, y_test, verbose=0)
        print(f"Test Accuracy: {test_acc:.4f}")
        print(f"Test Loss: {test_loss:.4f}")
        
        # Classification report
        y_pred = np.argmax(self.model.predict(X_test_scaled), axis=1)
        class_names = self.diseases + ["Unknown"]
        print("\n📊 Classification Report:")
        print(classification_report(y_test, y_pred, target_names=class_names))
        
        return history
    
    def predict_with_uncertainty(self, symptoms, n_iter=100):
        """Make predictions with uncertainty estimation using Monte Carlo Dropout"""
        if isinstance(symptoms, list):
            # Convert symptom names to vector
            symptom_vector = np.zeros(len(self.symptoms))
            for symptom in symptoms:
                if symptom in self.symptom_to_index:
                    symptom_vector[self.symptom_to_index[symptom]] = 1.0
        else:
            symptom_vector = symptoms
        
        # Scale input
        symptom_vector = symptom_vector.reshape(1, -1)
        symptom_vector_scaled = self.scaler.transform(symptom_vector)
        
        # Monte Carlo predictions
        predictions = []
        for _ in range(n_iter):
            pred = self.model(symptom_vector_scaled, training=True)
            predictions.append(pred.numpy())
        
        predictions = np.array(predictions)
        mean_pred = np.mean(predictions, axis=0)
        std_pred = np.std(predictions, axis=0)
        
        return mean_pred[0], std_pred[0]
    
    def predict_with_knowledge_fusion(self, symptoms):
        """Combine ML prediction with knowledge base search"""
        # Get ML prediction
        ml_mean, ml_std = self.predict_with_uncertainty(symptoms)
        
        # Get knowledge base similarity scores
        kb_scores = self.kb.search_diseases_by_symptoms(symptoms)
        
        # Combine predictions (weighted average)
        ml_weight = 0.7
        kb_weight = 0.3
        
        combined_scores = {}
        for disease in self.diseases:
            ml_idx = self.disease_to_index[disease]
            ml_score = ml_mean[ml_idx]
            kb_score = kb_scores.get(disease, 0.0)
            
            combined_score = ml_weight * ml_score + kb_weight * kb_score
            uncertainty = ml_std[ml_idx]
            
            combined_scores[disease] = {
                'score': combined_score,
                'uncertainty': uncertainty,
                'ml_score': ml_score,
                'kb_score': kb_score
            }
        
        # Sort by combined score
        sorted_diseases = sorted(combined_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        return sorted_diseases
    
    def get_detailed_prediction(self, symptoms):
        """Get comprehensive prediction with recommendations"""
        # Get predictions
        predictions = self.predict_with_knowledge_fusion(symptoms)
        top_disease = predictions[0]
        disease_name = top_disease[0]
        scores = top_disease[1]
        
        # Get disease information
        disease_info = self.kb.get_disease_info(disease_name)
        
        # Confidence assessment
        confidence = scores['score']
        uncertainty = scores['uncertainty']
        
        if confidence > 0.7:
            confidence_level = "High"
        elif confidence > 0.4:
            confidence_level = "Moderate"
        else:
            confidence_level = "Low"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(disease_info, confidence_level, symptoms)
        
        return {
            'primary_diagnosis': disease_name,
            'confidence': confidence,
            'confidence_level': confidence_level,
            'uncertainty': uncertainty,
            'disease_info': disease_info,
            'all_predictions': predictions[:3],  # Top 3
            'recommendations': recommendations,
            'input_symptoms': symptoms
        }
    
    def _generate_recommendations(self, disease_info, confidence_level, symptoms):
        """Generate personalized recommendations"""
        recommendations = {
            'immediate_actions': [],
            'tests': disease_info.recommended_tests if disease_info else [],
            'treatments': disease_info.treatments if disease_info else [],
            'when_to_see_doctor': disease_info.when_to_see_doctor if disease_info else "Consult a healthcare provider",
            'prevention': disease_info.prevention if disease_info else []
        }
        
        # Immediate actions based on confidence and severity
        if confidence_level == "Low":
            recommendations['immediate_actions'].extend([
                "Monitor symptoms closely",
                "Consider consulting a healthcare provider for proper diagnosis",
                "Keep a symptom diary"
            ])
        elif disease_info and disease_info.severity == "severe":
            recommendations['immediate_actions'].extend([
                "Seek immediate medical attention",
                "Do not delay treatment",
                "Monitor vital signs"
            ])
        else:
            recommendations['immediate_actions'].extend([
                "Rest and stay hydrated",
                "Monitor symptom progression",
                "Follow general health guidelines"
            ])
        
        # Check for emergency symptoms
        emergency_symptoms = ["Shortness of Breath", "Chest Pain", "High Fever", "Severe Headache"]
        if any(symptom in symptoms for symptom in emergency_symptoms):
            recommendations['immediate_actions'].insert(0, "⚠️ SEEK IMMEDIATE MEDICAL ATTENTION")
        
        return recommendations
    
    def save_model(self, filepath):
        """Save the trained model and associated data"""
        if self.model:
            self.model.save(f"{filepath}_model.keras")
            
            # Save scaler and mappings
            with open(f"{filepath}_data.pkl", 'wb') as f:
                pickle.dump({
                    'scaler': self.scaler,
                    'symptom_to_index': self.symptom_to_index,
                    'disease_to_index': self.disease_to_index,
                    'index_to_disease': self.index_to_disease,
                    'symptoms': self.symptoms,
                    'diseases': self.diseases
                }, f)
            
            print(f"✅ Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a pre-trained model"""
        try:
            self.model = tf.keras.models.load_model(f"{filepath}_model.keras")
            
            with open(f"{filepath}_data.pkl", 'rb') as f:
                data = pickle.load(f)
                self.scaler = data['scaler']
                self.symptom_to_index = data['symptom_to_index']
                self.disease_to_index = data['disease_to_index']
                self.index_to_disease = data['index_to_disease']
                self.symptoms = data['symptoms']
                self.diseases = data['diseases']
            
            print(f"✅ Model loaded from {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False

if __name__ == "__main__":
    # Train and save the improved model
    predictor = ImprovedHealthPredictor()
    
    print("🤖 Training Improved Health Prediction Model")
    print("=" * 50)
    
    # Train model
    history = predictor.train_model(epochs=100)
    
    # Save model
    predictor.save_model("improved_health_model")
    
    # Test prediction
    print("\n🧪 Testing prediction...")
    test_symptoms = ["Fever", "Cough", "Fatigue"]
    result = predictor.get_detailed_prediction(test_symptoms)
    
    print(f"\nTest symptoms: {test_symptoms}")
    print(f"Primary diagnosis: {result['primary_diagnosis']}")
    print(f"Confidence: {result['confidence']:.3f} ({result['confidence_level']})")
    print("=" * 50) 