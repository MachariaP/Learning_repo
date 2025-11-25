# Testing Django Signals 🧪

Testing signals is crucial for maintaining reliable applications. This guide covers strategies and patterns for effectively testing your signal handlers.

---

## 🎯 What to Test

When testing signals, focus on:

1. **Signal is sent** when expected event occurs
2. **Receiver executes** when signal is sent
3. **Receiver produces correct results** with various inputs
4. **Error handling** works as expected

---

## 📝 Basic Signal Testing

### Test That Signal is Sent

```python
# tests/test_signals.py
from django.test import TestCase
from django.db.models.signals import post_save
from unittest.mock import patch, MagicMock
from myapp.models import Order

class OrderSignalTests(TestCase):
    
    def test_post_save_signal_is_sent_on_order_creation(self):
        """Test that post_save signal fires when order is created"""
        # Create a mock handler
        mock_handler = MagicMock()
        
        # Connect the mock to the signal
        post_save.connect(mock_handler, sender=Order)
        
        try:
            # Create an order
            order = Order.objects.create(
                customer_name='John Doe',
                total=100.00
            )
            
            # Assert signal was sent
            mock_handler.assert_called_once()
            
            # Verify signal arguments
            call_args = mock_handler.call_args
            self.assertEqual(call_args.kwargs['sender'], Order)
            self.assertEqual(call_args.kwargs['instance'], order)
            self.assertTrue(call_args.kwargs['created'])
            
        finally:
            # Always disconnect to avoid affecting other tests
            post_save.disconnect(mock_handler, sender=Order)
```

### Test Receiver Logic

```python
from django.test import TestCase
from django.contrib.auth.models import User
from myapp.models import Profile

class UserProfileSignalTests(TestCase):
    
    def test_profile_created_for_new_user(self):
        """Test that profile is automatically created for new users"""
        # Create a user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Check profile was created
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertEqual(user.profile.user, user)
    
    def test_profile_not_duplicated_on_user_update(self):
        """Test that updating user doesn't create duplicate profile"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        initial_profile_count = Profile.objects.filter(user=user).count()
        
        # Update the user
        user.email = 'newemail@example.com'
        user.save()
        
        # Profile count should still be 1
        self.assertEqual(
            Profile.objects.filter(user=user).count(),
            initial_profile_count
        )
```

---

## 🔧 Using Mocks Effectively

### Mock External Services

```python
from django.test import TestCase
from unittest.mock import patch
from myapp.models import Order

class OrderNotificationTests(TestCase):
    
    @patch('myapp.signals.handlers.send_mail')
    def test_confirmation_email_sent_on_order_creation(self, mock_send_mail):
        """Test that confirmation email is sent when order is created"""
        order = Order.objects.create(
            customer_name='John Doe',
            customer_email='john@example.com',
            total=100.00
        )
        
        # Verify send_mail was called
        mock_send_mail.assert_called_once()
        
        # Verify email arguments
        call_args = mock_send_mail.call_args
        self.assertIn('Order Confirmed', call_args[1]['subject'])
        self.assertEqual(call_args[1]['recipient_list'], ['john@example.com'])
    
    @patch('myapp.signals.handlers.send_mail')
    def test_email_failure_does_not_crash_order_creation(self, mock_send_mail):
        """Test that email failure doesn't prevent order creation"""
        # Make send_mail raise an exception
        mock_send_mail.side_effect = Exception("SMTP Error")
        
        # This should not raise an exception
        order = Order.objects.create(
            customer_name='John Doe',
            customer_email='john@example.com',
            total=100.00
        )
        
        # Order should still be created
        self.assertIsNotNone(order.pk)
```

### Mock Signal Receivers

```python
from django.test import TestCase
from unittest.mock import patch

class OrderProcessingTests(TestCase):
    
    @patch('myapp.signals.handlers.update_inventory')
    @patch('myapp.signals.handlers.send_confirmation_email')
    def test_all_handlers_called_on_order_creation(
        self, mock_email, mock_inventory
    ):
        """Test that all signal handlers are invoked"""
        Order.objects.create(
            customer_name='John Doe',
            total=100.00
        )
        
        mock_email.assert_called_once()
        mock_inventory.assert_called_once()
```

---

## 🔌 Temporarily Disabling Signals

### Using a Context Manager

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

# Usage in tests
class OrderTests(TestCase):
    
    def test_order_without_signal(self):
        """Test order creation with signal disabled"""
        from myapp.signals.handlers import send_order_notification
        
        with disable_signal(post_save, send_order_notification, Order):
            # Signal won't fire here
            order = Order.objects.create(total=100)
```

### Using factory_boy with Signals Disabled

```python
# factories.py
import factory
from factory.django import DjangoModelFactory
from myapp.models import User, Order

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

# Create user without triggering signals
@factory.django.mute_signals(post_save)
class UserFactoryNoSignals(UserFactory):
    pass

# In tests
class ProfileTests(TestCase):
    
    def test_user_without_auto_profile(self):
        """Test that we can create user without profile"""
        user = UserFactoryNoSignals()
        self.assertFalse(hasattr(user, 'profile'))
```

### Using a Test Mixin

```python
# tests/mixins.py
from django.db.models.signals import post_save, pre_save

class DisableSignalsMixin:
    """Mixin to disable signals during tests"""
    
    disabled_signals = []  # Override in subclass
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._disconnected = []
        for signal, receiver, sender in cls.disabled_signals:
            signal.disconnect(receiver, sender=sender)
            cls._disconnected.append((signal, receiver, sender))
    
    @classmethod
    def tearDownClass(cls):
        for signal, receiver, sender in cls._disconnected:
            signal.connect(receiver, sender=sender)
        super().tearDownClass()

# Usage
class OrderTestsWithoutEmails(DisableSignalsMixin, TestCase):
    disabled_signals = [
        (post_save, send_order_notification, Order),
    ]
    
    def test_order_creation(self):
        # No email will be sent
        order = Order.objects.create(total=100)
```

---

## 🎭 Testing Custom Signals

### Test Signal Definition and Sending

```python
from django.test import TestCase
from unittest.mock import MagicMock
from myapp.signals import order_completed
from myapp.services import OrderService

class CustomSignalTests(TestCase):
    
    def test_order_completed_signal_is_sent(self):
        """Test that order_completed signal fires when order completes"""
        mock_handler = MagicMock()
        order_completed.connect(mock_handler)
        
        try:
            order = Order.objects.create(status='pending', total=100)
            OrderService.complete_order(order)
            
            # Verify signal was sent
            mock_handler.assert_called_once()
            
            # Verify signal data
            call_kwargs = mock_handler.call_args.kwargs
            self.assertEqual(call_kwargs['order'], order)
            
        finally:
            order_completed.disconnect(mock_handler)
    
    def test_order_completed_signal_not_sent_if_already_complete(self):
        """Test that signal doesn't fire for already completed orders"""
        mock_handler = MagicMock()
        order_completed.connect(mock_handler)
        
        try:
            order = Order.objects.create(status='completed', total=100)
            OrderService.complete_order(order)  # Should do nothing
            
            mock_handler.assert_not_called()
            
        finally:
            order_completed.disconnect(mock_handler)
```

### Test Custom Signal Receivers

```python
from django.test import TestCase
from unittest.mock import patch
from myapp.signals import order_completed

class OrderCompletedHandlerTests(TestCase):
    
    @patch('myapp.signals.handlers.send_completion_email')
    def test_completion_email_handler(self, mock_send_email):
        """Test that completion email is sent when signal fires"""
        order = Order.objects.create(
            customer_email='test@example.com',
            total=100
        )
        
        # Manually send the signal
        order_completed.send(
            sender=self.__class__,
            order=order
        )
        
        # Verify handler was triggered
        mock_send_email.assert_called_once_with(order)
```

---

## 📊 Testing with pytest

### Using pytest-django

```python
# tests/test_signals.py
import pytest
from django.contrib.auth.models import User
from myapp.models import Profile

@pytest.mark.django_db
class TestUserProfileSignal:
    
    def test_profile_created_for_new_user(self):
        """Test that profile is automatically created"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        assert hasattr(user, 'profile')
        assert user.profile.user == user
    
    def test_profile_persists_after_user_update(self):
        """Test that profile remains after user update"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        profile_id = user.profile.id
        
        user.email = 'new@example.com'
        user.save()
        
        user.refresh_from_db()
        assert user.profile.id == profile_id

@pytest.fixture
def mock_send_mail(mocker):
    """Fixture to mock email sending"""
    return mocker.patch('myapp.signals.handlers.send_mail')

@pytest.mark.django_db
def test_welcome_email_sent(mock_send_mail):
    """Test welcome email is sent on user creation"""
    User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass'
    )
    
    mock_send_mail.assert_called_once()
    call_args = mock_send_mail.call_args
    assert 'Welcome' in call_args[1]['subject']
```

### Fixture to Disable Signals

```python
# conftest.py
import pytest
from django.db.models.signals import post_save
from myapp.signals.handlers import create_user_profile
from django.contrib.auth.models import User

@pytest.fixture
def no_profile_signal():
    """Disable profile creation signal"""
    post_save.disconnect(create_user_profile, sender=User)
    yield
    post_save.connect(create_user_profile, sender=User)

@pytest.mark.django_db
def test_user_without_profile(no_profile_signal):
    """Test creating user without automatic profile"""
    user = User.objects.create_user(
        username='testuser',
        password='testpass'
    )
    assert not Profile.objects.filter(user=user).exists()
```

---

## 🏗️ Testing Signal Error Handling

### Test Error Recovery

```python
from django.test import TestCase
from unittest.mock import patch, MagicMock

class SignalErrorHandlingTests(TestCase):
    
    @patch('myapp.signals.handlers.send_mail')
    @patch('myapp.signals.handlers.logger')
    def test_email_error_is_logged(self, mock_logger, mock_send_mail):
        """Test that email errors are logged"""
        mock_send_mail.side_effect = Exception("SMTP Error")
        
        Order.objects.create(
            customer_email='test@example.com',
            total=100
        )
        
        # Verify error was logged
        mock_logger.error.assert_called()
        self.assertIn("Failed to send", str(mock_logger.error.call_args))
    
    def test_signal_error_does_not_rollback_transaction(self):
        """Test that handler errors don't prevent model save"""
        with patch('myapp.signals.handlers.process_order') as mock_process:
            mock_process.side_effect = Exception("Processing Error")
            
            # This should still succeed (if handler catches errors)
            order = Order.objects.create(total=100)
            
            # Order should exist
            self.assertTrue(Order.objects.filter(pk=order.pk).exists())
```

### Test send_robust() Behavior

```python
from django.test import TestCase
from myapp.signals import order_completed

class RobustSignalTests(TestCase):
    
    def test_send_robust_catches_handler_exceptions(self):
        """Test that send_robust catches exceptions"""
        def failing_handler(sender, **kwargs):
            raise ValueError("Handler error")
        
        def success_handler(sender, **kwargs):
            pass
        
        order_completed.connect(failing_handler)
        order_completed.connect(success_handler)
        
        try:
            results = order_completed.send_robust(
                sender=self.__class__,
                order=MagicMock()
            )
            
            # Should have 2 results
            self.assertEqual(len(results), 2)
            
            # One should be an exception
            exceptions = [r for _, r in results if isinstance(r, Exception)]
            self.assertEqual(len(exceptions), 1)
            
        finally:
            order_completed.disconnect(failing_handler)
            order_completed.disconnect(success_handler)
```

---

## 💡 Testing Tips

### Tip 1: Test Handlers in Isolation

```python
# Test the handler function directly, not through signals
from myapp.signals.handlers import create_user_profile

class ProfileHandlerTests(TestCase):
    
    def test_profile_creation_logic(self):
        """Test handler logic directly"""
        user = User.objects.create_user(
            username='test',
            password='test'
        )
        
        # Call handler directly
        create_user_profile(
            sender=User,
            instance=user,
            created=True
        )
        
        self.assertTrue(hasattr(user, 'profile'))
```

### Tip 2: Use TransactionTestCase for Signal Tests

```python
from django.test import TransactionTestCase

class TransactionalSignalTests(TransactionTestCase):
    """Use when testing signals with transactions"""
    
    def test_signal_runs_after_commit(self):
        """Test signal behavior with transactions"""
        # Some signals only fire after transaction commits
        pass
```

### Tip 3: Check Signal Connection

```python
def test_signal_is_connected(self):
    """Verify signal handler is properly connected"""
    from myapp.signals.handlers import create_profile
    
    connected_receivers = [
        r[1]() for r in post_save.receivers
        if r[1]() is not None
    ]
    
    self.assertIn(create_profile, connected_receivers)
```

---

## 🎓 Quick Check

Make sure you can:

- ✅ Test that signals fire at the right time
- ✅ Test signal receiver logic in isolation
- ✅ Use mocks to test external service calls
- ✅ Temporarily disable signals for specific tests
- ✅ Test error handling in signal handlers

---

## 🚀 Next Steps

Now let's learn about **[Common Pitfalls](./04-common-pitfalls.md)** with signals!

---

*Continue to: [Common Pitfalls →](./04-common-pitfalls.md)*
