from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import SeekerProfile, ProfileSkill
from .forms import SeekerProfileForm, ProfileSkillForm

def _get_or_create_profile(user):
    profile, _ = SeekerProfile.objects.get_or_create(user=user)
    return profile

@login_required
def profile_edit_view(request):
    if request.user.role != "seeker":
        messages.error(request, "Only Job Seekers can edit this page.")
        return redirect("accounts:dashboard")

    profile = _get_or_create_profile(request.user)
    if request.method == "POST":
        form = SeekerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profiles:skills")
    else:
        form = SeekerProfileForm(instance=profile)

    return render(request, "profiles/edit.html", {"form": form})

@login_required
def profile_skills_view(request):
    if request.user.role != "seeker":
        messages.error(request, "Only Job Seekers can manage skills.")
        return redirect("accounts:dashboard")

    profile = _get_or_create_profile(request.user)
    if request.method == "POST":
        form = ProfileSkillForm(request.POST)
        if form.is_valid():
            ps = form.save(commit=False)
            ps.seeker = profile
            # prevent duplicates
            exists = ProfileSkill.objects.filter(seeker=profile, skill=ps.skill).exists()
            if exists:
                messages.warning(request, f"{ps.skill.name} already added.")
            else:
                ps.save()
                messages.success(request, f"Added skill: {ps.skill.name}.")
            return redirect("profiles:skills")
    else:
        form = ProfileSkillForm()

    skills = ProfileSkill.objects.filter(seeker=profile).select_related("skill")
    return render(request, "profiles/skills.html", {"form": form, "skills": skills})

@login_required
def profile_skill_delete_view(request, pk: int):
    if request.user.role != "seeker":
        messages.error(request, "Only Job Seekers can manage skills.")
        return redirect("accounts:dashboard")

    profile = _get_or_create_profile(request.user)
    item = get_object_or_404(ProfileSkill, pk=pk, seeker=profile)
    item.delete()
    messages.info(request, "Skill removed.")
    return redirect("profiles:skills")
