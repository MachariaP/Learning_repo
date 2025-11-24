# Django ORM Quiz 📝

Test your understanding of Django ORM with these questions!

---

## 🔰 Level 1: Basics

### Question 1
What is an ORM and why is it useful?

<details>
<summary>Show Answer</summary>

ORM (Object-Relational Mapping) is a technique that lets you interact with your database using Python code instead of SQL. Benefits include:

- **Pythonic syntax** - Write Python, not SQL
- **Database-agnostic** - Switch databases without code changes
- **Security** - Built-in protection against SQL injection
- **Productivity** - Less code to write and maintain
- **Type safety** - Python objects with proper types

</details>

---

### Question 2
What's the difference between `filter()` and `get()`?

<details>
<summary>Show Answer</summary>

- **`filter()`**: Returns a QuerySet (potentially empty) of all matching records
- **`get()`**: Returns a single object and raises exceptions if 0 or multiple found

```python
# filter() - returns QuerySet
books = Book.objects.filter(author='John')  # Could be 0, 1, or many

# get() - returns single object
book = Book.objects.get(pk=1)  # Exactly 1, or raises exception
```

`get()` raises:
- `DoesNotExist` if no match
- `MultipleObjectsReturned` if multiple matches

</details>

---

### Question 3
What does this code do? What's the problem with it?

```python
book = Book.objects.filter(pk=999)[0]
```

<details>
<summary>Show Answer</summary>

It tries to get the first book with pk=999. 

**Problem**: It raises `IndexError` if no book exists with that pk.

**Better approaches:**
```python
# Option 1: first() returns None if not found
book = Book.objects.filter(pk=999).first()

# Option 2: get() with try/except
try:
    book = Book.objects.get(pk=999)
except Book.DoesNotExist:
    book = None
```

</details>

---

### Question 4
When are QuerySets evaluated (when do they hit the database)?

<details>
<summary>Show Answer</summary>

QuerySets are **lazy** - they don't hit the database until evaluated. Evaluation happens when:

- **Iteration**: `for book in books:`
- **Slicing with step**: `books[::2]`
- **len()**: `len(books)`
- **list()**: `list(books)`
- **bool()**: `if books:`
- **repr()**: `print(books)`
- **Indexing**: `books[0]`

```python
# This does NOT query the database
books = Book.objects.filter(price__lt=30)

# THIS queries the database
for book in books:  # Evaluation happens here
    print(book.title)
```

</details>

---

## 📊 Level 2: Intermediate

### Question 5
What's the N+1 problem and how do you fix it?

<details>
<summary>Show Answer</summary>

**N+1 Problem**: When accessing related objects in a loop, Django makes 1 query for the main objects, then N additional queries for each related object.

```python
# ❌ N+1 Problem - 101 queries for 100 books!
books = Book.objects.all()  # 1 query
for book in books:
    print(book.author.name)  # 1 query per book (100 queries)
```

**Solutions:**

1. **select_related()** for ForeignKey/OneToOne:
```python
books = Book.objects.select_related('author').all()  # 1 query
```

2. **prefetch_related()** for ManyToMany/Reverse FK:
```python
books = Book.objects.prefetch_related('tags').all()  # 2 queries
```

</details>

---

### Question 6
What's the difference between `select_related()` and `prefetch_related()`?

<details>
<summary>Show Answer</summary>

| Feature | select_related | prefetch_related |
|---------|---------------|------------------|
| SQL | JOIN in single query | Separate query |
| Relationship | ForeignKey, OneToOne | ManyToMany, Reverse FK |
| Memory | Loads in one go | Two separate loads |

```python
# select_related - Single query with JOIN
books = Book.objects.select_related('author')
# SQL: SELECT * FROM books JOIN authors ON ...

# prefetch_related - Separate query
authors = Author.objects.prefetch_related('books')
# SQL 1: SELECT * FROM authors
# SQL 2: SELECT * FROM books WHERE author_id IN (...)
```

</details>

---

### Question 7
How do you perform an OR query in Django?

<details>
<summary>Show Answer</summary>

Use Q objects with the `|` operator:

```python
from django.db.models import Q

# OR query
books = Book.objects.filter(
    Q(author='John') | Q(author='Jane')
)

# More complex
books = Book.objects.filter(
    Q(status='published') & (Q(price__lt=20) | Q(is_featured=True))
)
```

Regular `filter()` only supports AND:
```python
# This is AND
Book.objects.filter(author='John', price__lt=30)
```

</details>

---

### Question 8
What's the difference between `annotate()` and `aggregate()`?

<details>
<summary>Show Answer</summary>

- **`aggregate()`**: Returns a single dictionary with calculated values across all records
- **`annotate()`**: Adds calculated fields to each object in the QuerySet

```python
from django.db.models import Count, Avg

# aggregate() - Single result
result = Book.objects.aggregate(
    total=Count('id'),
    avg_price=Avg('price')
)
# {'total': 100, 'avg_price': 34.99}

# annotate() - Value per object
authors = Author.objects.annotate(
    book_count=Count('books')
)
for author in authors:
    print(f"{author.name}: {author.book_count}")
```

</details>

---

## 🚀 Level 3: Advanced

### Question 9
What are F expressions and when should you use them?

<details>
<summary>Show Answer</summary>

F expressions reference database field values directly without loading them into Python. Use them for:

1. **Atomic updates** (avoid race conditions):
```python
# ❌ Race condition possible
product.stock = product.stock - 1
product.save()

# ✅ Atomic
Product.objects.filter(pk=1).update(stock=F('stock') - 1)
```

2. **Comparing fields**:
```python
# Products where discount_price < price
on_sale = Product.objects.filter(discount_price__lt=F('price'))
```

3. **Efficient updates**:
```python
# 10% discount on all products
Product.objects.update(price=F('price') * 0.9)
```

</details>

---

### Question 10
What's wrong with this code?

```python
from django.db.models import F

book = Book.objects.get(pk=1)
book.view_count = F('view_count') + 1
book.save()
print(f"Views: {book.view_count}")
```

<details>
<summary>Show Answer</summary>

After `save()` with F expression, the field contains the F object, not the actual value!

```python
print(book.view_count)  # Prints: F(view_count) + 1
```

**Solution**: Refresh from database:
```python
book.refresh_from_db()
print(book.view_count)  # Now prints actual value: 101
```

**Better approach**: Use `update()`:
```python
Book.objects.filter(pk=1).update(view_count=F('view_count') + 1)
# Then get fresh object if needed
book = Book.objects.get(pk=1)
```

</details>

---

### Question 11
How do you create a conditional count?

<details>
<summary>Show Answer</summary>

Use `filter` argument (Django 2.0+) or Case/When:

```python
from django.db.models import Count, Q, Case, When

# Method 1: filter argument (preferred)
stats = Order.objects.aggregate(
    total=Count('id'),
    pending=Count('id', filter=Q(status='pending')),
    completed=Count('id', filter=Q(status='completed'))
)

# Method 2: Case/When
stats = Order.objects.aggregate(
    pending=Count(Case(When(status='pending', then=1))),
    completed=Count(Case(When(status='completed', then=1)))
)
```

</details>

---

### Question 12
How do you use Subqueries?

<details>
<summary>Show Answer</summary>

Use `Subquery` and `OuterRef`:

```python
from django.db.models import Subquery, OuterRef

# Get latest order for each customer
latest_orders = Order.objects.filter(
    customer=OuterRef('pk')
).order_by('-created_at')

customers = Customer.objects.annotate(
    last_order_date=Subquery(latest_orders.values('created_at')[:1])
)

# Check existence with Exists
from django.db.models import Exists

recent_orders = Order.objects.filter(
    customer=OuterRef('pk'),
    created_at__gte=last_month
)

customers = Customer.objects.annotate(
    has_recent_order=Exists(recent_orders)
)
```

</details>

---

### Question 13
When should you use raw SQL vs the ORM?

<details>
<summary>Show Answer</summary>

**Use ORM when:**
- Standard CRUD operations
- Filtering, ordering, pagination
- Aggregations and annotations
- Cross-database compatibility needed

**Use Raw SQL when:**
- Database-specific features (full-text search, array operations)
- Complex queries ORM can't express
- Performance-critical operations
- Legacy database integration

**Raw SQL Options:**
```python
# Returns model instances
Book.objects.raw('SELECT * FROM books WHERE ...')

# Returns raw data
with connection.cursor() as cursor:
    cursor.execute('SELECT ...')
    rows = cursor.fetchall()
```

⚠️ **Always use parameterized queries to prevent SQL injection!**

</details>

---

### Question 14
How do you optimize a view that displays books with authors, categories, and tags?

<details>
<summary>Show Answer</summary>

```python
def book_list(request):
    books = (
        Book.objects
        # ForeignKey relations - use select_related
        .select_related('author', 'category')
        # ManyToMany - use prefetch_related
        .prefetch_related('tags')
        # Only load needed fields
        .only('title', 'slug', 'price', 'author__name', 'category__name')
        # Filter early
        .filter(status='published')
        # Order for consistent results
        .order_by('-published_date')
    )
    
    # Paginate to limit results
    paginator = Paginator(books, 20)
    page = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'books/list.html', {'page': page})
```

This results in only 2 queries regardless of how many books are displayed.

</details>

---

## 📊 Score Yourself

| Score | Level |
|-------|-------|
| 0-4 | Beginner - Review the basics |
| 5-8 | Intermediate - Good foundation! |
| 9-11 | Advanced - Excellent understanding |
| 12-14 | Expert - You really know the ORM! |

---

*Return to: [ORM Overview →](./README.md)*
