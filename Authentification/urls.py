from django.urls import path
from . import views

urlpatterns = [
    path('Register/', views.register, name="register"),
    path('Signin/', views.signin, name="signin"),
    path('Signout/', views.signout, name="signout"),
]