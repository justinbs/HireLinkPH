HireLinkPH

AI-assisted job matching platform for Job Seekers and Employers.
Built for Application Development & Emerging Technologies.

🧠 Tech Stack

Backend: Django 5, Python 3.12
AI Matching: scikit-learn (TF-IDF + cosine similarity)
Database: SQLite (default for dev)
Frontend: Django Templates + Bootstrap 5
Auth/Roles: Seeker, Employer, Admin (Admin via superuser only)

🚀 Features (Current Sprints)
Sprint 1

Django foundation

Models from ERD

Admin wiring

Sprint 2

Register / Login / Logout

Role-based landing pages

Sprint 3

Seeker: Profile & skills management
Employer: Organization profile + Job CRUD

Sprint 4

AI recommendations for seekers (ranked with % fit + reasons)

Pagination for long lists, humanized dates

Polished UI, toasts, role-aware navbar brand redirect

Public registration for Seeker/Employer only

⚙️ Quick Start
0) Prerequisites

Python 3.12 (recommended)

Git

1. Clone the Repository
git clone https://github.com/justinbs/HireLinkPH.git
cd HireLinkPH

2. Create & Activate Virtual Environment
Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate


If you see an execution policy error:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Migrate Database
python manage.py migrate

5. Create Superuser
python manage.py createsuperuser


(Choose username/email/password)

6. Run Server
python manage.py runserver


Visit: http://127.0.0.1:8000/

🧭 How to Use
Job Seeker (Happy Path)

Click Create an Account → choose Job Seeker.

Fill out profile and add skills.

Open Recommended Jobs (via navbar or home CTA).

Filter by city, setup, schedule, or salary.

Click Apply.

Employer

Create an Account → choose Employer.

Set up Organization.

Create Job Posts, manage skills, view candidates.

Admin

Visit /admin/

Log in with the superuser created above.

🔗 Useful URLs
Purpose	URL
Home	/
Login	/accounts/login/
Register	/accounts/register/ (?role=seeker or ?role=employer)
Seeker Profile	/profiles/me/
Seeker Skills	/profiles/skills/
Recommendations	/matching/recommendations/
Employer Organization	/jobs/employer/
Employer Job List	/jobs/employer/jobs/
Admin	/admin/
🧩 Configuration (Optional for Dev)

Using SQLite by default — no .env required.
If needed, you can define:

SECRET_KEY=<your_secret_key>
DEBUG=True
ALLOWED_HOSTS=*


To use .env:

Add a .env file.

Load via python-dotenv (optional).

🧰 Common Issues & Fixes

Can’t activate venv on Windows

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate


ModuleNotFoundError: sklearn

pip install scikit-learn
# or
pip install -r requirements.txt


Template not found (e.g. accounts/register.html)
→ Ensure you pulled the latest main branch and are running from the project root.

Git shows “Everything up-to-date” but no changes on GitHub

git add -A
git commit -m "msg"
git push -u origin HEAD

🧑‍💻 Dev Notes

Branching: work on main for now (sprints committed sequentially).

Commit style:

Sprint X: Short title


Add a detailed body if needed:

git commit -m "Subject" -m "Long description..."


Static files:
Whitenoise serves static in dev; no extra setup required.


License / Use

Academic project for Mapúa University coursework.
