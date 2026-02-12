🧠 NeuroVerse: Dynamic Quiz Portal
NeuroVerse is a feature-rich web application built to facilitate online assessments. It features a dual-portal system for administrators and students, utilizing a relational database to manage users, quizzes, and real-time responses.

🚀 Key Features
🔐 Security & Authentication
Admin Gatekeeping: Secure signup requires a specific Admin Access Key (NEURO2026) to prevent unauthorized access.

Password Hashing: Uses werkzeug.security for secure password storage and verification.

Session Management: Role-based access control (Admin vs. Student) ensures users only access their authorized dashboards.

🛠 Administrator Portal
Dynamic Quiz Publishing: Admins can create quizzes with multiple question types (MCQs or Text) and assign specific marks per question.

Option Mapping: A custom Jinja2 filter automatically converts numerical indices to character labels ('a', 'b', 'c', 'd') for a professional UI.

Response Management: View student scores and total marks directly from the admin dashboard.

📖 Student Portal
Self-Registration: Simple student signup and login interface.

Interactive Testing: Attempt quizzes and submit answers in real-time.

Auto-Grading: The system automatically calculates scores by comparing student input against stored correct answers.

🛠️ Tech Stack
Backend Framework: Flask

Database ORM: SQLAlchemy

Database Engine: SQLite

Security: Werkzeug Security (Hashing)

Templating: Jinja2

📊 Database Architecture
The application uses a structured SQLite schema with the following tables:

users: Stores credentials and roles (Admin/Student).

quizzes: Stores quiz titles and associated admin IDs.

questions: Manages question text, types, and correct answers.

options: Links multiple-choice options to specific questions.

responses: Tracks student scores and submission data.




Blue print of the structure files are as below : 

```
NeuroVerse/
├── neuro/                  # Your Virtual Environment (venv) 
│   ├── Include/
│   ├── Lib/
│   └── pyvenv.cfg          # Python 3.13.7 configuration 
├── instance/               # Flask-SQLAlchemy instance folder
│   └── database.db         # The SQLite database file
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css       # Custom styling for the portal
│   └── js/
│       └── scripts.js      # Frontend interactivity
├── templates/              # HTML Templates (Jinja2)
│   ├── admin_login.html    # Admin login portal
│   ├── admin_signup.html   # Admin registration with access key
│   ├── admin_dashboard.html# Quiz management hub
│   ├── create_quiz.html    # Dynamic quiz creation form
│   ├── student_dashboard.html # Quiz listing for students
│   ├── attempt_quiz.html   # The interface for taking a quiz
│   ├── user_login.html     # Student login
│   ├── user_signup.html    # Student signup
│   └── index.html          # Main landing page
├── .gitignore              # Files to exclude from Git (venv, .db, etc.) 
├── app.py                  # Main application logic and DB models
└── requirements.txt        # List of dependencies (Flask, Flask-SQLAlchemy)










