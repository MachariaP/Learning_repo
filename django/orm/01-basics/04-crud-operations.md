# Basic CRUD Operations 🔧

CRUD stands for **Create, Read, Update, Delete** - the four basic operations you can perform on data.

---

## 📋 Setup: Our Example Model

We'll use this model for all examples:

```python
# models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pages = models.IntegerField()
    is_published = models.BooleanField(default=False)
    published_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title
```

---

## ➕ CREATE - Adding New Records

### Method 1: create() - One Step

```python
# Create and save in one step
book = Book.objects.create(
    title='Django for Beginners',
    author='John Doe',
    price=29.99,
    pages=300
)

print(book.id)  # Auto-assigned ID
# Output: 1
```

### Method 2: Instantiate + save() - Two Steps

```python
# Step 1: Create object in memory
book = Book(
    title='Python Crash Course',
    author='Jane Smith',
    price=39.99,
    pages=450
)

# Step 2: Save to database
book.save()

print(book.id)  # ID assigned after save
# Output: 2
```

### Method 3: Saving with setattr

```python
book = Book()
book.title = 'Learning Python'
book.author = 'Mark Johnson'
book.price = 34.99
book.pages = 500
book.save()
```

### Bulk Create - Multiple Records

```python
# Create multiple records efficiently
books = [
    Book(title='Book 1', author='Author 1', price=19.99, pages=200),
    Book(title='Book 2', author='Author 2', price=24.99, pages=250),
    Book(title='Book 3', author='Author 3', price=29.99, pages=300),
]

# Save all at once (single query!)
Book.objects.bulk_create(books)
```

---

## 📖 READ - Retrieving Records

### Get All Records

```python
# Get all books
all_books = Book.objects.all()

# This returns a QuerySet
print(all_books)
# <QuerySet [<Book: Django for Beginners>, <Book: Python Crash Course>, ...]>

# Iterate over results
for book in all_books:
    print(f"{book.title} - ${book.price}")
```

### Get Single Record by ID

```python
# Get book with id=1
book = Book.objects.get(id=1)
print(book.title)
# Output: 'Django for Beginners'

# Alternative: using pk (primary key)
book = Book.objects.get(pk=1)
```

### Get Single Record by Field

```python
# Get book by title (must be unique or raises error!)
book = Book.objects.get(title='Django for Beginners')

# Get book by multiple fields
book = Book.objects.get(title='Django for Beginners', author='John Doe')
```

⚠️ **Warning:** `get()` raises exceptions:
- `DoesNotExist` - No matching record
- `MultipleObjectsReturned` - More than one match

### Filter Records

```python
# Get books under $30
cheap_books = Book.objects.filter(price__lt=30)

# Get books by specific author
john_books = Book.objects.filter(author='John Doe')

# Get published books
published = Book.objects.filter(is_published=True)
```

### Get First/Last Record

```python
# First record
first_book = Book.objects.first()

# Last record
last_book = Book.objects.last()

# First matching filter
first_cheap = Book.objects.filter(price__lt=30).first()
```

### Check if Records Exist

```python
# Check if any books exist
has_books = Book.objects.exists()  # True/False

# Check if filtered records exist
has_cheap_books = Book.objects.filter(price__lt=20).exists()
```

### Count Records

```python
# Count all books
total = Book.objects.count()
print(f"Total books: {total}")

# Count filtered records
cheap_count = Book.objects.filter(price__lt=30).count()
```

### Order Records

```python
# Order by price (ascending)
books = Book.objects.order_by('price')

# Order by price (descending)
books = Book.objects.order_by('-price')

# Order by multiple fields
books = Book.objects.order_by('author', '-price')
```

### Limit Records (Slicing)

```python
# First 5 books
first_five = Book.objects.all()[:5]

# Books 5-10
middle_books = Book.objects.all()[5:10]

# Top 3 most expensive
top_3 = Book.objects.order_by('-price')[:3]
```

### Select Specific Fields

```python
# Get only title and price (returns dictionaries)
books = Book.objects.values('title', 'price')
# <QuerySet [{'title': 'Django...', 'price': Decimal('29.99')}, ...]>

# Get only titles (returns tuples)
titles = Book.objects.values_list('title')
# <QuerySet [('Django...',), ('Python...',), ...]>

# Get flat list of titles
titles = Book.objects.values_list('title', flat=True)
# <QuerySet ['Django...', 'Python...', ...]>
```

---

## ✏️ UPDATE - Modifying Records

### Update Single Record

```python
# Get the book
book = Book.objects.get(pk=1)

# Modify fields
book.price = 24.99
book.is_published = True

# Save changes
book.save()
```

### Update Specific Fields Only

```python
book = Book.objects.get(pk=1)
book.price = 19.99
book.save(update_fields=['price'])  # Only updates price field
```

### Update Multiple Records (Bulk Update)

```python
# Update all books by John Doe to be published
Book.objects.filter(author='John Doe').update(is_published=True)

# Increase all prices by 5
from django.db.models import F
Book.objects.all().update(price=F('price') + 5)
```

### Get or Create

```python
# Get existing or create new
book, created = Book.objects.get_or_create(
    title='New Book',
    defaults={
        'author': 'Unknown',
        'price': 9.99,
        'pages': 100
    }
)

if created:
    print("New book was created")
else:
    print("Existing book was found")
```

### Update or Create

```python
# Update if exists, create if not
book, created = Book.objects.update_or_create(
    title='Django Guide',
    defaults={
        'author': 'Django Team',
        'price': 49.99,
        'pages': 600
    }
)
```

---

## 🗑️ DELETE - Removing Records

### Delete Single Record

```python
# Get and delete
book = Book.objects.get(pk=1)
book.delete()

# Returns tuple: (number deleted, {model: count})
# (1, {'myapp.Book': 1})
```

### Delete Multiple Records

```python
# Delete all books under $20
Book.objects.filter(price__lt=20).delete()

# Delete all books by author
Book.objects.filter(author='John Doe').delete()
```

### Delete All Records

```python
# Delete everything (careful!)
Book.objects.all().delete()
```

---

## 📊 CRUD Summary Table

| Operation | Method | Example |
|-----------|--------|---------|
| **Create** | `create()` | `Book.objects.create(title='New')` |
| **Create** | `save()` | `book.save()` |
| **Create** | `bulk_create()` | `Book.objects.bulk_create(books)` |
| **Read** | `all()` | `Book.objects.all()` |
| **Read** | `get()` | `Book.objects.get(pk=1)` |
| **Read** | `filter()` | `Book.objects.filter(price__lt=30)` |
| **Read** | `first()` | `Book.objects.first()` |
| **Read** | `count()` | `Book.objects.count()` |
| **Update** | `save()` | `book.price = 20; book.save()` |
| **Update** | `update()` | `Book.objects.filter(...).update(price=20)` |
| **Delete** | `delete()` | `book.delete()` |
| **Delete** | `delete()` | `Book.objects.filter(...).delete()` |

---

## 💻 Complete Example Session

```python
# Django shell: python manage.py shell

>>> from myapp.models import Book
>>> from datetime import date

# CREATE
>>> book1 = Book.objects.create(
...     title='Django Unleashed',
...     author='Andrew Pinkham',
...     price=49.99,
...     pages=840
... )
>>> print(f"Created: {book1.title} (ID: {book1.id})")
Created: Django Unleashed (ID: 1)

# READ
>>> all_books = Book.objects.all()
>>> print(f"Total books: {all_books.count()}")
Total books: 1

>>> book = Book.objects.get(pk=1)
>>> print(f"Found: {book.title} by {book.author}")
Found: Django Unleashed by Andrew Pinkham

# UPDATE
>>> book.price = 44.99
>>> book.is_published = True
>>> book.published_date = date.today()
>>> book.save()
>>> print(f"Updated price: ${book.price}")
Updated price: $44.99

# DELETE
>>> book.delete()
(1, {'myapp.Book': 1})
>>> print(f"Books remaining: {Book.objects.count()}")
Books remaining: 0
```

---

## ⚠️ Common Pitfalls

### 1. Using get() Without Try/Except

```python
# ❌ Bad - Will crash if not found
book = Book.objects.get(pk=999)

# ✅ Good - Handle the exception
try:
    book = Book.objects.get(pk=999)
except Book.DoesNotExist:
    book = None

# ✅ Better - Use first() which returns None
book = Book.objects.filter(pk=999).first()
```

### 2. Forgetting to Save

```python
# ❌ Bad - Changes not saved!
book = Book.objects.get(pk=1)
book.price = 19.99
# Forgot book.save()!

# ✅ Good
book = Book.objects.get(pk=1)
book.price = 19.99
book.save()  # Don't forget this!
```

### 3. Inefficient Bulk Updates

```python
# ❌ Bad - N+1 queries
for book in Book.objects.filter(author='John'):
    book.is_published = True
    book.save()  # One query per book!

# ✅ Good - Single query
Book.objects.filter(author='John').update(is_published=True)
```

---

## 🎓 Quick Check

Before moving on, make sure you can:

- ✅ Create records using `create()` and `save()`
- ✅ Retrieve records using `all()`, `get()`, `filter()`, `first()`
- ✅ Update records using `save()` and `update()`
- ✅ Delete records using `delete()`
- ✅ Handle `DoesNotExist` exceptions

---

## 🚀 Next Steps

Now let's learn about **[QuerySets](../02-intermediate/01-querysets.md)** in detail!

---

*Continue to: [QuerySet Basics →](../02-intermediate/01-querysets.md)*
