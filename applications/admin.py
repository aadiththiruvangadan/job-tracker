from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'job_title', 'status', 'applied_date', 'user')
    list_filter = ('status', 'applied_date')
    search_fields = ('company_name', 'job_title')