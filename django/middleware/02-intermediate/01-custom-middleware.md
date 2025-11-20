# Creating Custom Middleware 🛠️

Welcome to the intermediate level! Now you'll learn to create your own middleware from scratch.

---

## 🎯 What You'll Learn

In this section:
- How to create a custom middleware class
- How to configure it in Django
- Real-world examples you can use
- Common patterns and best practices

---

## 📝 Basic Template

Every custom middleware follows this pattern:

```python
class MyCustomMiddleware:
    """
    Description of what this middleware does
    """
    
    def __init__(self, get_response):
        """
        One-time configuration and initialization
        """
        self.get_response = get_response
        # Any setup code here
    
    def __call__(self, request):
        """
        Code to run for each request/response
        """
        # Code to run before the view
        
        response = self.get_response(request)
        
        # Code to run after the view
        
        return response
```

---

## 🚀 Example 1: Simple Request Counter

Let's create middleware that counts how many requests each user makes:

```python
# middleware/request_counter.py

class RequestCounterMiddleware:
    """
    Counts total requests and requests per user
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.total_requests = 0
        self.user_requests = {}
    
    def __call__(self, request):
        # Increment total counter
        self.total_requests += 1
        
        # Count requests per user
        user_id = request.user.id if request.user.is_authenticated else 'anonymous'
        self.user_requests[user_id] = self.user_requests.get(user_id, 0) + 1
        
        # Log the stats
        print(f"📊 Total Requests: {self.total_requests}")
        print(f"📊 User {user_id} Requests: {self.user_requests[user_id]}")
        
        # Process the request
        response = self.get_response(request)
        
        return response
```

**What this does:**
- Counts every request made to your site
- Tracks requests per user
- Prints statistics to console

---

## 🔐 Example 2: IP Blocking Middleware

Block requests from specific IP addresses:

```python
# middleware/ip_blocker.py

from django.http import HttpResponseForbidden

class IPBlockerMiddleware:
    """
    Blocks requests from blacklisted IP addresses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # List of blocked IPs
        self.blocked_ips = [
            '192.168.1.100',
            '10.0.0.50',
        ]
    
    def __call__(self, request):
        # Get user's IP address
        user_ip = request.META.get('REMOTE_ADDR')
        
        # Check if IP is blocked
        if user_ip in self.blocked_ips:
            print(f"🚫 Blocked request from {user_ip}")
            return HttpResponseForbidden("Your IP address is blocked")
        
        # IP is allowed, continue
        response = self.get_response(request)
        return response
```

**What this does:**
- Gets the user's IP address
- Checks against a blacklist
- Blocks the request if IP is blacklisted
- Shows how to stop requests early

---

## ⏱️ Example 3: Request Timer Middleware

Measure how long each request takes:

```python
# middleware/request_timer.py

import time
from django.utils.deprecation import MiddlewareMixin

class RequestTimerMiddleware:
    """
    Measures and logs the time taken for each request
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Record start time
        start_time = time.time()
        
        # Store on request for views to access
        request.start_time = start_time
        
        # Process request
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Add to response headers
        response['X-Request-Time'] = f"{duration:.4f}s"
        
        # Log slow requests (over 1 second)
        if duration > 1.0:
            print(f"⚠️ SLOW REQUEST: {request.path} took {duration:.2f}s")
        else:
            print(f"✅ {request.path} took {duration:.4f}s")
        
        return response
```

**What this does:**
- Times every request
- Adds timing to response headers
- Warns about slow requests
- Shows how to add data to requests and responses

---

## 🎨 Example 4: Custom Headers Middleware

Add custom headers to all responses:

```python
# middleware/custom_headers.py

class CustomHeadersMiddleware:
    """
    Adds custom headers to all responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Define your custom headers
        self.headers = {
            'X-Powered-By': 'My Awesome Django App',
            'X-Developer': 'Your Name',
            'X-Version': '1.0.0',
        }
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add all custom headers
        for header, value in self.headers.items():
            response[header] = value
        
        return response
```

**What this does:**
- Adds custom headers to every response
- Useful for branding or debugging
- Shows how to modify responses

---

## 📱 Example 5: Device Detection Middleware

Detect if user is on mobile or desktop:

```python
# middleware/device_detection.py

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
        # Get user agent string
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        # Check if it's a mobile device
        is_mobile = any(keyword in user_agent for keyword in self.mobile_keywords)
        
        # Add to request for views to use
        request.is_mobile = is_mobile
        request.device_type = 'mobile' if is_mobile else 'desktop'
        
        print(f"📱 Device: {request.device_type}")
        
        response = self.get_response(request)
        return response
```

**What this does:**
- Detects mobile vs desktop users
- Adds device info to request
- Views can then render different templates
- Shows how to add custom attributes to requests

---

## ⚙️ How to Install Your Middleware

After creating middleware, add it to `settings.py`:

```python
# settings.py

MIDDLEWARE = [
    # Django's built-in middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Your custom middleware
    'middleware.request_counter.RequestCounterMiddleware',
    'middleware.ip_blocker.IPBlockerMiddleware',
    'middleware.request_timer.RequestTimerMiddleware',
    'middleware.custom_headers.CustomHeadersMiddleware',
    'middleware.device_detection.DeviceDetectionMiddleware',
]
```

**Important**: The path is `app_name.file_name.ClassName`

---

## 📂 Project Structure

Organize your middleware files:

```
myproject/
├── manage.py
├── myproject/
│   ├── settings.py
│   └── middleware/          ← Create this folder
│       ├── __init__.py      ← Empty file
│       ├── request_counter.py
│       ├── ip_blocker.py
│       ├── request_timer.py
│       ├── custom_headers.py
│       └── device_detection.py
└── myapp/
    └── views.py
```

---

## 💡 Best Practices

### 1. **Keep It Simple**
Each middleware should do ONE thing well.

❌ **Bad**:
```python
class AllInOneMiddleware:
    # Handles authentication, logging, caching, etc.
    # Too much!
```

✅ **Good**:
```python
class LoggingMiddleware:
    # Only handles logging
    
class CachingMiddleware:
    # Only handles caching
```

---

### 2. **Make It Fast**

Middleware runs on EVERY request!

❌ **Bad**:
```python
def __call__(self, request):
    # Slow database query
    all_users = User.objects.all()  # Don't do this!
    response = self.get_response(request)
    return response
```

✅ **Good**:
```python
def __call__(self, request):
    # Only query if needed
    if request.user.is_authenticated:
        # Quick, specific query
        user_data = cache.get(f'user_{request.user.id}')
    response = self.get_response(request)
    return response
```

---

### 3. **Handle Errors Gracefully**

```python
def __call__(self, request):
    try:
        # Your code here
        response = self.get_response(request)
        return response
    except Exception as e:
        # Log the error
        print(f"Middleware error: {e}")
        # Don't crash! Return something
        return HttpResponse("An error occurred", status=500)
```

---

### 4. **Use Configuration**

Make middleware configurable:

```python
from django.conf import settings

class ConfigurableMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Get config from settings
        self.enabled = getattr(settings, 'MY_MIDDLEWARE_ENABLED', True)
        self.threshold = getattr(settings, 'MY_MIDDLEWARE_THRESHOLD', 100)
    
    def __call__(self, request):
        if not self.enabled:
            # Middleware is disabled
            return self.get_response(request)
        
        # Your logic here
        response = self.get_response(request)
        return response
```

Then in `settings.py`:
```python
MY_MIDDLEWARE_ENABLED = True
MY_MIDDLEWARE_THRESHOLD = 50
```

---

## ⚠️ Common Mistakes

### Mistake 1: Forgetting to return response
```python
def __call__(self, request):
    response = self.get_response(request)
    # Forgot to return!  ❌
```

### Mistake 2: Not calling get_response
```python
def __call__(self, request):
    # Do stuff
    return HttpResponse("Done")  # View never runs! ❌
```

### Mistake 3: Wrong import path
```python
# In settings.py
MIDDLEWARE = [
    'RequestTimerMiddleware',  # ❌ Wrong!
    'middleware.request_timer.RequestTimerMiddleware',  # ✅ Correct!
]
```

---

## 🎓 Quick Check

You should now be able to:

- ✅ Create a basic middleware class
- ✅ Add middleware to settings.py
- ✅ Modify requests before they reach views
- ✅ Modify responses before they're sent
- ✅ Add custom attributes to requests
- ✅ Stop requests early if needed

---

## 🚀 Next Steps

Now that you can create middleware, learn how to:
- **[Process Requests](./02-request-processing.md)** in detail
- Handle different types of requests
- Work with request data

---

## 💭 Practice Exercise

**Challenge**: Create middleware that:
1. Counts total page views
2. Tracks unique visitors
3. Logs requests to a file
4. Adds a custom "X-Page-Views" header

<details>
<summary><b>💡 Solution Hint</b></summary>

```python
class PageViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.total_views = 0
        self.unique_visitors = set()
    
    def __call__(self, request):
        self.total_views += 1
        visitor_ip = request.META.get('REMOTE_ADDR')
        self.unique_visitors.add(visitor_ip)
        
        response = self.get_response(request)
        response['X-Page-Views'] = str(self.total_views)
        
        return response
```

</details>

---

*Continue to: [Request Processing →](./02-request-processing.md)*
