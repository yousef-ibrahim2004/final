# SocialHub

A mini Facebook-like social media platform built with Django.

## Features

- User registration with email verification
- Login/Logout/Password reset via email
- User profiles with bio and avatar
- Post creation (text + image), likes, comments
- Home feed, post detail, profile, settings
- Privacy controls and notification preferences

## Setup

1. Clone the repo
2. Create and activate a virtual environment
3. Install requirements:  
   `pip install -r requirements.txt`
4. Configure `.env` for secrets and email
5. Run migrations:  
   `python manage.py migrate`
6. Start the server:  
   `python manage.py runserver`

## Email

Configure Gmail SMTP in `.env` for email features.

## License

MIT