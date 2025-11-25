# How Django Signals Work 🔧

## The Signal Mechanism

Django signals work through three main components:

1. **Signal** - The event notification itself
2. **Sender** - The code that sends/triggers the signal
3. **Receiver** - The function that responds to the signal

---

## 📊 Step-by-Step Flow

Let's trace what happens when you save a Django model:

```
┌─────────────────────────────────────────────────────────────┐
│                    YOU CALL model.save()                     │
└─────────────────────────────────┬───────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────┐
│           STEP 1: Django prepares to save                    │
│     - pre_save signal is sent BEFORE saving to database      │
└─────────────────────────────────┬───────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────┐
│           STEP 2: All pre_save receivers run                 │
│     - Each receiver function is called                       │
│     - They can modify the instance before it's saved         │
└─────────────────────────────────┬───────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────┐
│           STEP 3: Django saves to database                   │
│     - The actual INSERT or UPDATE happens                    │
└─────────────────────────────────┬───────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────┐
│           STEP 4: post_save signal is sent                   │
│     - Sent AFTER the save is complete                        │
└─────────────────────────────────┬───────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────┐
│           STEP 5: All post_save receivers run                │
│     - Each receiver function is called                       │
│     - They can perform follow-up actions                     │
└─────────────────────────────────┬───────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────┐
│                    SAVE COMPLETE!                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 The Three Key Components

### 1. The Signal Object

A signal is an instance of `django.dispatch.Signal`:

```python
from django.dispatch import Signal

# Django's built-in signals are defined like this:
pre_save = Signal()
post_save = Signal()
pre_delete = Signal()
post_delete = Signal()
```

### 2. The Sender

The sender is the class or object that triggers the signal. For model signals, it's usually the model class:

```python
# When you save a User model...
user = User(username="john")
user.save()  # This triggers signals with sender=User
```

### 3. The Receiver

The receiver is a function that runs when the signal is triggered:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def my_receiver_function(sender, instance, created, **kwargs):
    # sender = User class
    # instance = the actual user object that was saved
    # created = True if new, False if updated
    print(f"User {instance.username} was saved!")
```

---

## 📝 Understanding Receiver Arguments

Every signal receiver function receives specific arguments. Let's break them down:

### For `post_save` Signal:

```python
@receiver(post_save, sender=MyModel)
def my_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    """
    sender:        The model class (MyModel)
    instance:      The actual model instance that was saved
    created:       Boolean - True if a new record was created
    raw:           Boolean - True if the model is saved as presented (fixture loading)
    using:         The database alias being used
    update_fields: The set of fields to update (if save() was called with update_fields)
    **kwargs:      Always include this for forward compatibility!
    """
    pass
```

### For `pre_save` Signal:

```python
@receiver(pre_save, sender=MyModel)
def my_handler(sender, instance, raw, using, update_fields, **kwargs):
    """
    Same as post_save, but NO 'created' argument!
    Why? Because the object hasn't been saved yet, so we don't know.
    """
    pass
```

### For `post_delete` Signal:

```python
@receiver(post_delete, sender=MyModel)
def my_handler(sender, instance, using, **kwargs):
    """
    sender:   The model class
    instance: The instance that was deleted (still in memory!)
    using:    The database alias being used
    """
    pass
```

---

## 💻 Complete Working Example

Let's see a complete example of signal flow:

```python
# models.py
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(blank=True)
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
```

```python
# signals.py
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Article

# This runs BEFORE saving
@receiver(pre_save, sender=Article)
def generate_slug(sender, instance, **kwargs):
    """Auto-generate slug from title before saving"""
    if not instance.slug:
        instance.slug = slugify(instance.title)
    print(f"PRE_SAVE: Generating slug '{instance.slug}' for '{instance.title}'")

# This runs AFTER saving
@receiver(post_save, sender=Article)
def notify_about_article(sender, instance, created, **kwargs):
    """Notify when article is created or updated"""
    if created:
        print(f"POST_SAVE: NEW article created: {instance.title}")
        # send_notification("New article published!")
    else:
        print(f"POST_SAVE: Article UPDATED: {instance.title}")

# This runs AFTER deleting
@receiver(post_delete, sender=Article)
def cleanup_after_delete(sender, instance, **kwargs):
    """Clean up after article is deleted"""
    print(f"POST_DELETE: Article deleted: {instance.title}")
    # delete_related_files(instance)
```

```python
# Usage in Django shell or view
>>> from myapp.models import Article

# Creating a new article
>>> article = Article(title="My First Article", content="Hello World!")
>>> article.save()
PRE_SAVE: Generating slug 'my-first-article' for 'My First Article'
POST_SAVE: NEW article created: My First Article

# Updating the article
>>> article.content = "Updated content"
>>> article.save()
PRE_SAVE: Generating slug 'my-first-article' for 'My First Article'
POST_SAVE: Article UPDATED: My First Article

# Deleting the article
>>> article.delete()
POST_DELETE: Article deleted: My First Article
```

---

## 🔄 Signal Connection Methods

There are two ways to connect signals:

### Method 1: Using the @receiver Decorator (Recommended)

```python
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def my_handler(sender, instance, **kwargs):
    # Handle the signal
    pass
```

### Method 2: Using .connect() Method

```python
from django.db.models.signals import post_save

def my_handler(sender, instance, **kwargs):
    # Handle the signal
    pass

# Connect the signal
post_save.connect(my_handler, sender=User)
```

---

## 📍 Where to Put Signal Code

The recommended approach is:

### 1. Create a `signals.py` file in your app:

```
myapp/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── signals.py      # ← Your signals go here!
├── views.py
└── ...
```

### 2. Import signals in your app's `apps.py`:

```python
# myapp/apps.py
from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals  # ← Import signals here!
```

### 3. Make sure your app config is used in `__init__.py`:

```python
# myapp/__init__.py
default_app_config = 'myapp.apps.MyappConfig'
```

---

## 💡 Key Points to Remember

1. **`pre_save`** runs BEFORE the database operation
2. **`post_save`** runs AFTER the database operation
3. **`created`** argument tells you if it's a new object
4. **Always include `**kwargs`** in your receiver function
5. **Signals run synchronously** - they block until complete

---

## ⚠️ Important Warnings

1. **Don't call `save()` in `post_save` without protection!**
   ```python
   # BAD - Infinite loop!
   @receiver(post_save, sender=User)
   def bad_handler(sender, instance, **kwargs):
       instance.save()  # This triggers post_save again!

   # GOOD - Check if created
   @receiver(post_save, sender=User)
   def good_handler(sender, instance, created, **kwargs):
       if created:
           instance.do_something()
           instance.save()  # Only runs once for new objects
   ```

2. **Signals from `bulk_create` and `update()` are NOT sent!**
   ```python
   # These do NOT trigger signals:
   User.objects.bulk_create([user1, user2])  # No signals!
   User.objects.filter(active=True).update(score=0)  # No signals!
   ```

---

## 🎓 Quick Check

Before moving on, make sure you understand:

- ✅ The three components: Signal, Sender, Receiver
- ✅ The difference between `pre_save` and `post_save`
- ✅ How to use the `@receiver` decorator
- ✅ What arguments signal receivers receive
- ✅ Where to put your signal code

---

## 🚀 Next Steps

Now that you understand how signals work, let's explore **[Built-in Django Signals](./03-builtin-signals.md)**!

---

*Continue to: [Built-in Django Signals →](./03-builtin-signals.md)*
