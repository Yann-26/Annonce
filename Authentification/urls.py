from django.urls import path
from . import views

urlpatterns = [
    path('Register/', views.register, name="register"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
]