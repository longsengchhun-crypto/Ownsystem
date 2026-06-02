from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ClientRegistrationForm, UserLoginForm, ClientProfileForm
from notifications.utils import notify_admin

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
        
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Vanguard Creative, {user.first_name}! Your account has been created.")
            
            # Send notification to admins
            notify_admin(
                title="New Client Account Created",
                message=f"Client {user.username} ({user.get_full_name()}) has registered.\nEmail: {user.email}"
            )
            
            return redirect('dashboard:home')
    else:
        form = ClientRegistrationForm()
        
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
        
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Logged in as {user.username}.")
                return redirect('dashboard:home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
        
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('website:home')

@login_required
def profile_view(request):
    from .models import ClientProfile
    profile, created = ClientProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile details have been successfully updated.")
            return redirect('accounts:profile')
    else:
        form = ClientProfileForm(instance=profile)
        
    return render(request, 'accounts/profile.html', {'form': form})
