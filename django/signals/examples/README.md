# Django Signals - Code Examples 💻

This directory contains complete, working examples of Django signals. You can copy these directly into your projects.

---

## 📁 File Structure

```
examples/
├── README.md          # This file
├── basic_signals.py   # Basic signal examples
├── user_profile.py    # User profile auto-creation
├── audit_log.py       # Audit logging system
└── complete_app/      # Complete mini-application
    ├── models.py
    ├── signals.py
    ├── handlers.py
    └── apps.py
```

---

## 🔰 Basic Signals Example

### basic_signals.py

```python
"""
Basic Django Signals Examples
=============================

This file demonstrates the fundamentals of Django signals.
Copy this into your Django project to try it out.
"""

from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

# -----------------------------------------------------------------------------
# MODELS
# -----------------------------------------------------------------------------

class Article(models.Model):
    """Example model for demonstrating signals"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


# -----------------------------------------------------------------------------
# SIGNAL HANDLERS
# -----------------------------------------------------------------------------

@receiver(pre_save, sender=Article)
def article_pre_save(sender, instance, **kwargs):
    """
    Runs BEFORE the article is saved to the database.
    
    Use cases:
    - Auto-generate fields (like slugs)
    - Validate data
    - Modify data before saving
    """
    from django.utils.text import slugify
    
    # Auto-generate slug if not provided
    if not instance.slug:
        instance.slug = slugify(instance.title)
        
        # Ensure uniqueness
        original_slug = instance.slug
        counter = 1
        while Article.objects.filter(slug=instance.slug).exclude(pk=instance.pk).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1
    
    print(f"PRE_SAVE: About to save article '{instance.title}' with slug '{instance.slug}'")


@receiver(post_save, sender=Article)
def article_post_save(sender, instance, created, **kwargs):
    """
    Runs AFTER the article is saved to the database.
    
    Args:
        created (bool): True if this is a new article, False if updating
    
    Use cases:
    - Send notifications
    - Update related objects
    - Log the event
    """
    if created:
        print(f"POST_SAVE: New article created: '{instance.title}' (ID: {instance.pk})")
        # Here you might: send email, create related objects, etc.
    else:
        print(f"POST_SAVE: Article updated: '{instance.title}' (ID: {instance.pk})")


@receiver(pre_delete, sender=Article)
def article_pre_delete(sender, instance, **kwargs):
    """
    Runs BEFORE the article is deleted from the database.
    
    Use cases:
    - Validation (prevent deletion)
    - Backup data
    - Clean up files
    """
    print(f"PRE_DELETE: About to delete article '{instance.title}'")
    
    # Example: Prevent deletion of published articles
    # if instance.is_published:
    #     raise Exception("Cannot delete published articles!")


@receiver(post_delete, sender=Article)
def article_post_delete(sender, instance, **kwargs):
    """
    Runs AFTER the article is deleted from the database.
    
    Note: The instance still exists in memory but is deleted from DB.
    
    Use cases:
    - Clean up files
    - Update counters
    - Notify other systems
    """
    print(f"POST_DELETE: Article '{instance.title}' has been deleted")


# -----------------------------------------------------------------------------
# HOW TO USE
# -----------------------------------------------------------------------------

"""
To use these signals:

1. Place this code in your Django app (e.g., myapp/signals.py)

2. Import signals in your app's apps.py:
   
   # myapp/apps.py
   from django.apps import AppConfig
   
   class MyappConfig(AppConfig):
       name = 'myapp'
       
       def ready(self):
           import myapp.signals

3. Test in Django shell:
   
   >>> from myapp.models import Article
   
   # Create
   >>> article = Article.objects.create(title="My First Article", content="Hello!")
   PRE_SAVE: About to save article 'My First Article' with slug 'my-first-article'
   POST_SAVE: New article created: 'My First Article' (ID: 1)
   
   # Update
   >>> article.title = "My Updated Article"
   >>> article.save()
   PRE_SAVE: About to save article 'My Updated Article' with slug 'my-first-article'
   POST_SAVE: Article updated: 'My Updated Article' (ID: 1)
   
   # Delete
   >>> article.delete()
   PRE_DELETE: About to delete article 'My Updated Article'
   POST_DELETE: Article 'My Updated Article' has been deleted
"""
```

---

## 👤 User Profile Example

### user_profile.py

```python
"""
Automatic User Profile Creation
===============================

This is one of the most common uses of Django signals:
automatically creating a related profile when a user is created.
"""

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile when a new User is created"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the Profile when the User is saved"""
    # Check if profile exists (it might not for superusers created via createsuperuser)
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # Create profile if it doesn't exist
        Profile.objects.get_or_create(user=instance)


# -----------------------------------------------------------------------------
# USAGE EXAMPLE
# -----------------------------------------------------------------------------

"""
# In Django shell or views:

>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('john', 'john@example.com', 'password123')

# Profile is automatically created!
>>> user.profile
<Profile: john's profile>

>>> user.profile.bio = "Hello, I'm John!"
>>> user.profile.location = "New York"
>>> user.save()  # This also saves the profile

# Access profile data
>>> user.profile.bio
"Hello, I'm John!"
"""
```

---

## 📋 Audit Log Example

### audit_log.py

```python
"""
Audit Logging with Django Signals
=================================

Track all changes to important models automatically.
"""

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
import json


class AuditLog(models.Model):
    """Stores audit trail of model changes"""
    ACTION_CHOICES = [
        ('CREATE', 'Created'),
        ('UPDATE', 'Updated'),
        ('DELETE', 'Deleted'),
    ]
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    object_repr = models.CharField(max_length=200)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    changes = models.JSONField(default=dict)
    user = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.action} {self.content_type} #{self.object_id}"


class AuditableMixin:
    """Mixin to make models auditable"""
    
    _original_values = None
    _current_user = None
    
    def set_current_user(self, user):
        """Set the user who is making changes"""
        self._current_user = user


# Example auditable model
class Product(models.Model, AuditableMixin):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


# Signal handlers for audit logging
@receiver(pre_save, sender=Product)
def store_original_values(sender, instance, **kwargs):
    """Store original values before save for change tracking"""
    if instance.pk:
        try:
            original = sender.objects.get(pk=instance.pk)
            instance._original_values = {
                field.name: getattr(original, field.name)
                for field in sender._meta.fields
            }
        except sender.DoesNotExist:
            instance._original_values = {}
    else:
        instance._original_values = {}


@receiver(post_save, sender=Product)
def audit_log_save(sender, instance, created, **kwargs):
    """Create audit log entry when product is saved"""
    content_type = ContentType.objects.get_for_model(sender)
    
    if created:
        AuditLog.objects.create(
            content_type=content_type,
            object_id=str(instance.pk),
            object_repr=str(instance),
            action='CREATE',
            changes={'created': True, 'values': {
                field.name: str(getattr(instance, field.name))
                for field in sender._meta.fields
            }},
            user=getattr(instance, '_current_user', None)
        )
    else:
        # Track what changed
        changes = {}
        original = getattr(instance, '_original_values', {})
        
        for field in sender._meta.fields:
            old_value = original.get(field.name)
            new_value = getattr(instance, field.name)
            if old_value != new_value:
                changes[field.name] = {
                    'old': str(old_value),
                    'new': str(new_value)
                }
        
        if changes:
            AuditLog.objects.create(
                content_type=content_type,
                object_id=str(instance.pk),
                object_repr=str(instance),
                action='UPDATE',
                changes=changes,
                user=getattr(instance, '_current_user', None)
            )


@receiver(post_delete, sender=Product)
def audit_log_delete(sender, instance, **kwargs):
    """Create audit log entry when product is deleted"""
    content_type = ContentType.objects.get_for_model(sender)
    
    AuditLog.objects.create(
        content_type=content_type,
        object_id=str(instance.pk),
        object_repr=str(instance),
        action='DELETE',
        changes={'deleted_values': {
            field.name: str(getattr(instance, field.name))
            for field in sender._meta.fields
        }},
        user=getattr(instance, '_current_user', None)
    )


# -----------------------------------------------------------------------------
# USAGE EXAMPLE
# -----------------------------------------------------------------------------

"""
# Create a product
>>> product = Product.objects.create(name="Widget", price=9.99, stock=100)

# View audit log
>>> AuditLog.objects.first()
<AuditLog: CREATE Product #1>
>>> AuditLog.objects.first().changes
{'created': True, 'values': {'id': '1', 'name': 'Widget', 'price': '9.99', 'stock': '100', 'is_active': 'True'}}

# Update the product
>>> product.price = 14.99
>>> product.save()

# View the change
>>> log = AuditLog.objects.first()
>>> log.action
'UPDATE'
>>> log.changes
{'price': {'old': '9.99', 'new': '14.99'}}

# Delete
>>> product.delete()
>>> AuditLog.objects.first().action
'DELETE'
"""
```

---

## 🏗️ Complete Application Example

### complete_app/models.py

```python
"""Models for the complete signals example application"""

from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    article_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    article_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"
```

### complete_app/signals.py

```python
"""Signal definitions for the application"""

from django.dispatch import Signal

# Custom signals
article_published = Signal()  # Sent when article status changes to 'published'
article_viewed = Signal()     # Sent when article is viewed
```

### complete_app/handlers.py

```python
"""Signal handlers for the application"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models import F
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .models import Author, Article, Comment, Category
from .signals import article_published, article_viewed


# -----------------------------------------------------------------------------
# USER SIGNALS
# -----------------------------------------------------------------------------

@receiver(post_save, sender=User)
def create_author_profile(sender, instance, created, **kwargs):
    """Create Author profile for new users"""
    if created:
        Author.objects.create(user=instance)


# -----------------------------------------------------------------------------
# ARTICLE SIGNALS
# -----------------------------------------------------------------------------

@receiver(pre_save, sender=Article)
def generate_article_slug(sender, instance, **kwargs):
    """Auto-generate slug from title"""
    if not instance.slug:
        instance.slug = slugify(instance.title)
        
        # Ensure uniqueness
        original_slug = instance.slug
        counter = 1
        while Article.objects.filter(slug=instance.slug).exclude(pk=instance.pk).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1


@receiver(pre_save, sender=Article)
def track_status_change(sender, instance, **kwargs):
    """Track if status is changing to published"""
    if instance.pk:
        try:
            old_instance = Article.objects.get(pk=instance.pk)
            instance._was_published = (
                old_instance.status != 'published' and 
                instance.status == 'published'
            )
        except Article.DoesNotExist:
            instance._was_published = False
    else:
        instance._was_published = instance.status == 'published'


@receiver(post_save, sender=Article)
def handle_article_published(sender, instance, created, **kwargs):
    """Send signal when article is published"""
    if getattr(instance, '_was_published', False):
        article_published.send(sender=sender, article=instance)


@receiver(post_save, sender=Article)
def update_author_article_count(sender, instance, created, **kwargs):
    """Update author's article count"""
    if created:
        Author.objects.filter(pk=instance.author_id).update(
            article_count=F('article_count') + 1
        )


@receiver(post_delete, sender=Article)
def decrement_author_article_count(sender, instance, **kwargs):
    """Decrement author's article count when article deleted"""
    Author.objects.filter(pk=instance.author_id).update(
        article_count=F('article_count') - 1
    )


@receiver(article_published)
def notify_followers(sender, article, **kwargs):
    """Notify when article is published (placeholder)"""
    print(f"SIGNAL: Article published: {article.title}")
    # In real app: send emails, push notifications, etc.


@receiver(article_viewed)
def increment_view_count(sender, article, **kwargs):
    """Increment article view count"""
    Article.objects.filter(pk=article.pk).update(
        view_count=F('view_count') + 1
    )


# -----------------------------------------------------------------------------
# CATEGORY SIGNALS
# -----------------------------------------------------------------------------

@receiver(post_save, sender=Article)
def update_category_count_on_save(sender, instance, created, **kwargs):
    """Update category article count"""
    if created and instance.category:
        Category.objects.filter(pk=instance.category_id).update(
            article_count=F('article_count') + 1
        )


@receiver(post_delete, sender=Article)
def update_category_count_on_delete(sender, instance, **kwargs):
    """Decrement category article count"""
    if instance.category:
        Category.objects.filter(pk=instance.category_id).update(
            article_count=F('article_count') - 1
        )


# -----------------------------------------------------------------------------
# COMMENT SIGNALS
# -----------------------------------------------------------------------------

@receiver(post_save, sender=Comment)
def notify_article_author(sender, instance, created, **kwargs):
    """Notify article author of new comment"""
    if created:
        article = instance.article
        author_email = article.author.user.email
        
        if author_email:
            # In production, use async task
            print(f"EMAIL: New comment on '{article.title}' from {instance.user.username}")
            # send_mail(
            #     f"New comment on '{article.title}'",
            #     f"{instance.user.username} commented: {instance.text[:100]}...",
            #     'noreply@example.com',
            #     [author_email],
            # )
```

### complete_app/apps.py

```python
"""App configuration"""

from django.apps import AppConfig


class CompleteAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'complete_app'
    
    def ready(self):
        # Import handlers to register signals
        from . import handlers  # noqa: F401
```

---

## 🎯 How to Use These Examples

1. **Copy the relevant code** into your Django project
2. **Update imports** to match your app structure
3. **Register signals** in your `apps.py`
4. **Run migrations** for any new models
5. **Test in Django shell** to verify signals work

---

*Return to: [Signals Overview →](../README.md)*
