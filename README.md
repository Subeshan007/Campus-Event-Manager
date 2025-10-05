# 🎓 Campus Event Manager# Campus-Event-Manager

Campus Event Manager is a digital platform that simplifies planning and participation in campus activities. It enables event creation, online registration, notifications, and real-time updates. Students can explore and join events easily, while organizers manage schedules, track participants, and analyze feedback efficiently.

A comprehensive web-based platform for **Sri Manakula Vinayagar Engineering College (SMVEC)** to streamline campus event management with three distinct user portals, modern authentication, and real-time analytics.

![SMVEC Events](https://img.shields.io/badge/SMVEC-Events%20Management-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Firebase](https://img.shields.io/badge/Firebase-Authentication-orange)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-Educational-yellow)

## 🚀 Live Demo

**[🌐 View Live Application](YOUR_DEPLOYMENT_LINK_HERE)**

> Deploy on: Replit, Heroku, AWS, Google Cloud, or any Python hosting platform

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [User Portals](#user-portals)
- [Security](#security)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)

## 🏛️ Overview

The **Campus Event Manager** is a full-featured event management system designed specifically for Sri Manakula Vinayagar Engineering College. It facilitates seamless interaction between students, event organizers, and administrators through role-based access control and comprehensive features.

### 🎯 Purpose

- **Centralized Event Discovery** - Students find and register for campus events easily
- **Simplified Event Creation** - Organizers create and manage events with approval workflows
- **Administrative Oversight** - Admins maintain quality control and system analytics
- **Enhanced Engagement** - Foster campus community through organized events

### ✨ Key Highlights

- 🔐 **Multi-Portal Architecture** - Separate interfaces for students, organizers, and admins
- 🔥 **Firebase Authentication** - Google Sign-in + traditional registration
- 📊 **Real-Time Analytics** - Comprehensive dashboards for all user types
- 📱 **Mobile Responsive** - Works seamlessly on all devices
- 🎫 **QR Code Check-in** - Automated attendance tracking system
- 📧 **Email Notifications** - Automated updates and reminders
- 🖼️ **Image Upload** - Event promotional images with secure handling
- 📈 **Event Lifecycle** - Complete workflow from creation to completion

## ✨ Features

### 👨‍🎓 Student Portal

- **Event Discovery**
  - Browse all approved campus events
  - Filter by category, date, and department
  - Search functionality for quick access
  - View event details, capacity, and pricing

- **Event Registration**
  - One-click event registration
  - View registration confirmation
  - Automatic capacity management
  - Email confirmation notifications

- **Personal Dashboard**
  - View registered events
  - Track attendance history
  - Access QR codes for check-in
  - Submit event feedback and ratings

- **Profile Management**
  - Update personal information
  - Register number and department details
  - View registration statistics
  - Notification preferences

### 📋 Organizer Portal

- **Event Creation**
  - Create events with rich details
  - Upload promotional images
  - Set capacity limits and pricing
  - Define event categories and tags

- **Event Management**
  - Edit event details (before approval)
  - Monitor registration numbers
  - Generate attendance reports
  - Cancel or postpone events

- **Attendance Tracking**
  - QR code generation for each event
  - Scan student QR codes for check-in
  - Real-time attendance tracking
  - Export attendance sheets

- **Analytics Dashboard**
  - Registration trends and metrics
  - Attendance rate analysis
  - Event performance comparison
  - Feedback and ratings overview

- **Communication**
  - Send notifications to registered students
  - Automated reminder emails
  - Post-event feedback collection
  - Direct messaging capabilities

### 👔 Administrator Portal

- **User Management**
  - View all users (students, organizers, admins)
  - Approve/reject organizer registrations
  - Manage user roles and permissions
  - Deactivate or delete accounts

- **Event Oversight**
  - Review pending events for approval
  - Approve or reject event submissions
  - Edit any event details
  - Archive completed events

- **System Analytics**
  - Platform usage statistics
  - User registration trends
  - Event performance metrics
  - Category-wise analytics

- **Content Moderation**
  - Review event descriptions
  - Manage inappropriate content
  - Monitor feedback and ratings
  - Handle reported issues

- **System Configuration**
  - Manage event categories
  - Configure notification templates
  - Set system-wide policies
  - Database maintenance tools

### 🔔 Notification System

- **In-App Notifications**
  - Real-time updates
  - Registration confirmations
  - Event reminders
  - Status changes

- **Email Notifications**
  - Welcome emails
  - Event confirmations
  - Reminder emails (24 hours before)
  - Cancellation notices

### 💬 Feedback System

- **Event Ratings**
  - 5-star rating system
  - Written feedback and comments
  - Anonymous submission option
  - Aggregate ratings display

- **Analytics Integration**
  - Organizer feedback dashboard
  - Trend analysis
  - Improvement suggestions
  - Response management

## 🛠️ Technology Stack

### Backend Framework
- **Flask 2.3.3** - Lightweight Python web framework
- **Werkzeug 2.3.7** - WSGI utilities and security
- **Gunicorn 21.2.0** - Production WSGI server
- **Python 3.8+** - Core programming language

### Database & ORM
- **PostgreSQL** - Relational database system
- **SQLAlchemy 3.0.5** - Python SQL toolkit and ORM
- **psycopg2-binary 2.9.7** - PostgreSQL adapter

### Authentication & Security
- **Firebase Authentication** - Google OAuth integration
- **Werkzeug Security** - Password hashing (scrypt algorithm)
- **Session Management** - Secure Flask sessions
- **CSRF Protection** - Cross-site request forgery prevention

### Frontend Technologies
- **HTML5/CSS3** - Modern web standards
- **Bootstrap 5.3.0** - Responsive UI framework
- **Jinja2** - Server-side template engine
- **Font Awesome 6.4.0** - Icon library
- **Chart.js** - Data visualization
- **Vanilla JavaScript** - Client-side interactivity

### Additional Libraries
- **qrcode[pil] 7.4.2** - QR code generation
- **email-validator 2.0.0** - Email validation
- **python-dotenv** - Environment variable management
- **Pillow** - Image processing

### Development Tools
- **Git** - Version control
- **pip** - Package management
- **Virtual Environment** - Dependency isolation

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Web Browser                             │
│        (Student / Organizer / Admin Interfaces)                 │
└────────────────────┬────────────────────────────────────────────┘
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Flask Application                            │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │   Auth       │  │  Student     │  │  Organizer         │   │
│  │   Routes     │  │  Routes      │  │  Routes            │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │   Admin      │  │  Utils       │  │  Models            │   │
│  │   Routes     │  │  Functions   │  │  (SQLAlchemy)      │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└────────────┬──────────────────────────────┬────────────────────┘
             │                              │
             ▼                              ▼
┌──────────────────────────┐    ┌────────────────────────────┐
│  Firebase Authentication │    │   PostgreSQL Database      │
│  ┌────────────────────┐  │    │  ┌──────────────────────┐ │
│  │  Google OAuth      │  │    │  │  Users               │ │
│  │  Email/Password    │  │    │  │  Events              │ │
│  │  Session Tokens    │  │    │  │  Registrations       │ │
│  └────────────────────┘  │    │  │  Feedback            │ │
└──────────────────────────┘    │  │  Notifications       │ │
                                │  └──────────────────────┘ │
                                └────────────────────────────┘
```

### Data Models

#### **User Model**
- `id` - Primary key
- `email` - Unique email address
- `password_hash` - Encrypted password
- `full_name` - User's full name
- `role` - student/organizer/admin
- `register_number` - Student ID (students only)
- `department` - Academic department
- `is_approved` - Organizer approval status
- `created_at` - Registration timestamp

#### **Event Model**
- `id` - Primary key
- `title` - Event name
- `description` - Detailed description
- `organizer_id` - Foreign key to User
- `venue` - Event location
- `date` - Event date
- `time` - Event time
- `category` - Event type
- `capacity` - Maximum participants
- `current_registrations` - Enrolled count
- `image_url` - Promotional image path
- `status` - pending/approved/rejected
- `is_paid` - Free or paid event
- `price` - Ticket price
- `qr_code` - Check-in QR code
- `created_at` - Creation timestamp

#### **Registration Model**
- `id` - Primary key
- `event_id` - Foreign key to Event
- `user_id` - Foreign key to User
- `registered_at` - Registration timestamp
- `attended` - Check-in status
- `attended_at` - Check-in timestamp

#### **Feedback Model**
- `id` - Primary key
- `event_id` - Foreign key to Event
- `user_id` - Foreign key to User
- `rating` - 1-5 stars
- `comment` - Written feedback
- `is_anonymous` - Privacy flag
- `created_at` - Submission timestamp

#### **Notification Model**
- `id` - Primary key
- `user_id` - Foreign key to User
- `message` - Notification text
- `type` - info/warning/success
- `is_read` - Read status
- `created_at` - Timestamp

## 📦 Installation

### Prerequisites

- **Python 3.8+** installed
- **PostgreSQL 12+** database server
- **Git** for version control
- **pip** package manager
- **Firebase Account** (for authentication)

### Quick Start (Automated Setup)

```bash
# 1. Clone the repository
git clone https://github.com/Subeshan007/Campus-Event-Manager.git
cd Campus-Event-Manager/CampusEventManager

# 2. Run automated setup
python setup.py
```

The setup script will:
- ✅ Install all Python dependencies
- ✅ Create necessary directories
- ✅ Set up environment variables
- ✅ Initialize the database
- ✅ Create default admin account
- ✅ Generate session secrets

### Manual Installation

#### Step 1: Clone Repository

```bash
git clone https://github.com/Subeshan007/Campus-Event-Manager.git
cd Campus-Event-Manager/CampusEventManager
```

#### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install flask==2.3.3
pip install werkzeug==2.3.7
pip install gunicorn==21.2.0
pip install psycopg2-binary==2.9.7
pip install flask-sqlalchemy==3.0.5
pip install email-validator==2.0.0
pip install qrcode[pil]==7.4.2
pip install python-dotenv
pip install pillow
```

Or create a `requirements.txt`:

```text
flask==2.3.3
werkzeug==2.3.7
gunicorn==21.2.0
psycopg2-binary==2.9.7
flask-sqlalchemy==3.0.5
email-validator==2.0.0
qrcode[pil]==7.4.2
python-dotenv
pillow
```

Then install:
```bash
pip install -r requirements.txt
```

#### Step 4: Setup PostgreSQL Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE smvec_events;

# Grant permissions (if needed)
GRANT ALL PRIVILEGES ON DATABASE smvec_events TO your_user;
```

#### Step 5: Create .env File

Create a `.env` file in the `CampusEventManager` directory:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-here
DEBUG=True
FLASK_ENV=development

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/smvec_events

# Firebase Configuration
FIREBASE_API_KEY=your-firebase-api-key
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_APP_ID=your-firebase-app-id
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Application Settings
UPLOAD_FOLDER=static/uploads
MAX_FILE_SIZE=5242880  # 5MB in bytes
```

#### Step 6: Create Required Directories

```bash
mkdir -p static/uploads
mkdir -p static/css
mkdir -p static/js
mkdir -p static/qrcodes
```

#### Step 7: Initialize Database

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...     exit()
```

#### Step 8: Create Default Admin

```python
python
>>> from app import app, db
>>> from models import User
>>> from werkzeug.security import generate_password_hash
>>> 
>>> with app.app_context():
...     admin = User(
...         email='admin@smvec.ac.in',
...         password_hash=generate_password_hash('admin123'),
...         full_name='System Administrator',
...         role='admin',
...         is_approved=True
...     )
...     db.session.add(admin)
...     db.session.commit()
...     print("Admin created successfully!")
```

## ▶️ Running the Application

### Development Mode

```bash
cd CampusEventManager
python main.py
```

The application will start at `http://127.0.0.1:5000`

### Production Mode

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --reuse-port main:app
```

### Using Replit

1. Import the repository to Replit
2. Set environment variables in Replit Secrets
3. Click "Run" button
4. Access via Replit's provided URL

## ⚙️ Configuration

### Firebase Setup

1. **Create Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Add Project"
   - Enter project name: "SMVEC Campus Events"

2. **Enable Google Authentication**
   - Navigate to Authentication → Sign-in method
   - Enable Google provider
   - Configure OAuth consent screen

3. **Get Firebase Credentials**
   - Go to Project Settings → General
   - Under "Your apps", click Web app icon
   - Copy API Key, Project ID, App ID
   - Add to `.env` file

4. **Configure Authorized Domains**
   - In Firebase Console: Authentication → Settings
   - Add your domain to Authorized domains list

### Database Configuration

**PostgreSQL Connection String Format:**
```
postgresql://username:password@host:port/database_name
```

**Example:**
```
DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/smvec_events
```

### Email Configuration (Optional)

For Gmail SMTP:
1. Enable 2-Factor Authentication
2. Generate App Password
3. Use App Password in `.env` file

## 👥 Usage Guide

### Default Administrator Login

```
Email: admin@smvec.ac.in
Password: admin123
```

⚠️ **Important:** Change the default password immediately after first login!

### Student Registration

1. **Visit Homepage** - Navigate to `http://localhost:5000`
2. **Click "Register"** - Select "Student" role
3. **Fill Registration Form:**
   - Full Name
   - Email Address
   - Register Number (e.g., 20CS001)
   - Department
   - Password (min 8 characters)
4. **Alternative:** Use "Sign in with Google"

### Organizer Registration

1. **Click "Register as Organizer"** - Select "Organizer" role
2. **Provide Details** - Full name, email, organization, password
3. **Wait for Approval** - Admin reviews and approves your request
4. **Login** - Once approved, access organizer features

### Creating an Event (Organizer)

1. Login to organizer portal
2. Click "Create Event"
3. Fill event details (title, description, venue, date, time, capacity)
4. Upload promotional image
5. Submit for approval
6. Track registrations after approval

### Event Approval (Admin)

1. Login to admin portal
2. View "Pending Events"
3. Review event details
4. Approve or reject with reason
5. Monitor approved events

### Registering for Events (Student)

1. Browse events on homepage
2. Click event card to view details
3. Click "Register" button
4. Receive confirmation email
5. Access QR code in "My Events"

### Attendance Tracking (Organizer)

1. Open your event page
2. Access "Check-in" section
3. Scan student QR codes
4. Mark attendance automatically
5. Export attendance sheet

## 🔐 Security Features

### Password Security
- **Scrypt Hashing** - Industry-standard password hashing
- **Salt Generation** - Unique salt for each password
- **No Plain Text** - Passwords never stored in plain text

### Session Management
- **Secure Cookies** - HTTPOnly and Secure flags
- **Session Timeout** - Auto-logout after inactivity
- **CSRF Protection** - Token-based protection

### File Upload Security
- **File Type Validation** - Only images allowed
- **Size Restrictions** - Max 5MB per file
- **Filename Sanitization** - Prevent path traversal
- **Secure Storage** - Protected upload directory

### Access Control
- **Role-Based Permissions** - Three distinct user roles
- **Route Protection** - Login required decorators
- **Authorization Checks** - Users access only their data

### Database Security
- **Parameterized Queries** - SQL injection prevention
- **ORM Usage** - SQLAlchemy security
- **Connection Pooling** - Efficient management
- **Encrypted Connections** - SSL/TLS for database

## 🚀 Deployment

### Deploy to Replit (Easiest)

1. Fork repository to Replit
2. Configure Secrets (environment variables)
3. Click "Run"
4. Access via Replit URL

### Deploy to Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create smvec-campus-events

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FIREBASE_API_KEY=your-firebase-key

# Deploy
git push heroku main

# Initialize database
heroku run python
```

### Deploy to AWS EC2

1. Launch Ubuntu 22.04 EC2 instance
2. Install Python, PostgreSQL, Nginx
3. Clone repository and setup
4. Configure Nginx reverse proxy
5. Setup systemd service for auto-start

### Deploy to Google Cloud

```bash
# Create app.yaml
runtime: python39
entrypoint: gunicorn -b :$PORT main:app

# Deploy
gcloud app deploy
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
- Check PostgreSQL is running
- Verify DATABASE_URL in `.env`
- Test: `psql -U postgres -d smvec_events`

**Firebase Authentication Fails**
- Verify Firebase credentials in `.env`
- Ensure Authentication is enabled
- Check authorized domains

**File Upload Fails**
- Check MAX_FILE_SIZE setting
- Verify upload directory permissions
- Confirm file type (JPG, PNG only)

**Email Not Sending**
- Use Gmail App Password
- Check SMTP settings
- Verify firewall allows SMTP

**Module Not Found**
- Activate virtual environment
- Run `pip install -r requirements.txt`

## 📊 Analytics & Reports

### Student Analytics
- Personal event history
- Attendance statistics
- Department participation
- Feedback trends

### Organizer Analytics
- Event performance metrics
- Registration rates
- Attendance tracking
- Feedback ratings

### Administrator Analytics
- Platform usage stats
- User growth trends
- Event approval rates
- System health metrics

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes with clean, documented code
4. Commit: `git commit -m "Add: Amazing feature"`
5. Push: `git push origin feature/amazing-feature`
6. Create Pull Request

### Code Standards

- **Python**: PEP 8 compliance
- **Docstrings**: All functions documented
- **Comments**: Explain complex logic
- **Testing**: Unit tests for new features
- **Security**: No hardcoded credentials

## 📞 Support

### Get Help

- 📧 **GitHub Issues**: [Report bugs or request features](https://github.com/Subeshan007/Campus-Event-Manager/issues)
- 📖 **Documentation**: This README and code comments
- 💬 **Discussions**: GitHub Discussions for questions

### Institution Contact

**Sri Manakula Vinayagar Engineering College**
- 📍 Madagadipet, Puducherry - 605107, India
- 🌐 Website: [smvec.ac.in](https://smvec.ac.in)
- 📧 Email: principal@smvec.ac.in
- ☎️ Phone: +91-413-2610101

## 📄 License

This project is developed for **Sri Manakula Vinayagar Engineering College** for educational and institutional use.

## 🙏 Acknowledgments

- **SMVEC Administration** - Vision and support
- **Faculty Advisors** - Guidance and feedback
- **Student Community** - Testing and suggestions
- **Open Source Community** - Libraries and tools
- **Firebase** - Authentication services
- **PostgreSQL** - Database system
- **Flask Community** - Web framework

## 👨‍💻 Author

**Subeshan**

- GitHub: [@Subeshan007](https://github.com/Subeshan007)
- Repository: [Campus-Event-Manager](https://github.com/Subeshan007/Campus-Event-Manager)

## ⚠️ Disclaimer

This application is for campus event management at SMVEC. Users are responsible for accurate information, privacy protection, following institutional policies, and maintaining appropriate content.

## 🔮 Future Enhancements

- [ ] Mobile app (React Native/Flutter)
- [ ] Push notifications
- [ ] ML-powered event recommendations
- [ ] College ERP integration
- [ ] Payment gateway integration
- [ ] Calendar sync (Google Calendar)
- [ ] Social media sharing
- [ ] Event live streaming
- [ ] Certificate generation
- [ ] Multi-language support
- [ ] Dark mode theme
- [ ] Advanced analytics with predictions

---

<div align="center">

**🎓 Empowering Campus Life Through Technology 🎓**

**Made with ❤️ for Sri Manakula Vinayagar Engineering College**

⭐ Star this repo if you find it helpful!

[Report Bug](https://github.com/Subeshan007/Campus-Event-Manager/issues) | [Request Feature](https://github.com/Subeshan007/Campus-Event-Manager/issues) | [Documentation](#)

</div>
