# How Middleware Works 🔧

Now that you know **what** middleware is, let's understand **how** it actually works!

---

## 🎯 The Request-Response Cycle

Every time a user visits your website, this happens:

```
1. User types URL or clicks a link
2. Browser sends REQUEST to your server
3. Django receives the request
4. REQUEST passes through MIDDLEWARE (top to bottom)
5. Request reaches your VIEW (your code)
6. Your view creates a RESPONSE
7. RESPONSE passes through MIDDLEWARE (bottom to top)
8. Browser receives the response and displays the page
```

---

## 🏗️ Middleware Structure (The Basics)

A middleware in Django is a Python class with these parts:

```python
class MyMiddleware:
    def __init__(self, get_response):
        """
        One-time setup when Django starts
        Think of this as 'preparing your tools'
        """
        self.get_response = get_response
        # You can do setup here
    
    def __call__(self, request):
        """
        This runs for EVERY request
        """
        # CODE HERE runs BEFORE the view
        # --------------------------------
        
        response = self.get_response(request)  # Calls the view
        
        # CODE HERE runs AFTER the view
        # --------------------------------
        
        return response
```

---

## 📖 Step-by-Step Breakdown

Let's break down what happens in a middleware:

### Step 1: Initialization (`__init__`)

```python
def __init__(self, get_response):
    self.get_response = get_response
    print("Middleware is being set up!")
    # This only runs ONCE when Django starts
```

**When**: When your Django application starts up
**Purpose**: Set up anything your middleware needs

---

### Step 2: Request Processing (`__call__` - before)

```python
def __call__(self, request):
    # This code runs BEFORE your view
    print(f"Incoming request to: {request.path}")
    
    # You can:
    # - Check the request
    # - Modify the request
    # - Add data to the request
    # - Even reject the request and return early!
```

**When**: Before your view/controller code runs
**Purpose**: Inspect or modify incoming requests

---

### Step 3: View Execution

```python
    response = self.get_response(request)
    # This line calls your view and gets the response
```

**When**: After request processing, before response processing
**Purpose**: This is where your actual application logic runs

---

### Step 4: Response Processing (`__call__` - after)

```python
    # This code runs AFTER your view
    print(f"Outgoing response: {response.status_code}")
    
    # You can:
    # - Check the response
    # - Modify the response
    # - Add headers
    # - Log information
    
    return response
```

**When**: After your view creates a response
**Purpose**: Inspect or modify outgoing responses

---

## 🎨 Visual Example with Real Code

Let's create a simple logging middleware:

```python
class SimpleLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("🚀 Logging Middleware started!")
    
    def __call__(self, request):
        # BEFORE the view runs
        print(f"📥 Request: {request.method} {request.path}")
        
        # Call the view
        response = self.get_response(request)
        
        # AFTER the view runs
        print(f"📤 Response: {response.status_code}")
        
        return response
```

**What happens when a user visits `/home/`:**

```
📥 Request: GET /home/
[Your view runs here]
📤 Response: 200
```

---

## 🔄 Multiple Middleware Flow

When you have multiple middleware, they form layers like an onion:

```python
MIDDLEWARE = [
    'middleware.Security',      # Layer 1
    'middleware.Session',       # Layer 2
    'middleware.Auth',          # Layer 3
]
```

**Request Flow (Going IN):**
```
User Request
    ↓
Security Middleware    ← Process request
    ↓
Session Middleware     ← Process request
    ↓
Auth Middleware        ← Process request
    ↓
YOUR VIEW
```

**Response Flow (Going OUT):**
```
YOUR VIEW
    ↓
Auth Middleware        ← Process response
    ↓
Session Middleware     ← Process response
    ↓
Security Middleware    ← Process response
    ↓
User Response
```

---

## 💡 Important Patterns

### Pattern 1: Short-Circuit (Stop Early)

```python
def __call__(self, request):
    # Check if user is banned
    if request.user.is_banned:
        # Stop here! Don't call other middleware or views
        return HttpResponse("You are banned", status=403)
    
    # Continue normally
    response = self.get_response(request)
    return response
```

**When to use**: When you need to reject requests immediately

---

### Pattern 2: Modify Request

```python
def __call__(self, request):
    # Add something to the request
    request.start_time = time.time()
    
    response = self.get_response(request)
    return response
```

**When to use**: When you need to add data for views to use

---

### Pattern 3: Modify Response

```python
def __call__(self, request):
    response = self.get_response(request)
    
    # Add a custom header
    response['X-Custom-Header'] = 'My Value'
    
    return response
```

**When to use**: When you need to modify all responses

---

### Pattern 4: Measure Performance

```python
import time

def __call__(self, request):
    start_time = time.time()
    
    response = self.get_response(request)
    
    duration = time.time() - start_time
    print(f"⏱️ Request took {duration:.2f} seconds")
    
    return response
```

**When to use**: For logging and monitoring

---

## 🎯 Practical Example: Request Timing Middleware

Let's create a complete, working middleware:

```python
import time

class RequestTimingMiddleware:
    """Measures how long each request takes"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Record start time
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Add timing header to response
        response['X-Request-Duration'] = f"{duration:.4f}s"
        
        # Log to console
        print(f"⏱️ {request.path} took {duration:.4f} seconds")
        
        return response
```

**What this does:**
1. Records when request started
2. Lets the view process the request
3. Calculates how long it took
4. Adds timing info to response headers
5. Logs the timing

---

## ⚠️ Things to Remember

1. **`__init__` runs once**, `__call__` runs for every request
2. **Always return a response** from `__call__`
3. **Order matters** - middleware is like layers of an onion
4. **Keep it fast** - slow middleware slows down ALL requests
5. **Don't forget** to call `self.get_response(request)`

---

## 🎓 Quick Check

Make sure you understand:

- ✅ `__init__` is for one-time setup
- ✅ `__call__` runs for every request
- ✅ Code before `get_response` processes the request
- ✅ Code after `get_response` processes the response
- ✅ You can stop requests early by returning immediately
- ✅ Middleware is executed in order (top to bottom, then bottom to top)

---

## 🚀 Next Steps

Ready to learn about different types of middleware? 

Continue to: **[Types of Middleware →](./03-types-of-middleware.md)**

---

## 💭 Practice Challenge

**Try to answer:**
1. What happens if you forget to return `response`?
2. What happens if you don't call `self.get_response(request)`?
3. Where would you add code to log request times?

**Answers at the bottom**

---

<details>
<summary><b>📝 Answers to Practice Challenge</b></summary>

1. **Forgetting to return response**: Django will crash with an error because views must return a response object.

2. **Not calling get_response**: Your view will never run! The request stops at your middleware.

3. **Logging request times**: Record time before `get_response`, calculate duration after, log the difference.

</details>

---

*Continue to: [Types of Middleware →](./03-types-of-middleware.md)*
