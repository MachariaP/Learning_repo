# Q Objects for Complex Queries 🔍

## What are Q Objects?

`Q` objects allow you to build complex queries with **OR**, **AND**, and **NOT** conditions that aren't possible with simple filter() calls.

```python
from django.db.models import Q
```

---

## 🎯 Why Q Objects?

Regular filter() only supports AND conditions:

```python
# This is AND - book must match ALL conditions
Book.objects.filter(price__lt=30, is_published=True)
# WHERE price < 30 AND is_published = True
```

**But what if you need OR?**

```python
# ❌ This doesn't work!
Book.objects.filter(author='John' OR author='Jane')

# ✅ Use Q objects
Book.objects.filter(Q(author='John') | Q(author='Jane'))
# WHERE author = 'John' OR author = 'Jane'
```

---

## 📊 Q Object Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `|` | OR | `Q(a=1) | Q(b=2)` |
| `&` | AND | `Q(a=1) & Q(b=2)` |
| `~` | NOT | `~Q(a=1)` |

---

## 🔗 OR Queries

### Basic OR

```python
from django.db.models import Q

# Books by John OR Jane
books = Book.objects.filter(
    Q(author='John Doe') | Q(author='Jane Smith')
)
# WHERE author = 'John Doe' OR author = 'Jane Smith'

# Books under $20 OR over $100
books = Book.objects.filter(
    Q(price__lt=20) | Q(price__gt=100)
)
```

### Multiple OR Conditions

```python
# Books by any of these authors
books = Book.objects.filter(
    Q(author='John') | Q(author='Jane') | Q(author='Bob')
)

# More elegant with a loop
authors = ['John', 'Jane', 'Bob']
query = Q()
for author in authors:
    query |= Q(author=author)
books = Book.objects.filter(query)

# Even better - use __in
books = Book.objects.filter(author__in=['John', 'Jane', 'Bob'])
```

---

## 🔄 AND Queries

### Explicit AND

```python
# Using Q with & (same as regular filter)
books = Book.objects.filter(
    Q(is_published=True) & Q(price__lt=30)
)
# WHERE is_published = True AND price < 30

# Same as:
books = Book.objects.filter(is_published=True, price__lt=30)
```

### Combining AND with OR

```python
# Published AND (cheap OR bestseller)
books = Book.objects.filter(
    Q(is_published=True) & (Q(price__lt=20) | Q(is_bestseller=True))
)
# WHERE is_published = True AND (price < 20 OR is_bestseller = True)

# (Python OR Django) AND published
books = Book.objects.filter(
    (Q(title__icontains='python') | Q(title__icontains='django')) 
    & Q(is_published=True)
)
```

---

## ❌ NOT Queries

### Basic NOT

```python
# Books NOT by John
books = Book.objects.filter(~Q(author='John'))
# WHERE NOT author = 'John'

# Same as exclude()
books = Book.objects.exclude(author='John')
```

### Complex NOT

```python
# NOT (expensive AND unpublished)
books = Book.objects.filter(
    ~(Q(price__gt=100) & Q(is_published=False))
)
# WHERE NOT (price > 100 AND is_published = False)

# Published books NOT in these categories
books = Book.objects.filter(
    Q(is_published=True) & ~Q(category__in=['Draft', 'Hidden'])
)
```

---

## 🎨 Complex Query Examples

### Example 1: Search Functionality

```python
def search_books(query):
    """Search books by title, author, or description"""
    return Book.objects.filter(
        Q(title__icontains=query) |
        Q(author__name__icontains=query) |
        Q(description__icontains=query)
    )
```

### Example 2: Date-Based Filtering

```python
from datetime import date, timedelta

today = date.today()
last_week = today - timedelta(days=7)
last_month = today - timedelta(days=30)

# Posts that are: new (this week) OR highly liked OR featured
posts = Post.objects.filter(
    Q(created_at__gte=last_week) |
    Q(likes__gt=100) |
    Q(is_featured=True)
)
```

### Example 3: User Permissions

```python
# Content visible to user
def get_visible_content(user):
    if user.is_staff:
        return Content.objects.all()
    
    return Content.objects.filter(
        Q(is_public=True) |  # Public content
        Q(author=user) |      # User's own content
        Q(shared_with=user)   # Shared with user
    )
```

### Example 4: E-commerce Product Filter

```python
def filter_products(
    categories=None,
    min_price=None,
    max_price=None,
    in_stock=None,
    on_sale=None,
    search=None
):
    query = Q()
    
    if categories:
        query &= Q(category__in=categories)
    
    if min_price is not None:
        query &= Q(price__gte=min_price)
    
    if max_price is not None:
        query &= Q(price__lte=max_price)
    
    if in_stock:
        query &= Q(stock__gt=0)
    
    if on_sale:
        query &= Q(discount_price__isnull=False)
    
    if search:
        query &= (
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(tags__name__icontains=search)
        )
    
    return Product.objects.filter(query).distinct()
```

---

## 🔧 Building Dynamic Queries

### Using a List of Conditions

```python
# Build OR query from a list
conditions = [
    Q(status='published'),
    Q(status='featured'),
    Q(status='pinned'),
]

# Combine with OR
from functools import reduce
from operator import or_

query = reduce(or_, conditions)
posts = Post.objects.filter(query)

# Or use a loop
query = Q()
for condition in conditions:
    query |= condition
```

### Conditional Query Building

```python
def search_books(filters):
    query = Q()
    
    if filters.get('title'):
        query &= Q(title__icontains=filters['title'])
    
    if filters.get('author'):
        query &= Q(author__name__icontains=filters['author'])
    
    if filters.get('min_price'):
        query &= Q(price__gte=filters['min_price'])
    
    if filters.get('max_price'):
        query &= Q(price__lte=filters['max_price'])
    
    if filters.get('published_only'):
        query &= Q(is_published=True)
    
    # If no filters, return all
    if not query:
        return Book.objects.all()
    
    return Book.objects.filter(query)
```

---

## 💡 Best Practices

### 1. Use Parentheses for Clarity

```python
# ❌ Confusing - what's the order?
Q(a=1) | Q(b=2) & Q(c=3)

# ✅ Clear - explicit grouping
(Q(a=1) | Q(b=2)) & Q(c=3)  # (a=1 OR b=2) AND c=3
Q(a=1) | (Q(b=2) & Q(c=3))  # a=1 OR (b=2 AND c=3)
```

### 2. Combine with Regular Filters

```python
# Q objects work with regular filter arguments
Book.objects.filter(
    Q(title__icontains='python') | Q(title__icontains='django'),
    is_published=True,  # Regular AND
    price__lt=50         # Regular AND
)
```

### 3. Start with Empty Q for Dynamic Queries

```python
# Start with empty Q()
query = Q()

# Build up the query
if condition1:
    query &= Q(field1=value1)
if condition2:
    query |= Q(field2=value2)

# Empty Q() matches everything if no conditions added
results = Model.objects.filter(query)
```

---

## 📊 Q Object Precedence

Without parentheses, `&` has higher precedence than `|`:

```python
Q(a=1) | Q(b=2) & Q(c=3)
# Is evaluated as:
Q(a=1) | (Q(b=2) & Q(c=3))
# SQL: a = 1 OR (b = 2 AND c = 3)
```

**Always use parentheses to be explicit!**

---

## 🎓 Quick Check

Before moving on, make sure you understand:

- ✅ How to create OR conditions with `|`
- ✅ How to create AND conditions with `&`
- ✅ How to negate conditions with `~`
- ✅ How to combine Q objects with regular filter arguments
- ✅ How to build dynamic queries

---

## 🚀 Next Steps

Now let's learn about **[F Expressions](./02-f-expressions.md)**!

---

*Continue to: [F Expressions →](./02-f-expressions.md)*
