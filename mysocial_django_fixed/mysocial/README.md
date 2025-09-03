
# Mini Social (Django)

Features: user profiles, posts with optional image, comments, likes, and follow system.

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

- Sign up at `/accounts/signup/`
- Login at `/accounts/login/`

### Notes
- Image upload requires Pillow (included). Files are stored under `media/`.
- Admin available at `/admin/`.
- Feed shows your posts and people you follow. Visit a profile to follow/unfollow.
