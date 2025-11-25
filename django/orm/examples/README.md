# Django ORM - Code Examples 💻

This directory contains complete, working examples of Django ORM techniques.

---

## 📁 Examples Overview

### Basic Model Example

```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    tags = models.ManyToManyField(Tag, related_name='books', blank=True)
    
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pages = models.PositiveIntegerField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    
    published_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    view_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1-5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['book', 'user']
    
    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"
```

---

## 🔍 QuerySet Examples

### Basic Queries

```python
# Get all books
all_books = Book.objects.all()

# Get single book
book = Book.objects.get(pk=1)
book = Book.objects.get(slug='django-guide')

# Filter books
published = Book.objects.filter(status='published')
cheap_books = Book.objects.filter(price__lt=30)
recent = Book.objects.filter(published_date__year=2023)

# Exclude
not_draft = Book.objects.exclude(status='draft')

# Chaining
featured_cheap = Book.objects.filter(is_featured=True).filter(price__lt=50)

# Count and exists
count = Book.objects.filter(status='published').count()
has_books = Book.objects.filter(author__name='John').exists()

# First and last
first = Book.objects.first()
last = Book.objects.order_by('-created_at').first()  # Most recent
```

### Filtering Examples

```python
from django.db.models import Q

# Price range
mid_range = Book.objects.filter(price__gte=20, price__lte=50)

# Contains (case-insensitive)
python_books = Book.objects.filter(title__icontains='python')

# Date lookups
this_year = Book.objects.filter(published_date__year=2023)
jan_books = Book.objects.filter(published_date__month=1)

# Related field lookups
author_books = Book.objects.filter(author__name='John Doe')
tagged = Book.objects.filter(tags__name='Django')

# OR queries with Q
search = Book.objects.filter(
    Q(title__icontains='python') | Q(description__icontains='python')
)

# Complex query
results = Book.objects.filter(
    Q(status='published'),
    Q(price__lt=50) | Q(is_featured=True)
)
```

---

## 📊 Aggregation Examples

```python
from django.db.models import Count, Sum, Avg, Max, Min, F

# Basic aggregation
stats = Book.objects.aggregate(
    total=Count('id'),
    avg_price=Avg('price'),
    max_price=Max('price'),
    min_price=Min('price'),
    total_pages=Sum('pages')
)

# Annotation - add calculated fields
authors_with_counts = Author.objects.annotate(
    book_count=Count('books'),
    avg_book_price=Avg('books__price')
)

for author in authors_with_counts:
    print(f"{author.name}: {author.book_count} books")

# Filter on annotation
prolific = Author.objects.annotate(
    book_count=Count('books')
).filter(book_count__gt=5)

# Group by with values
by_category = Book.objects.values('category__name').annotate(
    count=Count('id'),
    avg_price=Avg('price')
)
```

---

## 🔗 Relationship Examples

```python
# Forward relationship (Book -> Author)
book = Book.objects.get(pk=1)
author = book.author
print(author.name)

# Reverse relationship (Author -> Books)
author = Author.objects.get(pk=1)
books = author.books.all()

# ManyToMany
book = Book.objects.get(pk=1)
tags = book.tags.all()

# Add tags
python = Tag.objects.get(name='Python')
book.tags.add(python)

# Remove tags
book.tags.remove(python)

# Set tags
book.tags.set([tag1, tag2, tag3])

# Clear tags
book.tags.clear()
```

---

## ⚡ Optimization Examples

```python
from django.db.models import Prefetch

# Select related for ForeignKey
books = Book.objects.select_related('author', 'category').all()

for book in books:
    print(f"{book.title} by {book.author.name}")  # No extra query!

# Prefetch related for ManyToMany
books = Book.objects.prefetch_related('tags').all()

for book in books:
    print(f"{book.title}: {[t.name for t in book.tags.all()]}")  # No extra query!

# Combined
books = (
    Book.objects
    .select_related('author', 'category')
    .prefetch_related('tags', 'reviews')
)

# Custom prefetch
books = Book.objects.prefetch_related(
    Prefetch(
        'reviews',
        queryset=Review.objects.select_related('user').order_by('-created_at')[:5],
        to_attr='recent_reviews'
    )
)

for book in books:
    for review in book.recent_reviews:
        print(f"{review.user.username}: {review.rating}")
```

---

## 🔄 F Expression Examples

```python
from django.db.models import F

# Increment view count atomically
Book.objects.filter(pk=book_id).update(view_count=F('view_count') + 1)

# Compare fields
on_sale = Book.objects.filter(discount_price__lt=F('price'))

# Update based on another field
Book.objects.all().update(discount_price=F('price') * 0.9)

# Annotation with F
from django.db.models import ExpressionWrapper, DecimalField

books = Book.objects.annotate(
    price_per_page=ExpressionWrapper(
        F('price') / F('pages'),
        output_field=DecimalField(max_digits=10, decimal_places=4)
    )
)
```

---

## 🎯 Conditional Examples

```python
from django.db.models import Case, When, Value, CharField

# Categorize books by price
books = Book.objects.annotate(
    price_tier=Case(
        When(price__lt=20, then=Value('budget')),
        When(price__lt=50, then=Value('mid-range')),
        default=Value('premium'),
        output_field=CharField()
    )
)

# Conditional count
from django.db.models import Count, Q

stats = Book.objects.aggregate(
    total=Count('id'),
    published=Count('id', filter=Q(status='published')),
    featured=Count('id', filter=Q(is_featured=True))
)
```

---

## 📋 Practical Service Example

```python
# services.py
from django.db.models import Count, Avg, F, Q, Prefetch
from django.db.models.functions import TruncMonth
from .models import Book, Author, Category

class BookService:
    @staticmethod
    def get_featured_books(limit=10):
        """Get featured published books with related data"""
        return (
            Book.objects
            .filter(status='published', is_featured=True)
            .select_related('author', 'category')
            .prefetch_related('tags')
            .order_by('-published_date')[:limit]
        )
    
    @staticmethod
    def search_books(query, category=None, min_price=None, max_price=None):
        """Search books with filters"""
        qs = Book.objects.filter(status='published')
        
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(author__name__icontains=query)
            )
        
        if category:
            qs = qs.filter(category__slug=category)
        
        if min_price is not None:
            qs = qs.filter(price__gte=min_price)
        
        if max_price is not None:
            qs = qs.filter(price__lte=max_price)
        
        return qs.select_related('author', 'category').distinct()
    
    @staticmethod
    def get_book_stats():
        """Get comprehensive book statistics"""
        return Book.objects.aggregate(
            total_books=Count('id'),
            published_books=Count('id', filter=Q(status='published')),
            avg_price=Avg('price'),
            avg_rating=Avg('reviews__rating'),
            total_views=Sum('view_count')
        )
    
    @staticmethod
    def get_popular_authors(min_books=3):
        """Get authors with most books and best ratings"""
        return (
            Author.objects
            .annotate(
                book_count=Count('books', filter=Q(books__status='published')),
                avg_rating=Avg('books__reviews__rating')
            )
            .filter(book_count__gte=min_books)
            .order_by('-avg_rating', '-book_count')
        )
    
    @staticmethod
    def get_monthly_stats(year):
        """Get monthly publication stats for a year"""
        return (
            Book.objects
            .filter(published_date__year=year)
            .annotate(month=TruncMonth('published_date'))
            .values('month')
            .annotate(
                count=Count('id'),
                avg_price=Avg('price')
            )
            .order_by('month')
        )
```

---

## 🎉 Usage Example

```python
# In Django shell or views
from myapp.services import BookService

# Get featured books
featured = BookService.get_featured_books()
for book in featured:
    print(f"{book.title} by {book.author.name}")

# Search
results = BookService.search_books(
    query='django',
    min_price=20,
    max_price=50
)

# Stats
stats = BookService.get_book_stats()
print(f"Total books: {stats['total_books']}")
print(f"Average price: ${stats['avg_price']:.2f}")

# Popular authors
authors = BookService.get_popular_authors()
for author in authors:
    print(f"{author.name}: {author.book_count} books, {author.avg_rating:.1f} avg rating")
```

---

*Return to: [ORM Overview →](../README.md)*
