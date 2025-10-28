from django import forms
from .models import EmployerOrganization, Job, JobSkill
from profiles.models import Skill

class EmployerOrgForm(forms.ModelForm):
    class Meta:
        model = EmployerOrganization
        fields = ["organization_name", "contact_person", "contact_number"]

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title","description","location_city","schedule","work_setup",
            "salary_min","salary_max","closing_date","job_status"
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4})
        }

class JobSkillForm(forms.ModelForm):
    class Meta:
        model = JobSkill
        fields = ["skill", "required_level"]

    skill = forms.ModelChoiceField(queryset=Skill.objects.order_by("name"))
