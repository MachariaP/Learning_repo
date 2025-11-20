# Advanced Patterns 🎨

Master-level middleware patterns used in production systems. These patterns solve complex, real-world problems.

---

## 🎯 Pattern 1: Conditional Middleware

**Problem**: You want middleware to run only under certain conditions.

### Solution: Path-Based Activation

```python
class ConditionalMiddleware:
    """
    Only runs for specific URL patterns
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.active_paths = ['/api/', '/admin/']
        self.excluded_paths = ['/static/', '/media/']
    
    def __call__(self, request):
        # Skip if excluded
        for excluded in self.excluded_paths:
            if request.path.startswith(excluded):
                return self.get_response(request)
        
        # Only run for active paths
        should_run = any(
            request.path.startswith(path) 
            for path in self.active_paths
        )
        
        if should_run:
            # Do middleware work
            print(f"Processing: {request.path}")
        
        response = self.get_response(request)
        return response
```

---

## 🔄 Pattern 2: Middleware Chaining

**Problem**: You need middleware to pass data between each other.

### Solution: Request Attributes

```python
class DataCollectorMiddleware:
    """Collects data for other middleware"""
    
    def __call__(self, request):
        # Initialize data container
        request.middleware_data = {
            'start_time': time.time(),
            'request_id': str(uuid.uuid4()),
        }
        
        response = self.get_response(request)
        return response


class DataProcessorMiddleware:
    """Uses data from DataCollector"""
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Access data from previous middleware
        if hasattr(request, 'middleware_data'):
            duration = time.time() - request.middleware_data['start_time']
            request_id = request.middleware_data['request_id']
            
            print(f"Request {request_id} took {duration:.4f}s")
        
        return response
```

**Settings (order matters!):**
```python
MIDDLEWARE = [
    'DataCollectorMiddleware',  # MUST be before
    'DataProcessorMiddleware',   # Uses data from above
]
```

---

## 🎭 Pattern 3: Context Manager Middleware

**Problem**: You need setup and cleanup for each request.

### Solution: Context Manager

```python
from contextlib import contextmanager

class ContextManagerMiddleware:
    """
    Uses context manager for setup/cleanup
    """
    
    def __call__(self, request):
        with self.request_context(request):
            response = self.get_response(request)
        return response
    
    @contextmanager
    def request_context(self, request):
        """Setup and cleanup for each request"""
        # Setup
        print(f"🔧 Setting up for {request.path}")
        request.temp_data = {}
        
        try:
            yield  # Request processing happens here
        finally:
            # Cleanup (always runs!)
            print(f"🧹 Cleaning up for {request.path}")
            if hasattr(request, 'temp_data'):
                del request.temp_data
```

---

## 🔀 Pattern 4: Middleware Factory

**Problem**: You need to create similar middleware with different configurations.

### Solution: Factory Function

```python
def create_header_middleware(header_name, header_value):
    """
    Factory function to create middleware
    """
    
    class HeaderMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response
            self.header_name = header_name
            self.header_value = header_value
        
        def __call__(self, request):
            response = self.get_response(request)
            response[self.header_name] = self.header_value
            return response
    
    return HeaderMiddleware


# Usage in settings.py
ServerHeaderMiddleware = create_header_middleware('X-Server', 'MyServer')
VersionHeaderMiddleware = create_header_middleware('X-Version', '1.0.0')

MIDDLEWARE = [
    'myapp.middleware.ServerHeaderMiddleware',
    'myapp.middleware.VersionHeaderMiddleware',
]
```

---

## 🎪 Pattern 5: Decorator-Style Middleware

**Problem**: You want middleware-like behavior for specific views only.

### Solution: View Decorator

```python
from functools import wraps

def view_middleware(func):
    """
    Middleware as a decorator
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Before view
        print(f"Before view: {request.path}")
        
        # Call view
        response = func(request, *args, **kwargs)
        
        # After view
        print(f"After view: {response.status_code}")
        
        return response
    
    return wrapper


# Usage in views
@view_middleware
def my_view(request):
    return HttpResponse("Hello")
```

---

## 🔐 Pattern 6: Multi-Tenant Middleware

**Problem**: One application serves multiple tenants/organizations.

### Solution: Tenant Detection Middleware

```python
class MultiTenantMiddleware:
    """
    Detects and sets current tenant
    """
    
    def __call__(self, request):
        # Detect tenant from subdomain
        host = request.get_host()
        subdomain = host.split('.')[0]
        
        # Get tenant from database
        try:
            from myapp.models import Tenant
            tenant = Tenant.objects.get(subdomain=subdomain)
            request.tenant = tenant
            
            # Set database schema/connection
            connection.set_schema(tenant.schema_name)
            
        except Tenant.DoesNotExist:
            request.tenant = None
        
        response = self.get_response(request)
        return response
```

**Usage in views:**
```python
def my_view(request):
    tenant = request.tenant
    # Query only this tenant's data
    data = MyModel.objects.filter(tenant=tenant)
```

---

## 📡 Pattern 7: Webhook Middleware

**Problem**: You need to send data to external services after each request.

### Solution: Async Webhook Middleware

```python
import threading
import requests

class WebhookMiddleware:
    """
    Sends webhooks asynchronously
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.webhook_url = 'https://example.com/webhook'
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Send webhook asynchronously (don't block response)
        if response.status_code >= 400:
            # Only send on errors
            thread = threading.Thread(
                target=self.send_webhook,
                args=(request, response)
            )
            thread.daemon = True
            thread.start()
        
        return response
    
    def send_webhook(self, request, response):
        """Send webhook in background"""
        try:
            data = {
                'path': request.path,
                'status': response.status_code,
                'method': request.method,
            }
            requests.post(self.webhook_url, json=data, timeout=5)
        except Exception as e:
            print(f"Webhook failed: {e}")
```

---

## 🎯 Pattern 8: Feature Flag Middleware

**Problem**: You want to enable/disable features without deploying code.

### Solution: Feature Flag Middleware

```python
from django.core.cache import cache

class FeatureFlagMiddleware:
    """
    Checks feature flags for each request
    """
    
    def __call__(self, request):
        # Load feature flags (cached)
        flags = cache.get('feature_flags')
        
        if flags is None:
            # Load from database
            flags = self.load_feature_flags()
            cache.set('feature_flags', flags, 300)  # Cache 5 min
        
        # Add to request
        request.feature_flags = flags
        
        response = self.get_response(request)
        return response
    
    def load_feature_flags(self):
        """Load feature flags from database"""
        from myapp.models import FeatureFlag
        return {
            flag.name: flag.enabled 
            for flag in FeatureFlag.objects.all()
        }
```

**Usage in views:**
```python
def my_view(request):
    if request.feature_flags.get('new_ui', False):
        # Show new UI
        return render(request, 'new_template.html')
    else:
        # Show old UI
        return render(request, 'old_template.html')
```

---

## 🔄 Pattern 9: Request Replay Middleware

**Problem**: You want to record and replay requests for debugging.

### Solution: Request Recorder

```python
import json
import pickle

class RequestReplayMiddleware:
    """
    Records requests for later replay
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.recording = True
        self.requests_file = 'recorded_requests.json'
    
    def __call__(self, request):
        if self.recording:
            self.record_request(request)
        
        response = self.get_response(request)
        return response
    
    def record_request(self, request):
        """Save request details"""
        request_data = {
            'method': request.method,
            'path': request.path,
            'GET': dict(request.GET),
            'POST': dict(request.POST),
            'headers': dict(request.META),
        }
        
        # Append to file
        with open(self.requests_file, 'a') as f:
            f.write(json.dumps(request_data) + '\n')
    
    @classmethod
    def replay_requests(cls):
        """Replay recorded requests"""
        from django.test import Client
        
        client = Client()
        with open(cls.requests_file, 'r') as f:
            for line in f:
                req_data = json.loads(line)
                
                if req_data['method'] == 'GET':
                    client.get(req_data['path'], req_data['GET'])
                elif req_data['method'] == 'POST':
                    client.post(req_data['path'], req_data['POST'])
```

---

## 🎨 Pattern 10: Response Transformation Pipeline

**Problem**: You need to apply multiple transformations to responses.

### Solution: Transformation Pipeline

```python
class TransformationMiddleware:
    """
    Applies multiple transformations to responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.transformers = [
            self.minify_html,
            self.add_analytics,
            self.add_cache_busting,
        ]
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only transform HTML
        if 'text/html' in response.get('Content-Type', ''):
            content = response.content.decode('utf-8')
            
            # Apply each transformer
            for transformer in self.transformers:
                content = transformer(content, request)
            
            response.content = content.encode('utf-8')
            response['Content-Length'] = len(response.content)
        
        return response
    
    def minify_html(self, content, request):
        """Remove extra whitespace"""
        import re
        content = re.sub(r'\s+', ' ', content)
        return content
    
    def add_analytics(self, content, request):
        """Inject analytics code"""
        analytics = '<script>console.log("Analytics");</script>'
        content = content.replace('</body>', f'{analytics}</body>')
        return content
    
    def add_cache_busting(self, content, request):
        """Add cache busting to static files"""
        import time
        version = str(int(time.time()))
        content = content.replace('/static/', f'/static/{version}/')
        return content
```

---

## 🔬 Pattern 11: A/B Testing Middleware

**Problem**: You want to run A/B tests.

### Solution: A/B Test Middleware

```python
import random

class ABTestMiddleware:
    """
    Assigns users to A/B test groups
    """
    
    def __call__(self, request):
        # Get or create test group
        test_group = request.COOKIES.get('ab_test_group')
        
        if not test_group:
            # Assign randomly: 50% A, 50% B
            test_group = random.choice(['A', 'B'])
        
        request.ab_test_group = test_group
        
        response = self.get_response(request)
        
        # Save group in cookie
        response.set_cookie(
            'ab_test_group', 
            test_group,
            max_age=30*24*60*60  # 30 days
        )
        
        return response
```

**Usage in views:**
```python
def my_view(request):
    if request.ab_test_group == 'A':
        template = 'version_a.html'
    else:
        template = 'version_b.html'
    
    return render(request, template)
```

---

## 💡 Pattern Selection Guide

**Choose the right pattern:**

| Need | Pattern |
|------|---------|
| Run only on certain URLs | Conditional Middleware |
| Share data between middleware | Middleware Chaining |
| Setup/cleanup | Context Manager |
| Similar middleware variants | Factory Pattern |
| Per-view middleware | Decorator Pattern |
| Multi-org app | Multi-Tenant |
| External integrations | Webhook |
| Feature toggles | Feature Flags |
| Debugging | Request Replay |
| Response modifications | Transformation Pipeline |
| Experiments | A/B Testing |

---

## 🎓 Quick Check

You should now understand:

- ✅ Conditional middleware activation
- ✅ Middleware chaining and data sharing
- ✅ Context managers for cleanup
- ✅ Factory pattern for reusable middleware
- ✅ Multi-tenant architecture
- ✅ Async operations with webhooks
- ✅ Feature flags
- ✅ A/B testing

---

## 🚀 Next Steps

**Continue to**: [Security Considerations →](./04-security.md)

---

*Continue to: [Security Considerations →](./04-security.md)*
