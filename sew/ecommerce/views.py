from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import logout
from django.contrib import messages

def login_view(request):
    login_img = get_object_or_404(Master, name="login_img")
    
    if request.method == "POST":
        email = request.POST.get("email")  # Get email from the form
        password = request.POST.get("password")  # Get password from the form
        
        # Authenticate using email by checking the email and password manually
        try:
            user = User.objects.get(email=email)  # Get user by email
            if user.check_password(password):  # Check if the password is correct
                login(request, user)  # Django session-based login

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response = redirect("home")  # Redirect to home after login
                response.set_cookie("access_token", access_token, httponly=True, samesite="Lax")
                response.set_cookie("refresh_token", str(refresh), httponly=True, samesite="Lax")
                
                return response
            else:
                return render(request, "login.html", {"error": "Invalid credentials", "login_img": login_img})
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid credentials", "login_img": login_img})

    return render(request, "login.html", {"login_img": login_img})

def logout_view(request):
    logout(request)     # Clear session
    response = redirect("login")  # Redirect to login page
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

@login_required
def home_view(request):
    return render(request, "home.html", {"user": request.user})



def signup_view(request):
    login_img = get_object_or_404(Master, name="login_img")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "signup.html")

        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return render(request, "signup.html")
        
        # Create new user
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save() # Log the user in after successful registration
            return redirect("login")  # Redirect to home page after successful sign-up
        except Exception as e:
            messages.error(request, str(e))
            return render(request, "signup.html",{"login_img": login_img})
    
    return render(request, "signup.html",{"login_img": login_img})
