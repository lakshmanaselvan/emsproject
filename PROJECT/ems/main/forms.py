from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import UserProfile
from .models import Event
import uuid

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'password', 'role']
        labels = {
            'name':'',
            'email':'',
            'password':'',
            'role':'Select Role'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'style': 'width: 500px; text-align: center'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'style': 'width: 500px; text-align: center'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'style': 'width: 500px; text-align: center'}),
            'role': forms.Select(attrs={'class': 'form-control', 'style': 'width: 500px; text-align: center'}),
        }

    def save(self, commit=True):
        user_profile = super(RegistrationForm, self).save(commit=False)
        raw_password = self.cleaned_data['password']
        user_profile.password = make_password(raw_password)
        user_profile.token = uuid.uuid4().hex  # Generate a random token
        if commit:
            user_profile.save()
        return user_profile
    
    
    
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'categorie', 'venue', 'startTime', 'endTime', 'startDate', 'endDate', 'chief_guest']
        labels = {
            'title':'',
            'description':'',
            'categorie':'Select Catogries',
            'venue':'Select Venue',
            'startTime':'',
            'endTime':'',
            'startDate':'YYYY-MM-DD',
            'endDate':'YYYY-MM-DD',
            'chief_guest':''
        } 
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name', 'style': 'width: 500px; text-align: center'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Event Description', 'style': 'width: 500px; text-align: center'}),
            'categorie': forms.Select(attrs={'class':'form-control', 'style': 'width: 500px; text-align: center'}),
            'venue': forms.Select(attrs={'class':'form-control', 'style': 'width: 500px; text-align: center'}),
            'startTime': forms.TimeInput(attrs={'class':'form-control', 'placeholder':'Start Time', 'style': 'width: 500px; text-align: center'}, format='%H:%M'),
            'endTime': forms.TimeInput(attrs={'class':'form-control', 'placeholder':'End Time', 'style': 'width: 500px; text-align: center'}),
            'startDate': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Start Date', 'style': 'width: 500px; text-align: center'}),
            'endDate': forms.TextInput(attrs={'class':'form-control', 'placeholder':'End Date', 'style': 'width: 500px; text-align: center'}),
            'chief_guest': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Chief Guest', 'style': 'width: 500px; text-align: center'}),
        }