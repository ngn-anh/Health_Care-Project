from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Bệnh nhân'),
        ('doctor', 'Bác sĩ'),
        ('nurse', 'Y tá'),
        ('admin', 'Quản trị viên'),
        ('pharmacist', 'Dược sĩ'),
        ('lab_tech', 'Kỹ thuật viên'),
        ('insurance', 'Bảo hiểm'),
    )
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name or self.username