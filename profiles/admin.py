from django.contrib import admin
from .models import SeekerProfile, Skill, ProfileSkill

class ProfileSkillInline(admin.TabularInline):
    model = ProfileSkill
    extra = 0

@admin.register(SeekerProfile)
class SeekerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "preferred_salary_min", "preferred_salary_max", "preferred_work_setup", "preferred_schedule")
    inlines = [ProfileSkillInline]

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(ProfileSkill)
class ProfileSkillAdmin(admin.ModelAdmin):
    list_display = ("seeker", "skill", "level", "years_experience")
    list_filter = ("level",)
    search_fields = ("seeker__user__username", "skill__name")
