from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['resume']
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and not resume.name.lower().endswith('.pdf'):
            raise forms.ValidationError('Only PDF files are allowed.')
        return resume