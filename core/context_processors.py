from django.urls import reverse

def brand_link(request):
    href = "/"
    u = getattr(request, "user", None)
    if u and u.is_authenticated:
        role = getattr(u, "role", "")
        if role == "seeker":
            # send seekers to recommendations (fallback to profile edit)
            try:
                href = reverse("matching:recommendations")
            except Exception:
                href = reverse("profiles:edit")  # /profiles/me/
        elif role == "employer":
            href = reverse("jobs:job_list")      # employer job list
        else:
            href = reverse("admin:index")        # Django admin
    return {"brand_href": href}
