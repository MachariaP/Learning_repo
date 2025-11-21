# Django Middleware Project Guide 🚀
## Airbnb Clone & Web Application Middleware Implementation

## Overview

Middleware is a powerful feature in application design that acts as a bridge between the request and response phases of the application cycle. In this project, learners will explore the concept of middleware, learn how to write custom middleware, and implement logic such as request interception, permission enforcement, request data filtering, logging, and more. Learners will also examine real-world use cases, such as authentication and rate-limiting, and understand the best practices when integrating middleware into a Django application.

This hands-on project will guide you in building a series of middleware components for an Airbnb Clone or similar web application, allowing them to understand middleware's role in clean architecture and modular backend development.

---

## 🎯 Learning Objectives

By the end of this project, learners should be able to:

1. **Understand** the concept and lifecycle of middleware in Django
2. **Create** custom middleware to intercept and process incoming requests and outgoing responses
3. **Filter and modify** request/response data at the middleware level
4. **Implement** access control mechanisms using middleware
5. **Use middleware** to enforce API usage policies like rate limiting or request validation
6. **Integrate** third-party middleware and understand Django's default middleware stack
7. **Apply** best practices for organizing middleware logic in a scalable project

---

## 🎓 Learning Outcomes

Upon successful completion, learners will:

- ✅ Define and explain how Django middleware works within the request/response cycle
- ✅ Write and integrate custom middleware in a Django project
- ✅ Use middleware to enforce permissions and restrict access based on roles, IP, or headers
- ✅ Filter and clean incoming request data before reaching the views
- ✅ Log request and response metadata for auditing or debugging purposes
- ✅ Separate concerns effectively using middleware rather than overloading views
- ✅ Evaluate the trade-offs and limitations of using middleware for certain functionalities

---

## 📋 Implementation Tasks

Learners will:

### 1. Project Setup
- Scaffold a Django project with an `apps/core` structure for separation of concerns
- Set up proper directory structure for middleware organization
- Configure environment variables for different deployment scenarios

### 2. Build Custom Middleware

Create middleware components for:

#### a) **Request Logging Middleware**
- Log incoming requests with timestamp, method, path, and user information
- Log outgoing responses with status code and duration
- Store logs for auditing and debugging purposes

#### b) **Authentication & Authorization Middleware**
- Restrict access to authenticated users
- Enforce role-based access control (RBAC)
- Protect specific endpoints based on user permissions

#### c) **IP Blocking Middleware**
- Block requests from banned IP addresses
- Maintain whitelist/blacklist of IPs
- Handle requests from suspicious headers

#### d) **Request Validation Middleware**
- Modify or validate incoming JSON payloads
- Sanitize request data before processing
- Reject malformed requests early

#### e) **Rate Limiting Middleware**
- Implement request throttling per user/IP
- Prevent API abuse
- Return appropriate HTTP 429 responses

### 3. Configuration
- Configure the `MIDDLEWARE` stack correctly in `settings.py`
- Include both built-in and custom middleware
- Understand proper middleware ordering

### 4. Testing
- Test middleware behavior using Postman or Django's test client
- Verify interception, modification, and rejection of requests
- Write unit tests for middleware components

### 5. Documentation
- Document middleware behavior using inline comments
- Create Markdown files for clarity and maintainability
- Explain the purpose and configuration of each middleware

---

## 🏗️ Best Practices for Project Setup and Middleware Design

### 📁 Project Scaffolding Tips

**Recommended Structure:**
```
/project-root
  /apps
    /core
      /middleware
        __init__.py
        logging_middleware.py
        auth_middleware.py
        ip_blocker.py
        rate_limiter.py
        request_validator.py
      /models
      /views
    /users
    /listings
    /bookings
  /config
    settings.py
    urls.py
  manage.py
  .env
  requirements.txt
```

**Organization Tips:**
- Keep each custom middleware in a separate Python file under `apps/core/middleware/`
- Use descriptive file names that indicate the middleware's purpose
- Create an `__init__.py` to make the directory a proper Python package
- Use environment variables and Django settings to control behavior (e.g., toggle middleware for dev/production)

---

### 🎨 Middleware Design Best Practices

#### 1. **Keep Middleware Functions Small and Focused**
Avoid bloating a single middleware with multiple responsibilities.

❌ **Bad Example:**
```python
class AllInOneMiddleware:
    def __call__(self, request):
        # Authentication
        # Logging
        # Rate limiting
        # IP blocking
        # ... too much!
        pass
```

✅ **Good Example:**
```python
class AuthenticationMiddleware:
    """Handles only authentication logic"""
    def __call__(self, request):
        # Only authentication code here
        pass

class LoggingMiddleware:
    """Handles only logging logic"""
    def __call__(self, request):
        # Only logging code here
        pass
```

#### 2. **Chain Logic Properly**
Always call `get_response(request)` unless rejecting the request early.

```python
class MyMiddleware:
    def __call__(self, request):
        # Pre-processing
        if should_reject(request):
            return HttpResponseForbidden("Access Denied")
        
        # Process request
        response = self.get_response(request)
        
        # Post-processing
        return response
```

#### 3. **Use Django's Request Attributes**
Leverage `request.user`, `request.path`, and `request.method` for clean conditional logic.

```python
class RoleBasedMiddleware:
    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_staff:
                return HttpResponseForbidden("Staff only")
        
        return self.get_response(request)
```

#### 4. **Avoid Database-Heavy Logic**
Middleware runs on every request, so keep it fast!

❌ **Bad:**
```python
def __call__(self, request):
    all_users = User.objects.all()  # Slow!
    # ...
```

✅ **Good:**
```python
def __call__(self, request):
    if request.user.is_authenticated:
        user_cache = cache.get(f'user_{request.user.id}')  # Fast!
    # ...
```

#### 5. **Use Logging Middleware Responsibly**
Log minimal and relevant data to avoid clutter.

```python
import logging

logger = logging.getLogger(__name__)

class RequestLoggerMiddleware:
    def __call__(self, request):
        logger.info(f"{request.method} {request.path} - {request.user}")
        response = self.get_response(request)
        logger.info(f"Response: {response.status_code}")
        return response
```

#### 6. **Write Unit Tests for Middleware**
Test behavior and edge cases.

```python
from django.test import RequestFactory, TestCase

class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = MyMiddleware(get_response=lambda r: HttpResponse())
    
    def test_middleware_blocks_banned_ip(self):
        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = '192.168.1.100'  # Banned IP
        response = self.middleware(request)
        self.assertEqual(response.status_code, 403)
```

#### 7. **Document Each Middleware Clearly**
Explain what it does, why it exists, and where it sits in the stack.

```python
class IPBlockerMiddleware:
    """
    Blocks requests from blacklisted IP addresses.
    
    Purpose: Security - prevent access from known malicious IPs
    Position: Early in middleware stack (before authentication)
    Configuration: Set BLOCKED_IPS in settings.py
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_ips = getattr(settings, 'BLOCKED_IPS', [])
```

---

## ⚠️ Limitations and Considerations

While middleware can be powerful, it's important to recognize its limitations:

### What Middleware Should NOT Do

1. **Don't Replace Views or Serializers for Business Logic**
   - Middleware is for cross-cutting concerns
   - Business logic belongs in views, serializers, or service layers

2. **Avoid Heavy Computational Work**
   - Middleware runs on EVERY request
   - Poorly optimized code can degrade performance across the entire application

3. **Don't Ignore Middleware Ordering**
   - Order in `MIDDLEWARE` settings matters
   - Incorrect ordering may break expected behavior
   - Example: Authentication middleware must run before permission middleware

4. **Some Functionalities Are Better Elsewhere**
   - Input validation: Use Django forms or DRF serializers
   - Complex authentication: Use DRF permissions or decorators
   - View-specific logic: Use decorators or mixins

### Performance Considerations

```python
# ❌ Bad: Runs slow code on every request
class SlowMiddleware:
    def __call__(self, request):
        time.sleep(1)  # Delays every request!
        return self.get_response(request)

# ✅ Good: Fast and efficient
class FastMiddleware:
    def __call__(self, request):
        # Quick check
        if condition:
            return self.get_response(request)
        return HttpResponseForbidden()
```

### When to Use Alternatives

| Use Case | Use Middleware | Use Instead |
|----------|---------------|-------------|
| Log all requests | ✅ Yes | - |
| Authenticate user | ✅ Yes | - |
| Block IP addresses | ✅ Yes | - |
| Validate specific form | ❌ No | Django Forms |
| Protect single view | ❌ No | `@login_required` decorator |
| DRF endpoint permissions | ❌ No | DRF Permission Classes |
| Complex business logic | ❌ No | Service Layer |

---

## 🧪 Testing Your Middleware

### Using Django Test Client

```python
from django.test import TestCase, Client

class MiddlewareIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_rate_limiting(self):
        # Make 100 requests
        for i in range(100):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
        
        # 101st request should be rate limited
        response = self.client.get('/')
        self.assertEqual(response.status_code, 429)
```

### Using Postman

1. **Test Request Logging:**
   - Send GET/POST requests to various endpoints
   - Check server logs for logged information

2. **Test IP Blocking:**
   - Configure blocked IP in settings
   - Use Postman's proxy settings or modify headers
   - Verify 403 Forbidden response

3. **Test Rate Limiting:**
   - Send rapid successive requests
   - Verify rate limit headers in response
   - Confirm 429 status after threshold

4. **Test Authentication:**
   - Send requests without auth token
   - Verify 401 Unauthorized response
   - Send with valid token, verify 200 OK

---

## 📝 Project Assessment (Hybrid)

Your project will be evaluated primarily through manual reviews. To ensure you receive your full score, please:

- ✅ Complete your project on time
- 📄 Submit all required files
- 🔗 Generate your review link
- 👥 Have your peers review your work

An auto-check will also be in place to verify the presence of core files needed for manual review.

### ⏰ Important Note

If the deadline passes, you won't be able to generate your review link—so be sure to submit on time!

---

## 📚 Additional Resources

- [Django Middleware Documentation](https://docs.djangoproject.com/en/stable/topics/http/middleware/)
- [Basics Guide](./01-basics/01-what-is-middleware.md)
- [Intermediate Guide](./02-intermediate/01-custom-middleware.md)
- [Advanced Patterns](./03-advanced/03-advanced-patterns.md)
- [Code Examples](./examples/README.md)

---

## 🎯 Quick Start Checklist

- [ ] Set up Django project with apps/core structure
- [ ] Create middleware directory
- [ ] Implement request logging middleware
- [ ] Implement authentication middleware
- [ ] Implement IP blocking middleware
- [ ] Implement rate limiting middleware
- [ ] Configure MIDDLEWARE in settings.py
- [ ] Write tests for each middleware
- [ ] Document middleware behavior
- [ ] Test with Postman/test client
- [ ] Review and optimize performance
- [ ] Submit for peer review

---

We're here to support your learning journey. Happy coding! ✨

---

*For detailed implementation examples, see: [Code Examples →](./examples/README.md)*
