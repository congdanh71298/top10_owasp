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

## OWASP Top 10 2021 Implementations

### A01: Broken Access Control
- Login required for dashboard access
- Todo items restricted to owners only
- Audit logging of user actions

### A02: Cryptographic Failures
- Task encryption implemented
- Password hashing enforced

### A03: Injection
- Django prepared statements
- Input validation for email fields

### A04: Insecure Design
- Rate limiting on views
- Security tests available:
```bash
python -m pytest todo_app/tests/test_security.py -v
```

### A05: Security Misconfiguration
- HSTS and security headers enabled
- Environment variables for sensitive data

### A06: Vulnerable Components
- Dependencies checked via:
```bash
safety check
npm audit
```

### A07: Authentication Failures
- Password strength validation
- Account lockout protection

### A08: Data Integrity
- SRI checks for external resources
- Pinned dependency versions

### A09: Security Logging
- Comprehensive audit logging

### A10: SSRF Protection
- URL whitelist implementation
