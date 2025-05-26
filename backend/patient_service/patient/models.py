from mongoengine import Document, StringField

class Patient(Document):
    user = StringField(required=True, unique=True)
    medical_record_id = StringField(default="")