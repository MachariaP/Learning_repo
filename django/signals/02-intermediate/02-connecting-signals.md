# Connecting Signals 🔌

## Two Ways to Connect Signals

Django provides two methods to connect signal receivers:

1. **@receiver decorator** (Recommended)
2. **Signal.connect() method** (Programmatic)

---

## Method 1: Using @receiver Decorator

This is the most common and recommended approach.

### Basic Syntax

```python
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User

@receiver(post_save, sender=User)
def my_handler(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.username}")
```

### Connecting to Multiple Signals

You can connect one receiver to multiple signals:

```python
from django.db.models.signals import post_save, post_delete

# Connect to both post_save AND post_delete
@receiver([post_save, post_delete], sender=User)
def user_changed(sender, instance, **kwargs):
    # Handle both save and delete
    clear_user_cache(instance.pk)
```

### Connecting to Multiple Senders

```python
# Method 1: Use multiple decorators
@receiver(post_save, sender=Article)
@receiver(post_save, sender=Comment)
@receiver(post_save, sender=User)
def log_save(sender, instance, **kwargs):
    print(f"Saved: {sender.__name__} - {instance.pk}")

# Method 2: Don't specify sender (catches ALL models!)
@receiver(post_save)
def log_all_saves(sender, instance, **kwargs):
    print(f"Any model saved: {sender.__name__}")
```

---

## Method 2: Using Signal.connect()

This method gives you more control, especially for dynamic connections.

### Basic Syntax

```python
from django.db.models.signals import post_save

def my_handler(sender, instance, created, **kwargs):
    if created:
        print(f"New user: {instance.username}")

# Connect the signal
post_save.connect(my_handler, sender=User)
```

### Parameters for connect()

```python
signal.connect(
    receiver,          # The function to call
    sender=None,       # The sender to listen to (optional)
    weak=True,         # Use weak reference (default True)
    dispatch_uid=None  # Unique identifier to prevent duplicates
)
```

### Using dispatch_uid to Prevent Duplicate Connections

```python
# Without dispatch_uid, this could register twice
post_save.connect(my_handler, sender=User)
post_save.connect(my_handler, sender=User)  # Duplicate!

# With dispatch_uid, only connects once
post_save.connect(my_handler, sender=User, dispatch_uid='create_user_profile')
post_save.connect(my_handler, sender=User, dispatch_uid='create_user_profile')  # Ignored
```

### Dynamic Signal Connection

```python
# Connect signals programmatically based on settings
from django.conf import settings

def setup_signals():
    if settings.ENABLE_AUDIT_LOG:
        for model in [User, Article, Comment]:
            post_save.connect(audit_log_handler, sender=model)
            post_delete.connect(audit_log_handler, sender=model)
```

---

## Disconnecting Signals 🔓

Sometimes you need to temporarily or permanently disconnect a signal.

### Using Signal.disconnect()

```python
from django.db.models.signals import post_save

# Disconnect the signal
post_save.disconnect(my_handler, sender=User)

# If you used dispatch_uid, use it to disconnect
post_save.disconnect(dispatch_uid='create_user_profile')
```

### Temporarily Disabling Signals

```python
from contextlib import contextmanager
from django.db.models.signals import post_save

@contextmanager
def disable_signal(signal, receiver, sender):
    """Context manager to temporarily disable a signal"""
    signal.disconnect(receiver, sender=sender)
    try:
        yield
    finally:
        signal.connect(receiver, sender=sender)

# Usage
with disable_signal(post_save, create_profile, User):
    # Signal won't fire for operations in this block
    user = User.objects.create(username='test')
```

### More Robust Signal Disabling

```python
class DisableSignals:
    """Context manager to disable signals temporarily"""
    
    def __init__(self, signal, receiver, sender):
        self.signal = signal
        self.receiver = receiver
        self.sender = sender
        
    def __enter__(self):
        self.signal.disconnect(self.receiver, sender=self.sender)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.signal.connect(self.receiver, sender=self.sender)

# Usage
with DisableSignals(post_save, create_profile, User):
    User.objects.create(username='test')  # No profile created
```

---

## Where to Connect Signals 📍

### Option 1: In apps.py (Recommended)

```python
# myapp/apps.py
from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        # Import signals module to register receivers
        from . import signals
        
        # Or import specific signals
        from .signals import user_signals
```

### Option 2: In models.py (Not Recommended)

```python
# myapp/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(models.Model):
    username = models.CharField(max_length=100)

# Receiver defined in same file
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    pass

# This works but mixes concerns
```

### Option 3: In signals.py (Best Practice)

```python
# myapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

Then import in apps.py:

```python
# myapp/apps.py
class MyappConfig(AppConfig):
    def ready(self):
        import myapp.signals  # This registers the signals
```

---

## Advanced Connection Patterns

### Pattern 1: Conditional Signal Connection

```python
# Connect signals based on environment
from django.conf import settings

def connect_signals():
    if settings.DEBUG:
        post_save.connect(debug_log_handler, sender=User)
    
    if settings.ENABLE_NOTIFICATIONS:
        post_save.connect(send_notification, sender=Order)

# Call in apps.py ready()
```

### Pattern 2: Factory Function for Similar Receivers

```python
def make_audit_receiver(model_name):
    """Factory to create audit receivers for different models"""
    def receiver(sender, instance, created, **kwargs):
        action = 'created' if created else 'updated'
        AuditLog.objects.create(
            model=model_name,
            object_id=instance.pk,
            action=action
        )
    return receiver

# Create and connect receivers
for model in [User, Article, Comment]:
    handler = make_audit_receiver(model.__name__)
    post_save.connect(handler, sender=model, dispatch_uid=f'audit_{model.__name__}')
```

### Pattern 3: Class-Based Signal Handlers

```python
class UserSignalHandler:
    """Class-based signal handler for User model"""
    
    @staticmethod
    @receiver(post_save, sender=User)
    def on_user_saved(sender, instance, created, **kwargs):
        if created:
            UserSignalHandler.create_profile(instance)
            UserSignalHandler.send_welcome_email(instance)
    
    @staticmethod
    def create_profile(user):
        Profile.objects.create(user=user)
    
    @staticmethod
    def send_welcome_email(user):
        send_mail(
            'Welcome!',
            'Thanks for joining!',
            'noreply@example.com',
            [user.email]
        )
```

---

## Checking Signal Connections

### List All Receivers for a Signal

```python
from django.db.models.signals import post_save

# Get all receivers for post_save
receivers = post_save.receivers
print(f"Number of receivers: {len(receivers)}")

for receiver_info in receivers:
    receiver_key, receiver_ref = receiver_info
    print(f"Key: {receiver_key}")
    
    # Get actual function if using weak reference
    receiver_func = receiver_ref()
    if receiver_func:
        print(f"Function: {receiver_func.__name__}")
```

### Check if a Specific Receiver is Connected

```python
def is_receiver_connected(signal, receiver, sender):
    """Check if a receiver is connected to a signal"""
    for receiver_info in signal.receivers:
        receiver_key, receiver_ref = receiver_info
        
        # Check if receiver key matches sender
        if receiver_key[0] == id(sender) or receiver_key[0] is None:
            func = receiver_ref()
            if func == receiver:
                return True
    return False

# Usage
if is_receiver_connected(post_save, create_profile, User):
    print("Receiver is connected")
```

---

## 💡 Best Practices Summary

| Do | Don't |
|---|---|
| Use @receiver decorator | Connect signals in models.py |
| Put signals in signals.py | Forget to import signals |
| Import signals in apps.py ready() | Connect same signal multiple times |
| Use dispatch_uid for connect() | Use weak references carelessly |
| Keep receivers focused | Put complex logic in receivers |

---

## ⚠️ Common Pitfalls

### Pitfall 1: Signals Not Firing

```python
# ❌ Signal file created but never imported
# myapp/signals.py exists but not imported anywhere

# ✅ Import in apps.py
class MyappConfig(AppConfig):
    def ready(self):
        import myapp.signals
```

### Pitfall 2: Duplicate Connections

```python
# ❌ Signal connected twice (maybe due to code reloading)
post_save.connect(my_handler, sender=User)

# ✅ Use dispatch_uid
post_save.connect(my_handler, sender=User, dispatch_uid='unique_id')
```

### Pitfall 3: Receiver Not Garbage Collected

```python
# By default, connect() uses weak references
# If receiver is a local function, it may be garbage collected

def setup():
    def local_handler(sender, **kwargs):
        pass
    post_save.connect(local_handler, sender=User)
    # local_handler may be garbage collected!

# ✅ Use weak=False for local functions
post_save.connect(local_handler, sender=User, weak=False)

# Or better: Define handler at module level
```

---

## 🎓 Quick Check

Make sure you understand:

- ✅ How to use the @receiver decorator
- ✅ How to use signal.connect() method
- ✅ When to use dispatch_uid
- ✅ How to disconnect signals
- ✅ Where to put signal connection code

---

## 🚀 Next Steps

Now let's see **[Practical Use Cases](./03-practical-use-cases.md)** for signals in real projects!

---

*Continue to: [Practical Use Cases →](./03-practical-use-cases.md)*
