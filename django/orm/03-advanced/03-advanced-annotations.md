# Advanced Annotations 🎨

## Beyond Basic Annotations

Annotations can do much more than simple counts and averages. Let's explore advanced techniques!

---

## 📊 Database Functions

Django provides many database functions for annotations:

```python
from django.db.models.functions import (
    # String functions
    Lower, Upper, Length, Concat, Substr, Trim,
    # Date functions
    TruncDate, TruncMonth, TruncYear, ExtractYear, ExtractMonth,
    # Math functions
    Abs, Ceil, Floor, Round, Power, Sqrt,
    # Conditional
    Coalesce, NullIf, Greatest, Least,
    # Type conversion
    Cast,
)
```

---

## 📝 String Functions

```python
from django.db.models.functions import Lower, Upper, Length, Concat, Substr

# Lowercase titles
books = Book.objects.annotate(
    title_lower=Lower('title')
)

# Uppercase author names
books = Book.objects.annotate(
    author_upper=Upper('author__name')
)

# Title length
books = Book.objects.annotate(
    title_length=Length('title')
).filter(title_length__gt=50)

# Concatenate fields
users = User.objects.annotate(
    full_name=Concat('first_name', Value(' '), 'last_name')
)

# Extract substring
books = Book.objects.annotate(
    short_title=Substr('title', 1, 30)
)
```

---

## 📅 Date Functions

```python
from django.db.models.functions import (
    TruncDate, TruncMonth, TruncYear, TruncHour,
    ExtractYear, ExtractMonth, ExtractDay, ExtractWeekDay
)
from django.db.models import Count

# Group orders by month
monthly_orders = (
    Order.objects
    .annotate(month=TruncMonth('created_at'))
    .values('month')
    .annotate(count=Count('id'), total=Sum('amount'))
    .order_by('month')
)

# Group by year
yearly_sales = (
    Sale.objects
    .annotate(year=TruncYear('date'))
    .values('year')
    .annotate(total=Sum('amount'))
)

# Extract month for filtering
orders = Order.objects.annotate(
    month=ExtractMonth('created_at')
).filter(month__in=[11, 12])  # Nov and Dec

# Group by day of week
daily_orders = (
    Order.objects
    .annotate(weekday=ExtractWeekDay('created_at'))
    .values('weekday')
    .annotate(count=Count('id'))
)
```

---

## 🔢 Math Functions

```python
from django.db.models.functions import Abs, Round, Ceil, Floor, Power, Sqrt

# Absolute difference
products = Product.objects.annotate(
    price_diff=Abs(F('price') - F('suggested_price'))
)

# Round to 2 decimal places
products = Product.objects.annotate(
    avg_rating=Round(Avg('reviews__rating'), 2)
)

# Calculate distance (simplified)
locations = Location.objects.annotate(
    distance=Sqrt(
        Power(F('x') - target_x, 2) + 
        Power(F('y') - target_y, 2)
    )
).order_by('distance')
```

---

## 🎯 Conditional Expressions

### Case/When

```python
from django.db.models import Case, When, Value, CharField, IntegerField

# Categorize by price
products = Product.objects.annotate(
    price_tier=Case(
        When(price__lt=20, then=Value('budget')),
        When(price__lt=50, then=Value('mid-range')),
        When(price__lt=100, then=Value('premium')),
        default=Value('luxury'),
        output_field=CharField()
    )
)

# Assign priority scores
tickets = Ticket.objects.annotate(
    priority_score=Case(
        When(priority='urgent', then=Value(100)),
        When(priority='high', then=Value(75)),
        When(priority='medium', then=Value(50)),
        default=Value(25),
        output_field=IntegerField()
    )
).order_by('-priority_score')

# Boolean flags
posts = Post.objects.annotate(
    is_popular=Case(
        When(view_count__gt=1000, then=Value(True)),
        default=Value(False),
        output_field=BooleanField()
    )
)
```

### Conditional Aggregation

```python
# Count by status
orders = Order.objects.aggregate(
    total=Count('id'),
    pending=Count(Case(When(status='pending', then=1))),
    completed=Count(Case(When(status='completed', then=1))),
    cancelled=Count(Case(When(status='cancelled', then=1)))
)

# Sum by condition
sales = Product.objects.aggregate(
    total_revenue=Sum('price'),
    premium_revenue=Sum(Case(
        When(category='premium', then=F('price'))
    ))
)
```

---

## 🔄 Coalesce and NullIf

```python
from django.db.models.functions import Coalesce, NullIf

# Replace NULL with default
products = Product.objects.annotate(
    display_price=Coalesce('discount_price', 'price')
)

# Replace NULL with zero for calculations
stats = Order.objects.aggregate(
    avg_discount=Avg(Coalesce('discount', Value(0)))
)

# NullIf - return NULL if values match
products = Product.objects.annotate(
    actual_discount=NullIf('discount_price', 'price')
)
```

---

## 📊 Subqueries

Use `Subquery` and `OuterRef` for complex queries:

```python
from django.db.models import Subquery, OuterRef

# Get latest order date for each customer
latest_orders = Order.objects.filter(
    customer=OuterRef('pk')
).order_by('-created_at')

customers = Customer.objects.annotate(
    last_order_date=Subquery(latest_orders.values('created_at')[:1])
)

# Get the price of the most expensive product in each category
most_expensive = Product.objects.filter(
    category=OuterRef('pk')
).order_by('-price')

categories = Category.objects.annotate(
    max_price=Subquery(most_expensive.values('price')[:1]),
    top_product=Subquery(most_expensive.values('name')[:1])
)
```

### Exists Subquery

```python
from django.db.models import Exists, OuterRef

# Check if user has recent orders
recent_orders = Order.objects.filter(
    user=OuterRef('pk'),
    created_at__gte=last_month
)

users = User.objects.annotate(
    has_recent_order=Exists(recent_orders)
)

# Filter by existence
active_users = User.objects.filter(
    Exists(Order.objects.filter(user=OuterRef('pk')))
)
```

---

## 🎨 Window Functions

For analytics and ranking:

```python
from django.db.models import Window, F
from django.db.models.functions import RowNumber, Rank, DenseRank, Lag, Lead

# Rank products by sales
products = Product.objects.annotate(
    sales_rank=Window(
        expression=Rank(),
        order_by=F('sales_count').desc()
    )
)

# Rank within categories
products = Product.objects.annotate(
    category_rank=Window(
        expression=Rank(),
        partition_by=[F('category')],
        order_by=F('sales_count').desc()
    )
)

# Running total
orders = Order.objects.annotate(
    running_total=Window(
        expression=Sum('amount'),
        order_by=F('created_at').asc()
    )
)

# Compare with previous row
sales = Sale.objects.annotate(
    previous_amount=Window(
        expression=Lag('amount'),
        order_by=F('date').asc()
    ),
    growth=F('amount') - F('previous_amount')
)
```

---

## 💡 Practical Examples

### Dashboard Statistics

```python
from django.db.models import Count, Sum, Avg, F, Q, Case, When
from django.db.models.functions import TruncMonth, Coalesce

# Comprehensive order stats
stats = Order.objects.aggregate(
    total_orders=Count('id'),
    total_revenue=Sum('total'),
    avg_order_value=Avg('total'),
    
    # By status
    pending_orders=Count('id', filter=Q(status='pending')),
    completed_orders=Count('id', filter=Q(status='completed')),
    
    # Revenue by status
    pending_revenue=Sum('total', filter=Q(status='pending')),
    completed_revenue=Sum('total', filter=Q(status='completed')),
)

# Monthly trends
monthly = (
    Order.objects
    .annotate(month=TruncMonth('created_at'))
    .values('month')
    .annotate(
        orders=Count('id'),
        revenue=Sum('total'),
        avg_value=Avg('total')
    )
    .order_by('month')
)
```

### Leaderboard

```python
# User leaderboard with rank
users = User.objects.annotate(
    total_points=Sum('achievements__points'),
    rank=Window(
        expression=DenseRank(),
        order_by=F('total_points').desc(nulls_last=True)
    )
).order_by('rank')[:100]
```

---

## 🎓 Quick Check

Before moving on, make sure you understand:

- ✅ How to use string functions (Lower, Upper, Concat)
- ✅ How to use date functions (TruncMonth, ExtractYear)
- ✅ How to use Case/When for conditional annotations
- ✅ How to use Subquery and OuterRef
- ✅ Basics of Window functions

---

## 🚀 Next Steps

Now let's learn about **[Query Optimization](./04-query-optimization.md)**!

---

*Continue to: [Query Optimization →](./04-query-optimization.md)*
