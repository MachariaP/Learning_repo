# Response Processing 📤

Learn how to work with HTTP responses in middleware - modifying, enhancing, and controlling what gets sent back to users.

---

## 🎯 Understanding Responses

After your view processes a request, it creates a `response` object:

```python
response.status_code    # 200, 404, 500, etc.
response.content        # The actual HTML/JSON/data
response.headers        # HTTP headers
response.cookies        # Cookies to set
```

---

## 📖 Basic Response Processing

### Example 1: Adding Headers to All Responses

```python
class ResponseHeaderMiddleware:
    """
    Adds custom headers to every response
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add custom headers
        response['X-Server'] = 'My Django Server'
        response['X-Request-ID'] = getattr(request, 'request_id', 'unknown')
        response['X-Processing-Time'] = '0.05s'
        
        return response
```

**Result**: Every response now includes these headers!

---

### Example 2: Status Code Logger

```python
class StatusCodeLoggerMiddleware:
    """
    Logs all HTTP status codes
    """
    
    def __call__(self, request):
        response = self.get_response(request)
        
        status = response.status_code
        
        if status == 200:
            print(f"✅ Success: {request.path}")
        elif status == 404:
            print(f"❌ Not Found: {request.path}")
        elif status >= 500:
            print(f"💥 Server Error ({status}): {request.path}")
        elif status >= 400:
            print(f"⚠️ Client Error ({status}): {request.path}")
        
        return response
```

---

## 🎨 Modifying Response Content

### Example 3: Content Modification

```python
class ContentModifierMiddleware:
    """
    Modifies HTML content before sending
    """
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only modify HTML responses
        if 'text/html' in response.get('Content-Type', ''):
            # Convert bytes to string
            content = response.content.decode('utf-8')
            
            # Add a banner to all pages
            banner = '<div class="banner">Welcome to our site!</div>'
            content = content.replace('<body>', f'<body>{banner}')
            
            # Convert back to bytes
            response.content = content.encode('utf-8')
            
            # Update content length
            response['Content-Length'] = len(response.content)
        
        return response
```

**⚠️ Warning**: Modifying HTML can be slow for large pages!

---

### Example 4: JSON Response Wrapper

```python
import json
from django.http import JsonResponse

class JSONWrapperMiddleware:
    """
    Wraps all JSON responses in a consistent format
    """
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only wrap JSON responses
        if isinstance(response, JsonResponse):
            # Get original data
            original_data = json.loads(response.content)
            
            # Wrap it
            wrapped_data = {
                'success': response.status_code < 400,
                'data': original_data,
                'timestamp': str(datetime.datetime.now()),
                'request_id': getattr(request, 'request_id', None)
            }
            
            # Create new response
            response = JsonResponse(wrapped_data)
        
        return response
```

**Before:**
```json
{"users": ["Alice", "Bob"]}
```

**After:**
```json
{
    "success": true,
    "data": {"users": ["Alice", "Bob"]},
    "timestamp": "2024-01-15 10:30:00",
    "request_id": "abc-123"
}
```

---

## 🔐 Security Headers

### Example 5: Security Headers Middleware

```python
class SecurityHeadersMiddleware:
    """
    Adds security-related headers to all responses
    """
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Enforce HTTPS
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Content Security Policy
        response['Content-Security-Policy'] = "default-src 'self'"
        
        return response
```

**What this protects against:**
- Clickjacking attacks
- MIME type confusion
- Cross-site scripting (XSS)
- Forces HTTPS connections

---

### Example 6: CORS Headers

```python
class CORSMiddleware:
    """
    Adds CORS headers for API access
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Allowed origins
        self.allowed_origins = [
            'http://localhost:3000',
            'https://myapp.com',
        ]
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Get origin from request
        origin = request.META.get('HTTP_ORIGIN', '')
        
        # Check if allowed
        if origin in self.allowed_origins:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response['Access-Control-Allow-Credentials'] = 'true'
        
        return response
```

---

## 🍪 Working with Cookies

### Example 7: Cookie Manager

```python
class CookieManagerMiddleware:
    """
    Manages cookies in responses
    """
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Set a cookie
        response.set_cookie(
            key='last_visit',
            value=str(datetime.datetime.now()),
            max_age=60*60*24*30,  # 30 days
            secure=True,  # Only over HTTPS
            httponly=True,  # Not accessible via JavaScript
            samesite='Strict'  # CSRF protection
        )
        
        # Track visits
        visits = request.COOKIES.get('visits', '0')
        new_visits = int(visits) + 1
        response.set_cookie('visits', str(new_visits))
        
        return response
```

---

## 📊 Response Monitoring

### Example 8: Response Size Monitor

```python
class ResponseSizeMonitorMiddleware:
    """
    Monitors and logs response sizes
    """
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Get response size
        size = len(response.content)
        size_kb = size / 1024
        
        # Log large responses
        if size_kb > 100:  # Over 100KB
            print(f"⚠️ Large response: {request.path} ({size_kb:.2f} KB)")
        
        # Add size to headers
        response['X-Response-Size'] = f"{size_kb:.2f}KB"
        
        return response
```

---

### Example 9: Error Response Handler

```python
class ErrorResponseMiddleware:
    """
    Customizes error responses
    """
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Customize 404 responses
        if response.status_code == 404:
            response.content = b"""
                <html>
                <body>
                    <h1>Page Not Found</h1>
                    <p>Sorry, the page you're looking for doesn't exist.</p>
                    <a href="/">Go Home</a>
                </body>
                </html>
            """
        
        # Customize 500 responses
        elif response.status_code >= 500:
            response.content = b"""
                <html>
                <body>
                    <h1>Server Error</h1>
                    <p>Something went wrong on our end.</p>
                </body>
                </html>
            """
        
        return response
```

---

## 🚀 Performance Optimization

### Example 10: Response Compression

```python
import gzip

class CompressionMiddleware:
    """
    Compresses responses to save bandwidth
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.min_size = 1024  # Only compress if larger than 1KB
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if client accepts gzip
        if 'gzip' not in request.META.get('HTTP_ACCEPT_ENCODING', ''):
            return response
        
        # Don't compress small responses
        if len(response.content) < self.min_size:
            return response
        
        # Compress
        compressed = gzip.compress(response.content)
        
        # Only use if actually smaller
        if len(compressed) < len(response.content):
            response.content = compressed
            response['Content-Encoding'] = 'gzip'
            response['Content-Length'] = len(compressed)
            
            print(f"🗜️ Compressed: {len(response.content)} → {len(compressed)} bytes")
        
        return response
```

---

### Example 11: Caching Headers

```python
class CacheControlMiddleware:
    """
    Adds caching headers to responses
    """
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # For static files
        if request.path.startswith('/static/'):
            # Cache for 1 year
            response['Cache-Control'] = 'public, max-age=31536000'
        
        # For dynamic pages
        elif request.path.startswith('/'):
            # Don't cache
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response
```

---

## 🎯 Conditional Responses

### Example 12: ETag Support

```python
import hashlib

class ETagMiddleware:
    """
    Adds ETag headers for caching
    """
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Generate ETag from content
        etag = hashlib.md5(response.content).hexdigest()
        response['ETag'] = etag
        
        # Check if client has current version
        if request.META.get('HTTP_IF_NONE_MATCH') == etag:
            # Return 304 Not Modified
            from django.http import HttpResponseNotModified
            return HttpResponseNotModified()
        
        return response
```

**How it works:**
1. First visit: Server sends content + ETag
2. Second visit: Client sends ETag
3. If same: Server sends 304 (no content needed)
4. If different: Server sends new content

---

## 📱 Content Type Handling

### Example 13: Content Type Router

```python
class ContentTypeRouterMiddleware:
    """
    Routes different content types differently
    """
    
    def __call__(self, request):
        response = self.get_response(request)
        
        content_type = response.get('Content-Type', '')
        
        if 'application/json' in content_type:
            # Add JSON-specific headers
            response['X-Content-Format'] = 'JSON'
            
        elif 'text/html' in content_type:
            # Add HTML-specific headers
            response['X-Content-Format'] = 'HTML'
            
        elif 'image/' in content_type:
            # Add image-specific headers
            response['Cache-Control'] = 'max-age=86400'  # 1 day
        
        return response
```

---

## 💡 Best Practices

### 1. **Check Content Type Before Modifying**

```python
# ✅ Good
if 'text/html' in response.get('Content-Type', ''):
    # Modify HTML
    
# ❌ Bad - modifies everything
response.content = response.content.replace(b'old', b'new')
```

### 2. **Be Careful with Content Length**

```python
# When modifying content, update length:
response.content = new_content
response['Content-Length'] = len(response.content)
```

### 3. **Don't Break Existing Headers**

```python
# ✅ Good - preserves existing headers
if not response.get('Cache-Control'):
    response['Cache-Control'] = 'no-cache'

# ❌ Bad - overwrites existing
response['Cache-Control'] = 'no-cache'
```

---

## ⚠️ Common Mistakes

### 1. **Forgetting to Update Content-Length**
```python
# ❌ Wrong
response.content = new_content
# Size is now wrong!

# ✅ Correct
response.content = new_content
response['Content-Length'] = len(response.content)
```

### 2. **Modifying Binary Content as String**
```python
# ❌ Wrong
content = response.content  # Still bytes
content = content.replace('old', 'new')  # Error!

# ✅ Correct
content = response.content.decode('utf-8')
content = content.replace('old', 'new')
response.content = content.encode('utf-8')
```

### 3. **Breaking Streaming Responses**
```python
# ⚠️ Careful with streaming
if hasattr(response, 'streaming'):
    # Don't modify streaming responses!
    return response
```

---

## 🎓 Quick Check

You should now understand:

- ✅ How to access and modify response data
- ✅ How to add headers to responses
- ✅ How to work with different content types
- ✅ How to implement security headers
- ✅ How to handle errors in responses
- ✅ How to optimize responses for performance

---

## 🚀 Next Steps

Now that you understand request and response processing, see how to apply it!

**Continue to**: [Practical Use Cases →](./04-use-cases.md)

---

*Continue to: [Practical Use Cases →](./04-use-cases.md)*
