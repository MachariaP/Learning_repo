# Aggregations and Annotations 📊

## Overview

- **Aggregation**: Calculate a single value across a queryset (sum, count, average)
- **Annotation**: Add calculated values to each object in a queryset

---

## 🔢 Aggregation Functions

```python
from django.db.models import Count, Sum, Avg, Max, Min, StdDev, Variance
```

### Basic Aggregation

```python
from django.db.models import Count, Sum, Avg, Max, Min

# Get a single result dictionary
result = Book.objects.aggregate(
    total_books=Count('id'),
    total_pages=Sum('pages'),
    avg_price=Avg('price'),
    max_price=Max('price'),
    min_price=Min('price')
)

print(result)
# {'total_books': 100, 'total_pages': 25000, 'avg_price': 34.99, 
#  'max_price': 99.99, 'min_price': 9.99}
```

### Aggregation Examples

```python
# Count all books
total = Book.objects.aggregate(total=Count('id'))
# {'total': 100}

# Sum of all prices
revenue = Book.objects.aggregate(Sum('price'))
# {'price__sum': Decimal('3499.00')}

# Average price
avg = Book.objects.aggregate(Avg('price'))
# {'price__avg': Decimal('34.99')}

# Min and Max
extremes = Book.objects.aggregate(
    cheapest=Min('price'),
    most_expensive=Max('price')
)
# {'cheapest': Decimal('9.99'), 'most_expensive': Decimal('99.99')}
```

### Aggregation with Filtering

```python
# Average price of published books only
avg_published = Book.objects.filter(is_published=True).aggregate(
    avg_price=Avg('price')
)

# Total pages of books over $30
total_pages = Book.objects.filter(price__gt=30).aggregate(
    pages=Sum('pages')
)
```

---

## 📝 Annotation

Annotation adds calculated fields to each object in the queryset.

### Basic Annotation

```python
from django.db.models import Count, F, Value
from django.db.models.functions import Concat

# Add book count to each author
authors = Author.objects.annotate(
    book_count=Count('books')
)

for author in authors:
    print(f"{author.name}: {author.book_count} books")
# John Doe: 5 books
# Jane Smith: 3 books
```

### Annotation Examples

```python
# Count comments per post
posts = Post.objects.annotate(comment_count=Count('comments'))
for post in posts:
    print(f"{post.title}: {post.comment_count} comments")

# Average rating per product
products = Product.objects.annotate(avg_rating=Avg('reviews__rating'))

# Total sales per product
products = Product.objects.annotate(
    total_sales=Sum('orderitem__quantity')
)

# Multiple annotations
books = Book.objects.annotate(
    review_count=Count('reviews'),
    avg_rating=Avg('reviews__rating'),
    total_sales=Sum('sales__quantity')
)
```

### Filtering on Annotations

```python
# Authors with more than 5 books
prolific_authors = (
    Author.objects
    .annotate(book_count=Count('books'))
    .filter(book_count__gt=5)
)

# Products with average rating above 4
top_products = (
    Product.objects
    .annotate(avg_rating=Avg('reviews__rating'))
    .filter(avg_rating__gte=4)
)

# Posts with no comments
lonely_posts = (
    Post.objects
    .annotate(comment_count=Count('comments'))
    .filter(comment_count=0)
)
```

### Ordering by Annotation

```python
# Most popular authors (by book count)
popular_authors = (
    Author.objects
    .annotate(book_count=Count('books'))
    .order_by('-book_count')
)

# Top-rated products
top_rated = (
    Product.objects
    .annotate(avg_rating=Avg('reviews__rating'))
    .order_by('-avg_rating')
)[:10]
```

---

## 🎯 Conditional Aggregation

Use `Case` and `When` for conditional counting:

```python
from django.db.models import Case, When, IntegerField, Sum

# Count published vs unpublished books
stats = Book.objects.aggregate(
    published=Count(Case(When(is_published=True, then=1))),
    unpublished=Count(Case(When(is_published=False, then=1)))
)
# {'published': 75, 'unpublished': 25}

# Sum of sales by product status
sales_stats = Product.objects.aggregate(
    active_sales=Sum(
        Case(When(is_active=True, then='sales_count'))
    ),
    inactive_sales=Sum(
        Case(When(is_active=False, then='sales_count'))
    )
)
```

### Annotate with Conditions

```python
# Add flags based on conditions
books = Book.objects.annotate(
    price_category=Case(
        When(price__lt=20, then=Value('cheap')),
        When(price__lt=50, then=Value('medium')),
        default=Value('expensive')
    )
)

for book in books:
    print(f"{book.title}: {book.price_category}")
```

---

## 🔗 Aggregation Across Relations

```python
# For each author, count their books and sum total pages
authors = Author.objects.annotate(
    total_books=Count('books'),
    total_pages=Sum('books__pages'),
    avg_book_price=Avg('books__price')
)

# For each category, get statistics
categories = Category.objects.annotate(
    product_count=Count('products'),
    avg_price=Avg('products__price'),
    total_stock=Sum('products__stock')
)

# Deep relation aggregation
stores = Store.objects.annotate(
    total_revenue=Sum('orders__items__price')
)
```

---

## 📊 Grouping with values()

Use `values()` before `annotate()` to group results:

```python
# Count books by author
books_by_author = (
    Book.objects
    .values('author__name')
    .annotate(count=Count('id'))
    .order_by('-count')
)
# [{'author__name': 'John', 'count': 10}, {'author__name': 'Jane', 'count': 5}]

# Average price by category
price_by_category = (
    Book.objects
    .values('category__name')
    .annotate(avg_price=Avg('price'))
)

# Sales by month
from django.db.models.functions import TruncMonth

monthly_sales = (
    Order.objects
    .annotate(month=TruncMonth('created_at'))
    .values('month')
    .annotate(total=Sum('total_amount'))
    .order_by('month')
)
```

---

## 💡 Practical Examples

### E-commerce Dashboard Stats

```python
# Product statistics
from django.db.models import Count, Sum, Avg, F

# Get comprehensive product stats
stats = Product.objects.aggregate(
    total_products=Count('id'),
    total_stock_value=Sum(F('price') * F('stock')),
    avg_price=Avg('price'),
    out_of_stock=Count(Case(When(stock=0, then=1)))
)

# Top selling products with stats
top_products = (
    Product.objects
    .annotate(
        units_sold=Sum('orderitem__quantity'),
        revenue=Sum(F('orderitem__quantity') * F('price')),
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    )
    .filter(units_sold__gt=0)
    .order_by('-revenue')[:10]
)
```

### Blog Statistics

```python
# Author statistics
author_stats = (
    Author.objects
    .annotate(
        posts=Count('posts'),
        total_views=Sum('posts__view_count'),
        total_comments=Count('posts__comments'),
    )
)

# Calculate average comments per post using annotation values
# Note: For avg comments per post, we need total_comments / posts
from django.db.models import FloatField, ExpressionWrapper
from django.db.models.functions import Cast, NullIf

author_stats = (
    Author.objects
    .annotate(
        post_count=Count('posts'),
        comment_count=Count('posts__comments'),
    )
    .annotate(
        avg_comments_per_post=ExpressionWrapper(
            Cast('comment_count', FloatField()) / NullIf('post_count', 0),
            output_field=FloatField()
        )
    )
)

# Popular posts by engagement
from django.db.models import F

popular_posts = (
    Post.objects
    .annotate(
        engagement=F('view_count') + Count('comments') * 10 + Count('likes') * 5
    )
    .order_by('-engagement')[:20]
)
```

---

## 📋 Function Reference

| Function | Description | Example |
|----------|-------------|---------|
| `Count()` | Count records | `Count('id')` |
| `Sum()` | Sum of values | `Sum('price')` |
| `Avg()` | Average value | `Avg('rating')` |
| `Max()` | Maximum value | `Max('price')` |
| `Min()` | Minimum value | `Min('price')` |
| `StdDev()` | Standard deviation | `StdDev('price')` |
| `Variance()` | Variance | `Variance('price')` |

---

## ⚠️ Common Gotchas

### 1. Count Distinct

```python
# ❌ May count duplicates
count = Author.objects.annotate(
    tag_count=Count('books__tags')
).values('name', 'tag_count')

# ✅ Count distinct values
count = Author.objects.annotate(
    tag_count=Count('books__tags', distinct=True)
).values('name', 'tag_count')
```

### 2. NULL Values in Aggregation

```python
# Aggregations ignore NULL by default
# If you want to handle NULLs explicitly:
from django.db.models.functions import Coalesce

avg = Product.objects.aggregate(
    avg_rating=Coalesce(Avg('rating'), 0.0)
)
```

---

## 🎓 Quick Check

Before moving on, make sure you understand:

- ✅ Difference between aggregate() and annotate()
- ✅ How to use Count, Sum, Avg, Min, Max
- ✅ How to filter and order by annotations
- ✅ How to group with values() + annotate()
- ✅ How to use conditional aggregation

---

## 🚀 Next Steps

Now let's learn about **[Q Objects for Complex Queries](../03-advanced/01-q-objects.md)**!

---

*Continue to: [Q Objects →](../03-advanced/01-q-objects.md)*
