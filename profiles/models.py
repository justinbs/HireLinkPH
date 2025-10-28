from django.db import models
from django.conf import settings

class SeekerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    preferred_salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preferred_salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preferred_schedule = models.CharField(max_length=50, blank=True)  # full-time, part-time, shifting
    preferred_work_setup = models.CharField(max_length=20, blank=True)  # onsite, hybrid, remote
    location_radius_km = models.IntegerField(null=True, blank=True)

    seeker_created_at = models.DateTimeField(auto_now_add=True)
    seeker_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SeekerProfile<{self.user.username}>"

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    skill_created_at = models.DateTimeField(auto_now_add=True)
    skill_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProfileSkill(models.Model):
    LEVEL_CHOICES = [("beginner","Beginner"), ("intermediate","Intermediate"), ("advanced","Advanced")]
    seeker = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    years_experience = models.IntegerField(default=0)

    profile_skill_created_at = models.DateTimeField(auto_now_add=True)
    profile_skill_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("seeker", "skill")

    def __str__(self):
        return f"{self.seeker.user.username} - {self.skill.name} ({self.level})"
