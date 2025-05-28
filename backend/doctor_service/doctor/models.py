import datetime
from mongoengine import Document, StringField,DateTimeField  

class Doctor(Document):
    user = StringField(required=True, unique=True)
    specialty = StringField(default="")
    department = StringField(default="")

class Diagnosis(Document):
    doctor_id = StringField(required=True)
    patient_id = StringField(required=True)
    symptoms = StringField()
    diagnosis = StringField()
    prescription = StringField()
    note = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)