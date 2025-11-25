# Filtering and Lookups 🔍

## What are Field Lookups?

Field lookups are how you specify the conditions for WHERE clauses. They're written as keyword arguments with double underscores (`__`).

```python
# Basic syntax: field__lookup=value
Book.objects.filter(price__lt=30)  # WHERE price < 30
```

---

## 📊 Lookup Types Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FIELD LOOKUPS                             │
├──────────────────────────┬──────────────────────────────────┤
│  Comparison              │  exact, gt, gte, lt, lte         │
│  String                  │  contains, startswith, endswith  │
│  Case-insensitive        │  iexact, icontains, istartswith  │
│  List/Range              │  in, range                        │
│  NULL                    │  isnull                           │
│  Date/Time               │  year, month, day, date           │
│  Regex                   │  regex, iregex                    │
└──────────────────────────┴──────────────────────────────────┘
```

---

## 🔢 Comparison Lookups

### exact - Exact Match (Default)

```python
# These are equivalent
Book.objects.filter(title='Django Guide')
Book.objects.filter(title__exact='Django Guide')
```

### gt / gte - Greater Than

```python
# Greater than
expensive_books = Book.objects.filter(price__gt=50)
# WHERE price > 50

# Greater than or equal
medium_books = Book.objects.filter(price__gte=30)
# WHERE price >= 30
```

### lt / lte - Less Than

```python
# Less than
cheap_books = Book.objects.filter(price__lt=20)
# WHERE price < 20

# Less than or equal
affordable = Book.objects.filter(price__lte=25)
# WHERE price <= 25
```

### Combined Comparisons

```python
# Price between 20 and 50
mid_range = Book.objects.filter(price__gte=20, price__lte=50)
# WHERE price >= 20 AND price <= 50
```

---

## 📝 String Lookups

### contains / icontains - Substring Search

```python
# Case-sensitive
python_books = Book.objects.filter(title__contains='Python')
# WHERE title LIKE '%Python%'

# Case-insensitive (recommended)
python_books = Book.objects.filter(title__icontains='python')
# WHERE LOWER(title) LIKE '%python%'
```

### startswith / istartswith - Starts With

```python
# Case-sensitive
books = Book.objects.filter(title__startswith='The')
# WHERE title LIKE 'The%'

# Case-insensitive
books = Book.objects.filter(title__istartswith='the')
```

### endswith / iendswith - Ends With

```python
# Case-sensitive
guides = Book.objects.filter(title__endswith='Guide')
# WHERE title LIKE '%Guide'

# Case-insensitive
guides = Book.objects.filter(title__iendswith='guide')
```

### iexact - Case-insensitive Exact

```python
# Matches 'DJANGO', 'Django', 'django', etc.
book = Book.objects.filter(title__iexact='django guide')
```

---

## 📋 List and Range Lookups

### in - Match Any in List

```python
# Match any of these IDs
books = Book.objects.filter(id__in=[1, 3, 5, 7])
# WHERE id IN (1, 3, 5, 7)

# Match any of these titles
favorites = Book.objects.filter(title__in=['Book A', 'Book B', 'Book C'])

# Using a queryset
author_ids = Author.objects.filter(is_active=True).values_list('id', flat=True)
books = Book.objects.filter(author_id__in=author_ids)
```

### range - Between Two Values

```python
# Price between 20 and 50 (inclusive)
books = Book.objects.filter(price__range=(20, 50))
# WHERE price BETWEEN 20 AND 50

# Date range
from datetime import date
books = Book.objects.filter(
    published_date__range=(date(2023, 1, 1), date(2023, 12, 31))
)
```

---

## 📅 Date and Time Lookups

### Date Component Lookups

```python
# Filter by year
books_2023 = Book.objects.filter(published_date__year=2023)

# Filter by month
january_books = Book.objects.filter(published_date__month=1)

# Filter by day
first_of_month = Book.objects.filter(published_date__day=1)

# Filter by week day (1=Sunday, 7=Saturday)
weekend_published = Book.objects.filter(published_date__week_day__in=[1, 7])
```

### DateTime Specific Lookups

```python
# Filter by hour
morning_posts = Post.objects.filter(created_at__hour__lt=12)

# Filter by minute
on_the_hour = Post.objects.filter(created_at__minute=0)

# Filter by date part of datetime
today_posts = Post.objects.filter(created_at__date=date.today())
```

### Combining Date Lookups

```python
# All books published in January 2023
books = Book.objects.filter(
    published_date__year=2023,
    published_date__month=1
)

# Books published in Q1 2023
q1_books = Book.objects.filter(
    published_date__year=2023,
    published_date__month__in=[1, 2, 3]
)
```

---

## ❓ NULL Lookups

### isnull - Check for NULL

```python
# Books with no published date
unpublished = Book.objects.filter(published_date__isnull=True)
# WHERE published_date IS NULL

# Books that are published
published = Book.objects.filter(published_date__isnull=False)
# WHERE published_date IS NOT NULL
```

---

## 🔄 Related Field Lookups

### Spanning Relationships

```python
# Books by author name
books = Book.objects.filter(author__name='John Doe')
# JOIN with author table

# Books by author's email domain
books = Book.objects.filter(author__email__endswith='gmail.com')

# Deep nesting
comments = Comment.objects.filter(
    post__author__profile__is_verified=True
)
```

### Reverse Relationship Lookups

```python
# Authors who have written at least one book under $20
cheap_authors = Author.objects.filter(books__price__lt=20)

# Authors with published books
published_authors = Author.objects.filter(books__is_published=True)

# Use distinct() to avoid duplicates
published_authors = Author.objects.filter(books__is_published=True).distinct()
```

---

## 🔧 Advanced Lookups

### regex / iregex - Regular Expression

```python
# Case-sensitive regex
books = Book.objects.filter(title__regex=r'^[A-Z].*\d$')

# Case-insensitive regex
books = Book.objects.filter(title__iregex=r'^the\s')
```

---

## 🔗 Combining Filters

### Multiple Conditions (AND)

```python
# All conditions must be true (AND)
books = Book.objects.filter(
    is_published=True,
    price__lt=30,
    author__name='John Doe'
)
# WHERE is_published = True AND price < 30 AND author.name = 'John Doe'

# Chaining also uses AND
books = (
    Book.objects
    .filter(is_published=True)
    .filter(price__lt=30)
)
```

### Using exclude()

```python
# Published books that aren't expensive
books = (
    Book.objects
    .filter(is_published=True)
    .exclude(price__gt=50)
)
# WHERE is_published = True AND NOT price > 50
```

---

## 📊 Lookup Reference Table

| Lookup | Description | Example | SQL Equivalent |
|--------|-------------|---------|----------------|
| `exact` | Exact match | `title__exact='Django'` | `= 'Django'` |
| `iexact` | Case-insensitive exact | `title__iexact='django'` | `ILIKE 'django'` |
| `contains` | Contains substring | `title__contains='py'` | `LIKE '%py%'` |
| `icontains` | Case-insensitive contains | `title__icontains='py'` | `ILIKE '%py%'` |
| `startswith` | Starts with | `title__startswith='The'` | `LIKE 'The%'` |
| `istartswith` | Case-insensitive starts | `title__istartswith='the'` | `ILIKE 'the%'` |
| `endswith` | Ends with | `title__endswith='Guide'` | `LIKE '%Guide'` |
| `iendswith` | Case-insensitive ends | `title__iendswith='guide'` | `ILIKE '%guide'` |
| `in` | In list | `id__in=[1,2,3]` | `IN (1, 2, 3)` |
| `range` | Between values | `price__range=(10,20)` | `BETWEEN 10 AND 20` |
| `gt` | Greater than | `price__gt=50` | `> 50` |
| `gte` | Greater or equal | `price__gte=50` | `>= 50` |
| `lt` | Less than | `price__lt=50` | `< 50` |
| `lte` | Less or equal | `price__lte=50` | `<= 50` |
| `isnull` | Is NULL | `date__isnull=True` | `IS NULL` |
| `year` | Year of date | `date__year=2023` | `YEAR(date) = 2023` |
| `month` | Month of date | `date__month=1` | `MONTH(date) = 1` |
| `day` | Day of date | `date__day=15` | `DAY(date) = 15` |
| `regex` | Regex match | `title__regex=r'^A'` | `REGEXP '^A'` |
| `iregex` | Case-insensitive regex | `title__iregex=r'^a'` | `REGEXP '^a'` |

---

## 💡 Pro Tips

### 1. Use Case-Insensitive Lookups

```python
# ❌ May miss results
Book.objects.filter(title__contains='Python')

# ✅ Better - catches 'PYTHON', 'python', etc.
Book.objects.filter(title__icontains='python')
```

### 2. Combine with distinct()

```python
# ❌ May have duplicates
authors = Author.objects.filter(books__tags__name='Python')

# ✅ No duplicates
authors = Author.objects.filter(books__tags__name='Python').distinct()
```

### 3. Use exists() for Existence Checks

```python
# ❌ Loads all results just to check
if Book.objects.filter(is_published=True):
    pass

# ✅ Optimized query
if Book.objects.filter(is_published=True).exists():
    pass
```

---

## 🎓 Quick Check

Before moving on, make sure you understand:

- ✅ How to use comparison lookups (gt, lt, gte, lte)
- ✅ How to use string lookups (contains, startswith)
- ✅ How to use date lookups (year, month, day)
- ✅ How to span relationships in lookups
- ✅ The difference between filter() and exclude()

---

## 🚀 Next Steps

Now let's learn about **[Aggregations and Annotations](./04-aggregations.md)**!

---

*Continue to: [Aggregations and Annotations →](./04-aggregations.md)*
