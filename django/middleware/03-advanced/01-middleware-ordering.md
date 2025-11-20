# Middleware Ordering ⚡

Understanding middleware order is CRITICAL! The sequence determines how requests flow through your application.

---

## 🎯 Why Order Matters

Middleware is like layers of an onion:
- Requests go through from **top to bottom**
- Responses go through from **bottom to top**

**Wrong order** = broken functionality or security holes!

---

## 📊 The Execution Flow

```python
MIDDLEWARE = [
    'A',  # First
    'B',  # Second
    'C',  # Third
]
```

**Request Flow (Going IN):**
```
User Request
    ↓
A (process request)
    ↓
B (process request)
    ↓
C (process request)
    ↓
YOUR VIEW
```

**Response Flow (Going OUT):**
```
YOUR VIEW
    ↓
C (process response)
    ↓
B (process response)
    ↓
A (process response)
    ↓
User Response
```

---

## 🔐 Security Must Come First!

### ❌ Wrong Order

```python
MIDDLEWARE = [
    'MyCustomMiddleware',          # Business logic
    'SecurityMiddleware',          # Security (TOO LATE!)
]
```

**Problem**: Requests can reach your custom middleware before security checks!

### ✅ Correct Order

```python
MIDDLEWARE = [
    'SecurityMiddleware',          # Security FIRST
    'MyCustomMiddleware',          # Then business logic
]
```

---

## 📋 Django's Recommended Order

Here's the standard order with explanations:

```python
MIDDLEWARE = [
    # 1. SECURITY - Must be first!
    'django.middleware.security.SecurityMiddleware',
    
    # 2. SESSIONS - Needed for authentication
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # 3. COMMON - URL handling, etc.
    'django.middleware.common.CommonMiddleware',
    
    # 4. CSRF - Needs sessions
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # 5. AUTHENTICATION - Needs sessions & CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # 6. MESSAGES - Needs sessions & auth
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # 7. CLICKJACKING - Can be last
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Why this order?**

1. **Security**: Protects everything below it
2. **Sessions**: Required for auth and messages
3. **Common**: Basic HTTP features
4. **CSRF**: Needs session data
5. **Authentication**: Needs session + CSRF
6. **Messages**: Needs session + auth
7. **Clickjacking**: Just adds headers, can be anywhere

---

## 🎨 Real-World Scenarios

### Scenario 1: Adding Logging

**Where to put it?**

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'LoggingMiddleware',  # ← HERE! After security, sees all requests
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... rest
]
```

**Why here?**
- After security (logged requests are safe)
- Before everything else (logs all processing)

---

### Scenario 2: Rate Limiting

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'RateLimitMiddleware',  # ← HERE! Early, before expensive operations
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... rest
]
```

**Why here?**
- After security only
- Before sessions, auth, database (saves resources)

---

### Scenario 3: Custom Authentication

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'CustomAuthMiddleware',  # ← HERE! After Django's auth
    # ... rest
]
```

**Why here?**
- After Django's authentication
- Can modify `request.user`

---

### Scenario 4: Response Modification

```python
MIDDLEWARE = [
    # ... all the standard middleware
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ResponseModifierMiddleware',  # ← HERE! Near the end
]
```

**Why here?**
- Processes responses on the way back
- After all business logic

---

## ⚠️ Common Ordering Mistakes

### Mistake 1: CSRF Before Sessions

```python
# ❌ WRONG!
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',     # Needs sessions!
    'django.contrib.sessions.middleware.SessionMiddleware',
]
```

**Result**: CSRF tokens won't work!

```python
# ✅ CORRECT!
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]
```

---

### Mistake 2: Auth Before Sessions

```python
# ❌ WRONG!
MIDDLEWARE = [
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Needs sessions!
    'django.contrib.sessions.middleware.SessionMiddleware',
]
```

**Result**: Users can't log in!

```python
# ✅ CORRECT!
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]
```

---

### Mistake 3: Rate Limiting Too Late

```python
# ❌ INEFFICIENT!
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'DatabaseMiddleware',              # Heavy operation
    'RateLimitMiddleware',            # Too late! Already did expensive work
]
```

```python
# ✅ EFFICIENT!
MIDDLEWARE = [
    'RateLimitMiddleware',            # Block early!
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'DatabaseMiddleware',
]
```

---

## 🧪 Testing Middleware Order

### Simple Test

```python
# middleware/order_test.py

class OrderTestMiddleware:
    """Shows the order of execution"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.name = self.__class__.__name__
    
    def __call__(self, request):
        print(f"→ {self.name}: Processing REQUEST")
        
        response = self.get_response(request)
        
        print(f"← {self.name}: Processing RESPONSE")
        
        return response
```

**Create three test middleware:**

```python
class MiddlewareA(OrderTestMiddleware):
    pass

class MiddlewareB(OrderTestMiddleware):
    pass

class MiddlewareC(OrderTestMiddleware):
    pass
```

**Settings:**
```python
MIDDLEWARE = [
    'middleware.order_test.MiddlewareA',
    'middleware.order_test.MiddlewareB',
    'middleware.order_test.MiddlewareC',
]
```

**Output:**
```
→ MiddlewareA: Processing REQUEST
→ MiddlewareB: Processing REQUEST
→ MiddlewareC: Processing REQUEST
[View executes here]
← MiddlewareC: Processing RESPONSE
← MiddlewareB: Processing RESPONSE
← MiddlewareA: Processing RESPONSE
```

---

## 🎯 Decision Tree: Where to Place Your Middleware?

### Does it need authentication?
- **YES** → After `AuthenticationMiddleware`
- **NO** → Continue...

### Does it need sessions?
- **YES** → After `SessionMiddleware`
- **NO** → Continue...

### Is it security-related?
- **YES** → As early as possible (after SecurityMiddleware)
- **NO** → Continue...

### Is it expensive (database, API calls)?
- **YES** → After rate limiting and auth checks
- **NO** → Continue...

### Does it modify responses?
- **YES** → Near the end
- **NO** → Middle is usually fine

---

## 📚 Advanced Patterns

### Pattern 1: Conditional Ordering

Sometimes you want middleware to run at different times:

```python
class SmartMiddleware:
    """Runs at different times based on conditions"""
    
    def __call__(self, request):
        # Early exit for certain paths
        if request.path.startswith('/static/'):
            return self.get_response(request)
        
        # Do expensive work only for authenticated users
        if request.user.is_authenticated:
            # Heavy processing
            pass
        
        response = self.get_response(request)
        return response
```

---

### Pattern 2: Dependency Chain

```python
# This middleware needs data from another
class DataCollectorMiddleware:
    def __call__(self, request):
        request.collected_data = {'timestamp': time.time()}
        response = self.get_response(request)
        return response

class DataProcessorMiddleware:
    def __call__(self, request):
        # Uses data from DataCollectorMiddleware
        data = getattr(request, 'collected_data', {})
        # Process it...
        response = self.get_response(request)
        return response
```

**Settings (order matters!):**
```python
MIDDLEWARE = [
    'DataCollectorMiddleware',    # Must be BEFORE
    'DataProcessorMiddleware',    # Depends on data
]
```

---

## 💡 Best Practices

### 1. **Document Dependencies**

```python
class MyMiddleware:
    """
    My custom middleware.
    
    DEPENDENCIES:
    - Must be after: SessionMiddleware, AuthenticationMiddleware
    - Must be before: None
    - Adds: request.custom_data
    """
```

### 2. **Group by Purpose**

```python
MIDDLEWARE = [
    # === Security ===
    'django.middleware.security.SecurityMiddleware',
    'CustomSecurityMiddleware',
    
    # === Sessions & Auth ===
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # === Business Logic ===
    'MyBusinessMiddleware',
    
    # === Logging & Monitoring ===
    'LoggingMiddleware',
    'PerformanceMiddleware',
]
```

### 3. **Comment Complex Ordering**

```python
MIDDLEWARE = [
    'SecurityMiddleware',
    # Rate limit MUST be before session to save resources
    'RateLimitMiddleware',
    'SessionMiddleware',
    # Custom auth MUST be after Django auth
    'AuthenticationMiddleware',
    'CustomAuthMiddleware',
]
```

---

## 🎓 Quick Check

Before moving on, understand:

- ✅ Middleware executes top-to-bottom for requests
- ✅ Middleware executes bottom-to-top for responses
- ✅ Security must come first
- ✅ Dependencies determine order (sessions before auth)
- ✅ Rate limiting should be early
- ✅ Response modification should be late

---

## 🚀 Next Steps

**Continue to**: [Performance Optimization →](./02-performance.md)

---

## 💭 Practice Exercise

**Challenge**: Order these middleware correctly:

```python
- CustomHeadersMiddleware
- RateLimitMiddleware  
- LoggingMiddleware
- SessionMiddleware
- AuthenticationMiddleware
- SecurityMiddleware
- CsrfViewMiddleware
```

<details>
<summary><b>💡 Solution</b></summary>

```python
MIDDLEWARE = [
    'SecurityMiddleware',          # 1. Security first!
    'RateLimitMiddleware',         # 2. Block abusers early
    'LoggingMiddleware',           # 3. Log all requests
    'SessionMiddleware',           # 4. Sessions needed for auth
    'CsrfViewMiddleware',          # 5. Needs sessions
    'AuthenticationMiddleware',    # 6. Needs sessions + CSRF
    'CustomHeadersMiddleware',     # 7. Can be last (just adds headers)
]
```

</details>

---

*Continue to: [Performance Optimization →](./02-performance.md)*
