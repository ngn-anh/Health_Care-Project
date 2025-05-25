from django.urls import path
from .views import CustomLoginView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", CustomLoginView.as_view()),  # ✅ thay TokenObtainPairView
]
