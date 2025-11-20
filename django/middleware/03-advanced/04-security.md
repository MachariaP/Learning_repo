# Security Considerations 🔒

Security is CRITICAL in middleware! Since middleware runs on every request, security bugs affect your entire application.

---

## ⚠️ The Golden Rules

1. **Never trust user input**
2. **Validate everything**
3. **Fail securely (deny by default)**
4. **Log security events**
5. **Keep middleware simple to avoid bugs**

---

## 🚨 Common Security Vulnerabilities

### 1. SQL Injection in Middleware

❌ **VULNERABLE**:
```python
class VulnerableMiddleware:
    def __call__(self, request):
        # DANGER! User input directly in SQL
        user_id = request.GET.get('user_id', '')
        query = f"SELECT * FROM users WHERE id = {user_id}"
        # Attacker can send: ?user_id=1 OR 1=1
        
        response = self.get_response(request)
        return response
```

✅ **SECURE**:
```python
class SecureMiddleware:
    def __call__(self, request):
        user_id = request.GET.get('user_id', '')
        
        # Use Django ORM (safe from SQL injection)
        try:
            user = User.objects.get(id=int(user_id))
        except (ValueError, User.DoesNotExist):
            return HttpResponseForbidden("Invalid user ID")
        
        response = self.get_response(request)
        return response
```

---

### 2. XSS (Cross-Site Scripting)

❌ **VULNERABLE**:
```python
class VulnerableMiddleware:
    def __call__(self, request):
        response = self.get_response(request)
        
        # DANGER! User input directly in HTML
        name = request.GET.get('name', '')
        banner = f'<div>Welcome {name}!</div>'
        # Attacker can send: ?name=<script>alert('XSS')</script>
        
        content = response.content.decode('utf-8')
        content = content.replace('</body>', f'{banner}</body>')
        response.content = content.encode('utf-8')
        
        return response
```

✅ **SECURE**:
```python
from django.utils.html import escape

class SecureMiddleware:
    def __call__(self, request):
        response = self.get_response(request)
        
        # Escape user input!
        name = escape(request.GET.get('name', ''))
        banner = f'<div>Welcome {name}!</div>'
        
        content = response.content.decode('utf-8')
        content = content.replace('</body>', f'{banner}</body>')
        response.content = content.encode('utf-8')
        
        return response
```

---

### 3. Authentication Bypass

❌ **VULNERABLE**:
```python
class VulnerableAuthMiddleware:
    def __call__(self, request):
        # DANGER! Trusts user-provided header
        user_id = request.META.get('HTTP_X_USER_ID')
        if user_id:
            # Attacker can send fake header!
            request.user = User.objects.get(id=user_id)
        
        response = self.get_response(request)
        return response
```

✅ **SECURE**:
```python
class SecureAuthMiddleware:
    def __call__(self, request):
        # Use proper authentication
        token = request.META.get('HTTP_AUTHORIZATION', '')
        
        if token.startswith('Bearer '):
            token = token[7:]
            try:
                # Verify token cryptographically
                user = self.verify_token(token)
                request.user = user
            except InvalidToken:
                return HttpResponse("Unauthorized", status=401)
        
        response = self.get_response(request)
        return response
    
    def verify_token(self, token):
        # Use proper token verification (JWT, etc.)
        # NOT just trust what user sends!
        pass
```

---

## 🔐 Security Best Practices

### 1. Input Validation

```python
class InputValidationMiddleware:
    """
    Validates all user input
    """
    
    def __call__(self, request):
        # Validate query parameters
        for key, value in request.GET.items():
            if not self.is_safe_input(value):
                return HttpResponseBadRequest(f"Invalid input: {key}")
        
        # Validate POST data
        if request.method == 'POST':
            for key, value in request.POST.items():
                if not self.is_safe_input(value):
                    return HttpResponseBadRequest(f"Invalid input: {key}")
        
        response = self.get_response(request)
        return response
    
    def is_safe_input(self, value):
        """Check if input is safe"""
        # Maximum length
        if len(value) > 1000:
            return False
        
        # No null bytes
        if '\x00' in value:
            return False
        
        # Add more validation as needed
        return True
```

---

### 2. Rate Limiting (Prevent DDoS)

```python
import time
from collections import defaultdict
from django.core.cache import cache

class SecureRateLimitMiddleware:
    """
    Rate limiting to prevent abuse
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 100  # requests
        self.time_window = 60  # seconds
    
    def __call__(self, request):
        client_id = self.get_client_identifier(request)
        cache_key = f'rate_limit_{client_id}'
        
        # Get request count
        requests = cache.get(cache_key, [])
        current_time = time.time()
        
        # Remove old requests
        requests = [t for t in requests if current_time - t < self.time_window]
        
        # Check limit
        if len(requests) >= self.rate_limit:
            # Log the attack
            print(f"🚨 Rate limit exceeded: {client_id}")
            return HttpResponse(
                "Too many requests. Please try again later.",
                status=429
            )
        
        # Add this request
        requests.append(current_time)
        cache.set(cache_key, requests, self.time_window)
        
        response = self.get_response(request)
        return response
    
    def get_client_identifier(self, request):
        """Get unique client ID"""
        # Use multiple factors
        ip = request.META.get('REMOTE_ADDR', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        if request.user.is_authenticated:
            return f"user_{request.user.id}"
        
        return f"ip_{ip}"
```

---

### 3. HTTPS Enforcement

```python
class HTTPSEnforcementMiddleware:
    """
    Forces all connections to use HTTPS
    """
    
    def __call__(self, request):
        # Check if using HTTPS
        if not request.is_secure():
            # Redirect to HTTPS
            secure_url = request.build_absolute_uri(request.get_full_path())
            secure_url = secure_url.replace('http://', 'https://')
            
            return HttpResponsePermanentRedirect(secure_url)
        
        response = self.get_response(request)
        
        # Add HSTS header
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
```

---

### 4. Security Headers

```python
class SecurityHeadersMiddleware:
    """
    Adds security headers to all responses
    """
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Content Security Policy
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
        )
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=()'
        )
        
        return response
```

---

## 🔍 Secure Logging

### What to Log

```python
import logging

logger = logging.getLogger('security')

class SecurityLoggingMiddleware:
    """
    Logs security events
    """
    
    def __call__(self, request):
        # Log suspicious activity
        self.check_suspicious(request)
        
        response = self.get_response(request)
        
        # Log security events
        if response.status_code == 401:
            logger.warning(f"Unauthorized access attempt: {request.path}")
        
        if response.status_code == 403:
            logger.warning(f"Forbidden access attempt: {request.path}")
        
        return response
    
    def check_suspicious(self, request):
        """Check for suspicious activity"""
        # SQL injection attempts
        dangerous_params = ['OR', 'DROP', 'DELETE', 'UPDATE', 'INSERT']
        query_string = request.META.get('QUERY_STRING', '').upper()
        
        for param in dangerous_params:
            if param in query_string:
                logger.critical(f"🚨 SQL injection attempt from {request.META.get('REMOTE_ADDR')}: {query_string}")
        
        # XSS attempts
        if '<script' in query_string.lower():
            logger.critical(f"🚨 XSS attempt from {request.META.get('REMOTE_ADDR')}: {query_string}")
        
        # Path traversal attempts
        if '../' in request.path or '..\\' in request.path:
            logger.critical(f"🚨 Path traversal attempt from {request.META.get('REMOTE_ADDR')}: {request.path}")
```

### What NOT to Log

❌ **NEVER LOG**:
- Passwords
- Credit card numbers
- Social security numbers
- API keys
- Session tokens
- Personal health information

```python
class SafeLoggingMiddleware:
    """
    Logs safely without sensitive data
    """
    
    def __call__(self, request):
        # Filter sensitive data before logging
        safe_post = {}
        for key, value in request.POST.items():
            if self.is_sensitive(key):
                safe_post[key] = '[REDACTED]'
            else:
                safe_post[key] = value
        
        logger.info(f"POST data: {safe_post}")
        
        response = self.get_response(request)
        return response
    
    def is_sensitive(self, key):
        """Check if field contains sensitive data"""
        sensitive_keywords = [
            'password', 'passwd', 'pwd',
            'secret', 'token', 'api_key',
            'credit_card', 'ssn', 'cvv',
        ]
        
        key_lower = key.lower()
        return any(keyword in key_lower for keyword in sensitive_keywords)
```

---

## 🛡️ CSRF Protection

```python
from django.middleware.csrf import get_token

class CustomCSRFMiddleware:
    """
    Custom CSRF protection
    """
    
    def __call__(self, request):
        # Require CSRF token for state-changing methods
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            # Get CSRF token from header or POST data
            token = request.META.get('HTTP_X_CSRFTOKEN') or request.POST.get('csrfmiddlewaretoken')
            
            # Verify token
            if not token or not self.verify_token(request, token):
                return HttpResponseForbidden("CSRF verification failed")
        
        response = self.get_response(request)
        
        # Add CSRF token to response
        response['X-CSRFToken'] = get_token(request)
        
        return response
    
    def verify_token(self, request, token):
        """Verify CSRF token"""
        expected_token = get_token(request)
        return token == expected_token
```

---

## 🔑 Secure Token Management

```python
import hmac
import hashlib
from django.conf import settings

class SecureTokenMiddleware:
    """
    Manages secure API tokens
    """
    
    def __call__(self, request):
        if request.path.startswith('/api/'):
            # Get token from header
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            
            if not auth_header.startswith('Bearer '):
                return JsonResponse({'error': 'Missing token'}, status=401)
            
            token = auth_header[7:]
            
            # Verify token
            if not self.verify_token(token):
                return JsonResponse({'error': 'Invalid token'}, status=401)
            
            # Add user to request
            request.api_user = self.get_user_from_token(token)
        
        response = self.get_response(request)
        return response
    
    def verify_token(self, token):
        """Verify token using HMAC"""
        try:
            # Split token into data and signature
            data, signature = token.rsplit('.', 1)
            
            # Calculate expected signature
            expected_sig = hmac.new(
                settings.SECRET_KEY.encode(),
                data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Compare securely (prevent timing attacks)
            return hmac.compare_digest(signature, expected_sig)
            
        except Exception:
            return False
    
    def get_user_from_token(self, token):
        """Extract user from token"""
        # Implement token parsing
        pass
```

---

## 🚨 Security Checklist

Before deploying middleware, verify:

- [ ] No SQL injection vulnerabilities
- [ ] All user input is validated
- [ ] XSS protection in place
- [ ] CSRF tokens verified
- [ ] Rate limiting implemented
- [ ] HTTPS enforced
- [ ] Security headers added
- [ ] Sensitive data not logged
- [ ] Authentication properly implemented
- [ ] Authorization checks in place
- [ ] Error messages don't leak info
- [ ] Dependencies up to date
- [ ] Security audit performed

---

## 🎯 Security Testing

### Test for SQL Injection

```python
def test_sql_injection():
    """Test SQL injection protection"""
    from django.test import Client
    
    client = Client()
    
    # Try SQL injection
    response = client.get('/search/?q=1 OR 1=1')
    
    # Should be rejected or sanitized
    assert response.status_code in [400, 403] or 'OR 1=1' not in response.content.decode()
```

### Test for XSS

```python
def test_xss():
    """Test XSS protection"""
    from django.test import Client
    
    client = Client()
    
    # Try XSS
    response = client.get('/search/?q=<script>alert("XSS")</script>')
    
    # Should be escaped
    assert '<script>' not in response.content.decode()
    assert '&lt;script&gt;' in response.content.decode() or response.status_code in [400, 403]
```

---

## 💡 Security Best Practices Summary

1. **Validate all input** - Never trust users
2. **Escape all output** - Prevent XSS
3. **Use parameterized queries** - Prevent SQL injection
4. **Implement rate limiting** - Prevent abuse
5. **Enforce HTTPS** - Protect data in transit
6. **Add security headers** - Defense in depth
7. **Log security events** - Detect attacks
8. **Don't log sensitive data** - Protect privacy
9. **Use CSRF protection** - Prevent cross-site attacks
10. **Keep dependencies updated** - Patch vulnerabilities

---

## 🎓 Final Check

You should now understand:

- ✅ Common security vulnerabilities
- ✅ Input validation techniques
- ✅ XSS and SQL injection prevention
- ✅ Rate limiting for DDoS protection
- ✅ HTTPS enforcement
- ✅ Security headers
- ✅ Secure logging practices
- ✅ CSRF protection
- ✅ Token management
- ✅ Security testing

---

## 🎉 Congratulations!

You've completed the **Advanced Middleware Course**!

You now know:
- ✅ What middleware is and how it works
- ✅ All types of middleware
- ✅ How to create custom middleware
- ✅ Request and response processing
- ✅ Practical use cases
- ✅ Middleware ordering
- ✅ Performance optimization
- ✅ Advanced patterns
- ✅ Security best practices

---

## 🚀 Next Steps

1. **Practice**: Build your own middleware
2. **Review**: Go back to sections you found difficult
3. **Apply**: Use middleware in real projects
4. **Share**: Teach others what you learned
5. **Stay Updated**: Follow Django security announcements

---

## 📚 Additional Resources

- Django Documentation: https://docs.djangoproject.com/en/stable/topics/http/middleware/
- OWASP Security Guide: https://owasp.org/
- Django Security: https://docs.djangoproject.com/en/stable/topics/security/

---

*Happy coding and stay secure! 🔒*
