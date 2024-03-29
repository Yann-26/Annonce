from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
import re


# Create your views here.
def register(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            messages.error(request,
                           'Les deux mot de passe \
                            ne sont pas en conformité.'
                           )
            return redirect('register')
        if len(password) < 8:
            messages.error(request,
                           'Le mot de passe doit contenir\
                            au moins 8 caractères.'
                           )
            return redirect('register')
        if not re.search(r'[!@#$%^&*]', password):
            messages.error(request,
                           'Le mot de passe doit contenir  \
                            au moins un caractère spécial.'
                           )
            return redirect('register')
        if username.lower() in password.lower() or email.lower() in password.lower():
            messages.error(request,
                           'Le mot de passe ne doit pas être trop \
                            similaire à l\'username ou à l\'email.'
                           )
            return redirect('register')
        try:
            if User.objects.filter(username=username).first():
                messages.error(request, 'Username déjà utilisé!')
                return redirect('register')
            if User.objects.filter(email=email).first():
                messages.error(request, 'Email déjà utilisé!.')
                return redirect('register')
            user_obj = User(
                username=username,
                email=email,
            )
            user_obj.set_password(password)
            user_obj.save()
            return redirect('index')
        except Exception as e:
            print(e)
    return render(request, 'register.html') 


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                messages.error(request, 'Utilisateur introuvable!!!')
                return redirect('login')
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, 'Mot de passe érroné')
                return redirect('login')
            login(request, user)  
            return redirect('index')
        except Exception as e:
            print(e)
    return render(request, 'login.html')
    

def signout(request):
    logout(request)
    messages.success(request, 'Deconnexion reussite!!')
    return redirect('index')