# Django Middleware & ORM Quiz Questions 📝

Test your knowledge of Django middleware, signals, and ORM concepts!

---

## 🎯 Signals

### Question #0
**Which of the following methods connects a receiver function to a signal?**

- [ ] Signal.emit
- [x] **Signal.connect**
- [ ] Signal.notify
- [ ] Signal.link

**Explanation:** The `connect()` method is used to register a receiver function with a signal. When the signal is sent, all connected receivers are called.

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

# Method 1: Using decorator
@receiver(post_save, sender=MyModel)
def my_handler(sender, instance, **kwargs):
    pass

# Method 2: Using connect()
post_save.connect(my_handler, sender=MyModel)
```

---

### Question #1
**What is the main advantage of using Django signals?**

- [ ] To execute code asynchronously
- [x] **To decouple applications that need to be notified of events**
- [ ] To increase the speed of request processing
- [ ] To manage database transactions

**Explanation:** Signals allow certain senders to notify a set of receivers when an action has taken place. This helps decouple different parts of your application - one app doesn't need to know about another app's internals to react to events.

**Example Use Case:**
```python
# In app1/models.py
class Order(models.Model):
    # Order model doesn't know about email or notifications
    pass

# In app2/signals.py
@receiver(post_save, sender=Order)
def send_order_confirmation(sender, instance, created, **kwargs):
    if created:
        send_email(instance.customer.email, "Order confirmed!")

# In app3/signals.py
@receiver(post_save, sender=Order)
def update_inventory(sender, instance, created, **kwargs):
    if created:
        update_stock(instance.items)
```

---

### Question #2
**What should you use to ensure that a receiver function is not registered multiple times?**

- [x] **dispatch_uid**
- [ ] sender
- [ ] weak=True
- [ ] disconnect()

**Explanation:** The `dispatch_uid` parameter provides a unique identifier for the receiver, preventing duplicate registrations if the same code is imported multiple times.

```python
from django.db.models.signals import post_save

# Without dispatch_uid - might register multiple times
post_save.connect(my_handler, sender=MyModel)

# With dispatch_uid - guaranteed to register only once
post_save.connect(
    my_handler, 
    sender=MyModel,
    dispatch_uid="unique_handler_id"
)
```

**Why it matters:**
- Apps might be imported multiple times
- Prevents duplicate signal handlers
- Ensures predictable behavior

---

## 🗃️ Django ORM

### Question #3
**What will the following query do?**

```python
Entry.objects.filter(pub_date__year=2023)
```

- [ ] Retrieve entries published exactly on January 1, 2023
- [x] **Retrieve entries published in the year 2023**
- [ ] Retrieve entries with a pub_date of 2023-01-01
- [ ] Retrieve all entries published before 2023

**Explanation:** The `__year` lookup extracts the year from a date field and filters based on it. This returns all entries where the year portion of `pub_date` is 2023.

**More Examples:**
```python
# All entries in 2023
Entry.objects.filter(pub_date__year=2023)

# Entries in January 2023
Entry.objects.filter(pub_date__year=2023, pub_date__month=1)

# Entries on specific date
Entry.objects.filter(pub_date__date='2023-01-01')

# Entries before 2023
Entry.objects.filter(pub_date__year__lt=2023)
```

---

### Question #4
**Which Django ORM method is used to retrieve a single object from the database that matches a query?**

- [ ] filter()
- [x] **get()**
- [ ] all()
- [ ] exclude()

**Explanation:** The `get()` method returns a single object that matches the given query. It raises `DoesNotExist` if no object is found or `MultipleObjectsReturned` if more than one object matches.

**Examples:**
```python
# get() - Returns single object or raises exception
user = User.objects.get(id=1)  # Returns one User
user = User.objects.get(email='john@example.com')

# filter() - Always returns QuerySet (even if 1 or 0 results)
users = User.objects.filter(id=1)  # Returns QuerySet

# all() - Returns all objects
all_users = User.objects.all()

# exclude() - Returns all objects EXCEPT those matching
non_staff = User.objects.exclude(is_staff=True)
```

**Best Practices:**
```python
# Use get() when you expect exactly one result
try:
    user = User.objects.get(pk=user_id)
except User.DoesNotExist:
    # Handle missing user
    pass

# Use filter().first() when 0 or 1 results are acceptable
user = User.objects.filter(email=email).first()  # Returns None if not found
```

---

## 🔧 Middleware

### Question #5
**What is the primary purpose of middleware in Django?**

- [ ] To handle database queries
- [x] **To globally alter Django's request or response processing**
- [ ] To manage user authentication
- [ ] To manage URL routing

**Explanation:** Middleware is a framework of hooks into Django's request/response processing. It's a light, low-level plugin system for globally altering Django's input or output.

**What Middleware Does:**
```python
class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Code to execute for each request BEFORE view
        # Affects ALL requests globally
        
        response = self.get_response(request)
        
        # Code to execute for each request AFTER view
        # Affects ALL responses globally
        
        return response
```

**Common Uses:**
- ✅ Authentication (affects all requests)
- ✅ Logging (affects all requests)
- ✅ Security headers (affects all responses)
- ✅ CORS (affects all responses)
- ❌ Database queries (handled by models)
- ❌ URL routing (handled by URLconf)

---

### Question #6
**What happens if a middleware's __init__() method raises MiddlewareNotUsed?**

- [ ] Django will raise an error
- [x] **The middleware will be removed from the middleware chain**
- [ ] The middleware will be called again with different arguments
- [ ] Django will restart the server

**Explanation:** Raising `MiddlewareNotUsed` in `__init__()` tells Django to skip this middleware. This is useful for conditionally enabling middleware based on settings or environment.

```python
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings

class ConditionalMiddleware:
    def __init__(self, get_response):
        # Only enable in production
        if not settings.DEBUG:
            self.get_response = get_response
        else:
            # Middleware will be skipped
            raise MiddlewareNotUsed("Middleware disabled in debug mode")
    
    def __call__(self, request):
        # This won't run if DEBUG=True
        return self.get_response(request)
```

**Use Cases:**
- Disable middleware based on settings
- Skip middleware in development
- Conditional feature flags
- Environment-specific middleware

---

### Question #7
**Which method in middleware is responsible for processing each request and returning a response?**

- [ ] init
- [ ] get_response
- [x] **__call__**
- [ ] process_view

**Explanation:** The `__call__` method is invoked for every request. It receives the request, optionally processes it, calls `get_response(request)` to continue the chain, and returns a response.

```python
class MyMiddleware:
    def __init__(self, get_response):
        # Called once when Django starts
        self.get_response = get_response
    
    def __call__(self, request):
        # Called for EVERY request
        
        # Process request
        print(f"Request: {request.path}")
        
        # Get response from next middleware or view
        response = self.get_response(request)
        
        # Process response
        print(f"Response: {response.status_code}")
        
        return response
```

**Method Comparison:**
- `__init__`: One-time setup when server starts
- `__call__`: Runs for every request/response
- `get_response`: Callable to continue middleware chain (not a method you define)
- `process_view`: Legacy method (old-style middleware)

---

## 🔍 Advanced ORM

### Question #8
**What is the purpose of using Q objects in Django queries?**

- [ ] To perform database transactions
- [x] **To create complex queries with logical operators**
- [ ] To enforce foreign key constraints
- [ ] To automatically generate primary keys

**Explanation:** Q objects allow you to create complex queries using logical operators like OR (`|`), AND (`&`), and NOT (`~`). They're essential for building dynamic queries with multiple conditions.

**Basic Example:**
```python
from django.db.models import Q

# Without Q objects - can only do AND
User.objects.filter(is_active=True, is_staff=True)  # AND only

# With Q objects - can do OR
User.objects.filter(
    Q(is_staff=True) | Q(is_superuser=True)  # OR
)

# Complex example
User.objects.filter(
    (Q(is_active=True) & Q(last_login__gte=last_week))  # AND
    | Q(is_superuser=True)  # OR
)
```

**Advanced Use Cases:**
```python
# NOT operator
User.objects.filter(~Q(is_staff=True))  # NOT staff

# Dynamic query building
filters = Q()
if name:
    filters &= Q(name__icontains=name)
if email:
    filters &= Q(email__icontains=email)
users = User.objects.filter(filters)

# Search across multiple fields
search = "john"
User.objects.filter(
    Q(first_name__icontains=search) |
    Q(last_name__icontains=search) |
    Q(email__icontains=search)
)
```

---

### Question #9
**Which method would you use to create and save a model instance in a single step?**

- [ ] save()
- [x] **create()**
- [ ] update()
- [ ] add()

**Explanation:** The `create()` method creates a new instance and saves it to the database in one step, returning the created object.

**Method Comparison:**
```python
# Method 1: Create then save (2 steps)
user = User(username='john', email='john@example.com')
user.save()

# Method 2: create() - single step ✅
user = User.objects.create(
    username='john',
    email='john@example.com'
)

# update() - updates existing records
User.objects.filter(id=1).update(is_active=True)

# save() - instance method, not a manager method
user.username = 'jane'
user.save()

# add() - used for many-to-many relationships
user.groups.add(admin_group)
```

**Best Practices:**
```python
# Use create() for simple cases
user = User.objects.create(username='john')

# Use save() when you need more control
user = User(username='john')
user.set_password('password123')  # Additional processing
user.save()

# Use get_or_create() to avoid duplicates
user, created = User.objects.get_or_create(
    email='john@example.com',
    defaults={'username': 'john'}
)
if created:
    print("Created new user")
else:
    print("User already existed")
```

---

## 📊 Quiz Summary

### Topics Covered:
1. ✅ Django Signals (Questions 0-2)
2. ✅ Django ORM Basics (Questions 3-4)
3. ✅ Django Middleware (Questions 5-7)
4. ✅ Advanced ORM (Questions 8-9)

### Key Takeaways:

**Signals:**
- Use `Signal.connect()` or `@receiver` decorator
- Signals help decouple applications
- Always use `dispatch_uid` to prevent duplicate registrations

**ORM:**
- `get()` returns single object, `filter()` returns QuerySet
- Use `__year`, `__month`, etc. for date field lookups
- `create()` creates and saves in one step
- Q objects enable complex queries with OR/AND/NOT

**Middleware:**
- Primary purpose: globally alter request/response processing
- `__call__` method processes each request
- `MiddlewareNotUsed` removes middleware from chain
- Order matters in MIDDLEWARE settings

---

## 🎯 Study Resources

For more information, review:
- [Middleware Basics](./01-basics/01-what-is-middleware.md)
- [Custom Middleware](./02-intermediate/01-custom-middleware.md)
- [Advanced Patterns](./03-advanced/03-advanced-patterns.md)
- [Project Guide](./PROJECT-GUIDE.md)

---

**Good luck with your learning! 🚀**
