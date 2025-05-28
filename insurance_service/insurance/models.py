from django.db import models

# Lưu trữ hợp đồng bảo hiểm của bệnh nhân
class InsuranceContract(models.Model):
    patient_id = models.IntegerField()  # ID user từ user_service
    patient_name = models.CharField(max_length=100)
    insurance_number = models.CharField(max_length=50)
    provider = models.CharField(max_length=100)  # Tên công ty bảo hiểm
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)  # Đã xác minh hợp lệ
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.patient_name} - {self.insurance_number} ({self.provider})"


# Yêu cầu bồi thường bảo hiểm
class InsuranceClaim(models.Model):
    CLAIM_STATUS = (
        ("pending", "Chờ duyệt"),
        ("approved", "Đã duyệt"),
        ("rejected", "Từ chối"),
        ("paid", "Đã chi trả"),
    )
    contract = models.ForeignKey(InsuranceContract, on_delete=models.CASCADE, related_name="claims")
    invoice_id = models.IntegerField()  # ID hóa đơn từ InvoiceService
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=CLAIM_STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Claim {self.id} - {self.contract.patient_name} - {self.get_status_display()}"
