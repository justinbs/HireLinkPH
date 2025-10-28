HireLinkPH

AI-assisted job matching platform for Job Seekers and Employers. Built for Application Development & Emerging Technologies.

Tech Stack

Backend: Django 5, Python 3.12

AI Matching: scikit-learn (TF-IDF + cosine similarity)

DB: SQLite (dev default)

Frontend: Django templates + Bootstrap 5

Auth/Roles: Seeker, Employer, Admin (admin via superuser only)

Features (current sprints)

Sprint 1: Django foundation, models from ERD, admin wiring

Sprint 2: Register / login / logout + role-based landing pages

Sprint 3:

Seeker: profile & skills management

Employer: organization profile + Job CRUD

Sprint 4:

AI recommendations for seekers (ranked with % fit + reasons)

Pagination for long lists, humanized dates

Polished UI, toasts, role-aware navbar brand redirect

Public registration only for Seeker/Employer

Quick Start
0) Prerequisites

Python 3.12 (recommended)

Git


1) Clone
git clone https://github.com/justinbs/HireLinkPH.git
cd HireLinkPH

2) Create & activate virtualenv

Windows (PowerShell):

python -m venv .venv
.\.venv\Scripts\Activate
# If you see an execution policy error:
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned


macOS / Linux:

python3 -m venv .venv
source .venv/bin/activate

3) Install dependencies
pip install -r requirements.txt

4) Migrate DB
python manage.py migrate

5) Create an admin (superuser)
python manage.py createsuperuser
# choose username/email/password

6) Run
python manage.py runserver
# http://127.0.0.1:8000/

How to Use (happy path)
Job Seeker

Click Create an Account → choose Job Seeker.

Fill Profile and add Skills.

Open Recommended Jobs (navbar or home CTA).

Filter by city/setup/schedule/salary as needed; click Apply.

Employer

Create an Account → choose Employer.

Set up Organization.

Create Job Posts; manage skills, view Candidates.

Admin

Visit /admin/ and log in with the superuser created above.

Useful URLs

Home: /

Login: /accounts/login/

Register: /accounts/register/ (?role=seeker or ?role=employer supported)

Seeker profile: /profiles/me/

Seeker skills: /profiles/skills/

Recommendations: /matching/recommendations/

Employer org: /jobs/employer/

Employer job list: /jobs/employer/jobs/

Admin: /admin/

The HireLinkPH brand in the navbar routes to the correct dashboard per role.

Configuration
Environment variables (optional for dev)

Using SQLite by default — no .env required. If you want to set values:

SECRET_KEY (else Django’s dev key is used)

DEBUG (True by default in dev)

ALLOWED_HOSTS (for deployment)

For a simple local override, you can add a .env and load via python-dotenv if needed (not required for our coursework runs).

Common Issues & Fixes

Can’t activate venv on Windows

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

Re-run: .\.venv\Scripts\Activate

ModuleNotFoundError: sklearn

pip install scikit-learn or pip install -r requirements.txt

Template not found (e.g., accounts/register.html)

Ensure you pulled the latest main and you’re running from the project root.

“Everything up-to-date” but no changes on GitHub

git add -A && git commit -m "msg" then git push -u origin HEAD

Dev Notes

Branching: work on main for now (sprints committed sequentially).

Commit style: Sprint X: Short title + body if needed.

Add a detailed body with:
git commit -m "Subject" -m "Long description..."

Static files: Whitenoise serves static in dev; no extra setup required.

License / Use

Academic project for Mapúa coursework. Not for production use without further security hardening.
