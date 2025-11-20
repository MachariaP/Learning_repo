# Types of Middleware 📦

There are different types of middleware based on what they do and when they run. Let's explore them all!

---

## 🎯 Categorizing Middleware

Middleware can be categorized in two ways:

1. **By Purpose** - What does it do?
2. **By Hooks** - When does it run?

Let's explore both!

---

## 📚 Part 1: Middleware by Purpose

### 1. 🔐 Security Middleware

**Purpose**: Protect your application from attacks

**Examples**:
- CSRF protection (prevents fake form submissions)
- XSS protection (prevents malicious scripts)
- Security headers
- Input validation

```python
class SecurityMiddleware:
    def __call__(self, request):
        # Add security headers to all responses
        response = self.get_response(request)
        
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        return response
```

**When to use**: Always! Security should be on every site.

---

### 2. 🎫 Authentication Middleware

**Purpose**: Check who the user is and what they can access

**Examples**:
- Login verification
- Session management
- Permission checking
- User identification

```python
class AuthenticationMiddleware:
    def __call__(self, request):
        # Check if user is logged in
        if not request.user.is_authenticated:
            # Redirect to login page
            return redirect('/login/')
        
        response = self.get_response(request)
        return response
```

**When to use**: When you need users to log in.

---

### 3. 📝 Logging Middleware

**Purpose**: Record what's happening in your application

**Examples**:
- Request logging
- Error tracking
- Performance monitoring
- User activity tracking

```python
import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __call__(self, request):
        # Log incoming request
        logger.info(f"Request: {request.method} {request.path}")
        logger.info(f"User: {request.user}")
        logger.info(f"IP: {request.META.get('REMOTE_ADDR')}")
        
        response = self.get_response(request)
        
        # Log response
        logger.info(f"Response: {response.status_code}")
        
        return response
```

**When to use**: For debugging and monitoring production apps.

---

### 4. 💾 Caching Middleware

**Purpose**: Store responses to make your site faster

**Examples**:
- Page caching
- Response caching
- Database query caching

```python
from django.core.cache import cache

class CachingMiddleware:
    def __call__(self, request):
        # Check if we have cached response
        cache_key = f"page_{request.path}"
        cached_response = cache.get(cache_key)
        
        if cached_response:
            print("📦 Returning cached response")
            return cached_response
        
        # Get fresh response
        response = self.get_response(request)
        
        # Cache it for 5 minutes
        cache.set(cache_key, response, 300)
        
        return response
```

**When to use**: When pages don't change often.

---

### 5. 🔄 Session Middleware

**Purpose**: Remember information about users between requests

**Examples**:
- Shopping cart data
- User preferences
- Login state
- Temporary data

```python
class SessionMiddleware:
    def __call__(self, request):
        # Load session data
        request.session = self.load_session(request)
        
        response = self.get_response(request)
        
        # Save session data
        self.save_session(request)
        
        return response
```

**When to use**: When you need to remember user data.

---

### 6. 🌍 CORS Middleware

**Purpose**: Allow requests from other domains

**Examples**:
- API access from frontend apps
- Cross-domain requests
- Mobile app communication

```python
class CORSMiddleware:
    def __call__(self, request):
        response = self.get_response(request)
        
        # Allow requests from specific domains
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        
        return response
```

**When to use**: When building APIs or SPAs (Single Page Applications).

---

### 7. 🗜️ Compression Middleware

**Purpose**: Make responses smaller and faster

**Examples**:
- GZIP compression
- Minification

```python
import gzip

class CompressionMiddleware:
    def __call__(self, request):
        response = self.get_response(request)
        
        # Compress response if client supports it
        if 'gzip' in request.META.get('HTTP_ACCEPT_ENCODING', ''):
            response.content = gzip.compress(response.content)
            response['Content-Encoding'] = 'gzip'
        
        return response
```

**When to use**: For better performance, especially with large pages.

---

### 8. 🌐 Localization Middleware

**Purpose**: Show content in different languages

**Examples**:
- Language detection
- Timezone handling
- Currency conversion

```python
class LocalizationMiddleware:
    def __call__(self, request):
        # Detect user's language
        language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')
        request.LANGUAGE_CODE = language[:2]
        
        response = self.get_response(request)
        return response
```

**When to use**: For multi-language websites.

---

## 🎣 Part 2: Middleware Hooks (Advanced)

Besides the basic `__call__` method, middleware can have special hooks:

### Hook 1: `process_view`

**Runs**: Right before Django calls the view

```python
class MyMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view
        """
        print(f"About to call view: {view_func.__name__}")
        # Return None to continue
        return None
```

**Use case**: When you need to know which view is being called.

---

### Hook 2: `process_exception`

**Runs**: When a view raises an exception

```python
class ErrorHandlingMiddleware:
    def process_exception(self, request, exception):
        """
        Called when a view raises an exception
        """
        print(f"❌ Error occurred: {exception}")
        
        # You can return a custom error page
        return HttpResponse("Oops! Something went wrong", status=500)
```

**Use case**: Custom error handling and logging.

---

### Hook 3: `process_template_response`

**Runs**: For responses with a `render()` method

```python
class TemplateMiddleware:
    def process_template_response(self, request, response):
        """
        Called for template responses
        """
        # You can modify the template context
        response.context_data['extra_data'] = 'Added by middleware'
        return response
```

**Use case**: Adding data to all template contexts.

---

## 📊 Middleware Execution Order

Here's the complete flow with all hooks:

```
REQUEST
    ↓
[Middleware 1] __call__ (request phase)
    ↓
[Middleware 2] __call__ (request phase)
    ↓
[Middleware 1] process_view
    ↓
[Middleware 2] process_view
    ↓
VIEW EXECUTES
    ↓
[If exception] → process_exception (reverse order)
    ↓
[If template response] → process_template_response
    ↓
[Middleware 2] __call__ (response phase)
    ↓
[Middleware 1] __call__ (response phase)
    ↓
RESPONSE
```

---

## 🎯 Django's Built-in Middleware

Django comes with several middleware already:

1. **SecurityMiddleware** - Basic security features
2. **SessionMiddleware** - Session support
3. **CommonMiddleware** - Common utilities
4. **CsrfViewMiddleware** - CSRF protection
5. **AuthenticationMiddleware** - User authentication
6. **MessageMiddleware** - Flash messages
7. **XFrameOptionsMiddleware** - Clickjacking protection

**Found in**: `settings.py` under `MIDDLEWARE`

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

## 💡 Choosing the Right Type

**Ask yourself:**

1. **What do I need to do?**
   - Security → Security Middleware
   - Track users → Authentication Middleware
   - Debug → Logging Middleware
   - Speed up → Caching Middleware

2. **When should it run?**
   - Before view → Use request phase
   - After view → Use response phase
   - On errors → Use `process_exception`

3. **For all requests or specific ones?**
   - All → Middleware
   - Specific → Decorators or view logic

---

## ⚠️ Important Notes

**DO:**
- ✅ Use built-in middleware when available
- ✅ Keep middleware focused on one task
- ✅ Consider performance impact
- ✅ Test middleware thoroughly

**DON'T:**
- ❌ Put business logic in middleware
- ❌ Make middleware do too many things
- ❌ Forget about the order of middleware
- ❌ Make middleware slow

---

## 🎓 Quick Check

Before moving on, you should understand:

- ✅ Different types of middleware by purpose
- ✅ Security vs Authentication vs Logging middleware
- ✅ When to use each type
- ✅ Built-in middleware that Django provides
- ✅ Additional hooks like `process_view` and `process_exception`

---

## 🚀 Next Steps

Congratulations! You've completed the basics! 🎉

Now you're ready for **[Intermediate Level](../02-intermediate/)** where you'll:
- Write your own custom middleware
- Work with real-world examples
- Handle complex scenarios

**Continue to**: [Creating Custom Middleware →](../02-intermediate/01-custom-middleware.md)

---

## 💭 Think About It

**Question**: If you were building a blog website, which types of middleware would you need?

<details>
<summary><b>💡 Suggested Answer</b></summary>

You might need:
1. **Security Middleware** - Always!
2. **Authentication Middleware** - For admin/author login
3. **Session Middleware** - To track logged-in users
4. **Caching Middleware** - To make posts load faster
5. **Logging Middleware** - To track errors and usage

</details>

---

*Continue to: [Creating Custom Middleware →](../02-intermediate/01-custom-middleware.md)*
