from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from .forms import ApplicationForm
from django.db.models import Q
from django.core.paginator import Paginator


@login_required
def application_list(request):
    applications = Application.objects.filter(user=request.user)

    # Search by company or job title
    query = request.GET.get('q', '')
    if query:
        applications = applications.filter(
            Q(company_name__icontains=query) | Q(job_title__icontains=query)
        )

    # Filter by status
    status = request.GET.get('status', '')
    if status:
        applications = applications.filter(status=status)

    # Pagination
    paginator = Paginator(applications, 5)  # 5 per page, adjust as you like
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'status': status,
        'status_choices': Application.STATUS_CHOICES,
    }
    return render(request, 'applications/application_list.html', context)

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