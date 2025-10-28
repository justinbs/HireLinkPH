from django.db import models
from django.conf import settings
from profiles.models import Skill, SeekerProfile

class EmployerOrganization(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)

    employer_created_at = models.DateTimeField(auto_now_add=True)
    employer_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organization_name

class Job(models.Model):
    SCHEDULE_CHOICES = [("full-time","Full-time"),("part-time","Part-time"),("shifting","Shifting")]
    WORK_SETUP_CHOICES = [("onsite","Onsite"),("hybrid","Hybrid"),("remote","Remote")]
    STATUS_CHOICES = [("open","Open"), ("closed","Closed")]

    employer = models.ForeignKey(EmployerOrganization, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    location_city = models.CharField(max_length=100, blank=True)
    schedule = models.CharField(max_length=50, choices=SCHEDULE_CHOICES, blank=True)
    work_setup = models.CharField(max_length=20, choices=WORK_SETUP_CHOICES, blank=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    job_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

    job_created_at = models.DateTimeField(auto_now_add=True)
    job_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} @ {self.employer.organization_name}"

class JobSkill(models.Model):
    LEVEL_CHOICES = [("beginner","Beginner"), ("intermediate","Intermediate"), ("advanced","Advanced")]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    required_level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    job_skill_created_at = models.DateTimeField(auto_now_add=True)
    job_skill_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("job", "skill")

    def __str__(self):
        return f"{self.job.title} needs {self.skill.name} ({self.required_level})"

class Application(models.Model):
    STATUS_CHOICES = [
        ("submitted","Submitted"),
        ("viewed","Viewed"),
        ("shortlisted","Shortlisted"),
        ("rejected","Rejected"),
        ("interview","Interview"),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    seeker = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE)
    application_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
    applied_at = models.DateTimeField(auto_now_add=True)
    application_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("job", "seeker")

    def __str__(self):
        return f"{self.seeker.user.username} → {self.job.title} ({self.application_status})"
