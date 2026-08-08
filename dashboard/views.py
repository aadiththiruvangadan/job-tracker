from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import json
from applications.models import Application


@login_required
def dashboard_home(request):
    applications = Application.objects.filter(user=request.user)

    total = applications.count()
    status_counts = applications.values('status').annotate(count=Count('status'))

    # Build a dict with all statuses defaulting to 0, then fill in real counts
    status_labels = dict(Application.STATUS_CHOICES)
    counts_by_status = {key: 0 for key in status_labels}
    for entry in status_counts:
        counts_by_status[entry['status']] = entry['count']

    recent_applications = applications.order_by('-applied_date')[:5]

    chart_data = {
        'labels': [status_labels[key] for key in counts_by_status],
        'values': list(counts_by_status.values()),
    }

    context = {
        'total': total,
        'applied': counts_by_status.get('applied', 0),
        'interview': counts_by_status.get('interview', 0),
        'rejected': counts_by_status.get('rejected', 0),
        'accepted': counts_by_status.get('accepted', 0),
        'recent_applications': recent_applications,
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'dashboard/dashboard_home.html', context)