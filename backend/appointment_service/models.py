from django.db import models

# Create your models here.
from mongoengine import Document, ReferenceField, StringField, DateTimeField
from auth_service.models import Doctor, User, Patient
import datetime

class Appointment(Document):
    patient = ReferenceField(Patient, required=True)
    doctor = ReferenceField(Doctor, required=True)
    datetime = DateTimeField(default=datetime.datetime.utcnow)
    description = StringField()
    status = StringField(choices=["pending", "confirmed", "cancelled"], default="pending")