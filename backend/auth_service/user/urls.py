from django.urls import path
from .views import CustomLoginView, RegisterView, UserDetailView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", CustomLoginView.as_view()),  # ✅ thay TokenObtainPairView
    path('users/<str:id>/', UserDetailView.as_view()),
]
