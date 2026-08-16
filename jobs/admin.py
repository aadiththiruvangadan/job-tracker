from django.contrib import admin
from .models import Job, BookmarkedJob


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'location', 'source', 'posted_date')
    list_filter = ('source', 'posted_date')
    search_fields = ('job_title', 'company_name', 'tags')


@admin.register(BookmarkedJob)
class BookmarkedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'bookmarked_at')
