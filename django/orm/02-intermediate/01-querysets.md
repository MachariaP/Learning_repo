# QuerySet Basics 📋

## What is a QuerySet?

A **QuerySet** is Django's way of representing a database query. Think of it as a "recipe" for getting data - it describes what you want, but doesn't fetch the data until you actually need it.

---

## 🎯 Key Concept: Lazy Evaluation

QuerySets are **lazy** - they don't hit the database until you explicitly ask for the data.

```python
# This does NOT query the database yet
queryset = Book.objects.filter(price__lt=30)  # Just builds the query

# These actions DO query the database:
list(queryset)         # Converting to list
for book in queryset:  # Iterating
    print(book)
len(queryset)          # Getting length
queryset[0]            # Indexing
bool(queryset)         # Checking if results exist
```

---

## 📊 Visualizing QuerySet Laziness

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR CODE                                 │
│    books = Book.objects.filter(price__lt=30)                │
│                    ↓                                         │
│         [QuerySet Created - No DB Query]                    │
│                    ↓                                         │
│    for book in books:  # NOW the query executes             │
│                    ↓                                         │
│         [Database Query Executed]                           │
│                    ↓                                         │
│    Results cached in QuerySet                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 QuerySet Chaining

One of the most powerful features - chain multiple operations!

```python
# Each method returns a NEW QuerySet
queryset = (
    Book.objects
    .filter(is_published=True)
    .filter(price__lt=50)
    .exclude(author='Anonymous')
    .order_by('-published_date')
    [:10]
)

# Equivalent to one SQL query:
# SELECT * FROM books
# WHERE is_published = True AND price < 50 AND author != 'Anonymous'
# ORDER BY published_date DESC
# LIMIT 10
```

### Chaining Example Breakdown

```python
# Start with all books
all_books = Book.objects.all()

# Filter published books
published = all_books.filter(is_published=True)

# Filter by price
affordable = published.filter(price__lt=30)

# Exclude certain authors
filtered = affordable.exclude(author='Unknown')

# Order by date
ordered = filtered.order_by('-published_date')

# Take first 5
result = ordered[:5]

# All of these are QuerySets!
# The database is only queried when you evaluate the final result
```

---

## 📖 Essential QuerySet Methods

### Returning QuerySets (Chainable)

| Method | Description | Example |
|--------|-------------|---------|
| `all()` | Get all records | `Book.objects.all()` |
| `filter()` | Records matching conditions | `Book.objects.filter(price__lt=30)` |
| `exclude()` | Records NOT matching conditions | `Book.objects.exclude(author='John')` |
| `order_by()` | Sort records | `Book.objects.order_by('-price')` |
| `distinct()` | Remove duplicates | `Book.objects.distinct()` |
| `values()` | Return dictionaries | `Book.objects.values('title', 'price')` |
| `values_list()` | Return tuples | `Book.objects.values_list('title')` |
| `select_related()` | JOIN for ForeignKey | `Book.objects.select_related('author')` |
| `prefetch_related()` | Prefetch M2M | `Book.objects.prefetch_related('tags')` |
| `annotate()` | Add calculated fields | `Book.objects.annotate(...)` |
| `reverse()` | Reverse order | `Book.objects.all().reverse()` |
| `defer()` | Exclude fields | `Book.objects.defer('description')` |
| `only()` | Include only specific fields | `Book.objects.only('title', 'price')` |

### Returning Single Objects

| Method | Description | Raises Exception? |
|--------|-------------|-------------------|
| `get()` | Single record | Yes - DoesNotExist, MultipleObjectsReturned |
| `first()` | First record | No - Returns None |
| `last()` | Last record | No - Returns None |

### Returning Other Values

| Method | Description | Returns |
|--------|-------------|---------|
| `count()` | Number of records | Integer |
| `exists()` | Any records exist? | Boolean |
| `aggregate()` | Calculate on all records | Dictionary |

---

## 💻 Practical Examples

### Basic Filtering

```python
# Get all published books
published_books = Book.objects.filter(is_published=True)

# Get books by price range
mid_range = Book.objects.filter(price__gte=20, price__lte=50)

# Get books from 2023
books_2023 = Book.objects.filter(published_date__year=2023)

# Get books with 'Django' in title
django_books = Book.objects.filter(title__icontains='django')
```

### Combining Filter and Exclude

```python
# Published books that aren't free
paid_books = (
    Book.objects
    .filter(is_published=True)
    .exclude(price=0)
)

# Books not by John or Jane
other_authors = (
    Book.objects
    .exclude(author='John')
    .exclude(author='Jane')
)
```

### Ordering Results

```python
# Newest first
newest = Book.objects.order_by('-published_date')

# Cheapest first
cheapest = Book.objects.order_by('price')

# Multiple ordering
sorted_books = Book.objects.order_by('author', '-published_date')

# Random ordering
random_books = Book.objects.order_by('?')  # Note: Can be slow!
```

### Slicing (LIMIT/OFFSET)

```python
# First 10 books
first_10 = Book.objects.all()[:10]

# Books 20-30
page_3 = Book.objects.all()[20:30]

# Single book by position
third_book = Book.objects.all()[2]  # Note: 0-indexed

# Last 5 books
last_5 = Book.objects.order_by('-id')[:5]
```

### Values and Values List

```python
# Get dictionaries with specific fields
books_data = Book.objects.values('title', 'price')
# <QuerySet [{'title': 'Django', 'price': 29.99}, ...]>

# Get tuples
titles = Book.objects.values_list('title', 'price')
# <QuerySet [('Django', 29.99), ('Python', 39.99), ...]>

# Get flat list (single field only)
all_titles = Book.objects.values_list('title', flat=True)
# <QuerySet ['Django', 'Python', 'JavaScript', ...]>
```

### Distinct Values

```python
# Get unique authors
unique_authors = Book.objects.values_list('author', flat=True).distinct()

# Unique price points
price_points = Book.objects.values_list('price', flat=True).distinct()
```

---

## 🔄 QuerySet Evaluation (When Does the Query Run?)

### Iteration

```python
for book in Book.objects.all():  # Query runs here
    print(book.title)
```

### Slicing with Step

```python
books = Book.objects.all()[::2]  # Query runs (gets every other book)
```

### len()

```python
length = len(Book.objects.all())  # Query runs
# Better: Book.objects.count()  # More efficient
```

### list()

```python
books_list = list(Book.objects.all())  # Query runs
```

### bool()

```python
if Book.objects.filter(is_published=True):  # Query runs
    print("Has published books")
# Better: if Book.objects.filter(is_published=True).exists()
```

### repr() (Printing)

```python
print(Book.objects.all())  # Query runs to show results
```

---

## 🎮 QuerySet Caching

Once a QuerySet is evaluated, results are cached:

```python
# First iteration - hits database
queryset = Book.objects.all()
for book in queryset:  # Database query here
    print(book.title)

# Second iteration - uses cache (no new query!)
for book in queryset:  # Uses cached results
    print(book.price)
```

### When Cache is NOT Used

```python
# Slicing creates a new QuerySet
queryset = Book.objects.all()
first = queryset[0]   # Database query
second = queryset[1]  # Another database query!

# Better: evaluate once, then slice
all_books = list(Book.objects.all())  # One query
first = all_books[0]   # From cache
second = all_books[1]  # From cache
```

---

## 📊 See the Generated SQL

```python
# Print the SQL query
queryset = Book.objects.filter(price__lt=30).order_by('title')
print(queryset.query)

# Output:
# SELECT "myapp_book"."id", "myapp_book"."title", ...
# FROM "myapp_book"
# WHERE "myapp_book"."price" < 30
# ORDER BY "myapp_book"."title" ASC
```

---

## 💡 Best Practices

### 1. Use count() Instead of len()

```python
# ❌ Bad - Loads all records into memory
count = len(Book.objects.all())

# ✅ Good - Just gets the count
count = Book.objects.count()
```

### 2. Use exists() Instead of bool()

```python
# ❌ Bad - Loads at least one record
if Book.objects.filter(is_published=True):
    pass

# ✅ Good - Optimized query
if Book.objects.filter(is_published=True).exists():
    pass
```

### 3. Use first() Instead of [0]

```python
# ❌ Bad - Raises IndexError if empty
book = Book.objects.filter(price__lt=10)[0]

# ✅ Good - Returns None if empty
book = Book.objects.filter(price__lt=10).first()
```

### 4. Chain Filters in Single Statement

```python
# ❌ Less efficient - Multiple QuerySet objects
qs = Book.objects.all()
qs = qs.filter(is_published=True)
qs = qs.filter(price__lt=30)

# ✅ Better - Chain in one expression
qs = Book.objects.filter(is_published=True, price__lt=30)
```

---

## 🎓 Quick Check

Before moving on, make sure you understand:

- ✅ QuerySets are lazy - they don't execute until evaluated
- ✅ QuerySets are chainable - methods return new QuerySets
- ✅ QuerySets cache results after evaluation
- ✅ How to print the SQL query with `.query`
- ✅ When to use `count()`, `exists()`, `first()`

---

## 🚀 Next Steps

Now let's learn about **[Model Relationships](./02-relationships.md)**!

---

*Continue to: [Model Relationships →](./02-relationships.md)*
