# OWASP Top 10 Vulnerabilities Demo

This project demonstrates the OWASP Top 10 Web Application Security Risks with both vulnerable and secure implementations using Flask.

## Setup Instructions

### Environment Setup

1. Create a conda environment using the provided configuration:

```bash
conda env create -f environment.yml
conda activate owasp_env
```

2. Initialize the database:

```bash
python database_setup.py
```

3. Run the application:

```bash
python app.py
```

## OWASP Top 10 Demonstrations

The application includes examples of both vulnerable and secure implementations for:

- **A01:2021 - Broken Access Control**

  - Vulnerable: `/user/<username>`
  - Secure: `/user_secure`

- **A02:2021 - Cryptographic Failures**

  - Vulnerable: `/register`
  - Secure: `/register_secure`

- **A03:2021 - Injection**

  - Vulnerable: `/login`
  - Secure: `/login_secure`

- **A04:2021 - Insecure Design**

  - Vulnerable: `/checkout`
  - Secure: `/checkout_secure`

- **A05:2021 - Security Misconfiguration**

  - Vulnerable: `/debug`
  - Secure: `/debug_secure`

- **A06:2021 - Vulnerable and Outdated Components**

  - Vulnerable: `/legacy`
  - Secure: `/legacy_secure`

- **A07:2021 - Identification and Authentication Failures**

  - Vulnerable: `/admin`
  - Secure: `/admin_secure`

- **A08:2021 - Software and Data Integrity Failures**

  - Vulnerable: `/update`
  - Secure: `/update_secure`

- **A09:2021 - Security Logging and Monitoring Failures**

  - Vulnerable: `/login_attempt`
  - Secure: `/login_attempt_secure`

- **A10:2021 - Server-Side Request Forgery (SSRF)**
  - Vulnerable: `/fetch`
  - Secure: `/fetch_secure`

## Project Structure

```
├── app.py               # Main application with vulnerable and secure implementations
├── database_setup.py    # Database initialization script
├── requirements.txt     # Python package requirements
├── environment.yml      # Conda environment configuration
└── README.md            # Project documentation
```

## Warning

The vulnerable implementations are for educational purposes only. Do not use them in production environments.

This README provides clear setup instructions and documents all the OWASP Top 10 vulnerabilities demonstrated in the application, along with their corresponding endpoints.
