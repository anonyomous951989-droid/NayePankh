# 🌟 NayePankh Foundation — Volunteer Registration System

A complete **Full Stack Volunteer Registration System** built with Django for the NayePankh Foundation NGO.

> **Designed & Developed by Raj Devvanshi**

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation Guide](#-installation-guide)
- [Running the Project](#-running-the-project)
- [Project Structure](#-project-structure)
- [Database Models](#-database-models)
- [API Endpoints](#-api-endpoints)
- [Screenshots](#-screenshots)

---

## ✨ Features

### Landing Page
- Modern responsive design with hero section
- About Us, Mission & Vision sections
- Volunteer benefits showcase
- Contact form
- Animated statistics counter

### Volunteer Registration
- Complete registration form with 12+ fields
- File uploads (Resume & Profile Photo)
- Form validation (client + server side)
- Email notification after registration

### Authentication
- User Signup & Login
- Email Verification (Gmail SMTP)
- Password Reset
- Role-based access (Volunteer / Admin)

### Volunteer Dashboard
- View & edit profile
- Application status tracking
- Download Volunteer ID (PDF)
- View assigned events

### Admin Dashboard
- Statistics cards (Total, Approved, Pending, Active Events)
- View all volunteers with search, filter, and pagination
- Approve/reject applications with email notifications
- Export data to Excel & PDF
- Create and manage events

### Event Management
- Full CRUD (Create, Read, Update, Delete)
- Assign volunteers to events
- Attendance tracking (Present/Absent/Late)
- Event listing with search & pagination

### Reports
- Volunteer Registration Report
- Event Participation Report
- Attendance Report
- Monthly Statistics
- Export to Excel/PDF

### Extra Features
- REST API endpoints (Django REST Framework)
- Custom 404 & 500 error pages
- Responsive Bootstrap 5 design
- Glassmorphism & micro-animations
- Beginner-friendly code with comments

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.x |
| API | Django REST Framework |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Database | PostgreSQL |
| Auth | Django Auth + Email Verification |
| Export | openpyxl (Excel), ReportLab (PDF) |
| Email | Gmail SMTP |
| Fonts | Google Fonts (Inter, Outfit) |
| Icons | Bootstrap Icons |

---

## 🚀 Installation Guide

### Prerequisites
- Python 3.10+
- PostgreSQL installed and running
- Git

### Step 1: Clone the Repository
```bash
cd f:/Projects/VR
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Set Up PostgreSQL Database
```sql
-- Open PostgreSQL shell (psql) and run:
CREATE DATABASE nayepankh_db;
```

### Step 6: Configure Environment Variables
```bash
# Copy the example file
copy .env.example .env

# Edit .env with your settings:
# - SECRET_KEY: Generate a new one or use the default for development
# - DB_NAME, DB_USER, DB_PASSWORD: Your PostgreSQL credentials
# - EMAIL_HOST_USER: Your Gmail address
# - EMAIL_HOST_PASSWORD: Your Gmail App Password
```

### Step 7: Set Up Gmail SMTP (for email features)
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Enable **2-Step Verification**
3. Go to **App Passwords** (Security → 2-Step Verification → App Passwords)
4. Generate a new app password for "Mail"
5. Copy the 16-character password to your `.env` file as `EMAIL_HOST_PASSWORD`

### Step 8: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 9: Create a Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow the prompts to set username, email, and password
```

### Step 10: Run the Development Server
```bash
python manage.py runserver
```

### Step 11: Access the Application
- **Landing Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API**: http://127.0.0.1:8000/api/

---

## 🏃 Running the Project

```bash
# Activate virtual environment
venv\Scripts\activate

# Run migrations (if models changed)
python manage.py makemigrations
python manage.py migrate

# Start the server
python manage.py runserver

# Create superuser (first time only)
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic
```

---

## 📁 Project Structure

```
VR/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # This file
│
├── nayepankh/                # Project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Root URL routing
│   ├── wsgi.py               # WSGI entry point
│   └── asgi.py               # ASGI entry point
│
├── accounts/                 # Authentication app
│   ├── models.py             # Custom User model
│   ├── views.py              # Login, signup, verify, reset
│   ├── forms.py              # Auth forms
│   ├── urls.py               # Auth URL patterns
│   ├── admin.py              # User admin config
│   └── utils.py              # Email utilities
│
├── volunteers/               # Volunteer management app
│   ├── models.py             # VolunteerProfile model
│   ├── views.py              # Registration, profile, ID download
│   ├── forms.py              # Registration & edit forms
│   ├── urls.py               # Volunteer URL patterns
│   └── admin.py              # Volunteer admin config
│
├── events/                   # Event management app
│   ├── models.py             # Event, Assignment, Attendance
│   ├── views.py              # CRUD, assign, attendance
│   ├── forms.py              # Event & attendance forms
│   ├── urls.py               # Event URL patterns
│   └── admin.py              # Event admin config
│
├── dashboard/                # Dashboard app
│   ├── views.py              # Volunteer & admin dashboards
│   └── urls.py               # Dashboard URL patterns
│
├── reports/                  # Reports app
│   ├── views.py              # Report generation & export
│   └── urls.py               # Report URL patterns
│
├── core/                     # Core app (landing, contact)
│   ├── models.py             # ContactMessage model
│   ├── views.py              # Landing page, contact, errors
│   ├── forms.py              # Contact form
│   └── urls.py               # Core URL patterns
│
├── api/                      # REST API app
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # API endpoints
│   └── urls.py               # API URL patterns
│
├── templates/                # HTML templates
│   ├── base.html             # Base template
│   ├── navbar.html           # Navigation bar
│   ├── footer.html           # Footer (with Raj Devvanshi credit)
│   ├── 404.html              # Custom 404 page
│   ├── 500.html              # Custom 500 page
│   ├── accounts/             # Auth templates
│   ├── volunteers/           # Volunteer templates
│   ├── events/               # Event templates
│   ├── dashboard/            # Dashboard templates
│   └── reports/              # Report templates
│
├── static/                   # Static files
│   ├── css/style.css         # Custom stylesheet
│   └── js/main.js            # Custom JavaScript
│
└── media/                    # User uploads (created at runtime)
    ├── resumes/
    ├── photos/
    └── events/
```

---

## 📊 Database Models

| Model | Description |
|-------|-------------|
| **User** | Custom user with role, email verification |
| **VolunteerProfile** | Volunteer details (phone, skills, status, etc.) |
| **Event** | Event details (title, date, location, status) |
| **VolunteerAssignment** | Links volunteers to events |
| **Attendance** | Tracks event attendance |
| **ContactMessage** | Contact form submissions |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/volunteers/` | List all volunteers |
| GET | `/api/volunteers/<id>/` | Get volunteer details |
| GET | `/api/events/` | List all events |
| GET | `/api/events/<id>/` | Get event details |
| GET | `/api/stats/` | Dashboard statistics |

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Raj Devvanshi**

Built with ❤️ for NayePankh Foundation
