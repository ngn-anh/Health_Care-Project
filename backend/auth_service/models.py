from mongoengine import Document, StringField, EmailField, ReferenceField

class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(required=True, choices=[
        ("patient", "Patient"),
        ("doctor", "Doctor"),
        ("nurse", "Nurse"),
        ("admin", "Administrator"),
        ("pharmacist", "Pharmacist"),
        ("insurance", "Insurance Provider"),
        ("lab", "Lab Technician"),
    ])
    phone = StringField()
    address = StringField()

class Doctor(Document):
    user = StringField(required=True, unique=True)
    specialty = StringField(default="")
    department = StringField(default="")

class Patient(Document):
    user = StringField(required=True, unique=True)
    medical_record_id = StringField(default="")