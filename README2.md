# Django Middleware Learning Project: Airbnb Clone Backend

## 📜 Table of Contents
* [Project Overview](#1-project-overview)
* [Team Roles and Responsibilities](#2-team-roles-and-responsibilities)
* [Technology Stack Overview](#3-technology-stack-overview)
* [Database Design Overview](#4-database-design-overview)
* [Feature Breakdown](#5-feature-breakdown)
* [API Security Overview](#6-api-security-overview)
* [CI/CD Pipeline Overview](#7-cicd-pipeline-overview)
* [Resources](#8-resources)
* [License](#9-license)
* [Created By](#10-created-by)

---

## 1. Project Overview

**Brief Description:**

This project is a comprehensive learning platform designed to teach Django middleware concepts through hands-on implementation in an Airbnb Clone backend application. It demonstrates how middleware acts as a powerful bridge between the request and response phases of the application cycle, enabling cross-cutting concerns such as authentication, logging, rate limiting, and request/response modification to be handled in a clean, modular way.

The project showcases best practices in middleware design, including request interception, permission enforcement, data filtering, and real-world use cases like IP blocking and JSON payload validation. Learners gain practical experience in building a scalable, well-architected Django application with a focus on separation of concerns and modular backend development.

**Project Goals:**
* Build a modular Django application with custom middleware components for an Airbnb Clone platform
* Implement request/response interception and modification at the middleware level
* Create access control mechanisms using middleware for role-based and IP-based restrictions
* Develop logging and auditing capabilities for request/response tracking
* Apply rate limiting and request validation using middleware
* Demonstrate clean architecture principles through separation of concerns
* Provide a scalable project structure following Django best practices

**Key Tech Stack:**
* **Backend Framework:** Django 4.0
* **Database:** PostgreSQL (with psycopg2 binary driver)
* **Environment Management:** python-dotenv for configuration
* **Language:** Python 3.10+

---

## 2. Team Roles and Responsibilities

| Role | Key Responsibility |
|------|-------------------|
| **Backend Developer** | Design and implement custom middleware components, develop core business logic, create models and views, ensure proper middleware ordering and integration |
| **Database Administrator** | Design database schema for Users, Listings, Bookings, and Reviews; optimize queries; manage PostgreSQL database configuration and migrations |
| **DevOps Engineer** | Set up CI/CD pipelines, manage environment configurations, containerize the application with Docker, deploy to production environments, monitor system health |
| **Security Engineer** | Implement security middleware (authentication, rate limiting, IP blocking), conduct security audits, ensure compliance with OWASP standards, manage secrets and environment variables |
| **QA Engineer** | Write comprehensive tests for middleware behavior, create test cases for edge cases and security scenarios, perform integration testing, validate middleware ordering and execution |
| **Technical Documentation Specialist** | Document middleware functionality, maintain API documentation, create inline code comments, write user guides and developer onboarding materials |

---

## 3. Technology Stack Overview

| Technology | Purpose in the Project |
|-----------|----------------------|
| **Python 3.10+** | Primary programming language for backend development, providing modern syntax and performance improvements |
| **Django 4.0** | Web framework that provides the foundation for the application, including ORM, middleware stack, authentication, and admin interface |
| **PostgreSQL** | Production-grade relational database for storing users, listings, bookings, reviews, and audit logs with ACID compliance |
| **psycopg2-binary** | PostgreSQL adapter for Python, enabling Django to communicate with PostgreSQL database |
| **python-dotenv** | Environment variable management for securely handling configuration secrets (database credentials, API keys) across development and production |
| **Django Middleware Stack** | Built-in middleware components for security, session management, CSRF protection, authentication, and common request/response processing |
| **Django ORM** | Object-Relational Mapping for database queries, supporting complex lookups with Q objects and efficient data retrieval |
| **Django Signals** | Event-driven architecture for decoupling applications, enabling notifications when specific events occur (e.g., user registration, booking creation) |
| **Django Admin** | Built-in administrative interface for managing database records and monitoring application state |

---

## 4. Database Design Overview

**Key Entities:**

* **User** - Stores user account information including authentication credentials, profile data, and role assignments (guest, host, admin)
* **Listing** - Represents properties available for booking, containing details like title, description, location, price, amenities, and host relationship
* **Booking** - Records reservation information linking users to listings with check-in/check-out dates, guest count, and booking status
* **Review** - Captures user feedback on listings and hosts, including ratings, comments, and timestamps
* **AuditLog** - Tracks request/response metadata for debugging and security monitoring, including IP addresses, user agents, and timestamps
* **BannedIP** - Maintains a list of blocked IP addresses for security and access control

**Relationships:**

* **User to Listing (One-to-Many):** A single User (as a host) can create and manage multiple Listings. Each Listing belongs to one host User.
* **User to Booking (One-to-Many):** A User (as a guest) can make multiple Bookings. Each Booking is associated with one guest User.
* **Listing to Booking (One-to-Many):** A Listing can have multiple Bookings over time. Each Booking is for one specific Listing, creating a reservation history.
* **User to Review (One-to-Many):** A User can write multiple Reviews for different stays. Each Review is authored by one User.
* **Listing to Review (One-to-Many):** A Listing can receive multiple Reviews from different guests. Each Review is associated with one Listing.

---

## 5. Feature Breakdown

* **Custom Request Logging Middleware:** Automatically logs incoming requests and outgoing responses with metadata including timestamp, HTTP method, path, status code, and execution time. This feature provides comprehensive audit trails for debugging and security analysis without cluttering view logic.

* **Authentication Enforcement Middleware:** Ensures that specific routes are accessible only to authenticated users by intercepting requests before they reach views. This middleware validates user sessions and redirects unauthenticated users to the login page, centralizing authentication logic.

* **Role-Based Access Control (RBAC) Middleware:** Implements permission enforcement based on user roles (guest, host, admin). It checks user roles against required permissions for specific endpoints, preventing unauthorized access to administrative or host-specific functionalities.

* **IP Blocking Middleware:** Protects the application from malicious traffic by blocking requests from banned IP addresses or suspicious headers. This security layer prevents access from known bad actors and can be dynamically updated without changing view code.

* **Rate Limiting Middleware:** Enforces API usage policies by limiting the number of requests from a single IP or user within a time window. This prevents abuse, protects against DDoS attacks, and ensures fair resource allocation across all users.

* **JSON Payload Validation Middleware:** Validates and sanitizes incoming JSON payloads before they reach view functions. This middleware ensures data integrity, prevents malformed requests from causing errors, and can enforce schema validation rules.

* **Request Data Filtering Middleware:** Cleans and normalizes incoming request data, removing potentially harmful content, standardizing formats, and preparing data for processing by views and serializers.

* **Response Modification Middleware:** Adds custom headers to outgoing responses, such as security headers (CORS, CSP), API version information, or custom metadata, ensuring consistent response formatting across the application.

* **Performance Monitoring Middleware:** Tracks request processing time and can log slow requests for performance optimization. This helps identify bottlenecks and optimize critical paths in the application.

* **Error Handling Middleware:** Provides centralized exception handling and error formatting, converting Python exceptions into user-friendly JSON error responses with appropriate HTTP status codes.

---

## 6. API Security Overview

**Key Security Measures:**

* **Authentication Middleware:** Verifies user identity through session tokens or JWT authentication before granting access to protected resources. This is crucial because it ensures that only legitimate, logged-in users can access sensitive data and perform actions on their behalf, preventing unauthorized access and data breaches.

* **Rate Limiting:** Restricts the number of API requests per user or IP address within a specified time window (e.g., 100 requests per hour). This is essential to prevent brute force attacks, credential stuffing, DDoS attacks, and resource exhaustion, ensuring service availability for all legitimate users.

* **Input Validation and Sanitization:** Validates all incoming data against expected schemas and sanitizes user input to remove potentially harmful content. This prevents injection attacks (SQL, XSS, command injection), ensures data integrity, and protects against malformed requests that could crash the application.

* **IP Blocking and Geofencing:** Maintains a blocklist of banned IP addresses and can restrict access based on geographic location. This is crucial for blocking known malicious actors, preventing access from high-risk regions, and complying with regional data protection regulations.

* **CSRF Protection:** Django's built-in CSRF middleware protects against Cross-Site Request Forgery attacks by requiring valid CSRF tokens for state-changing operations. This prevents attackers from tricking users into performing unwanted actions on the application.

* **Secure Headers:** Middleware adds security headers like Content-Security-Policy, X-Frame-Options, and Strict-Transport-Security to responses. These headers protect against clickjacking, XSS attacks, and ensure connections use HTTPS, providing defense-in-depth security.

* **SQL Injection Prevention:** Django ORM automatically parameterizes queries, and middleware can perform additional validation to ensure no raw SQL injection attempts pass through. This prevents one of the most common and dangerous attack vectors.

* **Secrets Management:** Sensitive configuration (database passwords, API keys) is stored in environment variables using python-dotenv, never hardcoded in source code. This prevents credential leakage through version control and allows different secrets for different environments.

* **Audit Logging:** All authenticated actions and security-relevant events are logged with user identification, timestamp, and action details. This enables security monitoring, incident response, compliance reporting, and forensic analysis when security incidents occur.

---

## 7. CI/CD Pipeline Overview

Continuous Integration and Continuous Deployment (CI/CD) is a modern software development practice that automates the process of testing, building, and deploying code changes. For this Django middleware learning project, CI/CD ensures that every code change is automatically validated, tested, and potentially deployed to various environments without manual intervention.

The CI/CD strategy for this project involves:

**Continuous Integration:**
* Automated testing runs on every commit and pull request using GitHub Actions or similar CI platforms
* Code quality checks including linting (pylint, flake8), style enforcement (black), and security scanning (bandit)
* Unit tests for individual middleware components and integration tests for the full middleware stack
* Database migration validation to catch schema conflicts early
* Test coverage reporting to ensure comprehensive test suites

**Continuous Deployment:**
* Automated deployment to staging environments after successful CI pipeline completion
* Environment-specific configuration management using environment variables and .env files
* Docker containerization for consistent deployment across environments
* Database backup automation before production deployments
* Rollback mechanisms to quickly revert problematic deployments

**Tools and Technologies:**
* **GitHub Actions** for automated workflow execution on code events
* **Docker** for containerizing the Django application and ensuring environment consistency
* **PostgreSQL** migrations managed through Django's migration system
* **Environment variables** for configuration across dev, staging, and production
* **Automated testing frameworks** including Django's test client and pytest

This CI/CD approach ensures rapid, reliable delivery of new features and bug fixes while maintaining code quality and system stability. It reduces manual errors, speeds up the development cycle, and provides confidence that changes work as expected before reaching production users.

---

## 8. Resources

* **Django Official Documentation:** [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
* **Django Middleware Documentation:** [https://docs.djangoproject.com/en/4.0/topics/http/middleware/](https://docs.djangoproject.com/en/4.0/topics/http/middleware/)
* **PostgreSQL Documentation:** [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
* **Django Signals Documentation:** [https://docs.djangoproject.com/en/4.0/topics/signals/](https://docs.djangoproject.com/en/4.0/topics/signals/)
* **Django ORM Query Documentation:** [https://docs.djangoproject.com/en/4.0/topics/db/queries/](https://docs.djangoproject.com/en/4.0/topics/db/queries/)
* **Django Security Best Practices:** [https://docs.djangoproject.com/en/4.0/topics/security/](https://docs.djangoproject.com/en/4.0/topics/security/)
* **OWASP Top 10 Web Application Security Risks:** [https://owasp.org/www-project-top-ten/](https://owasp.org/www-project-top-ten/)
* **Twelve-Factor App Methodology:** [https://12factor.net/](https://12factor.net/)
* **Django REST Framework (for API development):** [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
* **Python dotenv Documentation:** [https://github.com/theskumar/python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 9. License

This project is licensed under the **MIT License**.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 10. Created By

**Phinehas Macharia**

*Full-Stack Developer & Django Middleware Architect*

This learning project was developed as part of a comprehensive Django middleware curriculum, demonstrating best practices in web application architecture, security implementation, and clean code design. For questions, contributions, or feedback, please reach out through the repository's issue tracker or pull request system.
