from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, ServiceForm, ServiceUpdateForm
from .models import Service
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
        else:
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username_or_email, password=password)
        if user is None:
            try:
                user = User.objects.get(email=username_or_email)
                user = authenticate(username=user.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username/email or password.')

    form = AuthenticationForm()
    return render(request, 'sign_in.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('home')

@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.ads_author = request.user
            service.save()
            messages.success(request, 'Service added successfully.')
            return redirect('available_services')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm()
    return render(request, 'add_service.html', {'form': form})

def available_services(request):
    occupation = request.GET.get('occupation')
    if occupation:
        services = Service.objects.filter(occupation=occupation)
    else:
        services = Service.objects.all()
    occupations = Service.objects.values_list('occupation', flat=True).distinct()
    return render(request, 'available_services.html', {'services': services, 'occupations': occupations})

@login_required
def update_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceUpdateForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('available_services')
    else:
        form = ServiceUpdateForm(instance=service)
    return render(request, 'edit_service.html', {'form': form})

@login_required
def remove_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, ads_author=request.user)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service removed successfully.')
        return redirect('available_services')
    return render(request, 'remove_service.html', {'service': service})