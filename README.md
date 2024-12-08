# OWASP Top 10 Vulnerabilities Demo with Django

This project demonstrates the OWASP Top 10 Web Application Security Risks with both vulnerable and secure implementations using Django.

## Setup Instructions

### Environment Setup

1. Create a conda environment using the provided configuration:
```bash
conda env create -f environment.yml
conda activate owasp_env
```

### Database Setup
1. Run database migrations
2. Create a superuser (optional)

### Running the Application
1. Start the Django development server
2. Access the application:
  - Main app: http://localhost:8000/todo_app/
  - Login: http://localhost:8000/todo_app/login/
  - Register: http://localhost:8000/todo_app/register/

## Features
- User registration and authentication
- Todo list management (create, read, update, delete)
- Task completion toggling
- Secure implementation of common web security features

## Security Features Demonstrated
- CSRF Protection
- SQL Injection Prevention
- XSS Protection
- Secure Authentication
- Session Security