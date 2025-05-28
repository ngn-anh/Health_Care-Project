from django.db import models

class Pharmacist(models.Model):
    user_id = models.CharField(max_length=100, unique=True)  # Liên kết với User từ auth_service
    license_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.license_number

class Medication(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    patient_id = models.CharField(max_length=100)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity_requested = models.IntegerField()
    status = models.CharField(max_length=20, choices=[("pending", "pending"), ("verified", "verified"), ("dispensed", "dispensed")], default="pending")
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.patient_id} - {self.medication.name}"