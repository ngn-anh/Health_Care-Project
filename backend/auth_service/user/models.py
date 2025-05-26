from django.forms import DateField
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
    fullname = StringField()
    gender = StringField(choices=["male", "female", "other"])


