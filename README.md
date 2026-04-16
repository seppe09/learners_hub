# Learner's Hub — Django Project

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit: http://127.0.0.1:8000/accounts/signup/

## URL Map

| URL | Page |
|-----|------|
| `/accounts/signup/` | Register |
| `/accounts/login/` | Sign in |
| `/accounts/dashboard/` | Dashboard (auth required) |
| `/accounts/logout/` | Sign out |
| `/profiles/create/` | Create profile (auth required) |
| `/profiles/view/` | View profile (auth required) |
| `/profiles/edit/` | Edit profile (auth required) |
| `/admin/` | Django admin |
