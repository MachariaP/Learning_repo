# Middleware Code Examples 💻

Working code examples you can copy and use in your Django projects!

---

## 📁 Project Structure

```
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── middleware/
│       ├── __init__.py
│       ├── simple.py
│       ├── logging_middleware.py
│       ├── performance.py
│       └── security.py
└── myapp/
    └── views.py
```

---

## 1️⃣ Simple Request Logger

**File**: `middleware/simple.py`

```python
import time
from datetime import datetime

class SimpleRequestLoggerMiddleware:
    """
    Logs basic information about every request
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        print("✅ SimpleRequestLoggerMiddleware initialized!")
    
    def __call__(self, request):
        # Log request
        print(f"\n{'='*50}")
        print(f"📥 REQUEST at {datetime.now().strftime('%H:%M:%S')}")
        print(f"   Method: {request.method}")
        print(f"   Path: {request.path}")
        print(f"   User: {request.user}")
        
        # Process request
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        
        # Log response
        print(f"📤 RESPONSE")
        print(f"   Status: {response.status_code}")
        print(f"   Duration: {duration:.4f}s")
        print(f"{'='*50}\n")
        
        return response
```

**Add to settings.py:**
```python
MIDDLEWARE = [
    # ... other middleware
    'myproject.middleware.simple.SimpleRequestLoggerMiddleware',
]
```

---

## 2️⃣ Performance Timer

**File**: `middleware/performance.py`

```python
import time
from django.conf import settings

class PerformanceMiddleware:
    """
    Measures and warns about slow requests
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.slow_threshold = getattr(settings, 'SLOW_REQUEST_THRESHOLD', 1.0)
    
    def __call__(self, request):
        # Start timer
        start_time = time.time()
        
        # Add to request for views to use
        request.start_time = start_time
        
        # Process request
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Add header
        response['X-Request-Duration'] = f"{duration:.4f}s"
        
        # Warn about slow requests
        if duration > self.slow_threshold:
            print(f"⚠️ SLOW REQUEST!")
            print(f"   Path: {request.path}")
            print(f"   Duration: {duration:.2f}s")
        
        return response
```

**Add to settings.py:**
```python
SLOW_REQUEST_THRESHOLD = 0.5  # 500ms

MIDDLEWARE = [
    'myproject.middleware.performance.PerformanceMiddleware',
]
```

---

## 3️⃣ Custom Headers

**File**: `middleware/headers.py`

```python
class CustomHeadersMiddleware:
    """
    Adds custom headers to all responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add custom headers
        response['X-Powered-By'] = 'Django + Middleware'
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        
        return response
```

---

## 4️⃣ Request Counter

**File**: `middleware/counter.py`

```python
from collections import defaultdict

class RequestCounterMiddleware:
    """
    Counts requests per path
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.total_requests = 0
        self.path_counts = defaultdict(int)
    
    def __call__(self, request):
        # Increment counters
        self.total_requests += 1
        self.path_counts[request.path] += 1
        
        # Print stats every 10 requests
        if self.total_requests % 10 == 0:
            print(f"\n📊 Request Statistics:")
            print(f"   Total: {self.total_requests}")
            print(f"   Top Paths:")
            
            # Get top 5 paths
            top_paths = sorted(
                self.path_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            for path, count in top_paths:
                print(f"      {path}: {count}")
        
        response = self.get_response(request)
        return response
```

---

## 5️⃣ Device Detection

**File**: `middleware/device.py`

```python
class DeviceDetectionMiddleware:
    """
    Detects if user is on mobile or desktop
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.mobile_keywords = [
            'mobile', 'android', 'iphone', 'ipad',
            'ipod', 'blackberry', 'windows phone'
        ]
    
    def __call__(self, request):
        # Get user agent
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        # Detect device
        is_mobile = any(
            keyword in user_agent 
            for keyword in self.mobile_keywords
        )
        
        # Add to request
        request.is_mobile = is_mobile
        request.device_type = 'mobile' if is_mobile else 'desktop'
        
        response = self.get_response(request)
        
        # Add header
        response['X-Device-Type'] = request.device_type
        
        return response
```

**Usage in views:**
```python
def my_view(request):
    if request.is_mobile:
        template = 'mobile.html'
    else:
        template = 'desktop.html'
    
    return render(request, template)
```

---

## 6️⃣ IP Blocker

**File**: `middleware/ip_blocker.py`

```python
from django.http import HttpResponseForbidden
from django.conf import settings

class IPBlockerMiddleware:
    """
    Blocks requests from blacklisted IPs
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_ips = getattr(settings, 'BLOCKED_IPS', [])
    
    def __call__(self, request):
        # Get client IP
        ip = self.get_client_ip(request)
        
        # Check if blocked
        if ip in self.blocked_ips:
            print(f"🚫 Blocked IP: {ip}")
            return HttpResponseForbidden("Your IP is blocked")
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get real client IP (handles proxies)"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

**Add to settings.py:**
```python
BLOCKED_IPS = [
    '192.168.1.100',
    '10.0.0.50',
]
```

---

## 7️⃣ Complete Example: Logging Middleware

**File**: `middleware/logging_middleware.py`

```python
import logging
import json
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class ComprehensiveLoggingMiddleware:
    """
    Complete logging middleware with all features
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("Logging middleware initialized")
    
    def __call__(self, request):
        # Prepare request log
        request_data = self.prepare_request_log(request)
        
        # Log request
        logger.info(f"REQUEST: {json.dumps(request_data, indent=2)}")
        
        # Time the request
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Prepare response log
        response_data = self.prepare_response_log(
            request, response, duration
        )
        
        # Log response
        logger.info(f"RESPONSE: {json.dumps(response_data, indent=2)}")
        
        # Add timing header
        response['X-Request-Duration'] = f"{duration:.4f}s"
        
        return response
    
    def prepare_request_log(self, request):
        """Prepare request data for logging"""
        return {
            'timestamp': datetime.now().isoformat(),
            'method': request.method,
            'path': request.path,
            'query_params': dict(request.GET),
            'user': str(request.user),
            'ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
        }
    
    def prepare_response_log(self, request, response, duration):
        """Prepare response data for logging"""
        return {
            'timestamp': datetime.now().isoformat(),
            'path': request.path,
            'status': response.status_code,
            'duration': f"{duration:.4f}s",
            'content_type': response.get('Content-Type', ''),
            'size': len(response.content),
        }
```

---

## 8️⃣ Testing Your Middleware

**File**: `tests/test_middleware.py`

```python
from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from myproject.middleware.simple import SimpleRequestLoggerMiddleware

class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SimpleRequestLoggerMiddleware(
            get_response=lambda r: HttpResponse("OK")
        )
    
    def test_middleware_runs(self):
        """Test that middleware processes request"""
        request = self.factory.get('/')
        response = self.middleware(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK")
    
    def test_middleware_adds_header(self):
        """Test that middleware adds headers"""
        request = self.factory.get('/')
        response = self.middleware(request)
        
        # Check if your middleware adds headers
        self.assertIn('X-Request-Duration', response)
```

---

## 🎯 Complete settings.py Example

```python
# settings.py

MIDDLEWARE = [
    # 1. Security first
    'django.middleware.security.SecurityMiddleware',
    
    # 2. Custom security headers
    'myproject.middleware.headers.CustomHeadersMiddleware',
    
    # 3. IP blocking
    'myproject.middleware.ip_blocker.IPBlockerMiddleware',
    
    # 4. Sessions
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # 5. Common
    'django.middleware.common.CommonMiddleware',
    
    # 6. CSRF
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # 7. Authentication
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # 8. Device detection
    'myproject.middleware.device.DeviceDetectionMiddleware',
    
    # 9. Performance monitoring
    'myproject.middleware.performance.PerformanceMiddleware',
    
    # 10. Request counting
    'myproject.middleware.counter.RequestCounterMiddleware',
    
    # 11. Logging (last)
    'myproject.middleware.logging_middleware.ComprehensiveLoggingMiddleware',
    
    # Django's remaining middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Middleware settings
SLOW_REQUEST_THRESHOLD = 0.5  # seconds
BLOCKED_IPS = []

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'middleware.log',
        },
    },
    'loggers': {
        'myproject.middleware': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}
```

---

## 🚀 Quick Start

1. **Create the middleware directory:**
   ```bash
   mkdir -p myproject/middleware
   touch myproject/middleware/__init__.py
   ```

2. **Copy a middleware file** (e.g., `simple.py`)

3. **Add to settings.py:**
   ```python
   MIDDLEWARE = [
       # ... other middleware
       'myproject.middleware.simple.SimpleRequestLoggerMiddleware',
   ]
   ```

4. **Run your Django server:**
   ```bash
   python manage.py runserver
   ```

5. **Visit any page** and see middleware in action!

---

## 📝 Tips for Using These Examples

1. **Start Simple**: Begin with SimpleRequestLoggerMiddleware
2. **Customize**: Modify the examples for your needs
3. **Test**: Write tests for your middleware
4. **Monitor**: Watch the console output
5. **Iterate**: Add features as you learn

---

## 🎓 What's Next?

Try building your own middleware that:
- Tracks user preferences
- Implements custom caching
- Adds API rate limiting
- Handles custom authentication
- Monitors application health

---

*Copy, paste, and modify these examples to build your own middleware! 🚀*
