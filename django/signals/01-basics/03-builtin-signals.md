# Built-in Django Signals 📦

Django comes with many built-in signals that you can use right away. Let's explore them all!

---

## 📊 Signal Categories Overview

```
Django Built-in Signals
├── Model Signals (most commonly used)
│   ├── pre_save
│   ├── post_save
│   ├── pre_delete
│   ├── post_delete
│   ├── pre_init
│   ├── post_init
│   └── m2m_changed
│
├── Request/Response Signals
│   ├── request_started
│   ├── request_finished
│   └── got_request_exception
│
├── Management Signals
│   ├── pre_migrate
│   └── post_migrate
│
└── Test Signals
    └── setting_changed
```

---

## 🔥 Model Signals (Most Important!)

These are the signals you'll use most often. They're sent when model operations occur.

### 1. `pre_save` - Before Saving

**When it fires:** Just before `Model.save()` writes to the database

**Use cases:**
- Auto-generate fields (slugs, timestamps)
- Validate data before saving
- Modify data before it's saved

```python
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

@receiver(pre_save, sender=Article)
def auto_generate_slug(sender, instance, **kwargs):
    """Generate slug before saving if not provided"""
    if not instance.slug:
        instance.slug = slugify(instance.title)
```

**Available arguments:**
| Argument | Description |
|----------|-------------|
| `sender` | The model class |
| `instance` | The model instance being saved |
| `raw` | Boolean - True if saved exactly as presented |
| `using` | The database alias |
| `update_fields` | Fields being updated (or None) |

---

### 2. `post_save` - After Saving

**When it fires:** Immediately after `Model.save()` completes

**Use cases:**
- Send notifications
- Create related objects
- Log changes
- Update caches

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when a new user is created"""
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
```

**Available arguments:**
| Argument | Description |
|----------|-------------|
| `sender` | The model class |
| `instance` | The model instance that was saved |
| `created` | **Boolean - True if NEW record** |
| `raw` | Boolean - True if saved exactly as presented |
| `using` | The database alias |
| `update_fields` | Fields that were updated |

💡 **Pro Tip:** The `created` argument is incredibly useful for differentiating between new objects and updates!

---

### 3. `pre_delete` - Before Deleting

**When it fires:** Just before `Model.delete()` removes from database

**Use cases:**
- Validate if deletion should proceed
- Create backup records
- Cascade custom deletions

```python
from django.db.models.signals import pre_delete
from django.dispatch import receiver

@receiver(pre_delete, sender=Order)
def prevent_paid_order_deletion(sender, instance, **kwargs):
    """Prevent deletion of paid orders"""
    if instance.status == 'paid':
        raise Exception("Cannot delete paid orders!")
```

**Available arguments:**
| Argument | Description |
|----------|-------------|
| `sender` | The model class |
| `instance` | The instance being deleted |
| `using` | The database alias |

---

### 4. `post_delete` - After Deleting

**When it fires:** Immediately after `Model.delete()` completes

**Use cases:**
- Clean up files or related resources
- Update counters
- Send notifications

```python
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

@receiver(post_delete, sender=UserPhoto)
def delete_photo_file(sender, instance, **kwargs):
    """Delete the actual file when UserPhoto is deleted"""
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)
```

---

### 5. `m2m_changed` - Many-to-Many Relationships

**When it fires:** When ManyToMany relationships are modified

**Use cases:**
- Track relationship changes
- Update related objects
- Enforce business rules

```python
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

@receiver(m2m_changed, sender=Article.tags.through)
def track_tag_changes(sender, instance, action, pk_set, **kwargs):
    """Track when tags are added or removed from articles"""
    if action == "post_add":
        print(f"Tags added to article '{instance.title}': {pk_set}")
    elif action == "post_remove":
        print(f"Tags removed from article '{instance.title}': {pk_set}")
    elif action == "post_clear":
        print(f"All tags cleared from article '{instance.title}'")
```

**Available arguments:**
| Argument | Description |
|----------|-------------|
| `sender` | The intermediate model (`.through`) |
| `instance` | The instance being modified |
| `action` | Type of action (see below) |
| `pk_set` | Primary keys being added/removed |
| `model` | The class of objects in the relation |
| `reverse` | Boolean - True if reverse relation |

**Action types:**
- `pre_add` - Before adding objects
- `post_add` - After adding objects
- `pre_remove` - Before removing objects
- `post_remove` - After removing objects
- `pre_clear` - Before clearing all objects
- `post_clear` - After clearing all objects

---

### 6. `pre_init` & `post_init` - Object Instantiation

**When they fire:** When a model instance is created in Python (not database!)

```python
# These fire when you do:
article = Article()  # pre_init fires, then post_init fires
article = Article(title="Test")  # Same here

# They also fire when loading from database:
article = Article.objects.get(pk=1)  # Signals fire when object is loaded
```

**Use cases:**
- Store original values for comparison
- Initialize non-database attributes

```python
from django.db.models.signals import post_init
from django.dispatch import receiver

@receiver(post_init, sender=Article)
def store_original_title(sender, instance, **kwargs):
    """Store original title to detect changes later"""
    instance._original_title = instance.title
```

---

## 🌐 Request/Response Signals

These signals are sent during HTTP request/response processing.

### 1. `request_started`

**When it fires:** At the very beginning of request processing

```python
from django.core.signals import request_started
from django.dispatch import receiver
import time

@receiver(request_started)
def log_request_start(sender, environ, **kwargs):
    """Log when a request starts"""
    print(f"Request started: {environ.get('PATH_INFO')}")
```

---

### 2. `request_finished`

**When it fires:** After the response is sent to the client

```python
from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(request_finished)
def cleanup_after_request(sender, **kwargs):
    """Perform cleanup after request completes"""
    # Clean up temporary resources
    pass
```

---

### 3. `got_request_exception`

**When it fires:** When an unhandled exception occurs

```python
from django.core.signals import got_request_exception
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(got_request_exception)
def log_request_exception(sender, request, **kwargs):
    """Log unhandled exceptions"""
    logger.error(f"Exception on {request.path}", exc_info=True)
```

---

## 🔧 Management Signals

### 1. `pre_migrate` & `post_migrate`

**When they fire:** Before and after running migrations

```python
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    """Create default data after migrations"""
    if sender.name == 'myapp':
        # Create default categories, settings, etc.
        pass
```

---

## 📝 Quick Reference Table

| Signal | Fires When | Common Use Cases |
|--------|------------|------------------|
| `pre_save` | Before saving | Auto-generate fields, validate |
| `post_save` | After saving | Notifications, create related objects |
| `pre_delete` | Before deletion | Validation, prevent deletion |
| `post_delete` | After deletion | Clean up files, update counters |
| `m2m_changed` | M2M relations change | Track relationship changes |
| `pre_init` | Before object created | Store original state |
| `post_init` | After object created | Initialize attributes |
| `request_started` | Request begins | Logging, timing |
| `request_finished` | Request ends | Cleanup |
| `got_request_exception` | Exception occurs | Error logging |
| `pre_migrate` | Before migrations | Pre-migration checks |
| `post_migrate` | After migrations | Create default data |

---

## 💡 Import Quick Reference

```python
# Model signals
from django.db.models.signals import (
    pre_save,
    post_save,
    pre_delete,
    post_delete,
    pre_init,
    post_init,
    m2m_changed,
)

# Request/Response signals
from django.core.signals import (
    request_started,
    request_finished,
    got_request_exception,
)

# Management signals
from django.db.models.signals import (
    pre_migrate,
    post_migrate,
)

# The receiver decorator
from django.dispatch import receiver
```

---

## ⚠️ Important Reminders

1. **Bulk operations bypass signals:**
   ```python
   # NO signals fired!
   MyModel.objects.bulk_create([obj1, obj2])
   MyModel.objects.filter(status='old').update(status='new')
   MyModel.objects.all().delete()
   ```

2. **QuerySet.delete() DOES fire signals** (for each object)

3. **Always include `**kwargs`** in your receiver functions

4. **Be careful with `post_save` and calling `save()` again** - infinite loops!

---

## 🎓 Quick Check

Before moving on, make sure you know:

- ✅ The difference between `pre_save` and `post_save`
- ✅ When `m2m_changed` fires and what actions it provides
- ✅ That bulk operations don't trigger signals
- ✅ What arguments each signal provides

---

## 🚀 Next Steps

Now that you know the built-in signals, let's learn how to **[Create Signal Receivers](../02-intermediate/01-signal-receivers.md)** effectively!

---

*Continue to: [Creating Signal Receivers →](../02-intermediate/01-signal-receivers.md)*
