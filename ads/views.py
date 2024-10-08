from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, ServiceForm, ServiceUpdateForm
from .models import Service
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.exceptions import SuspiciousOperation, PermissionDenied
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
            return redirect('operations')
        else:
            messages.error(request, 'Invalid username/email or password.')
    else:
        # Check if redirected due to an expired session
        if not request.user.is_authenticated and request.session.get('has_expired'):
            messages.warning(request, 'Your session has expired. Please log in again.')
            request.session['has_expired'] = False  # Clear the flag

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

from django.core.paginator import Paginator

from django.db.models import Q

def available_services(request):
    occupation = request.GET.get('occupation')
    query = request.GET.get('q')  # Get the search query from the form input
    
    # Apply filtering based on search query and occupation
    services = Service.objects.all()
    
    if occupation:
        services = services.filter(occupation=occupation)

    if query:
        services = services.filter(Q(title__icontains=query) | Q(description__icontains=query))

    paginator = Paginator(services, 10)  # Show 10 services per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    occupations = Service.objects.values_list('occupation', flat=True).distinct()
    return render(request, 'available_services.html', {'page_obj': page_obj, 'occupations': occupations})

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
    """Handles the direct removal of a service."""
    if request.method == 'POST':
        service = get_object_or_404(Service, id=service_id, ads_author=request.user)
        service.delete()
        messages.success(request, 'Service removed successfully.')
        return redirect('operations')
    return HttpResponse(status=405)

@login_required
def operations(request):
    if not request.user.is_authenticated:
        request.session['has_expired'] = True  # Set a session flag
        return redirect('sign_in')

    user_services = Service.objects.filter(ads_author=request.user)
    return render(request, 'operations.html', {'user_services': user_services})


@login_required
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        # Delete all related services
        Service.objects.filter(ads_author=user).delete()
        # Delete user account
        user.delete()
        messages.success(request, 'Your account and all related services have been deleted.')
        return redirect('home')
    return render(request, 'delete_account.html')

@login_required
def profile(request):
    user_services = Service.objects.filter(ads_author=request.user)
    return render(request, 'profile.html', {'user_services': user_services})

def custom_page_not_found_view(request, exception):
    return render(request, '404.html', {}, status=404)

# Trigger error views for testing
def trigger_400(request):
    raise SuspiciousOperation("Bad Request")

def trigger_403(request):
    raise PermissionDenied("Forbidden")

def trigger_500(request):
    raise Exception("Internal Server Error")


def add_service_form(request):
    """Displays the form to add a new service."""
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.ads_author = request.user
            service.save()
            messages.success(request, 'Service added successfully.')
            return redirect('operations')
    return render(request, 'partials/add_service_form.html', {'form': form})

def edit_service_form(request, service_id):
    """Displays the form to edit an existing service."""
    service = get_object_or_404(Service, id=service_id)
    form = ServiceUpdateForm(instance=service)
    
    if request.method == 'POST':
        form = ServiceUpdateForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('operations')
    
    return render(request, 'partials/edit_service_form.html', {'form': form, 'service_id': service_id})