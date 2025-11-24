# What is an ORM? 🤔

## Simple Definition

**ORM (Object-Relational Mapping) is a technique that lets you interact with your database using your programming language instead of SQL.**

Instead of writing SQL queries, you work with Python objects. The ORM translates your Python code into SQL behind the scenes.

---

## 🏢 Real-World Analogy

Imagine you're at a restaurant in a foreign country:

**Without ORM (Direct SQL):**
- You need to speak the local language (SQL)
- You must know the grammar perfectly
- One mistake and you won't get your food

**With ORM:**
- You have a translator (ORM)
- You speak your language (Python)
- The translator handles the communication
- You get your food without learning a new language!

---

## 📊 Visual Comparison

### Without ORM (Raw SQL):
```sql
-- Creating a table
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2),
    published_date DATE
);

-- Inserting data
INSERT INTO books (title, author, price, published_date)
VALUES ('Django for Beginners', 'John Doe', 29.99, '2023-01-15');

-- Querying data
SELECT * FROM books WHERE price < 30.00 ORDER BY title;
```

### With Django ORM (Python):
```python
# Creating a "table" (model)
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published_date = models.DateField()

# Inserting data
Book.objects.create(
    title='Django for Beginners',
    author='John Doe',
    price=29.99,
    published_date='2023-01-15'
)

# Querying data
Book.objects.filter(price__lt=30.00).order_by('title')
```

**Same result, but the Python version is:**
- More readable
- Type-safe
- Protected against SQL injection
- Database-agnostic

---

## 🎯 Why Use an ORM?

### 1. **Write Less Code**

```python
# One line to get all books by a specific author
books = Book.objects.filter(author='John Doe')

# vs SQL:
# cursor.execute("SELECT * FROM books WHERE author = %s", ['John Doe'])
# books = cursor.fetchall()
```

### 2. **Database Agnostic**

Your code works with:
- SQLite (development)
- PostgreSQL (production)
- MySQL
- Oracle

Just change the settings - no code changes needed!

```python
# settings.py - Switch databases easily
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Just change this line!
        'NAME': 'mydatabase',
    }
}
```

### 3. **Security (SQL Injection Protection)**

```python
# SAFE - ORM escapes parameters automatically
Book.objects.filter(title=user_input)

# DANGEROUS - Raw SQL vulnerable to injection
cursor.execute(f"SELECT * FROM books WHERE title = '{user_input}'")
```

### 4. **Pythonic and Readable**

```python
# Clear and intuitive
recent_expensive_books = Book.objects.filter(
    price__gte=50,
    published_date__year=2023
).order_by('-price')[:10]
```

### 5. **Easy Relationships**

```python
# Get all books by an author, including their profile
author = Author.objects.select_related('profile').get(name='John')
books = author.books.all()
```

---

## 🔍 How Django ORM Works

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR PYTHON CODE                          │
│        Book.objects.filter(price__lt=30)                    │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO ORM                                │
│         Translates Python → SQL                              │
│    "SELECT * FROM books WHERE price < 30"                   │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              DATABASE (PostgreSQL/MySQL/etc)                 │
│                   Executes the SQL                           │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO ORM                                │
│          Converts results → Python objects                   │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    YOUR PYTHON CODE                          │
│      [<Book: Django Guide>, <Book: Python Tips>]            │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Quick Example

Let's see the ORM in action:

```python
# models.py - Define your data structure
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
# Django shell - Use your models
>>> from myapp.models import Author, Book

# Create an author
>>> author = Author.objects.create(name='Jane Doe', email='jane@example.com')

# Create a book
>>> book = Book.objects.create(title='Learning Django', author=author, price=39.99)

# Query books
>>> cheap_books = Book.objects.filter(price__lt=50)
>>> print(cheap_books)
<QuerySet [<Book: Learning Django>]>

# Access relationships
>>> book.author.name
'Jane Doe'
```

---

## 💡 Key Concepts to Remember

1. **Model = Table**
   - A Python class represents a database table

2. **Model Instance = Row**
   - An object represents a single row in the table

3. **Field = Column**
   - Model attributes represent table columns

4. **Manager = Query Interface**
   - `Model.objects` is how you query the database

5. **QuerySet = Collection of Results**
   - Queries return QuerySet objects (lazy evaluation!)

---

## ⚠️ Important Notes

- **Lazy Evaluation**: QuerySets don't hit the database until you need the data
- **Migrations**: You must run migrations to sync models with the database
- **The ORM is not magic**: Understanding the SQL it generates helps you write better code

---

## 🎓 Quick Check

Before moving on, make sure you understand:

- ✅ ORM maps Python objects to database tables
- ✅ You write Python, not SQL
- ✅ The ORM translates Python to SQL automatically
- ✅ It works with different databases without code changes
- ✅ It provides built-in security against SQL injection

---

## 🚀 Next Steps

Now that you understand what an ORM is, let's learn about **[Django Models](./02-models.md)**!

---

## 💭 Think About It

**Question**: What are the benefits of using an ORM vs writing raw SQL?

**Hint**: Think about security, portability, and code readability!

---

*Continue to: [Django Models →](./02-models.md)*
