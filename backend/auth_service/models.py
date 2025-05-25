from mongoengine import Document, StringField, EmailField

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
