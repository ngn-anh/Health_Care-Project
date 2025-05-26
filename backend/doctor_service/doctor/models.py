from mongoengine import Document, StringField

class Doctor(Document):
    user = StringField(required=True, unique=True)
    specialty = StringField(default="")
    department = StringField(default="")