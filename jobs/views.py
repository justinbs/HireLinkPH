from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import EmployerOrganization, Job, JobSkill
from .forms import EmployerOrgForm, JobForm, JobSkillForm

def _get_or_create_employer(user):
    org, _ = EmployerOrganization.objects.get_or_create(user=user, defaults={
        "organization_name": f"{user.username}'s Organization"
    })
    return org

@login_required
def employer_org_view(request):
    if request.user.role != "employer":
        messages.error(request, "Only Employers can access this page.")
        return redirect("accounts:dashboard")

    org = _get_or_create_employer(request.user)
    if request.method == "POST":
        form = EmployerOrgForm(request.POST, instance=org)
        if form.is_valid():
            form.save()
            messages.success(request, "Organization profile saved.")
            return redirect("jobs:job_list")
    else:
        form = EmployerOrgForm(instance=org)

    return render(request, "jobs/employer_org.html", {"form": form})

@login_required
def job_list_view(request):
    if request.user.role != "employer":
        messages.error(request, "Only Employers can access this page.")
        return redirect("accounts:dashboard")

    org = _get_or_create_employer(request.user)
    jobs = Job.objects.filter(employer=org).order_by("-job_created_at")
    return render(request, "jobs/job_list.html", {"org": org, "jobs": jobs})

@login_required
def job_create_view(request):
    if request.user.role != "employer":
        messages.error(request, "Only Employers can access this page.")
        return redirect("accounts:dashboard")

    org = _get_or_create_employer(request.user)
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = org
            job.save()
            messages.success(request, "Job created. Add required skills next.")
            return redirect("jobs:job_skills", pk=job.pk)
    else:
        form = JobForm()

    return render(request, "jobs/job_form.html", {"form": form, "title": "Create Job"})

@login_required
def job_update_view(request, pk:int):
    if request.user.role != "employer":
        messages.error(request, "Only Employers can access this page.")
        return redirect("accounts:dashboard")

    org = _get_or_create_employer(request.user)
    job = get_object_or_404(Job, pk=pk, employer=org)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated.")
            return redirect("jobs:job_list")
    else:
        form = JobForm(instance=job)

    return render(request, "jobs/job_form.html", {"form": form, "title": "Edit Job"})

@login_required
def job_delete_view(request, pk:int):
    if request.user.role != "employer":
        messages.error(request, "Only Employers can access this page.")
        return redirect("accounts:dashboard")

    org = _get_or_create_employer(request.user)
    job = get_object_or_404(Job, pk=pk, employer=org)
    job.delete()
    messages.info(request, "Job deleted.")
    return redirect("jobs:job_list")

@login_required
def job_skills_view(request, pk:int):
    if request.user.role != "employer":
        messages.error(request, "Only Employers can access this page.")
        return redirect("accounts:dashboard")

    org = _get_or_create_employer(request.user)
    job = get_object_or_404(Job, pk=pk, employer=org)

    if request.method == "POST":
        form = JobSkillForm(request.POST)
        if form.is_valid():
            js = form.save(commit=False)
            js.job = job
            exists = JobSkill.objects.filter(job=job, skill=js.skill).exists()
            if exists:
                messages.warning(request, f"{js.skill.name} already required.")
            else:
                js.save()
                messages.success(request, f"Added required skill: {js.skill.name}.")
            return redirect("jobs:job_skills", pk=job.pk)
    else:
        form = JobSkillForm()

    reqs = JobSkill.objects.filter(job=job).select_related("skill")
    return render(request, "jobs/job_skills.html", {"job": job, "form": form, "reqs": reqs})

def job_detail_view(request, pk:int):
    job = get_object_or_404(Job.objects.select_related("employer"), pk=pk)
    reqs = JobSkill.objects.filter(job=job).select_related("skill")
    return render(request, "jobs/job_detail.html", {"job": job, "reqs": reqs})
