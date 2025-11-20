# Practical Use Cases 🎯

Real-world middleware examples you can actually use in your projects. Each example solves a common problem!

---

## 🔐 Use Case 1: Maintenance Mode

**Problem**: You need to take your site down for maintenance but don't want to show errors.

**Solution**: Maintenance mode middleware

```python
# middleware/maintenance.py

from django.http import HttpResponse
from django.conf import settings
import datetime

class MaintenanceModeMiddleware:
    """
    Puts site in maintenance mode during specified times
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if maintenance mode is enabled
        maintenance_mode = getattr(settings, 'MAINTENANCE_MODE', False)
        
        if maintenance_mode:
            # Allow staff to access
            if request.user.is_authenticated and request.user.is_staff:
                return self.get_response(request)
            
            # Show maintenance page to everyone else
            return HttpResponse("""
                <html>
                <head><title>Maintenance Mode</title></head>
                <body style="text-align: center; padding: 50px; font-family: Arial;">
                    <h1>🔧 We'll be right back!</h1>
                    <p>We're performing scheduled maintenance.</p>
                    <p>Please check back in a few minutes.</p>
                </body>
                </html>
            """, status=503)
        
        return self.get_response(request)
```

**Settings:**
```python
# settings.py
MAINTENANCE_MODE = True  # Turn on maintenance
```

**Benefits:**
- Quick emergency maintenance
- Staff can still access site
- Clean user experience

---

## 📊 Use Case 2: Analytics & Tracking

**Problem**: You want to track page views, user behavior, and popular pages.

**Solution**: Analytics middleware

```python
# middleware/analytics.py

import json
from datetime import datetime
from collections import defaultdict

class AnalyticsMiddleware:
    """
    Tracks page views and user behavior
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.analytics = {
            'page_views': defaultdict(int),
            'unique_visitors': set(),
            'user_actions': [],
        }
    
    def __call__(self, request):
        # Record page view
        self.analytics['page_views'][request.path] += 1
        
        # Record unique visitor
        visitor_id = request.COOKIES.get('visitor_id', request.META.get('REMOTE_ADDR'))
        self.analytics['unique_visitors'].add(visitor_id)
        
        # Record timestamp
        action = {
            'path': request.path,
            'method': request.method,
            'user': str(request.user),
            'timestamp': datetime.now().isoformat(),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:100],
        }
        self.analytics['user_actions'].append(action)
        
        # Process request
        response = self.get_response(request)
        
        # Print stats every 10 requests
        if sum(self.analytics['page_views'].values()) % 10 == 0:
            print("\n📊 Analytics Summary:")
            print(f"   Total Views: {sum(self.analytics['page_views'].values())}")
            print(f"   Unique Visitors: {len(self.analytics['unique_visitors'])}")
            print(f"   Top Pages: {dict(sorted(self.analytics['page_views'].items(), key=lambda x: x[1], reverse=True)[:5])}")
        
        return response
```

**What it tracks:**
- Page views per URL
- Unique visitors
- User actions with timestamps
- Popular pages

---

## ⏱️ Use Case 3: Performance Monitoring

**Problem**: Some pages are slow but you don't know which ones.

**Solution**: Performance monitoring middleware

```python
# middleware/performance.py

import time
from django.conf import settings

class PerformanceMonitorMiddleware:
    """
    Monitors page performance and warns about slow pages
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.slow_threshold = getattr(settings, 'SLOW_PAGE_THRESHOLD', 1.0)  # seconds
        self.performance_log = []
    
    def __call__(self, request):
        # Start timer
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log performance data
        perf_data = {
            'path': request.path,
            'duration': duration,
            'status': response.status_code,
            'method': request.method,
        }
        self.performance_log.append(perf_data)
        
        # Add to response header
        response['X-Response-Time'] = f"{duration:.4f}s"
        
        # Warn about slow pages
        if duration > self.slow_threshold:
            print(f"🐌 SLOW PAGE ALERT!")
            print(f"   Path: {request.path}")
            print(f"   Duration: {duration:.2f}s")
            print(f"   Status: {response.status_code}")
        
        # Show average every 20 requests
        if len(self.performance_log) % 20 == 0:
            avg_time = sum(p['duration'] for p in self.performance_log) / len(self.performance_log)
            print(f"\n⚡ Average Response Time: {avg_time:.4f}s")
        
        return response
```

**Settings:**
```python
# settings.py
SLOW_PAGE_THRESHOLD = 0.5  # Warn if page takes over 0.5s
```

---

## 🔒 Use Case 4: IP Whitelist/Blacklist

**Problem**: You want to restrict access to certain IPs (for admin panel, API, etc.)

**Solution**: IP filtering middleware

```python
# middleware/ip_filter.py

from django.http import HttpResponseForbidden
from django.conf import settings

class IPFilterMiddleware:
    """
    Filters requests based on IP address
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.whitelist = getattr(settings, 'IP_WHITELIST', [])
        self.blacklist = getattr(settings, 'IP_BLACKLIST', [])
        self.protected_paths = getattr(settings, 'IP_PROTECTED_PATHS', ['/admin/'])
    
    def __call__(self, request):
        user_ip = self.get_client_ip(request)
        
        # Check blacklist first
        if user_ip in self.blacklist:
            print(f"🚫 Blocked IP: {user_ip}")
            return HttpResponseForbidden("Access Denied: IP Blocked")
        
        # Check if path is protected
        for protected_path in self.protected_paths:
            if request.path.startswith(protected_path):
                # Check whitelist
                if self.whitelist and user_ip not in self.whitelist:
                    print(f"🚫 Unauthorized IP trying to access {request.path}: {user_ip}")
                    return HttpResponseForbidden("Access Denied: IP Not Whitelisted")
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        """Get real client IP (handles proxies)"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

**Settings:**
```python
# settings.py
IP_WHITELIST = ['192.168.1.100', '10.0.0.5']  # Only these IPs can access protected paths
IP_BLACKLIST = ['192.168.1.200']  # These IPs are always blocked
IP_PROTECTED_PATHS = ['/admin/', '/api/sensitive/']
```

---

## 💾 Use Case 5: Database Query Counter

**Problem**: You want to know how many database queries each page makes (N+1 problem).

**Solution**: Query counter middleware

```python
# middleware/query_counter.py

from django.db import connection
from django.conf import settings

class QueryCounterMiddleware:
    """
    Counts database queries per request
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.query_threshold = getattr(settings, 'QUERY_THRESHOLD', 10)
    
    def __call__(self, request):
        # Reset query count
        queries_before = len(connection.queries)
        
        # Process request
        response = self.get_response(request)
        
        # Calculate queries made
        queries_after = len(connection.queries)
        query_count = queries_after - queries_before
        
        # Add to response header
        response['X-DB-Queries'] = str(query_count)
        
        # Warn about too many queries
        if query_count > self.query_threshold:
            print(f"⚠️ HIGH QUERY COUNT!")
            print(f"   Path: {request.path}")
            print(f"   Queries: {query_count}")
            
            # Show actual queries in debug mode
            if settings.DEBUG:
                recent_queries = connection.queries[queries_before:queries_after]
                for i, query in enumerate(recent_queries[:5], 1):
                    print(f"   Query {i}: {query['sql'][:100]}...")
        
        return response
```

**Note**: Only works when `DEBUG = True` in settings!

---

## 🌍 Use Case 6: Multi-Language Support

**Problem**: You want to detect user's language and show content in their language.

**Solution**: Language detection middleware

```python
# middleware/language.py

from django.utils import translation

class LanguageMiddleware:
    """
    Detects and sets user's preferred language
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.supported_languages = ['en', 'es', 'fr', 'de', 'ja']
    
    def __call__(self, request):
        # Check for language in URL parameter
        lang = request.GET.get('lang')
        
        # Check for language in cookie
        if not lang:
            lang = request.COOKIES.get('language')
        
        # Check browser's Accept-Language header
        if not lang:
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            for supported in self.supported_languages:
                if supported in accept_language.lower():
                    lang = supported
                    break
        
        # Default to English
        if not lang or lang not in self.supported_languages:
            lang = 'en'
        
        # Activate language
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        
        # Process request
        response = self.get_response(request)
        
        # Save language preference in cookie
        response.set_cookie('language', lang, max_age=365*24*60*60)
        
        # Deactivate language
        translation.deactivate()
        
        return response
```

---

## 🔔 Use Case 7: Request Rate Limiting

**Problem**: Prevent abuse by limiting how many requests a user can make.

**Solution**: Rate limiting middleware

```python
# middleware/rate_limit.py

import time
from collections import defaultdict
from django.http import HttpResponse

class RateLimitMiddleware:
    """
    Limits number of requests per user/IP
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Store: {ip: [timestamp1, timestamp2, ...]}
        self.request_history = defaultdict(list)
        self.max_requests = 100  # Max requests
        self.time_window = 60  # Per 60 seconds
    
    def __call__(self, request):
        # Get client identifier
        client_id = self.get_client_id(request)
        current_time = time.time()
        
        # Clean old requests
        cutoff_time = current_time - self.time_window
        self.request_history[client_id] = [
            t for t in self.request_history[client_id] 
            if t > cutoff_time
        ]
        
        # Check if limit exceeded
        if len(self.request_history[client_id]) >= self.max_requests:
            print(f"⛔ Rate limit exceeded for {client_id}")
            return HttpResponse(
                "Rate limit exceeded. Please try again later.",
                status=429
            )
        
        # Record this request
        self.request_history[client_id].append(current_time)
        
        # Process request
        response = self.get_response(request)
        
        # Add rate limit headers
        remaining = self.max_requests - len(self.request_history[client_id])
        response['X-RateLimit-Limit'] = str(self.max_requests)
        response['X-RateLimit-Remaining'] = str(remaining)
        
        return response
    
    def get_client_id(self, request):
        """Get unique identifier for client"""
        if request.user.is_authenticated:
            return f"user_{request.user.id}"
        return request.META.get('REMOTE_ADDR', 'unknown')
```

**What it does:**
- Tracks requests per user/IP
- Blocks after limit reached
- Shows remaining requests in headers
- Auto-resets after time window

---

## 📝 Use Case 8: Request/Response Logger

**Problem**: You need detailed logs of all requests and responses for debugging.

**Solution**: Comprehensive logging middleware

```python
# middleware/request_logger.py

import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RequestLoggerMiddleware:
    """
    Logs detailed information about requests and responses
    """
    
    def __call__(self, request):
        # Log request
        request_log = {
            'timestamp': datetime.now().isoformat(),
            'method': request.method,
            'path': request.path,
            'user': str(request.user),
            'ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
            'query_params': dict(request.GET),
        }
        
        # Log POST data (be careful with sensitive data!)
        if request.method == 'POST':
            # Don't log passwords!
            safe_post = {k: v for k, v in request.POST.items() 
                        if 'password' not in k.lower()}
            request_log['post_data'] = safe_post
        
        logger.info(f"REQUEST: {json.dumps(request_log, indent=2)}")
        
        # Process request
        response = self.get_response(request)
        
        # Log response
        response_log = {
            'timestamp': datetime.now().isoformat(),
            'path': request.path,
            'status': response.status_code,
            'content_type': response.get('Content-Type', ''),
            'size': len(response.content),
        }
        
        logger.info(f"RESPONSE: {json.dumps(response_log, indent=2)}")
        
        return response
```

---

## 🎯 Use Case 9: Mobile App API Versioning

**Problem**: You need to support multiple API versions for different app versions.

**Solution**: API versioning middleware

```python
# middleware/api_version.py

from django.http import JsonResponse

class APIVersionMiddleware:
    """
    Handles API versioning for mobile apps
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.min_supported_version = '1.0'
        self.current_version = '2.0'
    
    def __call__(self, request):
        # Only check API endpoints
        if request.path.startswith('/api/'):
            # Get version from header
            api_version = request.META.get('HTTP_X_API_VERSION', '')
            
            if not api_version:
                return JsonResponse({
                    'error': 'API version required',
                    'current_version': self.current_version
                }, status=400)
            
            # Check if version is supported
            if api_version < self.min_supported_version:
                return JsonResponse({
                    'error': 'API version not supported',
                    'min_version': self.min_supported_version,
                    'current_version': self.current_version,
                    'message': 'Please update your app'
                }, status=426)  # Upgrade Required
            
            # Add version to request for views to use
            request.api_version = api_version
            print(f"📱 API v{api_version} request to {request.path}")
        
        response = self.get_response(request)
        
        # Add version to response
        if request.path.startswith('/api/'):
            response['X-API-Version'] = self.current_version
        
        return response
```

---

## 💡 Combining Multiple Use Cases

You can use multiple middleware together:

```python
# settings.py

MIDDLEWARE = [
    # Security first
    'middleware.ip_filter.IPFilterMiddleware',
    
    # Then rate limiting
    'middleware.rate_limit.RateLimitMiddleware',
    
    # Then monitoring
    'middleware.performance.PerformanceMonitorMiddleware',
    'middleware.query_counter.QueryCounterMiddleware',
    
    # Then business logic
    'middleware.language.LanguageMiddleware',
    'middleware.api_version.APIVersionMiddleware',
    
    # Finally logging
    'middleware.request_logger.RequestLoggerMiddleware',
    'middleware.analytics.AnalyticsMiddleware',
]
```

---

## 🎓 Quick Summary

You now have practical middleware for:

- ✅ Maintenance mode
- ✅ Analytics tracking
- ✅ Performance monitoring
- ✅ IP filtering
- ✅ Query counting
- ✅ Language detection
- ✅ Rate limiting
- ✅ Request logging
- ✅ API versioning

---

## 🚀 Next Steps

Ready for advanced concepts?

**Continue to**: [Advanced Level →](../03-advanced/)

Or start with: [Middleware Ordering →](../03-advanced/01-middleware-ordering.md)

---

*Continue to: [Middleware Ordering →](../03-advanced/01-middleware-ordering.md)*
