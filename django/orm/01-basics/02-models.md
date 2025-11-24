# Django Models 📋

## What is a Model?

A **model** is a Python class that defines the structure of your data. Each model maps to a single database table.

Think of a model as a blueprint for your data - it tells Django:
- What data you want to store
- What type each piece of data should be
- How different pieces of data relate to each other

---

## 📊 Model = Database Table

```
┌─────────────────────────────────────────────────────────────┐
│                    PYTHON MODEL                              │
│                                                              │
│   class Book(models.Model):                                  │
│       title = models.CharField(max_length=200)               │
│       author = models.CharField(max_length=100)              │
│       price = models.DecimalField(...)                       │
│       published = models.DateField()                         │
│                                                              │
└─────────────────────────────────┬───────────────────────────┘
                                  ↓
                            [Migration]
                                  ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE TABLE                            │
│                                                              │
│   books                                                      │
│   ├── id (auto-created)                                     │
│   ├── title (VARCHAR 200)                                   │
│   ├── author (VARCHAR 100)                                  │
│   ├── price (DECIMAL)                                       │
│   └── published (DATE)                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Creating Your First Model

### Step 1: Define the Model

```python
# myapp/models.py
from django.db import models

class Book(models.Model):
    """A model representing a book in a library"""
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pages = models.IntegerField()
    published_date = models.DateField()
    in_stock = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title
```

### Step 2: Create Migration

```bash
python manage.py makemigrations
```

Output:
```
Migrations for 'myapp':
  myapp/migrations/0001_initial.py
    - Create model Book
```

### Step 3: Apply Migration

```bash
python manage.py migrate
```

Output:
```
Operations to perform:
  Apply all migrations: myapp
Running migrations:
  Applying myapp.0001_initial... OK
```

**Now your database has a `books` table!**

---

## 🔍 Understanding Model Components

### The Class Definition

```python
class Book(models.Model):  # Inherits from models.Model
    # Fields go here
    pass
```

- Every model **must** inherit from `models.Model`
- The class name (Book) becomes the table name (myapp_book)

### The `__str__` Method

```python
def __str__(self):
    return self.title
```

This defines how the object is displayed as text:
```python
>>> book = Book.objects.first()
>>> print(book)
Django for Beginners  # Instead of "Book object (1)"
```

### The Meta Class

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    # ... other fields ...
    
    class Meta:
        ordering = ['-published_date']  # Default ordering
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        db_table = 'library_books'  # Custom table name
```

Common Meta options:
| Option | Description |
|--------|-------------|
| `ordering` | Default sort order |
| `verbose_name` | Human-readable name |
| `verbose_name_plural` | Plural name |
| `db_table` | Custom database table name |
| `unique_together` | Fields that must be unique together |
| `indexes` | Database indexes to create |

---

## 📝 Complete Model Example

```python
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Book category/genre"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Author(models.Model):
    """Author information"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    """Book information"""
    
    # Basic info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    
    # Relationships
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='books'
    )
    
    # Content
    description = models.TextField()
    pages = models.PositiveIntegerField()
    
    # Pricing
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Status
    in_stock = models.BooleanField(default=True)
    stock_count = models.PositiveIntegerField(default=0)
    
    # Dates
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['title']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def is_on_sale(self):
        return self.discount_price is not None
    
    @property
    def current_price(self):
        return self.discount_price if self.is_on_sale else self.price
```

---

## 💡 Model Design Best Practices

### 1. Use Descriptive Field Names

```python
# ❌ Bad
class Book(models.Model):
    n = models.CharField(max_length=200)  # What is 'n'?
    d = models.DateField()

# ✅ Good
class Book(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateField()
```

### 2. Add Help Text

```python
class Book(models.Model):
    isbn = models.CharField(
        max_length=13,
        help_text='13-character ISBN number'
    )
```

### 3. Use Appropriate Field Types

```python
# ❌ Bad - Using CharField for email
email = models.CharField(max_length=100)

# ✅ Good - Using EmailField (includes validation)
email = models.EmailField()
```

### 4. Add the `__str__` Method

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title  # Shows title in admin and shell
```

### 5. Use `related_name` for ForeignKeys

```python
class Book(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'  # Access as author.books.all()
    )
```

---

## 🔄 The Migration Workflow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Edit Model  │ --> │ makemigrations│ --> │   migrate    │
│  (Python)    │     │  (Creates    │     │  (Applies    │
│              │     │   migration) │     │   to DB)     │
└──────────────┘     └──────────────┘     └──────────────┘
```

**Commands:**
```bash
# Create migrations for model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Show migration status
python manage.py showmigrations

# See SQL that would be executed
python manage.py sqlmigrate myapp 0001
```

---

## ⚠️ Common Mistakes

### Mistake 1: Forgetting to Migrate

```bash
# You changed the model but forgot to...
python manage.py makemigrations
python manage.py migrate
```

### Mistake 2: Wrong `on_delete`

```python
# ❌ This will delete all books if author is deleted!
author = models.ForeignKey(Author, on_delete=models.CASCADE)

# ✅ Better options:
# Keep books but set author to NULL
author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

# Prevent deletion if author has books
author = models.ForeignKey(Author, on_delete=models.PROTECT)
```

### Mistake 3: Not Setting `blank` and `null` Correctly

```python
# For optional fields:
description = models.TextField(blank=True)  # Can be empty string
birth_date = models.DateField(null=True, blank=True)  # Can be NULL

# blank = form validation
# null = database NULL
```

---

## 🎓 Quick Check

Before moving on, make sure you understand:

- ✅ A model is a Python class that represents a database table
- ✅ Each attribute (field) becomes a column
- ✅ You must run migrations after changing models
- ✅ The `__str__` method defines how objects display as text
- ✅ The Meta class contains model configuration

---

## 🚀 Next Steps

Now let's learn about **[Model Fields](./03-model-fields.md)** in detail!

---

*Continue to: [Model Fields →](./03-model-fields.md)*
