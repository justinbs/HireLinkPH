
# HireLinkPH

AI-assisted job matching platform for Job Seekers and Employers. Built for Application Development & Emerging Technologies.


## Features

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


## Tech Stack

**Backend:** Django 5, Python 3.12

**AI Matching:** scikit-learn (TF-IDF + cosine similarity)

**DB:** SQLite

**Frontend:** Django templates + Bootstrap 5

**Auth/Roles:** Seeker, Employer, Admin (admin via superuser only)
## Quick Start

**0)** Prerequisites
- Python 3.12
- Git

**1)** Clone
In your Terminal,

git clone https://github.com/justinbs/HireLinkPH.git

cd HireLinkPH


**2)** Create & activate 
In your terminal,

python -m venv .venv

.\.venv\Scripts\Activate
 - If you see an execution policy error:
    - Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned


**3)** Install dependencies
In your terminal with venv activated,

pip install -r requirements.txt


**4)** Migrate DB
In the same terminal,

python manage.py Migrate


**5)** Create an admin (superuser)
In the same terminal, 

python manage.py createsuperuser


**6)** Run
In the same terminal, 

python manage.py runserver

#### http://127.0.0.1:8000/
#### http://127.0.0.1:8000/admin
## Demo
#### Job Seeker
1) Click Create an Account → choose Job Seeker.

2) Fill Profile and add Skills.

3) Open Recommended Jobs (navbar or home CTA).

4) Filter by city/setup/schedule/salary as needed; click Apply.

#### Employer
1) Create an Account → choose Employer.

2) Set up Organization.

3) Create Job Posts; manage skills, view Candidates.

#### Admin
Visit /admin/ and log in with the superuser created above.
## URLs
Home: /

Login: /accounts/login/

Register: /accounts/register/ (?role=seeker or ?role=employer supported)

Seeker profile: /profiles/me/

Seeker skills: /profiles/skills/

Recommendations: /matching/recommendations/

Employer org: /jobs/employer/

Employer job list: /jobs/employer/jobs/

Admin: /admin/
## Configuration
Environment variables (optional for dev)

Using SQLite by default — no .env required. If you want to set values:

SECRET_KEY (else Django’s dev key is used)

DEBUG (True by default in dev)

ALLOWED_HOSTS (for deployment)
## Common Issues & Fixes
#### Can’t activate venv on Windows

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

Re-run: .\.venv\Scripts\Activate

#### ModuleNotFoundError: sklearn

pip install scikit-learn or pip install -r requirements.txt

#### Template not found (e.g., accounts/register.html)

Ensure you pulled the latest main and you’re running from the project root.
