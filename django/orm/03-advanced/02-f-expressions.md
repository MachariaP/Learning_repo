# F Expressions 📐

## What are F Expressions?

`F()` expressions let you reference field values directly in the database, without loading them into Python memory. This is both efficient and enables atomic operations.

```python
from django.db.models import F
```

---

## 🎯 Why F Expressions?

### Problem: Race Conditions

```python
# ❌ Not atomic - race condition possible!
product = Product.objects.get(pk=1)
product.stock = product.stock - 1  # Read value into Python
product.save()                      # Write back

# Between read and write, another request might also read the old value!
```

### Solution: F Expressions

```python
# ✅ Atomic database operation
from django.db.models import F

Product.objects.filter(pk=1).update(stock=F('stock') - 1)
# SQL: UPDATE products SET stock = stock - 1 WHERE id = 1
# The operation happens entirely in the database!
```

---

## 📊 Basic F Expression Usage

### Incrementing/Decrementing Values

```python
from django.db.models import F

# Increment view count
Article.objects.filter(pk=article_id).update(
    view_count=F('view_count') + 1
)

# Decrease stock
Product.objects.filter(pk=product_id).update(
    stock=F('stock') - quantity
)

# Double the price
Product.objects.all().update(
    price=F('price') * 2
)

# Apply 10% discount
Product.objects.filter(category='sale').update(
    price=F('price') * 0.9
)
```

### Arithmetic with F Expressions

```python
# Addition
F('field') + 10
F('field1') + F('field2')

# Subtraction
F('field') - 5
F('price') - F('discount')

# Multiplication
F('quantity') * F('unit_price')

# Division
F('total') / F('count')

# Modulo
F('quantity') % 10
```

---

## 🔗 F Expressions in Filters

Compare fields within the same model:

```python
# Products where stock is below reorder level
low_stock = Product.objects.filter(
    stock__lt=F('reorder_level')
)

# Posts with more comments than likes
controversial = Post.objects.filter(
    comment_count__gt=F('like_count')
)

# Orders where total exceeds budget
over_budget = Order.objects.filter(
    total__gt=F('customer__budget')
)

# Products on sale (discount_price < price)
on_sale = Product.objects.filter(
    discount_price__lt=F('price')
)
```

---

## 📅 F Expressions with Dates

```python
from django.db.models import F
from datetime import timedelta

# Tasks that are overdue
overdue = Task.objects.filter(
    due_date__lt=F('completed_date')
)

# Using timedelta for date arithmetic
from django.db.models import DurationField
from django.db.models.functions import Cast

# Orders shipped more than 3 days after ordering
slow_shipping = Order.objects.filter(
    shipped_date__gt=F('order_date') + timedelta(days=3)
)

# Subscriptions expiring within 30 days
expiring_soon = Subscription.objects.filter(
    expiry_date__lte=F('created_date') + timedelta(days=30)
)
```

---

## 🔧 F Expressions in Annotations

```python
from django.db.models import F, ExpressionWrapper, DecimalField

# Calculate profit margin
products = Product.objects.annotate(
    profit=F('price') - F('cost')
)

for product in products:
    print(f"{product.name}: ${product.profit} profit")

# Calculate percentage discount
products = Product.objects.annotate(
    discount_percent=ExpressionWrapper(
        (F('price') - F('discount_price')) / F('price') * 100,
        output_field=DecimalField()
    )
)

# Total value in stock
products = Product.objects.annotate(
    stock_value=F('price') * F('stock')
)
```

---

## 🎯 Practical Examples

### Example 1: E-commerce Inventory

```python
from django.db.models import F

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    reserved = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)

# Reserve items (atomic)
def reserve_item(product_id, quantity):
    updated = Product.objects.filter(
        pk=product_id,
        stock__gte=F('reserved') + quantity  # Check availability
    ).update(
        reserved=F('reserved') + quantity
    )
    return updated > 0  # True if successful

# Complete purchase
def complete_purchase(product_id, quantity):
    Product.objects.filter(pk=product_id).update(
        stock=F('stock') - quantity,
        reserved=F('reserved') - quantity
    )

# Get products needing reorder
def get_low_stock():
    return Product.objects.filter(
        stock__lte=F('reorder_level')
    )
```

### Example 2: Social Media Engagement

```python
# Increment like count atomically
Post.objects.filter(pk=post_id).update(
    like_count=F('like_count') + 1,
    engagement_score=F('engagement_score') + 1
)

# Decrement like count
Post.objects.filter(pk=post_id).update(
    like_count=F('like_count') - 1,
    engagement_score=F('engagement_score') - 1
)

# Find viral posts (likes > followers * 0.1)
viral_posts = Post.objects.filter(
    like_count__gt=F('author__followers') * 0.1
)
```

### Example 3: Rating System

```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    rating_sum = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)

# Add a rating (atomic)
def add_rating(product_id, rating):
    Product.objects.filter(pk=product_id).update(
        rating_sum=F('rating_sum') + rating,
        rating_count=F('rating_count') + 1
    )

# Get products with average rating
from django.db.models import FloatField
from django.db.models.functions import Cast

products = Product.objects.annotate(
    avg_rating=Cast(F('rating_sum'), FloatField()) / F('rating_count')
).filter(rating_count__gt=0)
```

---

## ⚠️ Important: Refreshing from Database

After using F() with `save()`, the model instance doesn't have the new value:

```python
product = Product.objects.get(pk=1)
product.stock = F('stock') - 1
product.save()

print(product.stock)  # Prints F('stock') - 1, NOT the new value!

# Refresh from database to get actual value
product.refresh_from_db()
print(product.stock)  # Now prints the actual value
```

**Better approach: Use update()**

```python
# This doesn't require refresh
Product.objects.filter(pk=1).update(stock=F('stock') - 1)
```

---

## 🔄 Combining F with Other Features

### With Q Objects

```python
from django.db.models import Q, F

# Products that are:
# - On sale (discount_price < price) AND in stock
# - OR featured regardless of sale
products = Product.objects.filter(
    Q(discount_price__lt=F('price'), stock__gt=0) |
    Q(is_featured=True)
)
```

### With Aggregations

```python
from django.db.models import Sum, F

# Total revenue per order
orders = Order.objects.annotate(
    total=Sum(F('items__quantity') * F('items__unit_price'))
)

# Total inventory value
total_value = Product.objects.aggregate(
    total=Sum(F('price') * F('stock'))
)
```

---

## 💡 Best Practices

### 1. Use update() for Bulk Operations

```python
# ❌ Slow - loads each object
for product in Product.objects.filter(category='electronics'):
    product.price = product.price * 1.1
    product.save()

# ✅ Fast - single query
Product.objects.filter(category='electronics').update(
    price=F('price') * 1.1
)
```

### 2. Use F() for Atomic Operations

```python
# ❌ Race condition possible
counter = Counter.objects.get(pk=1)
counter.count += 1
counter.save()

# ✅ Atomic - no race condition
Counter.objects.filter(pk=1).update(count=F('count') + 1)
```

### 3. Remember to refresh_from_db()

```python
# After save() with F(), refresh to get actual value
article.view_count = F('view_count') + 1
article.save()
article.refresh_from_db()  # Get the actual value
```

---

## 🎓 Quick Check

Before moving on, make sure you understand:

- ✅ F expressions reference database fields directly
- ✅ F expressions enable atomic operations
- ✅ How to use F in filters to compare fields
- ✅ How to use F in updates for incrementing/decrementing
- ✅ When to use refresh_from_db()

---

## 🚀 Next Steps

Now let's learn about **[Advanced Annotations](./03-advanced-annotations.md)**!

---

*Continue to: [Advanced Annotations →](./03-advanced-annotations.md)*
