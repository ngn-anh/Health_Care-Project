from django.urls import path
from .views import InsuranceContractListCreateView, InsuranceContractDetailView, InsuranceClaimListCreateView, InsuranceClaimDetailView

urlpatterns = [
    path('contracts/', InsuranceContractListCreateView.as_view(), name='insurance-contract-list'),
    path('contracts/<int:pk>/', InsuranceContractDetailView.as_view(), name='insurance-contract-detail'),
    path('claims/', InsuranceClaimListCreateView.as_view(), name='insurance-claim-list'),
    path('claims/<int:pk>/', InsuranceClaimDetailView.as_view(), name='insurance-claim-detail'),
]
