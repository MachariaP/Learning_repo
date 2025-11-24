# Signal Best Practices 🏆

Follow these best practices to write clean, maintainable, and performant signal handlers.

---

## 1. 📁 Organize Signal Code Properly

### Recommended File Structure

```
myapp/
├── __init__.py
├── apps.py                 # Import signals in ready()
├── models.py
├── signals/
│   ├── __init__.py         # Define and export signals
│   ├── handlers.py         # Signal handlers
│   └── decorators.py       # Custom decorators (if needed)
├── views.py
└── ...
```

### Alternative: Separate by Domain

```
myapp/
├── signals/
│   ├── __init__.py
│   ├── user_signals.py     # User-related signals and handlers
│   ├── order_signals.py    # Order-related signals and handlers
│   └── payment_signals.py  # Payment-related signals and handlers
```

### Best Practice: Centralized Signal Definition

```python
# myapp/signals/__init__.py
from django.dispatch import Signal

# Define all custom signals here
user_registered = Signal()
order_completed = Signal()
payment_processed = Signal()

# Import handlers to register them
from . import handlers  # noqa: F401
```

---

## 2. 💬 Document Signals Thoroughly

```python
# signals/__init__.py
from django.dispatch import Signal

#: Sent when a new user completes registration.
#:
#: Sender:
#:     The view or service that registered the user
#:
#: Arguments:
#:     user (User): The newly registered user instance
#:     request (HttpRequest): The registration request
#:     via (str): Registration method ('web', 'api', 'social')
#:
#: Example:
#:     >>> from myapp.signals import user_registered
#:     >>> 
#:     >>> @receiver(user_registered)
#:     >>> def on_user_registered(sender, user, request, via, **kwargs):
#:     ...     send_welcome_email(user)
user_registered = Signal()
```

---

## 3. 🎯 Keep Handlers Focused (Single Responsibility)

### ❌ Bad: One Handler Does Everything

```python
@receiver(post_save, sender=Order)
def handle_order(sender, instance, created, **kwargs):
    if created:
        # Send email
        send_mail('Order confirmed', 'Thanks!', 'shop@example.com', [instance.user.email])
        
        # Update inventory
        for item in instance.items.all():
            item.product.stock -= item.quantity
            item.product.save()
        
        # Create invoice
        Invoice.objects.create(order=instance, amount=instance.total)
        
        # Update user stats
        instance.user.profile.total_orders += 1
        instance.user.profile.total_spent += instance.total
        instance.user.profile.save()
        
        # Log the event
        AuditLog.objects.create(action='order_created', data={'order_id': instance.id})
        
        # Notify warehouse
        warehouse_api.notify(instance)
```

### ✅ Good: Separate Handlers for Each Concern

```python
@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    """Send confirmation email to customer"""
    if created:
        send_mail('Order confirmed', 'Thanks!', 'shop@example.com', [instance.user.email])

@receiver(post_save, sender=Order)
def update_inventory_on_order(sender, instance, created, **kwargs):
    """Update product inventory"""
    if created:
        for item in instance.items.all():
            item.product.stock -= item.quantity
            item.product.save()

@receiver(post_save, sender=Order)
def create_order_invoice(sender, instance, created, **kwargs):
    """Create invoice for the order"""
    if created:
        Invoice.objects.create(order=instance, amount=instance.total)

@receiver(post_save, sender=Order)
def update_user_statistics(sender, instance, created, **kwargs):
    """Update user's order statistics"""
    if created:
        instance.user.profile.total_orders += 1
        instance.user.profile.total_spent += instance.total
        instance.user.profile.save()

@receiver(post_save, sender=Order)
def log_order_creation(sender, instance, created, **kwargs):
    """Create audit log entry"""
    if created:
        AuditLog.objects.create(action='order_created', data={'order_id': instance.id})

@receiver(post_save, sender=Order)
def notify_warehouse_of_new_order(sender, instance, created, **kwargs):
    """Notify warehouse system"""
    if created:
        warehouse_api.notify(instance)
```

---

## 4. 🛡️ Handle Errors Gracefully

### Use Logging Instead of Silencing Errors

```python
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    """Send notification with proper error handling"""
    if not created:
        return
    
    try:
        send_mail(
            'Order Confirmed',
            f'Your order #{instance.id} has been confirmed.',
            'orders@example.com',
            [instance.user.email],
        )
        logger.info(f"Order confirmation email sent for order #{instance.id}")
    except Exception as e:
        # Log the error but don't crash the save operation
        logger.error(
            f"Failed to send order confirmation email for order #{instance.id}: {e}",
            exc_info=True
        )
```

### Use send_robust() for Custom Signals

```python
def complete_order(order):
    """Complete order with robust signal handling"""
    order.status = 'completed'
    order.save()
    
    # send_robust() catches exceptions in handlers
    results = order_completed.send_robust(
        sender=self.__class__,
        order=order
    )
    
    # Log any failures
    for receiver, response in results:
        if isinstance(response, Exception):
            logger.error(
                f"Signal handler {receiver.__name__} failed: {response}",
                exc_info=response
            )
```

---

## 5. ⚡ Optimize for Performance

### Avoid Database Queries in Signal Handlers

```python
# ❌ Bad: N+1 queries
@receiver(post_save, sender=Order)
def update_inventory(sender, instance, created, **kwargs):
    if created:
        for item in instance.items.all():  # Query 1
            product = item.product           # Query N (one per item)
            product.stock -= item.quantity
            product.save()

# ✅ Good: Optimized with select_related
@receiver(post_save, sender=Order)
def update_inventory(sender, instance, created, **kwargs):
    if created:
        items = instance.items.select_related('product').all()  # Single query
        for item in items:
            item.product.stock -= item.quantity
            item.product.save()

# ✅ Better: Bulk update with F expressions
@receiver(post_save, sender=Order)
def update_inventory(sender, instance, created, **kwargs):
    if created:
        from django.db.models import F
        
        for item in instance.items.all():
            Product.objects.filter(pk=item.product_id).update(
                stock=F('stock') - item.quantity
            )
```

### Use Async Tasks for Heavy Operations

```python
# ❌ Bad: Slow operations block the request
@receiver(post_save, sender=Order)
def process_order(sender, instance, created, **kwargs):
    if created:
        generate_pdf_invoice(instance)      # 5 seconds
        notify_shipping_provider(instance)  # 3 seconds
        send_sms_notification(instance)     # 2 seconds

# ✅ Good: Offload to Celery/background tasks
@receiver(post_save, sender=Order)
def process_order(sender, instance, created, **kwargs):
    if created:
        # These run asynchronously, don't block the request
        generate_pdf_invoice.delay(instance.id)
        notify_shipping_provider.delay(instance.id)
        send_sms_notification.delay(instance.id)
```

### Check Conditions Early

```python
# ❌ Bad: Does work before checking condition
@receiver(post_save, sender=Article)
def update_search_index(sender, instance, **kwargs):
    search_data = {
        'title': instance.title,
        'content': instance.content,
        'tags': list(instance.tags.values_list('name', flat=True)),
    }
    if instance.status == 'published':
        search_index.update(instance.id, search_data)

# ✅ Good: Check condition first
@receiver(post_save, sender=Article)
def update_search_index(sender, instance, **kwargs):
    if instance.status != 'published':
        return  # Early exit
    
    search_data = {
        'title': instance.title,
        'content': instance.content,
        'tags': list(instance.tags.values_list('name', flat=True)),
    }
    search_index.update(instance.id, search_data)
```

---

## 6. 🚫 Avoid Common Anti-Patterns

### Anti-Pattern 1: Infinite Loops

```python
# ❌ DANGEROUS: Infinite loop!
@receiver(post_save, sender=User)
def update_profile_score(sender, instance, **kwargs):
    instance.profile.score = calculate_score(instance)
    instance.profile.save()  # Triggers post_save on Profile
    # If Profile has a signal that saves User... infinite loop!

# ✅ Safe: Use update() or update_fields
@receiver(post_save, sender=User)
def update_profile_score(sender, instance, **kwargs):
    Profile.objects.filter(user=instance).update(
        score=calculate_score(instance)
    )
```

### Anti-Pattern 2: Calling save() in post_save

```python
# ❌ DANGEROUS: Triggers another post_save!
@receiver(post_save, sender=User)
def set_default_values(sender, instance, created, **kwargs):
    if created:
        instance.welcome_sent = True
        instance.save()  # Triggers post_save again!

# ✅ Safe: Use update_fields
@receiver(post_save, sender=User)
def set_default_values(sender, instance, created, **kwargs):
    if created:
        User.objects.filter(pk=instance.pk).update(welcome_sent=True)
        
# ✅ Alternative: Use pre_save instead
@receiver(pre_save, sender=User)
def set_default_values(sender, instance, **kwargs):
    if not instance.pk:  # New object
        instance.welcome_sent = True
```

### Anti-Pattern 3: Hidden Dependencies

```python
# ❌ Bad: View depends on signal handler silently
# If handler fails or is removed, view might break!

# signals.py
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# views.py
def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    # Assumes profile exists... but what if signal didn't run?
    return render(request, 'user.html', {'profile': user.profile})

# ✅ Good: Handle the case explicitly
def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    profile = getattr(user, 'profile', None)
    if not profile:
        profile = Profile.objects.create(user=user)
    return render(request, 'user.html', {'profile': profile})
```

---

## 7. 🧪 Make Signals Testable

### Design for Testability

```python
# ❌ Hard to test: Logic inside handler
@receiver(post_save, sender=Order)
def process_order(sender, instance, created, **kwargs):
    if created:
        # All logic here... hard to test in isolation
        calculate_tax(instance)
        apply_discount(instance)
        update_inventory(instance)

# ✅ Easy to test: Logic in separate functions
def process_new_order(order):
    """Testable function for order processing"""
    calculate_tax(order)
    apply_discount(order)
    update_inventory(order)

@receiver(post_save, sender=Order)
def process_order(sender, instance, created, **kwargs):
    """Signal handler just calls the service function"""
    if created:
        process_new_order(instance)
```

### Disable Signals in Tests When Needed

```python
# tests/conftest.py (pytest) or tests.py
from django.db.models.signals import post_save
from myapp.signals import my_handler

import pytest

@pytest.fixture
def disable_signals():
    """Fixture to disable specific signals for testing"""
    post_save.disconnect(my_handler, sender=User)
    yield
    post_save.connect(my_handler, sender=User)

def test_user_creation_without_signal(disable_signals):
    # Signal won't fire during this test
    user = User.objects.create(username='test')
    assert not hasattr(user, 'profile')
```

---

## 8. 📝 Use Type Hints (Python 3.5+)

```python
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Model
from typing import Any, Type

@receiver(post_save, sender=User)
def create_user_profile(
    sender: Type[Model],
    instance: User,
    created: bool,
    raw: bool = False,
    using: str = 'default',
    update_fields: list[str] | None = None,
    **kwargs: Any
) -> None:
    """
    Create profile for new users.
    
    Args:
        sender: The model class (User)
        instance: The saved user instance
        created: True if a new record was created
        raw: True if model is saved as presented
        using: Database alias being used
        update_fields: Fields that were updated
    """
    if created:
        Profile.objects.create(user=instance)
```

---

## 9. 🎯 Summary: When to Use Signals

### ✅ Good Use Cases

| Use Case | Why |
|----------|-----|
| Cross-app communication | Apps shouldn't import each other |
| Reusable app events | Let other apps extend behavior |
| Audit logging | Centralized, non-intrusive logging |
| Cache invalidation | Automatic, consistent cache clearing |
| Denormalized data sync | Keep counters/stats updated |

### ❌ When NOT to Use Signals

| Situation | Better Alternative |
|-----------|-------------------|
| Same-app logic | Direct function calls |
| Complex workflows | Service classes |
| Ordered operations | Explicit method calls |
| Transaction-critical | Use database transactions |
| Need return values | Use regular functions |

---

## 🎓 Quick Reference Checklist

Before deploying signal code, verify:

- [ ] Handlers are focused (single responsibility)
- [ ] Errors are logged, not silenced
- [ ] No infinite loops (save() in post_save)
- [ ] Heavy operations are async
- [ ] Database queries are optimized
- [ ] Signals are properly documented
- [ ] Tests exist for signal handlers
- [ ] Signals are imported in apps.py ready()

---

## 🚀 Next Steps

Now let's learn about **[Testing Signals](./03-testing-signals.md)**!

---

*Continue to: [Testing Signals →](./03-testing-signals.md)*
