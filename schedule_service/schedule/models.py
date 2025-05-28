from django.db import models

class Schedule(models.Model):
    STAFF_ROLE_CHOICES = (
        ('doctor', 'Bác sĩ'),
        ('nurse', 'Y tá'),
    )
    staff_id = models.IntegerField()  # ID của user bên user_service
    staff_name = models.CharField(max_length=100)  # Lưu tên để hiển thị nhanh
    role = models.CharField(max_length=10, choices=STAFF_ROLE_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.get_role_display()} {self.staff_name} - {self.date} ({self.start_time}-{self.end_time})"