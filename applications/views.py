from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from .forms import ApplicationForm


@login_required
def application_list(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, 'applications/application_list.html', {'applications': applications})


@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    return render(request, 'applications/application_detail.html', {'application': application})


@login_required
def application_add(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Application added successfully.')
            return redirect('application_list')
    else:
        form = ApplicationForm()
    return render(request, 'applications/application_form.html', {'form': form, 'title': 'Add Application'})


@login_required
def application_edit(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated successfully.')
            return redirect('application_detail', pk=application.pk)
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'applications/application_form.html', {'form': form, 'title': 'Edit Application'})


@login_required
def application_delete(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Application deleted.')
        return redirect('application_list')
    return render(request, 'applications/application_confirm_delete.html', {'application': application})