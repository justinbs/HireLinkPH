from django import forms
from .models import SeekerProfile, ProfileSkill, Skill

class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = SeekerProfile
        fields = [
            "preferred_salary_min",
            "preferred_salary_max",
            "preferred_schedule",
            "preferred_work_setup",
            "location_radius_km",
        ]

class ProfileSkillForm(forms.ModelForm):
    class Meta:
        model = ProfileSkill
        fields = ["skill", "level", "years_experience"]

    # allow creating skills via dropdown only (pre-seeded by admin)
    skill = forms.ModelChoiceField(queryset=Skill.objects.order_by("name"))
