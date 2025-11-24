# Model Relationships 🔗

## Understanding Database Relationships

In relational databases, tables can be connected to each other. Django's ORM makes working with these relationships elegant and Pythonic.

---

## 📊 Three Types of Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                    RELATIONSHIPS                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ONE-TO-MANY (ForeignKey)                                   │
│  One author → Many books                                    │
│  [Author] ←──────── [Book] [Book] [Book]                   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ONE-TO-ONE (OneToOneField)                                 │
│  One user → One profile                                     │
│  [User] ←──────── [Profile]                                │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  MANY-TO-MANY (ManyToManyField)                            │
│  Many books ↔ Many tags                                     │
│  [Book]    ↔    [Tag]                                       │
│  [Book]    ↔    [Tag]                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ One-to-Many: ForeignKey

**Use when:** One record in a table can be related to many records in another table.

**Examples:**
- One Author → Many Books
- One Category → Many Products
- One User → Many Posts

### Defining ForeignKey

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,  # What happens when author is deleted
        related_name='books'       # How to access books from author
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.title
```

### Working with ForeignKey

```python
# Create an author
author = Author.objects.create(name='John Doe', email='john@example.com')

# Create books for this author
book1 = Book.objects.create(title='Book One', author=author, price=29.99)
book2 = Book.objects.create(title='Book Two', author=author, price=39.99)

# Access author from book (forward relation)
print(book1.author.name)  # 'John Doe'

# Access books from author (reverse relation using related_name)
print(author.books.all())  # <QuerySet [<Book: Book One>, <Book: Book Two>]>

# Count author's books
print(author.books.count())  # 2

# Filter books
cheap_books = author.books.filter(price__lt=35)
```

### on_delete Options

| Option | Description |
|--------|-------------|
| `CASCADE` | Delete related objects too |
| `PROTECT` | Prevent deletion if related objects exist |
| `SET_NULL` | Set to NULL (requires `null=True`) |
| `SET_DEFAULT` | Set to default value |
| `DO_NOTHING` | Do nothing (not recommended) |

```python
# Examples
class Book(models.Model):
    # When author is deleted, delete all their books
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    # When category is deleted, set to NULL
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    # Prevent deletion if books exist
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT)
```

---

## 2️⃣ One-to-One: OneToOneField

**Use when:** One record in a table has exactly one related record in another table.

**Examples:**
- One User → One Profile
- One Order → One ShippingAddress
- One Employee → One Desk

### Defining OneToOneField

```python
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
```

### Working with OneToOneField

```python
# Create user and profile
user = User.objects.create_user('john', 'john@example.com', 'password')
profile = Profile.objects.create(user=user, bio='Hello World!')

# Access profile from user
print(user.profile.bio)  # 'Hello World!'

# Access user from profile
print(profile.user.username)  # 'john'
```

---

## 3️⃣ Many-to-Many: ManyToManyField

**Use when:** Records in both tables can be related to multiple records in each other.

**Examples:**
- Books ↔ Tags
- Students ↔ Courses
- Articles ↔ Categories

### Defining ManyToManyField

```python
class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(
        Tag,
        related_name='books',
        blank=True  # Allow books without tags
    )
    
    def __str__(self):
        return self.title
```

### Working with ManyToManyField

```python
# Create tags
python = Tag.objects.create(name='Python')
django = Tag.objects.create(name='Django')
web = Tag.objects.create(name='Web Development')

# Create a book
book = Book.objects.create(title='Django for Beginners')

# Add tags to book
book.tags.add(python, django)  # Add multiple at once
book.tags.add(web)             # Add one

# Remove tags
book.tags.remove(web)

# Set all tags at once (replaces existing)
book.tags.set([python, django])

# Clear all tags
book.tags.clear()

# Get all tags for a book
print(book.tags.all())  # <QuerySet [<Tag: Python>, <Tag: Django>]>

# Get all books for a tag
print(python.books.all())  # <QuerySet [<Book: Django for Beginners>]>

# Check if tag exists
if python in book.tags.all():
    print("Book is tagged with Python")
```

### Many-to-Many with Extra Fields (Through Model)

Sometimes you need extra data about the relationship:

```python
class Student(models.Model):
    name = models.CharField(max_length=100)


class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(
        Student,
        through='Enrollment',  # Use custom through model
        related_name='courses'
    )


class Enrollment(models.Model):
    """Through model with extra fields"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=2, blank=True)
    
    class Meta:
        unique_together = ['student', 'course']


# Usage
student = Student.objects.create(name='Alice')
course = Course.objects.create(name='Python 101')

# Create enrollment with extra data
enrollment = Enrollment.objects.create(
    student=student,
    course=course,
    grade='A'
)

# Access the relationship
print(student.courses.all())
print(course.students.all())

# Access enrollment data
enrollment = Enrollment.objects.get(student=student, course=course)
print(enrollment.grade)  # 'A'
```

---

## 🔄 Related Queries

### Forward Relations (Book → Author)

```python
# Get author from book
book = Book.objects.get(pk=1)
author = book.author

# Filter books by author attribute
books = Book.objects.filter(author__name='John Doe')
books = Book.objects.filter(author__email__contains='example.com')
```

### Reverse Relations (Author → Books)

```python
# Using related_name
author = Author.objects.get(pk=1)
books = author.books.all()

# Filter authors by book attribute
authors = Author.objects.filter(books__price__lt=30)
authors = Author.objects.filter(books__title__icontains='python')
```

### Spanning Relationships

```python
# Get all tags for books by a specific author
tags = Tag.objects.filter(books__author__name='John Doe').distinct()

# Get all authors who have written books with a specific tag
authors = Author.objects.filter(books__tags__name='Python').distinct()
```

---

## ⚡ Performance: select_related vs prefetch_related

### The N+1 Problem

```python
# ❌ Bad - N+1 queries!
books = Book.objects.all()
for book in books:
    print(book.author.name)  # Each iteration hits database!
```

### select_related (for ForeignKey/OneToOne)

```python
# ✅ Good - Single query with JOIN
books = Book.objects.select_related('author').all()
for book in books:
    print(book.author.name)  # No additional query!

# Multiple levels
books = Book.objects.select_related('author', 'publisher', 'category')

# Nested relationships
comments = Comment.objects.select_related('post__author')
```

### prefetch_related (for ManyToMany/Reverse ForeignKey)

```python
# ✅ Good - Two queries (one for books, one for tags)
books = Book.objects.prefetch_related('tags').all()
for book in books:
    print(book.tags.all())  # Uses cached data!

# Multiple prefetches
authors = Author.objects.prefetch_related('books', 'books__tags')
```

---

## 📝 Summary Table

| Relationship | Field Type | Example | Use When |
|--------------|------------|---------|----------|
| One-to-Many | `ForeignKey` | Author → Books | One parent, many children |
| One-to-One | `OneToOneField` | User → Profile | Exactly one related record |
| Many-to-Many | `ManyToManyField` | Books ↔ Tags | Many-to-many connections |

---

## 🎓 Quick Check

Before moving on, make sure you understand:

- ✅ When to use ForeignKey vs OneToOneField vs ManyToManyField
- ✅ How `on_delete` options work
- ✅ How to use `related_name` for reverse relations
- ✅ How to add/remove ManyToMany relationships
- ✅ When to use `select_related` vs `prefetch_related`

---

## 🚀 Next Steps

Now let's learn about **[Filtering and Lookups](./03-filtering.md)**!

---

*Continue to: [Filtering and Lookups →](./03-filtering.md)*
