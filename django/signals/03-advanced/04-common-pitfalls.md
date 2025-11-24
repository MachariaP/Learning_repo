# Common Pitfalls with Django Signals ⚠️

Learn from these common mistakes to avoid bugs and performance issues in your Django applications.

---

## 1. 🔄 Infinite Loops

The most dangerous pitfall! Calling `save()` in a `post_save` handler triggers the signal again.

### ❌ The Problem

```python
@receiver(post_save, sender=User)
def update_user_score(sender, instance, **kwargs):
    instance.score = calculate_score(instance)
    instance.save()  # 💥 INFINITE LOOP!
```

### ✅ Solutions

**Solution 1: Use `update()` instead of `save()`**
```python
@receiver(post_save, sender=User)
def update_user_score(sender, instance, **kwargs):
    User.objects.filter(pk=instance.pk).update(
        score=calculate_score(instance)
    )
```

**Solution 2: Use `update_fields` with a flag**
```python
@receiver(post_save, sender=User)
def update_user_score(sender, instance, created, update_fields, **kwargs):
    # Skip if only score was updated (we triggered this)
    if update_fields and 'score' in update_fields:
        return
    
    instance.score = calculate_score(instance)
    instance.save(update_fields=['score'])
```

**Solution 3: Use a flag to prevent recursion**
```python
@receiver(post_save, sender=User)
def update_user_score(sender, instance, **kwargs):
    if getattr(instance, '_updating_score', False):
        return
    
    instance._updating_score = True
    try:
        instance.score = calculate_score(instance)
        instance.save()
    finally:
        instance._updating_score = False
```

**Solution 4: Disconnect signal temporarily**
```python
@receiver(post_save, sender=User)
def update_user_score(sender, instance, **kwargs):
    post_save.disconnect(update_user_score, sender=User)
    try:
        instance.score = calculate_score(instance)
        instance.save()
    finally:
        post_save.connect(update_user_score, sender=User)
```

---

## 2. 📦 Bulk Operations Don't Trigger Signals

A common source of bugs! `bulk_create()`, `update()`, and `delete()` queryset methods do NOT trigger signals.

### ❌ The Problem

```python
# signals.py
@receiver(post_save, sender=Article)
def update_search_index(sender, instance, **kwargs):
    search_index.update(instance)

# views.py
def publish_articles(request, ids):
    # This does NOT trigger post_save signals!
    Article.objects.filter(pk__in=ids).update(status='published')
    # Search index is now out of sync! 😱
```

### ✅ Solutions

**Solution 1: Loop and save individually (slower but triggers signals)**
```python
def publish_articles(request, ids):
    for article in Article.objects.filter(pk__in=ids):
        article.status = 'published'
        article.save()  # Signal fires for each
```

**Solution 2: Manually call signal handlers**
```python
def publish_articles(request, ids):
    articles = list(Article.objects.filter(pk__in=ids))
    
    # Bulk update
    Article.objects.filter(pk__in=ids).update(status='published')
    
    # Manually trigger search index update
    for article in articles:
        article.status = 'published'  # Update local instance
        update_search_index(Article, article, created=False)
```

**Solution 3: Create a service function that handles both**
```python
# services.py
def publish_articles(ids):
    """Publish articles and update search index"""
    articles = Article.objects.filter(pk__in=ids)
    
    # Bulk update
    articles.update(status='published')
    
    # Update search index directly
    for article in articles:
        search_index.update(article)

# Don't rely on signals for this
```

---

## 3. 🔕 Signals Not Firing

Signals seem like they should work but don't run at all.

### ❌ Common Causes

**Cause 1: Signals file not imported**
```python
# myapp/signals.py exists but...

# ❌ apps.py doesn't import it
class MyappConfig(AppConfig):
    name = 'myapp'
    
    def ready(self):
        pass  # Signals never loaded!

# ✅ Fixed
class MyappConfig(AppConfig):
    name = 'myapp'
    
    def ready(self):
        import myapp.signals  # Now they load!
```

**Cause 2: Wrong sender specified**
```python
# ❌ Typo in sender
@receiver(post_save, sender=Users)  # Should be User!
def my_handler(sender, instance, **kwargs):
    pass

# ❌ Wrong import
from myapp.models import User  # Local User
@receiver(post_save, sender=User)  # But signal is for auth.User!

# ✅ Correct
from django.contrib.auth import get_user_model
User = get_user_model()
@receiver(post_save, sender=User)
```

**Cause 3: Using the wrong app config**
```python
# myapp/__init__.py
# ❌ Missing or wrong
default_app_config = 'myapp.apps.WrongConfig'

# ✅ Correct
default_app_config = 'myapp.apps.MyappConfig'
```

**Cause 4: Circular imports**
```python
# ❌ signals.py imports models.py which imports signals.py
# myapp/models.py
from .signals import my_signal  # Circular!

# ✅ Import at function level or use apps.py
```

---

## 4. 🐌 Performance Issues

Signals run synchronously and can significantly slow down your application.

### ❌ The Problem

```python
@receiver(post_save, sender=Order)
def process_order(sender, instance, created, **kwargs):
    if created:
        # Each of these blocks the request!
        generate_pdf_invoice(instance)     # 3 seconds
        send_email_notification(instance)   # 2 seconds
        update_analytics(instance)          # 1 second
        notify_warehouse(instance)          # 2 seconds
        # Total: 8 seconds added to EVERY order creation!
```

### ✅ Solutions

**Solution 1: Use Celery for async processing**
```python
@receiver(post_save, sender=Order)
def process_order(sender, instance, created, **kwargs):
    if created:
        # Queue tasks for async processing
        generate_pdf_invoice.delay(instance.pk)
        send_email_notification.delay(instance.pk)
        update_analytics.delay(instance.pk)
        notify_warehouse.delay(instance.pk)
        # Returns immediately!
```

**Solution 2: Use Django's built-in async support (3.1+)**
```python
import asyncio
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Order)
def process_order(sender, instance, created, **kwargs):
    if created:
        async_to_sync(async_process_order)(instance.pk)

async def async_process_order(order_id):
    await asyncio.gather(
        generate_pdf_invoice_async(order_id),
        send_email_notification_async(order_id),
    )
```

**Solution 3: Use transaction.on_commit for post-transaction tasks**
```python
from django.db import transaction

@receiver(post_save, sender=Order)
def process_order(sender, instance, created, **kwargs):
    if created:
        # Only runs after transaction commits
        transaction.on_commit(
            lambda: send_email_notification.delay(instance.pk)
        )
```

---

## 5. 🗄️ Database Transaction Issues

Signals fire before the transaction is committed, which can cause problems.

### ❌ The Problem

```python
@receiver(post_save, sender=Order)
def notify_external_service(sender, instance, created, **kwargs):
    if created:
        # This sends the order ID to an external service
        external_api.notify(order_id=instance.pk)
        # But if the transaction rolls back, the order doesn't exist!
        # External service has invalid data! 😱
```

### ✅ Solution: Use transaction.on_commit

```python
from django.db import transaction

@receiver(post_save, sender=Order)
def notify_external_service(sender, instance, created, **kwargs):
    if created:
        # Only runs AFTER the transaction successfully commits
        transaction.on_commit(
            lambda: external_api.notify(order_id=instance.pk)
        )
```

### Another Example: Creating Related Objects

```python
# ❌ Problem: Reading data that might not be committed yet
@receiver(post_save, sender=Order)
def process_order_items(sender, instance, created, **kwargs):
    # Items might not be committed yet!
    items = instance.items.all()
    for item in items:
        # This might fail or return incomplete data
        process_item(item)

# ✅ Solution: Defer to after commit
@receiver(post_save, sender=Order)
def process_order_items(sender, instance, created, **kwargs):
    def _process():
        # Now data is definitely in database
        items = Order.objects.get(pk=instance.pk).items.all()
        for item in items:
            process_item(item)
    
    transaction.on_commit(_process)
```

---

## 6. 🔗 Hidden Dependencies

Signals create implicit dependencies that are hard to track and debug.

### ❌ The Problem

```python
# views.py - Developer expects profile to exist
def user_dashboard(request):
    user = request.user
    profile = user.profile  # 💥 Crash if signal didn't run!
    return render(request, 'dashboard.html', {'profile': profile})

# But the signal might not run if:
# - User was created via bulk_create
# - Signal was temporarily disabled for testing
# - Database was restored from backup
# - Migration created users directly
```

### ✅ Solutions

**Solution 1: Handle missing profile gracefully**
```python
def user_dashboard(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    if not profile:
        # Create profile on-demand
        profile = Profile.objects.create(user=user)
    return render(request, 'dashboard.html', {'profile': profile})
```

**Solution 2: Use get_or_create pattern**
```python
def user_dashboard(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'bio': '', 'avatar': None}
    )
    return render(request, 'dashboard.html', {'profile': profile})
```

**Solution 3: Use a property on the User model**
```python
# models.py
class User(AbstractUser):
    @property
    def profile(self):
        obj, created = Profile.objects.get_or_create(user=self)
        return obj
```

---

## 7. 🧪 Testing Complications

Signals can make tests unpredictable and harder to debug.

### ❌ Common Problems

**Problem 1: Tests interfere with each other**
```python
# test_order.py
def test_order_creation():
    order = Order.objects.create(total=100)
    # Signal sent email, test passes

# test_email.py  
def test_no_emails_sent():
    # This test fails because previous test connected signals!
```

**Problem 2: Tests are slow due to signal handlers**
```python
def test_bulk_user_creation():
    for i in range(1000):
        User.objects.create(username=f'user{i}')
    # Each creation triggers email, profile creation, etc.
    # Test takes forever!
```

### ✅ Solutions

**Solution 1: Use fixtures that disable signals**
```python
import pytest
from django.db.models.signals import post_save

@pytest.fixture
def disable_signals():
    from myapp.signals import create_profile
    post_save.disconnect(create_profile, sender=User)
    yield
    post_save.connect(create_profile, sender=User)

def test_fast_user_creation(disable_signals):
    for i in range(1000):
        User.objects.create(username=f'user{i}')
    # Fast! No signals fired
```

**Solution 2: Use factory_boy with muted signals**
```python
import factory
from django.db.models.signals import post_save

@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: f'user{n}')
```

---

## 8. 🎭 Receiver Order Unpredictability

The order in which receivers execute is not guaranteed!

### ❌ The Problem

```python
# You might expect these to run in order...
@receiver(post_save, sender=Order)
def first_handler(sender, instance, **kwargs):
    instance.processed_by_first = True

@receiver(post_save, sender=Order)
def second_handler(sender, instance, **kwargs):
    # This might run BEFORE first_handler!
    if not getattr(instance, 'processed_by_first', False):
        raise Error("Expected first_handler to run first!")
```

### ✅ Solutions

**Solution 1: Make handlers independent**
```python
# Each handler should work regardless of order
@receiver(post_save, sender=Order)
def handler_a(sender, instance, **kwargs):
    # Don't depend on handler_b
    do_task_a(instance)

@receiver(post_save, sender=Order)
def handler_b(sender, instance, **kwargs):
    # Don't depend on handler_a
    do_task_b(instance)
```

**Solution 2: Use explicit ordering when needed**
```python
# Single handler that calls functions in order
@receiver(post_save, sender=Order)
def process_order(sender, instance, created, **kwargs):
    if created:
        step_1_validate(instance)
        step_2_calculate(instance)
        step_3_notify(instance)
```

---

## 9. 🔑 Missing **kwargs

Forgetting `**kwargs` breaks forward compatibility.

### ❌ The Problem

```python
# ❌ This will break if Django adds new arguments!
@receiver(post_save, sender=User)
def my_handler(sender, instance, created):
    pass

# When Django adds a new argument... 💥
# TypeError: my_handler() got unexpected keyword argument 'new_arg'
```

### ✅ Solution

```python
# ✅ Always include **kwargs
@receiver(post_save, sender=User)
def my_handler(sender, instance, created, **kwargs):
    pass
```

---

## 📋 Quick Reference: Pitfall Checklist

Before deploying signal code, check for:

| Pitfall | Check |
|---------|-------|
| Infinite loops | No `save()` in post_save (or properly guarded) |
| Bulk operations | Aware that `update()`/`bulk_create()` skip signals |
| Signal not firing | Imported in apps.py `ready()` |
| Performance | Heavy tasks are async |
| Transactions | Using `on_commit` for external calls |
| Hidden deps | Code handles missing related objects |
| Testing | Can disable signals when needed |
| Order deps | Handlers are independent |
| **kwargs | All handlers include `**kwargs` |

---

## 🎓 Summary

The biggest pitfalls to avoid:

1. **Infinite loops** - Never call `save()` in post_save without protection
2. **Bulk operations** - They don't trigger signals!
3. **Performance** - Use async tasks for slow operations
4. **Hidden dependencies** - Don't assume signals always run
5. **Testing** - Design for testability from the start

---

## 🚀 Next Steps

You've completed the advanced section! Check out the **[Examples](../examples/)** directory for complete working code.

---

*Return to: [Signals Overview →](../README.md)*
