# Model Fields 📝

## What are Model Fields?

**Model fields** define the type of data stored in each column of your database table. Django provides many field types, each optimized for specific data.

---

## 🗂️ Field Categories Overview

```
Django Model Fields
├── String Fields
│   ├── CharField
│   ├── TextField
│   ├── EmailField
│   ├── URLField
│   └── SlugField
│
├── Numeric Fields
│   ├── IntegerField
│   ├── FloatField
│   ├── DecimalField
│   └── PositiveIntegerField
│
├── Boolean Fields
│   ├── BooleanField
│   └── NullBooleanField
│
├── Date/Time Fields
│   ├── DateField
│   ├── TimeField
│   ├── DateTimeField
│   └── DurationField
│
├── File Fields
│   ├── FileField
│   └── ImageField
│
└── Relationship Fields
    ├── ForeignKey
    ├── ManyToManyField
    └── OneToOneField
```

---

## 📝 String Fields

### CharField - Short Text

```python
# For text with a maximum length
title = models.CharField(max_length=200)
name = models.CharField(max_length=100, blank=True)  # Optional
code = models.CharField(max_length=10, unique=True)  # Must be unique
```

**Key options:**
- `max_length` (required) - Maximum characters
- `blank=True` - Allow empty strings in forms
- `unique=True` - No duplicates allowed
- `default='value'` - Default value

### TextField - Long Text

```python
# For unlimited text (no max_length)
description = models.TextField()
content = models.TextField(blank=True)
notes = models.TextField(default='No notes')
```

### EmailField - Email Addresses

```python
# Validates email format automatically
email = models.EmailField()
contact_email = models.EmailField(unique=True)
```

### URLField - URLs

```python
# Validates URL format
website = models.URLField(blank=True)
profile_url = models.URLField(max_length=500)
```

### SlugField - URL-Friendly Strings

```python
# For URL slugs (lowercase, hyphens)
slug = models.SlugField(unique=True)
# "Hello World" becomes "hello-world"
```

---

## 🔢 Numeric Fields

### IntegerField - Whole Numbers

```python
# Standard integers (-2147483648 to 2147483647)
quantity = models.IntegerField()
age = models.IntegerField(default=0)
```

### PositiveIntegerField - Positive Numbers Only

```python
# Only positive integers (0 to 2147483647)
stock = models.PositiveIntegerField(default=0)
views = models.PositiveIntegerField(default=0)
```

### FloatField - Decimal Numbers

```python
# Floating point numbers
rating = models.FloatField()
temperature = models.FloatField(null=True, blank=True)
```

### DecimalField - Precise Decimals

```python
# For money and precise calculations
price = models.DecimalField(max_digits=10, decimal_places=2)
# max_digits=10, decimal_places=2 → up to 99999999.99

tax_rate = models.DecimalField(max_digits=5, decimal_places=4)
# max_digits=5, decimal_places=4 → up to 9.9999
```

**When to use which:**
- `FloatField` - Scientific calculations, ratings
- `DecimalField` - Money, financial data (precise!)

---

## ✅ Boolean Fields

### BooleanField - True/False

```python
# True or False
is_active = models.BooleanField(default=True)
is_published = models.BooleanField(default=False)
featured = models.BooleanField(default=False)
```

### NullBooleanField (Deprecated in Django 4.0+)

```python
# Use BooleanField with null=True instead
has_newsletter = models.BooleanField(null=True, blank=True)
# Can be True, False, or NULL
```

---

## 📅 Date and Time Fields

### DateField - Dates Only

```python
# Stores date (YYYY-MM-DD)
birth_date = models.DateField()
published_date = models.DateField(null=True, blank=True)

# Auto-set on creation
created_date = models.DateField(auto_now_add=True)

# Auto-update on every save
modified_date = models.DateField(auto_now=True)
```

### DateTimeField - Date and Time

```python
# Stores date and time
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
scheduled_for = models.DateTimeField(null=True, blank=True)
```

### TimeField - Time Only

```python
# Stores time (HH:MM:SS)
start_time = models.TimeField()
end_time = models.TimeField()
```

### DurationField - Time Duration

```python
# Stores a duration (timedelta)
duration = models.DurationField()
# Usage: timedelta(hours=1, minutes=30)
```

---

## 📎 File Fields

### FileField - Any File

```python
# For file uploads
document = models.FileField(upload_to='documents/')
resume = models.FileField(upload_to='resumes/%Y/%m/')  # Organized by date
```

### ImageField - Images Only

```python
# For image uploads (validates image format)
avatar = models.ImageField(upload_to='avatars/')
photo = models.ImageField(upload_to='photos/', blank=True)
```

**Note:** ImageField requires Pillow: `pip install Pillow`

---

## 🔗 Relationship Fields

### ForeignKey - Many-to-One

```python
# Many books can belong to one author
class Book(models.Model):
    author = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE,
        related_name='books'
    )
```

### OneToOneField - One-to-One

```python
# One user has one profile
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
```

### ManyToManyField - Many-to-Many

```python
# A book can have many tags, a tag can be on many books
class Book(models.Model):
    tags = models.ManyToManyField('Tag', related_name='books')
```

---

## ⚙️ Common Field Options

| Option | Description | Example |
|--------|-------------|---------|
| `null=True` | Allow NULL in database | `DateField(null=True)` |
| `blank=True` | Allow empty in forms | `CharField(blank=True)` |
| `default=value` | Default value | `BooleanField(default=True)` |
| `unique=True` | Must be unique | `EmailField(unique=True)` |
| `choices=list` | Limit to choices | `CharField(choices=STATUS_CHOICES)` |
| `verbose_name='Name'` | Human-readable name | `CharField(verbose_name='Full Name')` |
| `help_text='...'` | Help text for forms | `EmailField(help_text='Enter email')` |
| `db_index=True` | Create database index | `CharField(db_index=True)` |
| `editable=False` | Hide from admin/forms | `DateField(editable=False)` |
| `primary_key=True` | Make primary key | `CharField(primary_key=True)` |

---

## 🎯 Using Choices

```python
class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

# Usage
>>> article = Article(status='published')
>>> article.status
'published'
>>> article.get_status_display()  # Human-readable
'Published'
```

### Using IntegerChoices (Django 3.0+)

```python
class Article(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 1, 'Draft'
        PUBLISHED = 2, 'Published'
        ARCHIVED = 3, 'Archived'
    
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.DRAFT
    )

# Usage
>>> article.status = Article.Status.PUBLISHED
>>> article.status
2
>>> article.get_status_display()
'Published'
```

### Using TextChoices (Django 3.0+)

```python
class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        PUBLISHED = 'PB', 'Published'
        ARCHIVED = 'AR', 'Archived'
    
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
```

---

## 📊 Field Reference Table

| Field Type | Python Type | Database Type | Use For |
|------------|-------------|---------------|---------|
| `CharField` | `str` | VARCHAR | Short text |
| `TextField` | `str` | TEXT | Long text |
| `IntegerField` | `int` | INTEGER | Whole numbers |
| `FloatField` | `float` | FLOAT | Decimals (approx) |
| `DecimalField` | `Decimal` | DECIMAL | Money, precise |
| `BooleanField` | `bool` | BOOLEAN | True/False |
| `DateField` | `date` | DATE | Dates |
| `DateTimeField` | `datetime` | DATETIME | Date & time |
| `EmailField` | `str` | VARCHAR | Emails |
| `URLField` | `str` | VARCHAR | URLs |
| `FileField` | `FieldFile` | VARCHAR | Files |
| `ImageField` | `ImageFieldFile` | VARCHAR | Images |
| `ForeignKey` | Model | FK constraint | Many-to-One |
| `ManyToManyField` | Manager | Join table | Many-to-Many |
| `OneToOneField` | Model | FK + unique | One-to-One |

---

## 💡 Best Practices

### 1. Choose the Right Field Type

```python
# ❌ Bad - Using CharField for email
email = models.CharField(max_length=100)

# ✅ Good - Using EmailField
email = models.EmailField()  # Includes validation!
```

### 2. Use DecimalField for Money

```python
# ❌ Bad - FloatField has precision issues
price = models.FloatField()  # 0.1 + 0.2 = 0.30000000000000004

# ✅ Good - DecimalField is precise
price = models.DecimalField(max_digits=10, decimal_places=2)
```

### 3. Set Sensible Defaults

```python
# ✅ Good defaults
is_active = models.BooleanField(default=True)
view_count = models.PositiveIntegerField(default=0)
created_at = models.DateTimeField(auto_now_add=True)
```

### 4. Use `null=True` and `blank=True` Correctly

```python
# For strings - use blank=True only
description = models.TextField(blank=True)  # Stores empty string ''

# For non-strings - use both
birth_date = models.DateField(null=True, blank=True)  # Stores NULL
```

---

## 🎓 Quick Check

Before moving on, make sure you understand:

- ✅ Different field types for different data
- ✅ When to use `CharField` vs `TextField`
- ✅ When to use `FloatField` vs `DecimalField`
- ✅ How to use `choices` for limited options
- ✅ The difference between `null` and `blank`

---

## 🚀 Next Steps

Now let's learn about **[Basic CRUD Operations](./04-crud-operations.md)**!

---

*Continue to: [Basic CRUD Operations →](./04-crud-operations.md)*
