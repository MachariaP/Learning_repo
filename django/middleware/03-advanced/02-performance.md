# Performance Optimization 🚀

Making your middleware fast and efficient. Slow middleware = slow entire application!

---

## ⚡ The Golden Rule

**Middleware runs on EVERY request!**

A slow middleware that takes 100ms means:
- 1,000 requests = 100 seconds of extra time
- 10,000 requests = 1,000 seconds (16 minutes!)
- 100,000 requests = 10,000 seconds (2.7 hours!)

**Make it fast or don't use middleware!**

---

## 🎯 Performance Principles

### 1. **Do Less Work**

❌ **Bad**: Heavy operation on every request
```python
class SlowMiddleware:
    def __call__(self, request):
        # Queries ALL users on EVERY request!
        all_users = User.objects.all()  # SLOW!
        response = self.get_response(request)
        return response
```

✅ **Good**: Only do work when needed
```python
class FastMiddleware:
    def __call__(self, request):
        # Only query if user is authenticated
        if request.user.is_authenticated:
            # And only get this specific user
            user_data = cache.get(f'user_{request.user.id}')
        
        response = self.get_response(request)
        return response
```

---

### 2. **Exit Early**

❌ **Bad**: Processes everything
```python
class SlowMiddleware:
    def __call__(self, request):
        # Does expensive work even for static files!
        data = expensive_operation()
        
        response = self.get_response(request)
        return response
```

✅ **Good**: Skip unnecessary work
```python
class FastMiddleware:
    def __call__(self, request):
        # Skip static files immediately
        if request.path.startswith('/static/'):
            return self.get_response(request)
        
        # Skip media files
        if request.path.startswith('/media/'):
            return self.get_response(request)
        
        # Only process dynamic pages
        data = expensive_operation()
        
        response = self.get_response(request)
        return response
```

---

### 3. **Use Caching**

❌ **Bad**: Recalculates every time
```python
class SlowMiddleware:
    def __call__(self, request):
        # Recalculates on every request!
        user_permissions = calculate_permissions(request.user)  # SLOW!
        
        response = self.get_response(request)
        return response
```

✅ **Good**: Cache the results
```python
from django.core.cache import cache

class FastMiddleware:
    def __call__(self, request):
        if not request.user.is_authenticated:
            response = self.get_response(request)
            return response
        
        # Try cache first
        cache_key = f'permissions_{request.user.id}'
        permissions = cache.get(cache_key)
        
        if permissions is None:
            # Only calculate if not in cache
            permissions = calculate_permissions(request.user)
            # Cache for 5 minutes
            cache.set(cache_key, permissions, 300)
        
        request.user_permissions = permissions
        response = self.get_response(request)
        return response
```

---

## 🔍 Measuring Performance

### Technique 1: Timing Decorator

```python
import time
import functools

def measure_time(func):
    """Decorator to measure function execution time"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        
        if duration > 0.01:  # Warn if over 10ms
            print(f"⚠️ {func.__name__} took {duration*1000:.2f}ms")
        
        return result
    return wrapper

class MonitoredMiddleware:
    @measure_time
    def __call__(self, request):
        response = self.get_response(request)
        return response
```

---

### Technique 2: Built-in Profiling

```python
import cProfile
import pstats
from io import StringIO

class ProfilingMiddleware:
    """Profiles middleware to find slow parts"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.profiler = cProfile.Profile()
    
    def __call__(self, request):
        # Only profile certain paths
        if request.path.startswith('/api/'):
            self.profiler.enable()
            
            response = self.get_response(request)
            
            self.profiler.disable()
            
            # Print stats
            s = StringIO()
            stats = pstats.Stats(self.profiler, stream=s)
            stats.sort_stats('cumulative')
            stats.print_stats(10)  # Top 10
            print(s.getvalue())
            
            return response
        
        return self.get_response(request)
```

---

## 💾 Database Optimization

### Problem: N+1 Queries

❌ **Bad**: Multiple queries
```python
class SlowMiddleware:
    def __call__(self, request):
        users = User.objects.all()
        for user in users:
            # Each iteration = 1 query! (N+1 problem)
            profile = user.profile  # QUERY!
        
        response = self.get_response(request)
        return response
```

✅ **Good**: One query with select_related
```python
class FastMiddleware:
    def __call__(self, request):
        # Get users with profiles in ONE query
        users = User.objects.select_related('profile').all()
        for user in users:
            profile = user.profile  # No query! Already loaded
        
        response = self.get_response(request)
        return response
```

---

### Use Query Optimization

```python
from django.db import connection

class OptimizedMiddleware:
    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Track queries
        before = len(connection.queries)
        
        # Only select needed fields
        user_data = User.objects.filter(
            id=request.user.id
        ).values(
            'id', 'username', 'email'  # Only these fields
        ).first()
        
        # Track queries
        after = len(connection.queries)
        queries_made = after - before
        
        if queries_made > 1:
            print(f"⚠️ Made {queries_made} queries!")
        
        response = self.get_response(request)
        return response
```

---

## 🎨 Lazy Loading

❌ **Bad**: Loads everything upfront
```python
class EagerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Loads all data at startup! SLOW!
        self.config_data = load_all_config()  # SLOW!
```

✅ **Good**: Load only when needed
```python
class LazyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._config_data = None
    
    @property
    def config_data(self):
        """Lazy load config data"""
        if self._config_data is None:
            self._config_data = load_all_config()
        return self._config_data
    
    def __call__(self, request):
        # Only loads config if this code path is reached
        if request.path == '/admin/':
            config = self.config_data
        
        response = self.get_response(request)
        return response
```

---

## 🚄 Async Middleware (Django 3.1+)

For I/O-bound operations, use async:

```python
import asyncio

class AsyncMiddleware:
    """Async middleware for better performance"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Check if it's async
        if asyncio.iscoroutinefunction(get_response):
            self.async_mode = True
        else:
            self.async_mode = False
    
    async def __call__(self, request):
        # Async operations
        await self.log_request_async(request)
        
        response = await self.get_response(request)
        
        await self.log_response_async(response)
        
        return response
    
    async def log_request_async(self, request):
        """Async logging (non-blocking)"""
        # Simulate async I/O
        await asyncio.sleep(0)  # Yield control
        print(f"Request: {request.path}")
    
    async def log_response_async(self, response):
        """Async logging (non-blocking)"""
        await asyncio.sleep(0)
        print(f"Response: {response.status_code}")
```

---

## 📊 Memory Optimization

### Problem: Memory Leaks

❌ **Bad**: Stores everything forever
```python
class MemoryLeakMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.all_requests = []  # GROWS FOREVER!
    
    def __call__(self, request):
        # Stores every request forever!
        self.all_requests.append({
            'path': request.path,
            'user': request.user,
            'time': datetime.now(),
        })
        
        response = self.get_response(request)
        return response
```

✅ **Good**: Limit storage
```python
from collections import deque

class MemoryEfficientMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Only keep last 1000 requests
        self.recent_requests = deque(maxlen=1000)
    
    def __call__(self, request):
        # Automatically drops old requests
        self.recent_requests.append({
            'path': request.path,
            'time': datetime.now(),
        })
        
        response = self.get_response(request)
        return response
```

---

## ⚡ Specific Optimizations

### 1. **String Operations**

❌ **Slow**:
```python
result = ""
for item in large_list:
    result += str(item)  # Creates new string each time!
```

✅ **Fast**:
```python
result = "".join(str(item) for item in large_list)
```

---

### 2. **Regular Expressions**

❌ **Slow**: Compile every time
```python
def __call__(self, request):
    import re
    if re.match(r'/api/v[0-9]+/', request.path):  # Compiles every request!
        pass
```

✅ **Fast**: Compile once
```python
import re

class FastRegexMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_pattern = re.compile(r'/api/v[0-9]+/')  # Compile once!
    
    def __call__(self, request):
        if self.api_pattern.match(request.path):
            pass
```

---

### 3. **JSON Processing**

❌ **Slow**: Parse every time
```python
def __call__(self, request):
    if request.body:
        data = json.loads(request.body)  # Parses every time
```

✅ **Fast**: Parse once, cache
```python
def __call__(self, request):
    if request.method == 'POST' and not hasattr(request, '_json_data'):
        try:
            request._json_data = json.loads(request.body)
        except:
            request._json_data = None
    
    data = getattr(request, '_json_data', None)
```

---

## 🎯 Performance Checklist

Before deploying middleware, check:

- [ ] Does it exit early for static files?
- [ ] Does it use caching where possible?
- [ ] Are database queries optimized?
- [ ] No N+1 query problems?
- [ ] No unbounded memory growth?
- [ ] Regular expressions compiled once?
- [ ] No unnecessary work in `__init__`?
- [ ] Tested with realistic load?

---

## 📈 Load Testing

### Simple Load Test

```python
# test_middleware.py

import time
from django.test import RequestFactory
from myapp.middleware import MyMiddleware

def load_test():
    """Simple load test"""
    middleware = MyMiddleware(lambda r: HttpResponse())
    factory = RequestFactory()
    
    # Warm up
    for _ in range(100):
        request = factory.get('/test/')
        middleware(request)
    
    # Measure
    start = time.time()
    iterations = 10000
    
    for _ in range(iterations):
        request = factory.get('/test/')
        middleware(request)
    
    duration = time.time() - start
    rps = iterations / duration
    
    print(f"Requests per second: {rps:.2f}")
    print(f"Average time: {(duration/iterations)*1000:.2f}ms")

if __name__ == '__main__':
    load_test()
```

---

## 💡 Best Practices Summary

1. **Profile first, optimize second** - Don't guess!
2. **Cache aggressively** - Recompute only when needed
3. **Exit early** - Skip work for static files
4. **Lazy load** - Load only when needed
5. **Limit memory** - Use `deque` with `maxlen`
6. **Optimize queries** - Use `select_related`, `prefetch_related`
7. **Compile once** - Regex, JSON schemas, etc.
8. **Monitor production** - Track actual performance

---

## 🎓 Quick Check

You should now understand:

- ✅ Why middleware performance matters
- ✅ How to measure middleware performance
- ✅ Common performance problems
- ✅ Caching strategies
- ✅ Database optimization
- ✅ Memory management
- ✅ How to profile and test

---

## 🚀 Next Steps

**Continue to**: [Advanced Patterns →](./03-advanced-patterns.md)

---

*Continue to: [Advanced Patterns →](./03-advanced-patterns.md)*
