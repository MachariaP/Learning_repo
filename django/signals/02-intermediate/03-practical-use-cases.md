# Practical Use Cases for Django Signals 🛠️

Let's explore real-world scenarios where Django signals shine. Each example includes complete, working code you can adapt for your projects.

---

## 1. 👤 User Profile Creation

**Scenario:** Automatically create a user profile when a new user registers.

```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
```

```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile for every new User"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save Profile when User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
```

---

## 2. 📧 Email Notifications

**Scenario:** Send notifications when important events occur.

```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Order, Comment

@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    """Send email notification when order is created or status changes"""
    if created:
        # New order notification
        subject = f"Order #{instance.id} Confirmed"
        message = render_to_string('emails/order_confirmed.html', {
            'order': instance
        })
        send_mail(
            subject,
            message,
            'orders@example.com',
            [instance.user.email],
            fail_silently=True
        )
    elif instance.status == 'shipped':
        # Shipping notification
        subject = f"Order #{instance.id} Has Shipped!"
        message = render_to_string('emails/order_shipped.html', {
            'order': instance
        })
        send_mail(
            subject,
            message,
            'orders@example.com',
            [instance.user.email],
            fail_silently=True
        )

@receiver(post_save, sender=Comment)
def notify_article_author(sender, instance, created, **kwargs):
    """Notify article author when someone comments"""
    if created and instance.article.author.email:
        send_mail(
            f"New comment on '{instance.article.title}'",
            f"{instance.user.username} commented: {instance.text[:100]}",
            'noreply@example.com',
            [instance.article.author.email],
            fail_silently=True
        )
```

---

## 3. 📝 Audit Logging

**Scenario:** Track all changes to important models for compliance or debugging.

```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Created'),
        ('UPDATE', 'Updated'),
        ('DELETE', 'Deleted'),
    ]
    
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField()
    object_repr = models.CharField(max_length=200)
    changes = models.JSONField(default=dict)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
```

```python
# signals.py
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import AuditLog, Product, Order
import json

# Store original values before save
@receiver(pre_save, sender=Product)
@receiver(pre_save, sender=Order)
def store_original_values(sender, instance, **kwargs):
    """Store original field values for change tracking"""
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
@receiver(post_save, sender=Order)
def create_audit_log_on_save(sender, instance, created, **kwargs):
    """Create audit log entry when object is saved"""
    
    if created:
        # New object
        AuditLog.objects.create(
            action='CREATE',
            model_name=sender.__name__,
            object_id=instance.pk,
            object_repr=str(instance),
            changes={'created': True},
            user=getattr(instance, '_current_user', None)
        )
    else:
        # Update - track what changed
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
                action='UPDATE',
                model_name=sender.__name__,
                object_id=instance.pk,
                object_repr=str(instance),
                changes=changes,
                user=getattr(instance, '_current_user', None)
            )

@receiver(post_delete, sender=Product)
@receiver(post_delete, sender=Order)
def create_audit_log_on_delete(sender, instance, **kwargs):
    """Create audit log entry when object is deleted"""
    AuditLog.objects.create(
        action='DELETE',
        model_name=sender.__name__,
        object_id=instance.pk,
        object_repr=str(instance),
        user=getattr(instance, '_current_user', None)
    )
```

---

## 4. 🖼️ File Cleanup

**Scenario:** Automatically delete files when model instances are deleted or updated.

```python
# signals.py
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os

@receiver(post_delete, sender=Product)
def delete_product_image_on_delete(sender, instance, **kwargs):
    """Delete product image file when Product is deleted"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)

@receiver(pre_save, sender=Product)
def delete_old_image_on_update(sender, instance, **kwargs):
    """Delete old image when uploading a new one"""
    if not instance.pk:
        return  # New object, nothing to delete
    
    try:
        old_instance = Product.objects.get(pk=instance.pk)
    except Product.DoesNotExist:
        return
    
    # Check if image changed
    if old_instance.image and old_instance.image != instance.image:
        if os.path.isfile(old_instance.image.path):
            os.remove(old_instance.image.path)
```

---

## 5. 🔢 Counter/Stats Updates

**Scenario:** Keep denormalized counters in sync automatically.

```python
# models.py
class Article(models.Model):
    title = models.CharField(max_length=200)
    comment_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()

class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['article', 'user']
```

```python
# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from .models import Comment, Like, Article

@receiver(post_save, sender=Comment)
def increment_comment_count(sender, instance, created, **kwargs):
    """Increment article comment count on new comment"""
    if created:
        Article.objects.filter(pk=instance.article_id).update(
            comment_count=F('comment_count') + 1
        )

@receiver(post_delete, sender=Comment)
def decrement_comment_count(sender, instance, **kwargs):
    """Decrement article comment count on comment delete"""
    Article.objects.filter(pk=instance.article_id).update(
        comment_count=F('comment_count') - 1
    )

@receiver(post_save, sender=Like)
def increment_like_count(sender, instance, created, **kwargs):
    """Increment article like count on new like"""
    if created:
        Article.objects.filter(pk=instance.article_id).update(
            like_count=F('like_count') + 1
        )

@receiver(post_delete, sender=Like)
def decrement_like_count(sender, instance, **kwargs):
    """Decrement article like count when like is removed"""
    Article.objects.filter(pk=instance.article_id).update(
        like_count=F('like_count') - 1
    )
```

---

## 6. 🔗 Slug Generation

**Scenario:** Auto-generate URL-friendly slugs from titles.

```python
# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Article, Category

def generate_unique_slug(model_class, instance, slug_field='slug', source_field='title'):
    """Generate a unique slug for a model instance"""
    source = getattr(instance, source_field)
    slug = slugify(source)
    
    if not slug:
        slug = 'untitled'
    
    unique_slug = slug
    counter = 1
    
    # Check for existing slugs, excluding current instance
    while model_class.objects.filter(**{slug_field: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
    
    return unique_slug

@receiver(pre_save, sender=Article)
def generate_article_slug(sender, instance, **kwargs):
    """Auto-generate slug for articles"""
    if not instance.slug:
        instance.slug = generate_unique_slug(Article, instance)

@receiver(pre_save, sender=Category)
def generate_category_slug(sender, instance, **kwargs):
    """Auto-generate slug for categories"""
    if not instance.slug:
        instance.slug = generate_unique_slug(Category, instance, source_field='name')
```

---

## 7. 🔍 Search Index Updates

**Scenario:** Update search index when content changes.

```python
# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Article
from .search import update_search_index, remove_from_search_index

@receiver(post_save, sender=Article)
def update_article_search_index(sender, instance, **kwargs):
    """Update search index when article is saved"""
    if instance.status == 'published':
        update_search_index('articles', instance.pk, {
            'title': instance.title,
            'content': instance.content,
            'author': instance.author.username,
            'tags': list(instance.tags.values_list('name', flat=True)),
            'published_at': instance.published_at.isoformat(),
        })
    else:
        # Remove unpublished articles from index
        remove_from_search_index('articles', instance.pk)

@receiver(post_delete, sender=Article)
def remove_article_from_search_index(sender, instance, **kwargs):
    """Remove article from search index when deleted"""
    remove_from_search_index('articles', instance.pk)
```

---

## 8. 💾 Cache Invalidation

**Scenario:** Automatically clear related caches when data changes.

```python
# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Article, Category, UserProfile

@receiver(post_save, sender=Article)
@receiver(post_delete, sender=Article)
def invalidate_article_cache(sender, instance, **kwargs):
    """Clear article-related caches"""
    # Clear specific article cache
    cache.delete(f'article_{instance.pk}')
    cache.delete(f'article_slug_{instance.slug}')
    
    # Clear list caches
    cache.delete('latest_articles')
    cache.delete(f'category_{instance.category_id}_articles')
    cache.delete(f'author_{instance.author_id}_articles')
    
    # Clear homepage cache
    cache.delete('homepage_featured')

@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):
    """Clear category-related caches"""
    cache.delete(f'category_{instance.pk}')
    cache.delete('all_categories')
    cache.delete('category_menu')

@receiver(post_save, sender=UserProfile)
def invalidate_user_cache(sender, instance, **kwargs):
    """Clear user profile cache"""
    cache.delete(f'user_profile_{instance.user_id}')
```

---

## 9. 🔔 Real-time Notifications (WebSocket/Channels)

**Scenario:** Send real-time updates to connected clients.

```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message, Notification

@receiver(post_save, sender=Message)
def broadcast_new_message(sender, instance, created, **kwargs):
    """Send message via WebSocket when new message is created"""
    if created:
        channel_layer = get_channel_layer()
        room_group_name = f'chat_{instance.room_id}'
        
        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': instance.id,
                    'text': instance.text,
                    'user': instance.user.username,
                    'timestamp': instance.created_at.isoformat(),
                }
            }
        )

@receiver(post_save, sender=Notification)
def broadcast_notification(sender, instance, created, **kwargs):
    """Send notification to user via WebSocket"""
    if created:
        channel_layer = get_channel_layer()
        user_group = f'notifications_{instance.user_id}'
        
        async_to_sync(channel_layer.group_send)(
            user_group,
            {
                'type': 'notification',
                'data': {
                    'id': instance.id,
                    'message': instance.message,
                    'link': instance.link,
                    'read': instance.read,
                }
            }
        )
```

---

## 10. 🎨 Image Processing

**Scenario:** Generate thumbnails or process images automatically.

```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from .models import Photo

@receiver(post_save, sender=Photo)
def create_thumbnail(sender, instance, created, **kwargs):
    """Create thumbnail for uploaded photos"""
    if not instance.image:
        return
    
    # Only process if image just uploaded (check if thumbnail missing or created)
    if created or not instance.thumbnail:
        img = Image.open(instance.image)
        
        # Create thumbnail
        thumbnail_size = (200, 200)
        img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        
        # Save thumbnail
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)
        thumb_io.seek(0)
        
        # Generate filename
        thumb_filename = f'thumb_{instance.image.name.split("/")[-1]}'
        
        # Update instance without triggering signal again
        Photo.objects.filter(pk=instance.pk).update(
            thumbnail=InMemoryUploadedFile(
                thumb_io, None, thumb_filename,
                'image/jpeg', sys.getsizeof(thumb_io), None
            )
        )
```

---

## 💡 Summary Table

| Use Case | Signal(s) | Key Benefit |
|----------|-----------|-------------|
| Profile Creation | post_save | One-to-one relationship automation |
| Email Notifications | post_save | Decoupled notification logic |
| Audit Logging | pre_save, post_save, post_delete | Automatic change tracking |
| File Cleanup | post_delete, pre_save | Prevent orphaned files |
| Counter Updates | post_save, post_delete | Denormalized data sync |
| Slug Generation | pre_save | Automatic URL-friendly slugs |
| Search Index | post_save, post_delete | Keep search in sync |
| Cache Invalidation | post_save, post_delete | Automatic cache management |
| Real-time Updates | post_save | WebSocket notifications |
| Image Processing | post_save | Automatic thumbnail generation |

---

## 🎓 Quick Check

Make sure you can:

- ✅ Identify when to use signals vs. direct code
- ✅ Implement common patterns like profile creation
- ✅ Handle file cleanup properly
- ✅ Update counters atomically with F() expressions
- ✅ Integrate with external systems (email, cache, search)

---

## 🚀 Next Steps

Now let's learn how to create **[Custom Signals](../03-advanced/01-custom-signals.md)** for your own events!

---

*Continue to: [Custom Signals →](../03-advanced/01-custom-signals.md)*
