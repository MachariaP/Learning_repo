# Creating Signal Receivers 📡

## What is a Signal Receiver?

A **signal receiver** is a function that gets called when a signal is sent. Think of it as a callback function that "listens" for specific events.

---

## 🎯 Basic Structure

Every signal receiver follows this basic structure:

```python
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(signal, sender=ModelClass)
def my_receiver_function(sender, **kwargs):
    # Your code here
    pass
```

---

## 📝 Step-by-Step: Creating Your First Receiver

### Step 1: Import Required Components

```python
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, UserProfile
```

### Step 2: Define the Receiver Function

```python
@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile when a new User is created.
    
    Args:
        sender: The User model class
        instance: The actual User object that was saved
        created: True if this is a new user, False if updating
        **kwargs: Additional arguments (always include this!)
    """
    if created:
        UserProfile.objects.create(user=instance)
        print(f"Profile created for user: {instance.username}")
```

### Step 3: Register the Signal (Important!)

Make sure Django loads your signal. Create a `signals.py` file and import it in your app's config:

```python
# myapp/signals.py
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, UserProfile

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

```python
# myapp/apps.py
from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals  # This loads the signals!
```

---

## 🔍 Understanding Receiver Arguments

### Common Arguments Explained

```python
@receiver(post_save, sender=Article)
def my_receiver(sender, instance, created, raw, using, update_fields, **kwargs):
    """
    Let's break down each argument:
    """
    
    # sender - The model class that sent the signal
    print(f"Signal from: {sender.__name__}")  # Output: "Signal from: Article"
    
    # instance - The actual model object
    print(f"Article title: {instance.title}")
    
    # created - Boolean indicating if this is a NEW object
    if created:
        print("This is a new article!")
    else:
        print("This article was updated!")
    
    # raw - True if the model is saved exactly as presented
    # (used when loading fixtures)
    if raw:
        print("Loading from fixture, skipping custom logic")
        return
    
    # using - The database alias being used
    print(f"Using database: {using}")  # Usually "default"
    
    # update_fields - Set of field names being updated
    # Only set if save(update_fields=['field1', 'field2']) was called
    if update_fields:
        print(f"Only these fields updated: {update_fields}")
```

---

## 💻 Practical Receiver Examples

### Example 1: Auto-Generate Slug

```python
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

@receiver(pre_save, sender=Article)
def generate_article_slug(sender, instance, **kwargs):
    """Generate URL-friendly slug from title"""
    if not instance.slug:
        instance.slug = slugify(instance.title)
        
        # Ensure uniqueness
        original_slug = instance.slug
        counter = 1
        while Article.objects.filter(slug=instance.slug).exclude(pk=instance.pk).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1
```

### Example 2: Send Welcome Email

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """Send welcome email to new users"""
    if created and instance.email:
        send_mail(
            subject='Welcome to Our Site!',
            message=f'Hello {instance.username}, thank you for joining!',
            from_email='noreply@example.com',
            recipient_list=[instance.email],
            fail_silently=True,  # Don't crash if email fails
        )
```

### Example 3: Create Audit Log

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
import json

@receiver(post_save, sender=Article)
def log_article_save(sender, instance, created, **kwargs):
    """Create audit log entry when article is saved"""
    AuditLog.objects.create(
        action='CREATE' if created else 'UPDATE',
        model_name=sender.__name__,
        object_id=instance.pk,
        changes=json.dumps({'title': instance.title}),
        user=getattr(instance, '_current_user', None)
    )

@receiver(post_delete, sender=Article)
def log_article_delete(sender, instance, **kwargs):
    """Create audit log entry when article is deleted"""
    AuditLog.objects.create(
        action='DELETE',
        model_name=sender.__name__,
        object_id=instance.pk,
        changes=json.dumps({'title': instance.title}),
    )
```

### Example 4: Update Counters

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F

@receiver(post_save, sender=Comment)
def increment_comment_count(sender, instance, created, **kwargs):
    """Increment article's comment count when new comment added"""
    if created:
        Article.objects.filter(pk=instance.article_id).update(
            comment_count=F('comment_count') + 1
        )

@receiver(post_delete, sender=Comment)
def decrement_comment_count(sender, instance, **kwargs):
    """Decrement article's comment count when comment deleted"""
    Article.objects.filter(pk=instance.article_id).update(
        comment_count=F('comment_count') - 1
    )
```

### Example 5: Delete Related Files

```python
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os

@receiver(post_delete, sender=UserPhoto)
def delete_photo_on_delete(sender, instance, **kwargs):
    """Delete photo file when UserPhoto object is deleted"""
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)

@receiver(pre_save, sender=UserPhoto)
def delete_old_photo_on_update(sender, instance, **kwargs):
    """Delete old photo file when updating with new photo"""
    if not instance.pk:
        return  # New object, nothing to delete
    
    try:
        old_photo = UserPhoto.objects.get(pk=instance.pk).photo
    except UserPhoto.DoesNotExist:
        return
    
    new_photo = instance.photo
    if old_photo and old_photo != new_photo:
        if os.path.isfile(old_photo.path):
            os.remove(old_photo.path)
```

---

## 🏗️ Receiver Organization Best Practices

### File Structure

```
myapp/
├── __init__.py
├── admin.py
├── apps.py          # Import signals in ready()
├── models.py
├── signals/         # Organized signals directory
│   ├── __init__.py  # Import all signal modules
│   ├── user_signals.py
│   ├── article_signals.py
│   └── payment_signals.py
├── views.py
└── ...
```

### Example: `signals/__init__.py`

```python
# myapp/signals/__init__.py
from .user_signals import *
from .article_signals import *
from .payment_signals import *
```

### Example: `signals/user_signals.py`

```python
# myapp/signals/user_signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import User, UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
```

---

## 💡 Pro Tips

### Tip 1: Use Descriptive Function Names

```python
# ❌ Bad
@receiver(post_save, sender=User)
def handler(sender, instance, **kwargs):
    pass

# ✅ Good
@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    pass
```

### Tip 2: Add Docstrings

```python
@receiver(post_save, sender=Order)
def send_order_confirmation(sender, instance, created, **kwargs):
    """
    Send order confirmation email when a new order is created.
    
    This receiver:
    - Only runs for new orders (checks created=True)
    - Sends email to the user associated with the order
    - Silently fails if email cannot be sent
    """
    if created:
        send_confirmation_email(instance)
```

### Tip 3: Handle Errors Gracefully

```python
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        try:
            send_email(instance.email, "Welcome!")
        except Exception as e:
            # Log error but don't crash the save operation
            logger.error(f"Failed to send welcome email: {e}")
```

---

## ⚠️ Common Mistakes to Avoid

### Mistake 1: Infinite Loop

```python
# ❌ WRONG - Creates infinite loop!
@receiver(post_save, sender=User)
def update_user(sender, instance, **kwargs):
    instance.save()  # This triggers post_save again!

# ✅ CORRECT - Use update_fields or check created
@receiver(post_save, sender=User)
def update_user(sender, instance, created, **kwargs):
    if created:
        instance.welcome_sent = True
        instance.save(update_fields=['welcome_sent'])
```

### Mistake 2: Missing **kwargs

```python
# ❌ WRONG - Will break if Django adds new arguments
@receiver(post_save, sender=User)
def my_handler(sender, instance, created):
    pass

# ✅ CORRECT - Always include **kwargs
@receiver(post_save, sender=User)
def my_handler(sender, instance, created, **kwargs):
    pass
```

### Mistake 3: Not Importing Signals

```python
# ❌ WRONG - Signals file never loaded!
# (Just creating signals.py isn't enough)

# ✅ CORRECT - Import in apps.py
class MyappConfig(AppConfig):
    def ready(self):
        import myapp.signals
```

---

## 🎓 Quick Check

Make sure you understand:

- ✅ How to create a receiver function with the @receiver decorator
- ✅ What arguments receivers receive and what they mean
- ✅ How to properly register signals in apps.py
- ✅ Common patterns for practical receivers
- ✅ How to avoid common mistakes

---

## 🚀 Next Steps

Now let's learn about **[Connecting Signals](./02-connecting-signals.md)** in different ways!

---

*Continue to: [Connecting Signals →](./02-connecting-signals.md)*
