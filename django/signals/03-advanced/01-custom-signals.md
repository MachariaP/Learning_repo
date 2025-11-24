# Creating Custom Signals 🎨

While Django's built-in signals cover most common scenarios, sometimes you need to create your own signals for custom events in your application.

---

## 🤔 When to Create Custom Signals

Create custom signals when:

- You want to notify other parts of your app about custom events
- You're building a reusable app that others can extend
- You want to decouple components without direct function calls
- Built-in signals don't cover your specific use case

**Examples:**
- User completed onboarding
- Order payment processed
- File upload completed
- Subscription renewed
- Report generated

---

## 📝 Creating a Custom Signal

### Step 1: Define the Signal

```python
# myapp/signals.py
from django.dispatch import Signal

# Define custom signals
order_completed = Signal()
payment_processed = Signal()
user_onboarding_completed = Signal()
report_generated = Signal()
```

### Step 2: Send the Signal

Send your signal from wherever the event occurs:

```python
# myapp/views.py or services.py
from .signals import order_completed, payment_processed

def complete_order(order):
    """Complete an order and notify listeners"""
    # Perform order completion logic
    order.status = 'completed'
    order.completed_at = timezone.now()
    order.save()
    
    # Send the signal!
    order_completed.send(
        sender=order.__class__,  # or sender=Order
        order=order,
        user=order.user
    )

def process_payment(order, payment_method):
    """Process payment and notify listeners"""
    # Process the payment
    result = payment_gateway.charge(
        amount=order.total,
        payment_method=payment_method
    )
    
    if result.success:
        # Send payment processed signal
        payment_processed.send(
            sender=None,  # Can be None for non-model signals
            order=order,
            transaction_id=result.transaction_id,
            amount=order.total
        )
    
    return result
```

### Step 3: Create Receivers

```python
# myapp/signals.py (or separate receiver files)
from django.dispatch import receiver
from .signals import order_completed, payment_processed

@receiver(order_completed)
def send_order_confirmation(sender, order, user, **kwargs):
    """Send confirmation email when order is completed"""
    send_mail(
        'Your order is complete!',
        f'Order #{order.id} has been completed.',
        'orders@example.com',
        [user.email]
    )

@receiver(order_completed)
def update_inventory(sender, order, **kwargs):
    """Update inventory when order is completed"""
    for item in order.items.all():
        item.product.stock -= item.quantity
        item.product.save()

@receiver(payment_processed)
def record_payment(sender, order, transaction_id, amount, **kwargs):
    """Record payment in payment history"""
    PaymentRecord.objects.create(
        order=order,
        transaction_id=transaction_id,
        amount=amount,
        status='success'
    )
```

---

## 🔧 Complete Working Example

Let's build a complete example with a custom signal for a subscription system:

### Define Signals

```python
# subscriptions/signals.py
from django.dispatch import Signal

# Custom signals for subscription events
subscription_created = Signal()
subscription_renewed = Signal()
subscription_cancelled = Signal()
subscription_expired = Signal()
```

### Create Models

```python
# subscriptions/models.py
from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    
    def __str__(self):
        return self.name

class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
```

### Create Services with Signal Sending

```python
# subscriptions/services.py
from django.utils import timezone
from datetime import timedelta
from .models import Subscription, Plan
from .signals import (
    subscription_created,
    subscription_renewed,
    subscription_cancelled,
    subscription_expired
)

class SubscriptionService:
    """Service class for subscription management"""
    
    @staticmethod
    def create_subscription(user, plan):
        """Create a new subscription"""
        subscription = Subscription.objects.create(
            user=user,
            plan=plan,
            end_date=timezone.now() + timedelta(days=plan.duration_days)
        )
        
        # Send custom signal
        subscription_created.send(
            sender=SubscriptionService,
            subscription=subscription,
            user=user,
            plan=plan
        )
        
        return subscription
    
    @staticmethod
    def renew_subscription(subscription):
        """Renew an existing subscription"""
        old_end_date = subscription.end_date
        subscription.end_date += timedelta(days=subscription.plan.duration_days)
        subscription.status = 'active'
        subscription.save()
        
        # Send custom signal
        subscription_renewed.send(
            sender=SubscriptionService,
            subscription=subscription,
            old_end_date=old_end_date,
            new_end_date=subscription.end_date
        )
        
        return subscription
    
    @staticmethod
    def cancel_subscription(subscription, reason=''):
        """Cancel a subscription"""
        subscription.status = 'cancelled'
        subscription.save()
        
        # Send custom signal
        subscription_cancelled.send(
            sender=SubscriptionService,
            subscription=subscription,
            reason=reason
        )
        
        return subscription
    
    @staticmethod
    def check_expired_subscriptions():
        """Check and expire subscriptions past their end date"""
        expired = Subscription.objects.filter(
            status='active',
            end_date__lt=timezone.now()
        )
        
        for subscription in expired:
            subscription.status = 'expired'
            subscription.save()
            
            # Send custom signal for each expired subscription
            subscription_expired.send(
                sender=SubscriptionService,
                subscription=subscription
            )
        
        return expired.count()
```

### Create Signal Handlers

```python
# subscriptions/handlers.py
from django.dispatch import receiver
from django.core.mail import send_mail
from .signals import (
    subscription_created,
    subscription_renewed,
    subscription_cancelled,
    subscription_expired
)
import logging

logger = logging.getLogger(__name__)

@receiver(subscription_created)
def send_welcome_email(sender, subscription, user, plan, **kwargs):
    """Send welcome email to new subscribers"""
    send_mail(
        subject=f'Welcome to {plan.name}!',
        message=f'''
        Hi {user.username},
        
        Thank you for subscribing to {plan.name}!
        Your subscription is active until {subscription.end_date}.
        
        Enjoy your membership!
        ''',
        from_email='subscriptions@example.com',
        recipient_list=[user.email],
        fail_silently=True
    )
    logger.info(f"Welcome email sent to {user.email}")

@receiver(subscription_created)
def grant_subscriber_permissions(sender, subscription, user, **kwargs):
    """Add user to subscribers group"""
    from django.contrib.auth.models import Group
    subscribers_group, _ = Group.objects.get_or_create(name='Subscribers')
    user.groups.add(subscribers_group)
    logger.info(f"Added {user.username} to Subscribers group")

@receiver(subscription_renewed)
def send_renewal_confirmation(sender, subscription, old_end_date, new_end_date, **kwargs):
    """Send confirmation when subscription is renewed"""
    send_mail(
        subject='Subscription Renewed!',
        message=f'''
        Your subscription has been renewed.
        New expiration date: {new_end_date}
        ''',
        from_email='subscriptions@example.com',
        recipient_list=[subscription.user.email],
        fail_silently=True
    )

@receiver(subscription_cancelled)
def handle_cancellation(sender, subscription, reason, **kwargs):
    """Handle subscription cancellation"""
    # Send cancellation confirmation
    send_mail(
        subject='Subscription Cancelled',
        message=f'''
        Your subscription has been cancelled.
        You will retain access until {subscription.end_date}.
        ''',
        from_email='subscriptions@example.com',
        recipient_list=[subscription.user.email],
        fail_silently=True
    )
    
    # Log the cancellation
    logger.info(f"Subscription cancelled for {subscription.user.username}. Reason: {reason}")

@receiver(subscription_expired)
def handle_expiration(sender, subscription, **kwargs):
    """Handle subscription expiration"""
    user = subscription.user
    
    # Send expiration notice
    send_mail(
        subject='Your Subscription Has Expired',
        message=f'''
        Hi {user.username},
        
        Your subscription has expired.
        Renew now to continue enjoying premium features!
        ''',
        from_email='subscriptions@example.com',
        recipient_list=[user.email],
        fail_silently=True
    )
    
    # Remove from subscribers group
    from django.contrib.auth.models import Group
    try:
        subscribers_group = Group.objects.get(name='Subscribers')
        user.groups.remove(subscribers_group)
    except Group.DoesNotExist:
        pass
    
    logger.info(f"Subscription expired for {user.username}")
```

### Register Handlers in apps.py

```python
# subscriptions/apps.py
from django.apps import AppConfig

class SubscriptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscriptions'
    
    def ready(self):
        import subscriptions.handlers  # Register signal handlers
```

### Usage in Views

```python
# subscriptions/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .services import SubscriptionService
from .models import Plan

@login_required
def subscribe(request, plan_id):
    """Subscribe user to a plan"""
    plan = Plan.objects.get(pk=plan_id)
    
    # Create subscription (signals will fire automatically!)
    subscription = SubscriptionService.create_subscription(
        user=request.user,
        plan=plan
    )
    
    return redirect('subscription_success')

@login_required
def cancel_subscription(request):
    """Cancel user's subscription"""
    subscription = request.user.subscription_set.filter(status='active').first()
    
    if subscription:
        reason = request.POST.get('reason', '')
        SubscriptionService.cancel_subscription(subscription, reason)
    
    return redirect('subscription_cancelled')
```

---

## 📊 Signal.send() vs Signal.send_robust()

### signal.send()

- Raises exceptions immediately
- If one receiver fails, subsequent receivers don't run
- Good for development/testing

```python
# If any receiver raises an exception, it propagates up
results = my_signal.send(sender=self, data=data)
```

### signal.send_robust()

- Catches exceptions in receivers
- All receivers run even if some fail
- Returns list of (receiver, response/exception) tuples
- Good for production

```python
# All receivers run, exceptions are caught
results = my_signal.send_robust(sender=self, data=data)

for receiver, response in results:
    if isinstance(response, Exception):
        logger.error(f"Signal handler {receiver} failed: {response}")
```

---

## 💡 Best Practices for Custom Signals

### 1. Document Your Signals

```python
# signals.py

#: Sent when an order is completed successfully.
#: 
#: Arguments:
#:     sender: The service class that completed the order
#:     order: The Order instance
#:     user: The User who placed the order
#:
#: Example:
#:     @receiver(order_completed)
#:     def handle_order_completed(sender, order, user, **kwargs):
#:         pass
order_completed = Signal()
```

### 2. Use Meaningful Names

```python
# ❌ Bad
signal1 = Signal()
my_signal = Signal()
s = Signal()

# ✅ Good
order_completed = Signal()
payment_processed = Signal()
user_registered = Signal()
```

### 3. Be Consistent with Arguments

```python
# ❌ Inconsistent
order_signal.send(sender=self, order=order)  # One way
order_signal.send(sender=None, obj=order)    # Another way

# ✅ Consistent
order_completed.send(sender=self.__class__, order=order)
```

### 4. Consider Using Classes

```python
# signals.py
class OrderSignals:
    """All signals related to orders"""
    completed = Signal()
    cancelled = Signal()
    shipped = Signal()
    refunded = Signal()

class PaymentSignals:
    """All signals related to payments"""
    processed = Signal()
    failed = Signal()
    refunded = Signal()

# Usage
from .signals import OrderSignals, PaymentSignals

OrderSignals.completed.send(sender=self, order=order)
PaymentSignals.processed.send(sender=self, payment=payment)
```

---

## ⚠️ Common Mistakes

### Mistake 1: Forgetting to Import Handlers

```python
# ❌ Handlers defined but never imported
# handlers.py exists but not imported in apps.py

# ✅ Import in apps.py
def ready(self):
    import myapp.handlers
```

### Mistake 2: Not Using **kwargs

```python
# ❌ Will break if signal adds new arguments
@receiver(my_signal)
def handler(sender, order, user):
    pass

# ✅ Always include **kwargs
@receiver(my_signal)
def handler(sender, order, user, **kwargs):
    pass
```

### Mistake 3: Heavy Processing in Handlers

```python
# ❌ Slow - blocks the main thread
@receiver(order_completed)
def process_order(sender, order, **kwargs):
    generate_pdf_report(order)  # Takes 30 seconds!
    send_to_warehouse(order)     # Takes 10 seconds!

# ✅ Use async tasks
@receiver(order_completed)
def process_order(sender, order, **kwargs):
    generate_pdf_report.delay(order.id)  # Celery task
    send_to_warehouse.delay(order.id)    # Celery task
```

---

## 🎓 Quick Check

Make sure you understand:

- ✅ How to create custom Signal objects
- ✅ How to send signals with send() and send_robust()
- ✅ How to structure signals in larger applications
- ✅ When to use custom signals vs built-in signals

---

## 🚀 Next Steps

Now let's learn about **[Signal Best Practices](./02-best-practices.md)**!

---

*Continue to: [Signal Best Practices →](./02-best-practices.md)*
