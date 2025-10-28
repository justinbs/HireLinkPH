from dataclasses import dataclass
from typing import Iterable, List, Dict, Tuple
from profiles.models import SeekerProfile, ProfileSkill
from jobs.models import Job, JobSkill

# TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class FitBreakdown:
    jaccard: float
    tfidf: float
    matched_skills: List[str]
    bonuses: Dict[str, float]
    final_score: float

def _safe_div(a: int, b: int) -> float:
    return (a / b) if b else 0.0

def _jaccard(set_a: set, set_b: set) -> Tuple[float, List[str]]:
    inter = set_a & set_b
    union = set_a | set_b
    return _safe_div(len(inter), len(union)), sorted(list(inter))

def _job_text(job: Job, job_skills: List[str]) -> str:
    parts = [job.title or "", job.description or "", " ".join(job_skills)]
    if job.work_setup: parts.append(job.work_setup)
    if job.schedule: parts.append(job.schedule)
    return " ".join(parts)

def _seeker_text(seeker: SeekerProfile, seeker_skills: List[str]) -> str:
    parts = [" ".join(seeker_skills)]
    if seeker.preferred_work_setup: parts.append(seeker.preferred_work_setup)
    if seeker.preferred_schedule: parts.append(seeker.preferred_schedule)
    return " ".join(parts)

def _tfidf_similarity(seeker_text: str, job_texts: List[str]) -> List[float]:
    corpus = [seeker_text] + job_texts
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(corpus)
    sims = cosine_similarity(X[0:1], X[1:]).flatten()
    return sims.tolist()

def compute_fit_score(seeker: SeekerProfile, job: Job) -> FitBreakdown:
    # names as sets
    seeker_skill_names = set(
        ProfileSkill.objects.filter(seeker=seeker)
        .select_related("skill")
        .values_list("skill__name", flat=True)
    )
    job_skill_names = set(
        JobSkill.objects.filter(job=job)
        .select_related("skill")
        .values_list("skill__name", flat=True)
    )

    jaccard, matched = _jaccard(seeker_skill_names, job_skill_names)

    # TF-IDF cosine (build small corpus per call; fine for MVP)
    seeker_text = _seeker_text(seeker, list(seeker_skill_names))
    job_text = _job_text(job, list(job_skill_names))
    tfidf_list = _tfidf_similarity(seeker_text, [job_text])
    tfidf = tfidf_list[0] if tfidf_list else 0.0

    # Bonuses
    bonuses: Dict[str, float] = {}
    bonus_total = 0.0

    # Salary: seeker_min <= job_max (when provided)
    if (seeker.preferred_salary_min is None) or (job.salary_max is None) or (seeker.preferred_salary_min <= job.salary_max):
        bonuses["salary_alignment"] = 0.10
        bonus_total += 0.10

    # Work setup match
    if seeker.preferred_work_setup and job.work_setup and seeker.preferred_work_setup == job.work_setup:
        bonuses["work_setup_match"] = 0.05
        bonus_total += 0.05

    # Schedule match
    if seeker.preferred_schedule and job.schedule and seeker.preferred_schedule == job.schedule:
        bonuses["schedule_match"] = 0.05
        bonus_total += 0.05

    # Blend: 60% Jaccard + 20% TF-IDF + bonuses (max 100)
    blended = (0.60 * jaccard) + (0.20 * tfidf) + bonus_total
    final = max(0.0, min(100.0, 100.0 * blended))

    return FitBreakdown(jaccard=jaccard, tfidf=tfidf, matched_skills=matched, bonuses=bonuses, final_score=final)

def rank_jobs_for_seeker(seeker: SeekerProfile, jobs_qs: Iterable[Job], limit: int = 20):
    rows = []
    # Optimize TF-IDF by batching: here we compute per job (still OK for MVP sizes)
    for job in jobs_qs:
        fb = compute_fit_score(seeker, job)
        rows.append((fb.final_score, fb, job))
    rows.sort(key=lambda x: x[0], reverse=True)
    return rows[:limit]

def rank_seekers_for_job(job: Job, seekers_qs: Iterable[SeekerProfile], limit: int = 50):
    rows = []
    for seeker in seekers_qs:
        fb = compute_fit_score(seeker, job)
        rows.append((fb.final_score, fb, seeker))
    rows.sort(key=lambda x: x[0], reverse=True)
    return rows[:limit]
