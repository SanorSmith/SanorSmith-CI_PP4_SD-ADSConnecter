from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Service, ServiceCategory

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ServiceForm(forms.ModelForm):
    occupation = forms.ModelChoiceField(queryset=ServiceCategory.objects.all(), label="Service Category")

    class Meta:
        model = Service
        fields = ['title', 'description', 'occupation', 'contact_info', 'featured_image']    
        
class ServiceUpdateForm(forms.ModelForm):
    occupation = forms.ModelChoiceField(queryset=ServiceCategory.objects.all(), label="Service Category")

    class Meta:
        model = Service
        fields = ['title', 'description', 'occupation', 'contact_info', 'featured_image']        
        
class ServiceDeleteForm(forms.Form):
    service_id = forms.IntegerField()        
    
class ServiceForm(forms.ModelForm):
    occupation = forms.ModelChoiceField(
        queryset=ServiceCategory.objects.all(), 
        label="Service Category",
        empty_label="Select a category"
    )

    class Meta:
        model = Service
        fields = ['title', 'description', 'occupation', 'contact_info', 'featured_image']