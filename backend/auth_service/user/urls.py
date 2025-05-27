from django.urls import path
from .views import CustomLoginView, RegisterView, UserDetailView, UserUpdateView, login_view, register_view

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", CustomLoginView.as_view()),  # ✅ thay TokenObtainPairView
    path('users/<str:id>', UserDetailView.as_view()),
    path('users/update/<str:id>', UserUpdateView.as_view()),
    path("login_view/", login_view, name="login_view"),
    path("register_view/", register_view, name="register_view"),
]
