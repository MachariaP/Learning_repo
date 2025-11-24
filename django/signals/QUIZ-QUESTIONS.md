# Django Signals Quiz 📝

Test your understanding of Django Signals with these questions!

---

## 🔰 Level 1: Basics

### Question 1
What is a Django Signal?

<details>
<summary>Show Answer</summary>

A Django Signal is a notification mechanism that allows certain senders to notify a set of receivers when some action has taken place. It's Django's implementation of the Observer design pattern, commonly used to decouple applications that need to react to events.

</details>

---

### Question 2
What is the difference between `pre_save` and `post_save` signals?

<details>
<summary>Show Answer</summary>

- **`pre_save`**: Fires BEFORE the model is saved to the database. The object has not been written to the database yet.
- **`post_save`**: Fires AFTER the model is saved to the database. The object already exists in the database.

Key difference: `post_save` has a `created` argument that tells you if this is a new object or an update.

</details>

---

### Question 3
Why should you always include `**kwargs` in your signal receiver functions?

<details>
<summary>Show Answer</summary>

You should always include `**kwargs` for forward compatibility. Django may add new arguments to signals in future versions. Without `**kwargs`, your handler would break with a `TypeError` when receiving unexpected arguments.

```python
# ❌ Bad - will break if Django adds new arguments
def my_handler(sender, instance, created):
    pass

# ✅ Good - handles any future arguments
def my_handler(sender, instance, created, **kwargs):
    pass
```

</details>

---

### Question 4
Where is the recommended place to put signal code in a Django app?

<details>
<summary>Show Answer</summary>

The recommended structure is:

1. Create a `signals.py` file (or `signals/` directory) in your app
2. Import the signals in your app's `apps.py` file inside the `ready()` method

```python
# myapp/apps.py
class MyappConfig(AppConfig):
    name = 'myapp'
    
    def ready(self):
        import myapp.signals  # Registers the signals
```

</details>

---

### Question 5
Name three common use cases for Django signals.

<details>
<summary>Show Answer</summary>

Common use cases include:

1. **Auto-creating related objects** (e.g., user profile when user is created)
2. **Sending notifications** (emails, webhooks) when objects are saved
3. **Auto-generating fields** (slugs, timestamps) before saving
4. **Audit logging** - tracking all changes to models
5. **Updating denormalized data** (counters, cached values)
6. **Cache invalidation** when data changes
7. **File cleanup** when objects are deleted

</details>

---

## 📊 Level 2: Intermediate

### Question 6
What's wrong with this code?

```python
@receiver(post_save, sender=User)
def update_profile(sender, instance, **kwargs):
    instance.profile.last_activity = timezone.now()
    instance.profile.save()
```

<details>
<summary>Show Answer</summary>

This creates an **infinite loop** if the Profile model also has a signal that saves the User. More generally, calling `save()` inside a `post_save` handler is dangerous.

**Better approach:**
```python
@receiver(post_save, sender=User)
def update_profile(sender, instance, **kwargs):
    Profile.objects.filter(user=instance).update(
        last_activity=timezone.now()
    )
```

</details>

---

### Question 7
Which of these operations will trigger `post_save` signals?

```python
# A
User.objects.create(username='john')

# B
User.objects.filter(username='john').update(email='john@example.com')

# C
User.objects.bulk_create([User(username='user1'), User(username='user2')])

# D
user = User(username='jane')
user.save()
```

<details>
<summary>Show Answer</summary>

Only **A** and **D** will trigger `post_save` signals.

- **A**: `create()` calls `save()` internally ✅
- **B**: `update()` uses SQL UPDATE directly, no signals ❌
- **C**: `bulk_create()` inserts directly, no signals ❌
- **D**: Calling `save()` triggers signals ✅

This is a common gotcha! Bulk operations bypass signals for performance.

</details>

---

### Question 8
How do you connect a signal receiver to multiple senders?

<details>
<summary>Show Answer</summary>

You have several options:

**Option 1: Multiple decorators**
```python
@receiver(post_save, sender=Article)
@receiver(post_save, sender=Comment)
@receiver(post_save, sender=User)
def log_save(sender, instance, **kwargs):
    print(f"Saved: {sender.__name__}")
```

**Option 2: No sender (catches ALL models)**
```python
@receiver(post_save)
def log_all_saves(sender, instance, **kwargs):
    print(f"Any model saved: {sender.__name__}")
```

**Option 3: Programmatic connection**
```python
for model in [Article, Comment, User]:
    post_save.connect(log_save, sender=model)
```

</details>

---

### Question 9
What is `dispatch_uid` and when should you use it?

<details>
<summary>Show Answer</summary>

`dispatch_uid` is a unique identifier for a signal receiver that prevents duplicate connections.

**Use it when:**
- Connecting signals with `signal.connect()` (not the decorator)
- Your app might be imported multiple times (e.g., during testing)
- You want to ensure a handler is only registered once

```python
# Without dispatch_uid - might connect twice!
post_save.connect(my_handler, sender=User)

# With dispatch_uid - only connects once
post_save.connect(
    my_handler, 
    sender=User, 
    dispatch_uid='create_user_profile'
)
```

</details>

---

### Question 10
How do you temporarily disable a signal for testing?

<details>
<summary>Show Answer</summary>

Several approaches:

**Option 1: Context manager**
```python
from contextlib import contextmanager

@contextmanager
def disable_signal(signal, receiver, sender):
    signal.disconnect(receiver, sender=sender)
    try:
        yield
    finally:
        signal.connect(receiver, sender=sender)

# Usage
with disable_signal(post_save, create_profile, User):
    user = User.objects.create(username='test')
```

**Option 2: factory_boy**
```python
@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
```

**Option 3: Test fixture**
```python
@pytest.fixture
def disable_profile_signal():
    post_save.disconnect(create_profile, sender=User)
    yield
    post_save.connect(create_profile, sender=User)
```

</details>

---

## 🚀 Level 3: Advanced

### Question 11
What's the difference between `signal.send()` and `signal.send_robust()`?

<details>
<summary>Show Answer</summary>

**`send()`**:
- If any receiver raises an exception, it propagates immediately
- Subsequent receivers don't run
- Good for development/testing

**`send_robust()`**:
- Catches exceptions from receivers
- All receivers run even if some fail
- Returns list of `(receiver, response)` tuples
- Good for production

```python
results = my_signal.send_robust(sender=self, data=data)

for receiver, response in results:
    if isinstance(response, Exception):
        logger.error(f"Handler {receiver} failed: {response}")
```

</details>

---

### Question 12
How do you create a custom signal?

<details>
<summary>Show Answer</summary>

```python
# signals.py
from django.dispatch import Signal

# Define the signal
order_completed = Signal()

# In your service/view - send the signal
def complete_order(order):
    order.status = 'completed'
    order.save()
    
    order_completed.send(
        sender=self.__class__,
        order=order,
        user=order.user
    )

# handlers.py - receive the signal
from django.dispatch import receiver
from .signals import order_completed

@receiver(order_completed)
def send_confirmation_email(sender, order, user, **kwargs):
    send_mail('Order Complete', 'Thanks!', 'shop@example.com', [user.email])
```

</details>

---

### Question 13
Why might this code cause problems in production?

```python
@receiver(post_save, sender=Order)
def process_order(sender, instance, created, **kwargs):
    if created:
        # Notify external warehouse API
        warehouse_api.notify(order_id=instance.pk)
```

<details>
<summary>Show Answer</summary>

**Problem**: The signal fires during the database transaction. If the transaction rolls back after the signal fires, the external warehouse is notified about an order that doesn't exist!

**Solution**: Use `transaction.on_commit()` to defer the external call until the transaction is committed:

```python
from django.db import transaction

@receiver(post_save, sender=Order)
def process_order(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda: warehouse_api.notify(order_id=instance.pk)
        )
```

</details>

---

### Question 14
What's wrong with relying on signal handler execution order?

```python
@receiver(post_save, sender=Order)
def handler_one(sender, instance, **kwargs):
    instance.processed_by_one = True

@receiver(post_save, sender=Order)  
def handler_two(sender, instance, **kwargs):
    if not instance.processed_by_one:
        raise Error("handler_one must run first!")
```

<details>
<summary>Show Answer</summary>

**The execution order of signal receivers is NOT guaranteed!** Handler two might run before handler one.

**Solutions:**

1. Make handlers independent:
```python
@receiver(post_save, sender=Order)
def handler_one(sender, instance, **kwargs):
    do_task_one(instance)  # Self-contained

@receiver(post_save, sender=Order)
def handler_two(sender, instance, **kwargs):
    do_task_two(instance)  # Self-contained, no dependency
```

2. Use a single handler with explicit ordering:
```python
@receiver(post_save, sender=Order)
def process_order(sender, instance, **kwargs):
    step_1(instance)
    step_2(instance)
    step_3(instance)
```

</details>

---

### Question 15
How do you track which fields changed in a model update?

<details>
<summary>Show Answer</summary>

Use `pre_save` to store original values, then compare in `post_save`:

```python
@receiver(pre_save, sender=Article)
def store_original(sender, instance, **kwargs):
    if instance.pk:
        try:
            original = Article.objects.get(pk=instance.pk)
            instance._original_values = {
                field.name: getattr(original, field.name)
                for field in sender._meta.fields
            }
        except Article.DoesNotExist:
            instance._original_values = {}
    else:
        instance._original_values = {}

@receiver(post_save, sender=Article)
def detect_changes(sender, instance, created, **kwargs):
    if not created:
        original = getattr(instance, '_original_values', {})
        for field in sender._meta.fields:
            old_value = original.get(field.name)
            new_value = getattr(instance, field.name)
            if old_value != new_value:
                print(f"{field.name} changed: {old_value} → {new_value}")
```

Alternatively, use `update_fields` if available:
```python
@receiver(post_save, sender=Article)
def check_updated_fields(sender, instance, update_fields, **kwargs):
    if update_fields:
        print(f"Updated fields: {update_fields}")
```

</details>

---

## 🏆 Bonus Questions

### Question 16
How would you implement a signal that only fires when a specific field changes?

<details>
<summary>Show Answer</summary>

```python
@receiver(pre_save, sender=Article)
def track_status_change(sender, instance, **kwargs):
    """Check if status is about to change"""
    instance._status_changed = False
    
    if instance.pk:
        try:
            old = Article.objects.get(pk=instance.pk)
            if old.status != instance.status:
                instance._status_changed = True
                instance._old_status = old.status
        except Article.DoesNotExist:
            pass

@receiver(post_save, sender=Article)
def on_status_changed(sender, instance, **kwargs):
    """React to status change"""
    if getattr(instance, '_status_changed', False):
        old_status = getattr(instance, '_old_status', None)
        print(f"Status changed from {old_status} to {instance.status}")
        
        if instance.status == 'published':
            send_notification("Article published!")
```

</details>

---

### Question 17
Design a reusable audit logging system using signals.

<details>
<summary>Show Answer</summary>

```python
# audit/models.py
from django.db import models
from django.contrib.contenttypes.models import ContentType

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('C', 'Create'),
        ('U', 'Update'),
        ('D', 'Delete'),
    ]
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    changes = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

# audit/signals.py
def register_audit(model_class):
    """Decorator to add audit logging to a model"""
    
    @receiver(pre_save, sender=model_class)
    def store_original(sender, instance, **kwargs):
        if instance.pk:
            try:
                original = sender.objects.get(pk=instance.pk)
                instance._audit_original = {
                    f.name: getattr(original, f.name)
                    for f in sender._meta.fields
                }
            except sender.DoesNotExist:
                pass
    
    @receiver(post_save, sender=model_class)
    def log_save(sender, instance, created, **kwargs):
        ct = ContentType.objects.get_for_model(sender)
        if created:
            AuditLog.objects.create(
                content_type=ct,
                object_id=str(instance.pk),
                action='C',
                changes={'new': {f.name: str(getattr(instance, f.name)) for f in sender._meta.fields}}
            )
        else:
            original = getattr(instance, '_audit_original', {})
            changes = {}
            for field in sender._meta.fields:
                old = original.get(field.name)
                new = getattr(instance, field.name)
                if old != new:
                    changes[field.name] = {'old': str(old), 'new': str(new)}
            if changes:
                AuditLog.objects.create(
                    content_type=ct,
                    object_id=str(instance.pk),
                    action='U',
                    changes=changes
                )
    
    @receiver(post_delete, sender=model_class)
    def log_delete(sender, instance, **kwargs):
        ct = ContentType.objects.get_for_model(sender)
        AuditLog.objects.create(
            content_type=ct,
            object_id=str(instance.pk),
            action='D'
        )
    
    return model_class

# Usage
@register_audit
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

</details>

---

## 📊 Score Yourself

| Score | Level |
|-------|-------|
| 0-5 | Beginner - Review the basics |
| 6-10 | Intermediate - Good foundation! |
| 11-14 | Advanced - Excellent understanding |
| 15-17 | Expert - You really know signals! |

---

*Return to: [Signals Overview →](./README.md)*
