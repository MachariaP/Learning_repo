# Airbnb Clone Middleware Implementation Guide 🏠

A practical, step-by-step guide to implementing middleware for an Airbnb Clone application.

---

## 🎯 Project Context

In this guide, you'll build middleware components for an Airbnb-style platform that includes:
- User authentication (guests and hosts)
- Property listings
- Booking system
- Reviews and ratings
- Payment processing

---

## 📁 Project Structure

```
airbnb_clone/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── utils.py
│   │   │   ├── logging_middleware.py
│   │   │   ├── auth_middleware.py
│   │   │   ├── ip_blocker.py
│   │   │   ├── rate_limiter.py
│   │   │   └── request_validator.py
│   │   ├── models.py
│   │   └── views.py
│   ├── users/
│   │   ├── models.py
│   │   └── views.py
│   ├── listings/
│   │   ├── models.py
│   │   └── views.py
│   └── bookings/
│       ├── models.py
│       └── views.py
├── .env
└── requirements.txt
```

---

## 🚀 Step-by-Step Implementation

### Step 0: Create Utility Functions

Before implementing middleware, create a utility file for shared functions.

**File:** `apps/core/middleware/utils.py`

```python
"""
Utility functions for middleware components.
"""

def get_client_ip(request):
    """
    Get the real client IP address, handling proxies and load balancers.
    
    Args:
        request: Django HttpRequest object
    
    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # X-Forwarded-For can contain multiple IPs, get the first one
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    return ip
```

---

### Step 1: Initial Setup

```bash
# Create Django project
django-admin startproject config .

# Create apps directory
mkdir apps
cd apps

# Create core app
python ../manage.py startapp core

# Create other apps
python ../manage.py startapp users
python ../manage.py startapp listings
python ../manage.py startapp bookings
```

**Update settings.py:**
```python
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Add apps directory to Python path
sys.path.insert(0, str(BASE_DIR / 'apps'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom apps
    'core',
    'users',
    'listings',
    'bookings',
]
```

---

### Step 2: Create Logging Middleware

**File:** `apps/core/middleware/logging_middleware.py`

```python
import logging
import json
import time
from datetime import datetime
from .utils import get_client_ip

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Logs all incoming requests and outgoing responses.
    
    Purpose: Audit trail and debugging
    Use case: Track API usage, identify issues, analyze user behavior
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("RequestLoggingMiddleware initialized")
    
    def __call__(self, request):
        # Record start time
        start_time = time.time()
        
        # Log request details
        request_data = {
            'timestamp': datetime.now().isoformat(),
            'method': request.method,
            'path': request.path,
            'user': str(request.user) if request.user.is_authenticated else 'Anonymous',
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
        }
        
        # Don't log sensitive data in production
        if request.method in ['POST', 'PUT', 'PATCH']:
            # Filter out passwords and payment info
            safe_data = {
                k: v for k, v in request.POST.items() 
                if not any(sensitive in k.lower() for sensitive in 
                          ['password', 'card', 'cvv', 'pin'])
            }
            request_data['body_sample'] = str(safe_data)[:500]
        
        logger.info(f"REQUEST: {json.dumps(request_data)}")
        
        # Process request
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        response_data = {
            'timestamp': datetime.now().isoformat(),
            'path': request.path,
            'status_code': response.status_code,
            'duration_ms': f"{duration * 1000:.2f}",
        }
        
        logger.info(f"RESPONSE: {json.dumps(response_data)}")
        
        # Add custom header
        response['X-Request-Duration'] = f"{duration:.4f}s"
        
        return response
```

---

### Step 3: Create Role-Based Access Control Middleware

**File:** `apps/core/middleware/auth_middleware.py`

```python
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings

class RoleBasedAccessMiddleware:
    """
    Enforces role-based access control for different endpoints.
    
    Purpose: Protect endpoints based on user roles (Guest, Host, Admin)
    Use case: Only hosts can create listings, only guests can book, etc.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Define protected paths and required roles
        self.protected_paths = {
            '/api/listings/create/': ['host', 'admin'],
            '/api/listings/edit/': ['host', 'admin'],
            '/api/bookings/manage/': ['host', 'admin'],
            '/api/admin/': ['admin'],
            '/api/users/manage/': ['admin'],
        }
    
    def __call__(self, request):
        # Check if path requires role verification
        for path, required_roles in self.protected_paths.items():
            if request.path.startswith(path):
                # User must be authenticated
                if not request.user.is_authenticated:
                    return JsonResponse({
                        'error': 'Authentication required',
                        'message': 'Please log in to access this resource'
                    }, status=401)
                
                # Check user role
                user_role = getattr(request.user, 'role', None)
                
                if user_role not in required_roles:
                    return JsonResponse({
                        'error': 'Insufficient permissions',
                        'message': f'This endpoint requires one of: {", ".join(required_roles)}',
                        'your_role': user_role or 'none'
                    }, status=403)
        
        return self.get_response(request)


class HostVerificationMiddleware:
    """
    Ensures hosts have completed verification before creating listings.
    
    Purpose: Quality control for listings
    Use case: Only verified hosts can create/manage listings
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.host_only_paths = [
            '/api/listings/create/',
            '/api/listings/edit/',
        ]
    
    def __call__(self, request):
        # Check if this is a host-only endpoint
        for path in self.host_only_paths:
            if request.path.startswith(path):
                if request.user.is_authenticated:
                    # Check if user is a host
                    if hasattr(request.user, 'role') and request.user.role == 'host':
                        # Check if host is verified
                        if not getattr(request.user, 'is_verified_host', False):
                            return JsonResponse({
                                'error': 'Verification required',
                                'message': 'Please complete host verification before creating listings',
                                'verification_url': '/api/hosts/verify/'
                            }, status=403)
        
        return self.get_response(request)
```

---

### Step 4: Create IP Blocking Middleware

**File:** `apps/core/middleware/ip_blocker.py`

```python
from django.http import HttpResponseForbidden
from django.conf import settings
from django.core.cache import cache
import logging
from .utils import get_client_ip

logger = logging.getLogger(__name__)

class IPBlockerMiddleware:
    """
    Blocks requests from banned IP addresses.
    
    Purpose: Security - prevent access from malicious IPs
    Use case: Block bots, scrapers, or abusive users
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Get blocked IPs from settings
        self.blocked_ips = set(getattr(settings, 'BLOCKED_IPS', []))
        # Get IP whitelist (admin IPs that bypass blocking)
        self.whitelist = set(getattr(settings, 'IP_WHITELIST', []))
    
    def __call__(self, request):
        client_ip = get_client_ip(request)
        
        # Whitelist bypasses all checks
        if client_ip in self.whitelist:
            return self.get_response(request)
        
        # Check if IP is blocked
        if client_ip in self.blocked_ips:
            logger.warning(f"Blocked request from banned IP: {client_ip}")
            return HttpResponseForbidden(
                "Access denied. Your IP address has been blocked."
            )
        
        # Check dynamic blocks (e.g., from rate limiting)
        dynamic_block = cache.get(f'blocked_ip_{client_ip}')
        if dynamic_block:
            logger.warning(f"Blocked request from dynamically banned IP: {client_ip}")
            return HttpResponseForbidden(
                "Access denied. Too many failed requests. Try again later."
            )
        
        return self.get_response(request)


class SuspiciousHeaderMiddleware:
    """
    Blocks requests with suspicious headers.
    
    Purpose: Security - detect and block potential attacks
    Use case: Block requests with SQL injection attempts, XSS, etc.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Suspicious patterns to look for
        self.suspicious_patterns = [
            '<script',
            'javascript:',
            'SELECT * FROM',
            'DROP TABLE',
            '../../../',  # Path traversal
            'eval(',
            'exec(',
        ]
    
    def __call__(self, request):
        # Check common headers for suspicious content
        headers_to_check = [
            request.META.get('HTTP_USER_AGENT', ''),
            request.META.get('HTTP_REFERER', ''),
            request.path,
        ]
        
        for header_value in headers_to_check:
            for pattern in self.suspicious_patterns:
                if pattern.lower() in header_value.lower():
                    logger.warning(
                        f"Suspicious pattern '{pattern}' detected in request from "
                        f"{request.META.get('REMOTE_ADDR')}"
                    )
                    return HttpResponseForbidden(
                        "Request blocked due to suspicious content"
                    )
        
        return self.get_response(request)
```

---

### Step 5: Create Rate Limiting Middleware

**File:** `apps/core/middleware/rate_limiter.py`

```python
import time
from collections import defaultdict
from django.http import JsonResponse
from django.core.cache import cache
import logging
from .utils import get_client_ip

logger = logging.getLogger(__name__)

class RateLimitMiddleware:
    """
    Implements rate limiting to prevent API abuse.
    
    Purpose: Prevent abuse and ensure fair usage
    Use case: Limit booking attempts, search queries, etc.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Different limits for different endpoints
        self.rate_limits = {
            '/api/bookings/create/': {
                'max_requests': 10,
                'time_window': 60,  # 10 requests per minute
            },
            '/api/search/': {
                'max_requests': 100,
                'time_window': 60,  # 100 searches per minute
            },
            '/api/': {  # Default for all API endpoints
                'max_requests': 1000,
                'time_window': 3600,  # 1000 requests per hour
            },
        }
    
    def __call__(self, request):
        # Get client identifier
        client_id = self.get_client_id(request)
        
        # Check rate limit for this path
        rate_limit_info = self.get_rate_limit_for_path(request.path)
        
        if rate_limit_info:
            max_requests = rate_limit_info['max_requests']
            time_window = rate_limit_info['time_window']
            
            # Create cache key
            cache_key = f'rate_limit_{client_id}_{request.path}'
            
            # Get current request count
            request_data = cache.get(cache_key, {'count': 0, 'reset_time': time.time() + time_window})
            
            current_time = time.time()
            
            # Reset if time window has passed
            if current_time > request_data['reset_time']:
                request_data = {
                    'count': 0,
                    'reset_time': current_time + time_window
                }
            
            # Check if limit exceeded
            if request_data['count'] >= max_requests:
                reset_in = int(request_data['reset_time'] - current_time)
                logger.warning(f"Rate limit exceeded for {client_id} on {request.path}")
                
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Please try again in {reset_in} seconds.',
                    'retry_after': reset_in,
                    'limit': max_requests,
                    'window': time_window,
                }, status=429)
            
            # Increment counter
            request_data['count'] += 1
            cache.set(cache_key, request_data, time_window)
        
        # Process request
        response = self.get_response(request)
        
        # Add rate limit headers
        if rate_limit_info:
            remaining = max_requests - request_data['count']
            response['X-RateLimit-Limit'] = str(max_requests)
            response['X-RateLimit-Remaining'] = str(max(0, remaining))
            response['X-RateLimit-Reset'] = str(int(request_data['reset_time']))
        
        return response
    
    def get_client_id(self, request):
        """Get unique identifier for client (user or IP)"""
        if request.user.is_authenticated:
            return f"user_{request.user.id}"
        
        # Use IP for anonymous users
        ip = get_client_ip(request)
        return f"ip_{ip}"
    
    def get_rate_limit_for_path(self, path):
        """Get the most specific rate limit for this path"""
        # Try exact match first
        if path in self.rate_limits:
            return self.rate_limits[path]
        
        # Try prefix match (longest first)
        for limit_path in sorted(self.rate_limits.keys(), key=len, reverse=True):
            if path.startswith(limit_path):
                return self.rate_limits[limit_path]
        
        return None
```

---

### Step 6: Create Request Validator Middleware

**File:** `apps/core/middleware/request_validator.py`

```python
import json
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class JSONValidatorMiddleware:
    """
    Validates incoming JSON payloads.
    
    Purpose: Ensure data quality before reaching views
    Use case: Validate booking data, listing information, etc.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.json_endpoints = [
            '/api/',
        ]
    
    def __call__(self, request):
        # Only check POST, PUT, PATCH requests to API endpoints
        if request.method in ['POST', 'PUT', 'PATCH']:
            if any(request.path.startswith(ep) for ep in self.json_endpoints):
                # Check Content-Type
                content_type = request.META.get('CONTENT_TYPE', '')
                
                if 'application/json' in content_type:
                    try:
                        # Try to parse JSON
                        if request.body:
                            json_data = json.loads(request.body)
                            # Attach parsed data to request
                            request.json_data = json_data
                    except json.JSONDecodeError as e:
                        logger.warning(f"Invalid JSON in request: {str(e)}")
                        return JsonResponse({
                            'error': 'Invalid JSON',
                            'message': 'Request body contains invalid JSON',
                            'details': str(e)
                        }, status=400)
        
        return self.get_response(request)


class BookingValidatorMiddleware:
    """
    Validates booking-specific requests.
    
    Purpose: Enforce business rules for bookings
    Use case: Validate dates, guest count, etc.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check booking creation endpoint
        if request.path == '/api/bookings/create/' and request.method == 'POST':
            if hasattr(request, 'json_data'):
                errors = []
                data = request.json_data
                
                # Validate required fields
                required_fields = ['listing_id', 'check_in', 'check_out', 'guests']
                for field in required_fields:
                    if field not in data:
                        errors.append(f"Missing required field: {field}")
                
                # Validate guest count
                if 'guests' in data:
                    try:
                        guests = int(data['guests'])
                        if guests < 1:
                            errors.append("Guest count must be at least 1")
                        if guests > 16:  # Airbnb's max
                            errors.append("Guest count cannot exceed 16")
                    except (ValueError, TypeError):
                        errors.append("Guest count must be a number")
                
                # If validation errors, return them
                if errors:
                    return JsonResponse({
                        'error': 'Validation failed',
                        'errors': errors
                    }, status=400)
        
        return self.get_response(request)
```

---

### Step 7: Configure Middleware Stack

**File:** `config/settings.py`

```python
MIDDLEWARE = [
    # 1. Security - must be first
    'django.middleware.security.SecurityMiddleware',
    
    # 2. IP blocking - block bad actors early
    'core.middleware.ip_blocker.IPBlockerMiddleware',
    'core.middleware.ip_blocker.SuspiciousHeaderMiddleware',
    
    # 3. Sessions
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # 4. Common
    'django.middleware.common.CommonMiddleware',
    
    # 5. CSRF
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # 6. Authentication
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # 7. Custom authentication/authorization
    'core.middleware.auth_middleware.RoleBasedAccessMiddleware',
    'core.middleware.auth_middleware.HostVerificationMiddleware',
    
    # 8. Rate limiting - after auth so we can identify users
    'core.middleware.rate_limiter.RateLimitMiddleware',
    
    # 9. Request validation
    'core.middleware.request_validator.JSONValidatorMiddleware',
    'core.middleware.request_validator.BookingValidatorMiddleware',
    
    # 10. Messages
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # 11. Clickjacking protection
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # 12. Logging - last to log complete request/response
    'core.middleware.logging_middleware.RequestLoggingMiddleware',
]

# Middleware Configuration
BLOCKED_IPS = [
    # Add IPs to block
]

IP_WHITELIST = [
    '127.0.0.1',  # Localhost
    # Add admin IPs
]

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/middleware.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'core.middleware': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}
```

---

## 🧪 Testing Your Middleware

### Test File: `apps/core/tests/test_middleware.py`

```python
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from core.middleware.rate_limiter import RateLimitMiddleware
from core.middleware.auth_middleware import RoleBasedAccessMiddleware
from core.middleware.ip_blocker import IPBlockerMiddleware

User = get_user_model()

class RateLimitMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RateLimitMiddleware(
            get_response=lambda r: HttpResponse("OK")
        )
    
    def test_rate_limit_enforced(self):
        """Test that rate limiting works"""
        # Make requests up to limit
        for i in range(10):
            request = self.factory.post('/api/bookings/create/')
            request.user = User()
            response = self.middleware(request)
            self.assertEqual(response.status_code, 200)
        
        # Next request should be rate limited
        request = self.factory.post('/api/bookings/create/')
        request.user = User()
        response = self.middleware(request)
        self.assertEqual(response.status_code, 429)


class AuthMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RoleBasedAccessMiddleware(
            get_response=lambda r: HttpResponse("OK")
        )
        
        # Create test users
        self.guest = User.objects.create(username='guest', role='guest')
        self.host = User.objects.create(username='host', role='host')
        self.admin = User.objects.create(username='admin', role='admin')
    
    def test_host_can_create_listing(self):
        """Test that hosts can create listings"""
        request = self.factory.post('/api/listings/create/')
        request.user = self.host
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)
    
    def test_guest_cannot_create_listing(self):
        """Test that guests cannot create listings"""
        request = self.factory.post('/api/listings/create/')
        request.user = self.guest
        response = self.middleware(request)
        self.assertEqual(response.status_code, 403)
```

---

## 📊 Manual Testing with Postman

### Test 1: Rate Limiting
```
Request:
POST /api/bookings/create/
Headers:
  Authorization: Bearer <token>
Body:
  {
    "listing_id": 123,
    "check_in": "2024-01-01",
    "check_out": "2024-01-05",
    "guests": 2
  }

Make 11 requests rapidly.
Expected: First 10 succeed (200), 11th fails (429)
```

### Test 2: Role-Based Access
```
Request:
POST /api/listings/create/
Headers:
  Authorization: Bearer <guest_token>
Body:
  {
    "title": "Cozy Apartment",
    "price": 100
  }

Expected: 403 Forbidden (guest cannot create listings)
```

### Test 3: IP Blocking
```
Request:
GET /api/listings/
Headers:
  X-Forwarded-For: 192.168.1.100  # Blocked IP

Expected: 403 Forbidden
```

---

## 🎯 Best Practices Summary

1. **Order matters**: Security → Auth → Rate limiting → Validation → Logging
2. **Keep it fast**: No heavy database queries in middleware
3. **Use cache**: For rate limiting and temporary blocks
4. **Log appropriately**: Don't log sensitive data
5. **Test thoroughly**: Unit tests + integration tests + manual testing
6. **Document clearly**: Each middleware should explain its purpose
7. **Handle errors gracefully**: Don't crash, return meaningful errors

---

## 🚀 Next Steps

1. ✅ Implement all middleware components
2. ✅ Configure settings.py
3. ✅ Write unit tests
4. ✅ Test with Postman
5. ✅ Review logs
6. ✅ Optimize performance
7. ✅ Document API endpoints
8. ✅ Submit for review

---

**Ready to build? Start with the logging middleware and work your way through each component! 🎉**
