from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Profile
from .forms import RegisterForm, ResumeUploadForm
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def resume_upload_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resume uploaded successfully.')
            return redirect('resume_upload')
    else:
        form = ResumeUploadForm(instance=profile)
    return render(request,'accounts/resume_upload.html',{'form':form, 'profile':profile})