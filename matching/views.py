from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from profiles.models import SeekerProfile
from jobs.models import Job, Application
from .services import rank_jobs_for_seeker, rank_seekers_for_job
from django.core.paginator import Paginator

@login_required
def recommendations_view(request):
    if request.user.role != "seeker":
        messages.error(request, "Only Job Seekers can view recommendations.")
        return render(request, "dashboards/seeker.html")

    seeker, _ = SeekerProfile.objects.get_or_create(user=request.user)
    jobs = Job.objects.filter(job_status="open").select_related("employer")

    # --- filters ---
    city = request.GET.get("city", "").strip()
    setup = request.GET.get("setup", "").strip()
    schedule = request.GET.get("schedule", "").strip()
    smin = request.GET.get("salary_min", "").strip()
    smax = request.GET.get("salary_max", "").strip()

    if city:
        jobs = jobs.filter(location_city__icontains=city)
    if setup:
        jobs = jobs.filter(work_setup=setup)
    if schedule:
        jobs = jobs.filter(schedule=schedule)
    if smin.isdigit():
        jobs = jobs.filter(salary_max__gte=int(smin))
    if smax.isdigit():
        jobs = jobs.filter(salary_min__lte=int(smax))

    ranked = rank_jobs_for_seeker(seeker, jobs, limit=500)  # a big list; we’ll paginate it

    # mark already applied
    applied_ids = set(
        Application.objects.filter(seeker=seeker).values_list("job_id", flat=True)
    )

    # paginate the ranked list (list of tuples)
    paginator = Paginator(ranked, 10)  # 10 rows per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "filters": {"city": city, "setup": setup, "schedule": schedule, "salary_min": smin, "salary_max": smax},
        "applied_ids": applied_ids,
    }
    return render(request, "matching/recommendations.html", context)

@login_required
def candidates_for_job_view(request, pk: int):
    if request.user.role != "employer":
        messages.error(request, "Only Employers can view candidates.")
        return render(request, "dashboards/employer.html")

    job = get_object_or_404(Job.objects.select_related("employer"), pk=pk, employer__user=request.user)
    seekers = SeekerProfile.objects.select_related("user").all()
    ranked = rank_seekers_for_job(job, seekers, limit=200)
    context = {"job": job, "ranked": ranked}
    return render(request, "matching/candidates.html", context)
