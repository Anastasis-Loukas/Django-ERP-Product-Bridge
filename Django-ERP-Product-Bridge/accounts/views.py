from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm


# Handles user authentication (login process)
def login_view(request):

    # Check if the form was submitted
    if request.method == 'POST':
        # Retrieve submitted credentials from POST data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user against Django's authentication backend
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in (creates session)
            login(request, user)
            return redirect('home')
        else:
            # Display error message if authentication fails
            messages.error(request, "Invalid credentials")

    # Render login page (GET request or failed POST)
    return render(request, 'accounts/login.html')


# Handles user registration (account creation)
def register_view(request):

    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        # Validate form data (password rules, unique username, etc.)
        if form.is_valid():
            form.save()  # Create new user in database
            return redirect("login")

    else:
        # Initialize empty registration form (GET request)
        form = CustomUserCreationForm()

    # Render registration page with form instance
    return render(request, "accounts/register.html", {"form": form})


# Home page – accessible only to authenticated users
@login_required(login_url='login')
def home_view(request):
    return render(request, 'accounts/home.html')


# Logs out authenticated user and clears session
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')