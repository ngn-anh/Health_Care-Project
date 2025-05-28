from django.db import models

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Chờ xử lý'),
        ('completed', 'Đã thanh toán'),
        ('failed', 'Thất bại'),
        ('refunded', 'Đã hoàn tiền'),
    )
    user_id = models.IntegerField()  # ID user từ user_service
    user_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=50)  # Ví dụ: 'Chuyển khoản', 'Tiền mặt', 'Bảo hiểm'
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user_name} - {self.amount} ({self.get_status_display()})"