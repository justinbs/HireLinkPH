from django.contrib import admin
from .models import EmployerOrganization, Job, JobSkill, Application

class JobSkillInline(admin.TabularInline):
    model = JobSkill
    extra = 0

@admin.register(EmployerOrganization)
class EmployerOrgAdmin(admin.ModelAdmin):
    list_display = ("organization_name", "user", "contact_person", "contact_number")
    search_fields = ("organization_name", "user__username")

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "employer", "location_city", "schedule", "work_setup", "job_status")
    list_filter = ("schedule", "work_setup", "job_status")
    search_fields = ("title", "employer__organization_name", "location_city")
    inlines = [JobSkillInline]

@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
    list_display = ("job", "skill", "required_level")
    list_filter = ("required_level",)
    search_fields = ("job__title", "skill__name")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "seeker", "application_status", "applied_at")
    list_filter = ("application_status",)
    search_fields = ("job__title", "seeker__user__username")
