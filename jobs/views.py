from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Job, BookmarkedJob


@login_required
def job_list(request):
    jobs = Job.objects.all()

    query = request.GET.get('q', '').strip()
    tag = request.GET.get('tag', '').strip()

    if query:
        from django.db.models import Q
        jobs = jobs.filter(
            Q(job_title__icontains=query) | Q(company_name__icontains=query)
        )

    if tag:
        jobs = jobs.filter(description__icontains=tag)

    paginator = Paginator(jobs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    bookmarked_ids = set(
        BookmarkedJob.objects.filter(user=request.user).values_list('job_id', flat=True)
    )

    return render(request, 'jobs/job_list.html', {
        'page_obj': page_obj,
        'query': query,
        'tag': tag,
        'bookmarked_ids': bookmarked_ids,
    })


@login_required
def job_bookmark_toggle(request, pk):
    job = get_object_or_404(Job, pk=pk)
    bookmark, created = BookmarkedJob.objects.get_or_create(user=request.user, job=job)
    if not created:
        bookmark.delete()
        messages.success(request, 'Removed from bookmarks.')
    else:
        messages.success(request, 'Job bookmarked.')
    return redirect(request.META.get('HTTP_REFERER', 'job_list'))
