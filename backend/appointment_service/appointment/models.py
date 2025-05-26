from mongoengine import Document, StringField, DateTimeField
import datetime

class Appointment(Document):
    patient = StringField(required=True)  # Lưu ID bệnh nhân dưới dạng chuỗi
    doctor = StringField(required=True)   # Lưu ID bác sĩ dưới dạng chuỗi
    datetime = DateTimeField(default=datetime.datetime.utcnow)
    description = StringField()
    status = StringField(choices=["pending", "confirmed", "cancelled"], default="pending")
