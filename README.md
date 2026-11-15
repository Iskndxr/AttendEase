# AttendEase

A class attendance system for colleges. Lecturers create class sessions with a
unique session code, and students check in to record their attendance.

> Solo project (diploma coursework).

## Features

- Role-based accounts: students, lecturers, the Discipline Unit (Unit Tatatertib),
  and the Deputy Director of Academic Affairs (TPHEA)
- Departments, subjects, and classes linked to lecturers
- Class sessions with auto-generated session codes for check-in
- Students assigned to a mentor lecturer
- Profile completion flow for new users

## Tech stack

- **Back-end:** Python, Django, with a custom user model
- **Database:** SQLite
- **Front-end:** Django templates, HTML, CSS, JavaScript

## Running locally

```bash
git clone https://github.com/Iskndxr/AttendEase.git
cd AttendEase/AttendEase/AttendEase
python -m venv .venv
source .venv/bin/activate
pip install django
python manage.py migrate
python manage.py runserver
```

For anything beyond local testing, set your own `DJANGO_SECRET_KEY` environment variable.
