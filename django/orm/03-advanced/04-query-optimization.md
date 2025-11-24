# Query Optimization ⚡

## Why Optimize?

Database queries are often the biggest performance bottleneck. A few milliseconds saved per query can mean seconds saved on page load with many queries.

---

## 🔍 The N+1 Problem

The most common Django ORM performance issue:

```python
# ❌ N+1 queries - 1 query for books, N queries for authors!
books = Book.objects.all()  # 1 query

for book in books:
    print(book.author.name)  # 1 query per book! (N queries)

# If you have 100 books, that's 101 queries!
```

---

## 🚀 Solution 1: select_related()

For **ForeignKey** and **OneToOneField** relationships (single-valued):

```python
# ✅ Single query with JOIN
books = Book.objects.select_related('author').all()

for book in books:
    print(book.author.name)  # No additional query!

# SQL: SELECT * FROM books JOIN authors ON books.author_id = authors.id
```

### Multiple Relations

```python
# Multiple select_related
books = Book.objects.select_related('author', 'publisher', 'category')

# Nested relations
comments = Comment.objects.select_related('post__author')
# Gets comment -> post -> author in single query
```

---

## 🚀 Solution 2: prefetch_related()

For **ManyToManyField** and **reverse ForeignKey** relationships (multi-valued):

```python
# ✅ Two queries: one for books, one for tags
books = Book.objects.prefetch_related('tags').all()

for book in books:
    print(book.tags.all())  # No additional query!

# SQL Query 1: SELECT * FROM books
# SQL Query 2: SELECT * FROM tags WHERE id IN (1, 2, 3, ...)
```

### Prefetching Reverse Relations

```python
# Get authors with all their books
authors = Author.objects.prefetch_related('books')

for author in authors:
    print(f"{author.name}: {author.books.count()} books")
```

---

## 🎯 Prefetch Objects for Fine Control

Customize prefetch queries with `Prefetch`:

```python
from django.db.models import Prefetch

# Prefetch only published books
authors = Author.objects.prefetch_related(
    Prefetch('books', queryset=Book.objects.filter(is_published=True))
)

# Prefetch with custom attribute name
authors = Author.objects.prefetch_related(
    Prefetch(
        'books',
        queryset=Book.objects.filter(is_published=True),
        to_attr='published_books'  # Access as author.published_books
    )
)

# Complex prefetch with ordering
authors = Author.objects.prefetch_related(
    Prefetch(
        'books',
        queryset=Book.objects.order_by('-published_date')[:5],
        to_attr='latest_books'
    )
)
```

---

## 📊 Combining select_related and prefetch_related

```python
# Optimal query for complex relations
books = (
    Book.objects
    .select_related('author', 'publisher')  # FK relations
    .prefetch_related('tags', 'reviews')     # M2M and reverse FK
)

# Complex example
posts = (
    Post.objects
    .select_related('author', 'category')
    .prefetch_related(
        'tags',
        'comments',
        Prefetch(
            'comments',
            queryset=Comment.objects.select_related('user').order_by('-created_at')[:10],
            to_attr='recent_comments'
        )
    )
)
```

---

## 🔧 only() and defer()

Load only specific fields:

```python
# Only load specific fields
books = Book.objects.only('title', 'price')
# Other fields loaded on demand (extra query if accessed!)

# Defer specific fields (load everything except these)
books = Book.objects.defer('description', 'content')

# Combine with select_related
books = Book.objects.select_related('author').only(
    'title', 'price', 'author__name'
)
```

---

## 📈 Indexing

### Adding Database Indexes

```python
class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)  # Simple index
    isbn = models.CharField(max_length=13, unique=True)       # Unique = indexed
    
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author', 'published_date']),  # Composite
            models.Index(fields=['-published_date']),  # Descending
        ]
```

### When to Add Indexes

Add indexes for fields you frequently:
- Filter on (`filter()`, `exclude()`)
- Order by (`order_by()`)
- Join on (ForeignKey fields)

---

## 🧪 Measuring Query Performance

### Using Django Debug Toolbar

Install it for development:
```bash
pip install django-debug-toolbar
```

### Logging Queries

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

### Manual Query Counting

```python
from django.db import connection, reset_queries
from django.conf import settings

settings.DEBUG = True
reset_queries()

# Your code here
books = list(Book.objects.all())
for book in books:
    print(book.author.name)

# Check queries
print(f"Queries: {len(connection.queries)}")
for query in connection.queries:
    print(query['sql'])
```

---

## 📊 Pagination

Don't load everything at once:

```python
from django.core.paginator import Paginator

# Paginate results
books = Book.objects.all()
paginator = Paginator(books, 25)  # 25 per page

page = paginator.get_page(1)
for book in page:
    print(book.title)

# In views
def book_list(request):
    books = Book.objects.select_related('author').all()
    paginator = Paginator(books, 25)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'books.html', {'page': page})
```

---

## 💡 Quick Optimization Checklist

| Problem | Solution |
|---------|----------|
| N+1 on ForeignKey | `select_related()` |
| N+1 on ManyToMany | `prefetch_related()` |
| Loading unused fields | `only()` or `defer()` |
| No indexes on filter fields | Add `db_index=True` |
| Loading all results | Pagination |
| Count with len() | Use `count()` |
| Existence check | Use `exists()` |
| Large updates in loop | Use `update()` or `bulk_update()` |

---

## 🎯 Common Patterns

### Efficient List View

```python
def book_list(request):
    books = (
        Book.objects
        .select_related('author', 'publisher')
        .prefetch_related('tags')
        .only('title', 'price', 'slug', 'author__name', 'publisher__name')
        .order_by('-published_date')
    )
    
    paginator = Paginator(books, 20)
    page = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'books/list.html', {'page': page})
```

### Efficient Detail View

```python
def book_detail(request, slug):
    book = (
        Book.objects
        .select_related('author', 'publisher')
        .prefetch_related(
            'tags',
            Prefetch(
                'reviews',
                queryset=Review.objects.select_related('user').order_by('-created_at')[:10]
            )
        )
        .get(slug=slug)
    )
    
    return render(request, 'books/detail.html', {'book': book})
```

---

## 🎓 Quick Check

Before moving on, make sure you understand:

- ✅ What causes the N+1 problem
- ✅ When to use `select_related` vs `prefetch_related`
- ✅ How to use `Prefetch` for custom prefetching
- ✅ When to add database indexes
- ✅ How to measure query performance

---

## 🚀 Next Steps

Now let's learn about **[Raw SQL and Custom Queries](./05-raw-sql.md)**!

---

*Continue to: [Raw SQL →](./05-raw-sql.md)*
