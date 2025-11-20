# Request Processing 📥

Learn how to work with HTTP requests in middleware, from basic to advanced techniques.

---

## 🎯 Understanding Requests

When a user visits your site, Django creates a `request` object containing all information about that visit:

```python
request.method        # GET, POST, PUT, DELETE, etc.
request.path          # /home/, /api/users/, etc.
request.user          # The logged-in user
request.GET           # URL parameters (?page=1&sort=name)
request.POST          # Form data
request.META          # Headers and server info
request.FILES         # Uploaded files
request.body          # Raw request body
```

---

## 📖 Basic Request Processing

### Example 1: Logging All Requests

```python
class RequestLoggerMiddleware:
    """
    Logs every request with details
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Log request details
        print(f"📥 METHOD: {request.method}")
        print(f"📥 PATH: {request.path}")
        print(f"📥 USER: {request.user}")
        print(f"📥 IP: {request.META.get('REMOTE_ADDR')}")
        
        response = self.get_response(request)
        return response
```

**Output when someone visits `/home/`:**
```
📥 METHOD: GET
📥 PATH: /home/
📥 USER: john_doe
📥 IP: 192.168.1.100
```

---

### Example 2: Detecting Request Method

```python
class MethodDetectorMiddleware:
    """
    Handles different HTTP methods differently
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.method == 'GET':
            print("👀 User is viewing a page")
            
        elif request.method == 'POST':
            print("📝 User is submitting data")
            
        elif request.method == 'DELETE':
            print("🗑️ User is deleting something")
            
        elif request.method == 'PUT':
            print("✏️ User is updating something")
        
        response = self.get_response(request)
        return response
```

---

## 🔍 Working with Request Data

### Example 3: Processing GET Parameters

```python
class QueryParamProcessorMiddleware:
    """
    Process URL query parameters
    """
    
    def __call__(self, request):
        # URL: /search/?q=python&page=2
        
        search_query = request.GET.get('q', '')
        page_number = request.GET.get('page', '1')
        
        if search_query:
            print(f"🔍 Searching for: {search_query}")
            print(f"📄 Page: {page_number}")
            
            # Add processed data to request
            request.search_info = {
                'query': search_query,
                'page': int(page_number)
            }
        
        response = self.get_response(request)
        return response
```

**Usage in views:**
```python
def search_view(request):
    # Access the processed data
    if hasattr(request, 'search_info'):
        query = request.search_info['query']
        page = request.search_info['page']
```

---

### Example 4: Processing POST Data

```python
class FormDataProcessorMiddleware:
    """
    Process form submissions
    """
    
    def __call__(self, request):
        if request.method == 'POST':
            # Get form data
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            
            print(f"📝 Form submitted:")
            print(f"   Username: {username}")
            print(f"   Email: {email}")
            
            # Validate data
            if not username or not email:
                print("⚠️ Missing required fields")
        
        response = self.get_response(request)
        return response
```

---

## 🛡️ Request Validation

### Example 5: Content Type Validation

```python
from django.http import HttpResponse

class ContentTypeValidatorMiddleware:
    """
    Validates request content type for API endpoints
    """
    
    def __call__(self, request):
        # Only check API endpoints
        if request.path.startswith('/api/'):
            
            # For POST/PUT, require JSON
            if request.method in ['POST', 'PUT']:
                content_type = request.META.get('CONTENT_TYPE', '')
                
                if 'application/json' not in content_type:
                    return HttpResponse(
                        "Content-Type must be application/json",
                        status=400
                    )
        
        response = self.get_response(request)
        return response
```

**What this does:**
- Checks API requests have correct content type
- Rejects invalid requests early
- Returns error before hitting views

---

### Example 6: Request Size Limiter

```python
class RequestSizeLimiterMiddleware:
    """
    Limits the size of incoming requests
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # 5MB limit
        self.max_size = 5 * 1024 * 1024
    
    def __call__(self, request):
        # Check content length
        content_length = request.META.get('CONTENT_LENGTH')
        
        if content_length:
            content_length = int(content_length)
            
            if content_length > self.max_size:
                return HttpResponse(
                    f"Request too large. Max size: {self.max_size} bytes",
                    status=413
                )
        
        response = self.get_response(request)
        return response
```

---

## 🎨 Modifying Requests

### Example 7: Adding Request Metadata

```python
import datetime

class RequestMetadataMiddleware:
    """
    Adds useful metadata to every request
    """
    
    def __call__(self, request):
        # Add timestamp
        request.timestamp = datetime.datetime.now()
        
        # Add unique request ID
        import uuid
        request.request_id = str(uuid.uuid4())
        
        # Add client info
        request.client_info = {
            'ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referer': request.META.get('HTTP_REFERER', ''),
        }
        
        print(f"🆔 Request ID: {request.request_id}")
        print(f"⏰ Timestamp: {request.timestamp}")
        
        response = self.get_response(request)
        return response
```

**Usage in views:**
```python
def my_view(request):
    print(f"Processing request {request.request_id}")
    print(f"Received at {request.timestamp}")
    print(f"From IP: {request.client_info['ip']}")
```

---

### Example 8: Request Sanitization

```python
class InputSanitizerMiddleware:
    """
    Sanitizes user input to prevent XSS attacks
    """
    
    def __call__(self, request):
        if request.method == 'POST':
            # Create a mutable copy
            post_data = request.POST.copy()
            
            # Sanitize each field
            for key, value in post_data.items():
                # Remove dangerous characters
                cleaned = value.replace('<', '&lt;').replace('>', '&gt;')
                post_data[key] = cleaned
            
            # Replace POST data (be careful with this!)
            request.POST = post_data
        
        response = self.get_response(request)
        return response
```

**⚠️ Warning**: Modifying POST data directly can cause issues. This is just an example!

---

## 🔐 Authentication & Authorization

### Example 9: API Key Authentication

```python
from django.http import JsonResponse

class APIKeyAuthMiddleware:
    """
    Checks for valid API key in request headers
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # In production, load from database or environment
        self.valid_api_keys = [
            'abc123def456',
            'xyz789ghi012',
        ]
    
    def __call__(self, request):
        # Only check API endpoints
        if request.path.startswith('/api/'):
            
            # Get API key from header
            api_key = request.META.get('HTTP_X_API_KEY', '')
            
            if not api_key:
                return JsonResponse(
                    {'error': 'API key required'},
                    status=401
                )
            
            if api_key not in self.valid_api_keys:
                return JsonResponse(
                    {'error': 'Invalid API key'},
                    status=403
                )
            
            # Add API key to request for views to use
            request.api_key = api_key
            print(f"✅ Valid API key: {api_key[:8]}...")
        
        response = self.get_response(request)
        return response
```

**Usage:**
```bash
curl -H "X-API-Key: abc123def456" http://example.com/api/data/
```

---

### Example 10: User Agent Blocking

```python
class BotBlockerMiddleware:
    """
    Blocks known bad bots and scrapers
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_agents = [
            'badbot',
            'scraper',
            'spam',
        ]
    
    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        # Check if it's a blocked bot
        for bot in self.blocked_agents:
            if bot in user_agent:
                print(f"🤖 Blocked bot: {user_agent}")
                return HttpResponse("Access Denied", status=403)
        
        response = self.get_response(request)
        return response
```

---

## 📊 Request Analytics

### Example 11: Request Statistics

```python
from collections import defaultdict
import time

class RequestStatsMiddleware:
    """
    Collects statistics about requests
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.stats = {
            'total': 0,
            'methods': defaultdict(int),
            'paths': defaultdict(int),
            'users': defaultdict(int),
        }
    
    def __call__(self, request):
        # Increment counters
        self.stats['total'] += 1
        self.stats['methods'][request.method] += 1
        self.stats['paths'][request.path] += 1
        
        if request.user.is_authenticated:
            self.stats['users'][request.user.username] += 1
        
        # Print stats every 10 requests
        if self.stats['total'] % 10 == 0:
            print("\n📊 Request Statistics:")
            print(f"   Total: {self.stats['total']}")
            print(f"   Methods: {dict(self.stats['methods'])}")
            print(f"   Top Paths: {dict(list(self.stats['paths'].items())[:5])}")
        
        response = self.get_response(request)
        return response
```

---

## 💡 Best Practices

### 1. **Read-Only When Possible**
```python
# ✅ Good - Just reading
user_id = request.user.id

# ⚠️ Be careful - Modifying
request.custom_data = {'key': 'value'}  # OK
request.POST = modified_data  # Risky!
```

### 2. **Check Before Accessing**
```python
# ❌ Bad
email = request.POST['email']  # Crashes if missing

# ✅ Good
email = request.POST.get('email', '')  # Returns '' if missing
```

### 3. **Handle Missing Data**
```python
# ✅ Good
user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
if user_agent:
    # Process it
```

---

## ⚠️ Common Pitfalls

1. **Don't assume data exists**
   ```python
   # ❌ Bad
   username = request.POST['username']
   
   # ✅ Good
   username = request.POST.get('username', '')
   ```

2. **Don't modify request.POST directly** (usually)
   - It's a QueryDict and can cause issues
   - Read from it, don't write to it

3. **Remember request.body can only be read once**
   ```python
   # ❌ Bad
   body1 = request.body  # First read
   body2 = request.body  # Empty! Already consumed
   ```

---

## 🎓 Quick Check

You should now understand:

- ✅ How to access request data (GET, POST, META)
- ✅ How to validate requests
- ✅ How to add data to requests for views
- ✅ How to handle different HTTP methods
- ✅ How to implement authentication checks
- ✅ Best practices for request processing

---

## 🚀 Next Steps

Ready to learn about processing responses?

**Continue to**: [Response Processing →](./03-response-processing.md)

---

*Continue to: [Response Processing →](./03-response-processing.md)*
