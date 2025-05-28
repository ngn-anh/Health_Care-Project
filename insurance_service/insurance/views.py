from rest_framework import generics, permissions
from .models import InsuranceContract, InsuranceClaim
from .serializers import InsuranceContractSerializer, InsuranceClaimSerializer

# Quản lý hợp đồng bảo hiểm
class InsuranceContractListCreateView(generics.ListCreateAPIView):
    queryset = InsuranceContract.objects.all()
    serializer_class = InsuranceContractSerializer
    permission_classes = [permissions.IsAdminUser]

class InsuranceContractDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InsuranceContract.objects.all()
    serializer_class = InsuranceContractSerializer
    permission_classes = [permissions.IsAdminUser]

# Quản lý yêu cầu bồi thường bảo hiểm
class InsuranceClaimListCreateView(generics.ListCreateAPIView):
    queryset = InsuranceClaim.objects.all().order_by('-created_at')
    serializer_class = InsuranceClaimSerializer
    permission_classes = [permissions.IsAdminUser]

class InsuranceClaimDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InsuranceClaim.objects.all()
    serializer_class = InsuranceClaimSerializer
    permission_classes = [permissions.IsAdminUser]
