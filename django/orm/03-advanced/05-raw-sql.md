# Raw SQL and Custom Queries 🔧

## When to Use Raw SQL

Most of the time, the Django ORM is sufficient. Use raw SQL when:
- You need database-specific features
- Complex queries that ORM can't express
- Performance optimization for specific queries
- Working with legacy databases

---

## 📊 Methods for Raw SQL

```
┌─────────────────────────────────────────────────────────────┐
│                    RAW SQL OPTIONS                           │
├─────────────────────────────────────────────────────────────┤
│  Model.objects.raw()    - Returns model instances           │
│  connection.cursor()    - Returns raw rows                  │
│  .extra()               - Add SQL to ORM query (deprecated) │
│  RawSQL()               - SQL expression in ORM             │
└─────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ Using raw()

Returns model instances from raw SQL:

```python
# Basic raw query
books = Book.objects.raw('SELECT * FROM myapp_book')

for book in books:
    print(book.title)  # It's a Book instance!

# With parameters (ALWAYS use parameters!)
books = Book.objects.raw(
    'SELECT * FROM myapp_book WHERE price < %s',
    [30.00]
)

# Named parameters
books = Book.objects.raw(
    'SELECT * FROM myapp_book WHERE author_id = %(author_id)s',
    {'author_id': 1}
)
```

### raw() with JOINs

```python
# Join with authors
books = Book.objects.raw('''
    SELECT b.*, a.name as author_name
    FROM myapp_book b
    JOIN myapp_author a ON b.author_id = a.id
    WHERE a.name = %s
''', ['John Doe'])

for book in books:
    print(f"{book.title} by {book.author_name}")
```

### raw() Requirements

```python
# Must include primary key!
# ❌ Wrong
books = Book.objects.raw('SELECT title FROM myapp_book')

# ✅ Correct
books = Book.objects.raw('SELECT id, title FROM myapp_book')
```

---

## 2️⃣ Using cursor()

For complete control over SQL:

```python
from django.db import connection

def get_authors_with_book_counts():
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT a.name, COUNT(b.id) as book_count
            FROM myapp_author a
            LEFT JOIN myapp_book b ON a.id = b.author_id
            GROUP BY a.id, a.name
            HAVING COUNT(b.id) > %s
            ORDER BY book_count DESC
        ''', [5])
        
        # Returns list of tuples
        return cursor.fetchall()

# Usage
results = get_authors_with_book_counts()
for name, count in results:
    print(f"{name}: {count} books")
```

### Cursor Methods

```python
with connection.cursor() as cursor:
    cursor.execute('SELECT * FROM myapp_book WHERE id = %s', [1])
    
    # Get one row
    row = cursor.fetchone()  # (1, 'Title', 29.99, ...)
    
    # Get all rows
    cursor.execute('SELECT * FROM myapp_book')
    rows = cursor.fetchall()  # [(1, ...), (2, ...), ...]
    
    # Get N rows
    rows = cursor.fetchmany(10)
    
    # Get column names
    columns = [col[0] for col in cursor.description]
```

### Named Tuples for Better Access

```python
from collections import namedtuple

def get_book_stats():
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT 
                category,
                COUNT(*) as count,
                AVG(price) as avg_price
            FROM myapp_book
            GROUP BY category
        ''')
        
        columns = [col[0] for col in cursor.description]
        BookStats = namedtuple('BookStats', columns)
        
        return [BookStats(*row) for row in cursor.fetchall()]

# Usage
stats = get_book_stats()
for stat in stats:
    print(f"{stat.category}: {stat.count} books, avg ${stat.avg_price:.2f}")
```

---

## 3️⃣ RawSQL in ORM Queries

Add raw SQL fragments to ORM queries:

```python
from django.db.models.expressions import RawSQL

# Use RawSQL in annotations
books = Book.objects.annotate(
    price_per_page=RawSQL(
        'price / NULLIF(pages, 0)',
        []
    )
).order_by('-price_per_page')

# With parameters
books = Book.objects.annotate(
    is_expensive=RawSQL(
        'price > %s',
        [50.00]
    )
)
```

---

## ⚠️ Security: SQL Injection Prevention

**NEVER** use string formatting with SQL:

```python
# ❌ DANGEROUS - SQL injection vulnerability!
name = request.GET['name']
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")

# ❌ ALSO DANGEROUS
cursor.execute("SELECT * FROM users WHERE name = '%s'" % name)

# ✅ SAFE - Use parameterized queries
cursor.execute("SELECT * FROM users WHERE name = %s", [name])

# ✅ SAFE - Named parameters
cursor.execute(
    "SELECT * FROM users WHERE name = %(name)s",
    {'name': name}
)
```

---

## 📝 Practical Examples

### Complex Reporting Query

```python
def get_sales_report(start_date, end_date):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT 
                DATE_TRUNC('month', o.created_at) as month,
                c.name as category,
                COUNT(DISTINCT o.id) as orders,
                SUM(oi.quantity) as units_sold,
                SUM(oi.quantity * oi.unit_price) as revenue
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            JOIN categories c ON p.category_id = c.id
            WHERE o.created_at BETWEEN %s AND %s
            GROUP BY month, c.name
            ORDER BY month, revenue DESC
        ''', [start_date, end_date])
        
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
```

### Full-Text Search (PostgreSQL)

```python
def search_books(query):
    return Book.objects.raw('''
        SELECT *, 
               ts_rank(search_vector, plainto_tsquery('english', %s)) as rank
        FROM myapp_book
        WHERE search_vector @@ plainto_tsquery('english', %s)
        ORDER BY rank DESC
        LIMIT 20
    ''', [query, query])
```

### Database-Specific Features

```python
# PostgreSQL array aggregation
def get_authors_with_genres():
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT 
                a.name,
                array_agg(DISTINCT b.genre) as genres
            FROM authors a
            JOIN books b ON a.id = b.author_id
            GROUP BY a.id, a.name
        ''')
        return cursor.fetchall()
```

---

## 🔄 Transactions with Raw SQL

```python
from django.db import transaction

def transfer_funds(from_account, to_account, amount):
    with transaction.atomic():
        with connection.cursor() as cursor:
            # Deduct from source
            cursor.execute('''
                UPDATE accounts 
                SET balance = balance - %s 
                WHERE id = %s AND balance >= %s
            ''', [amount, from_account, amount])
            
            if cursor.rowcount == 0:
                raise ValueError("Insufficient funds")
            
            # Add to destination
            cursor.execute('''
                UPDATE accounts 
                SET balance = balance + %s 
                WHERE id = %s
            ''', [amount, to_account])
```

---

## 💡 Best Practices

### 1. Prefer ORM When Possible

```python
# ❌ Unnecessary raw SQL
cursor.execute('SELECT * FROM books WHERE price < 30')

# ✅ Use ORM
Book.objects.filter(price__lt=30)
```

### 2. Use raw() When You Need Model Instances

```python
# When you need Book objects with custom SQL
books = Book.objects.raw('''
    SELECT * FROM myapp_book
    WHERE ... complex conditions ...
''')
```

### 3. Use cursor() for Non-Model Data

```python
# When you just need data, not model instances
with connection.cursor() as cursor:
    cursor.execute('SELECT category, COUNT(*) FROM books GROUP BY category')
```

### 4. Always Use Parameters

```python
# ✅ Always parameterize user input
cursor.execute('SELECT * FROM books WHERE author = %s', [user_input])
```

---

## 🎓 Quick Check

Before finishing, make sure you understand:

- ✅ When to use `raw()` vs `cursor()`
- ✅ How to safely use parameters to prevent SQL injection
- ✅ How to use `RawSQL` in ORM queries
- ✅ When raw SQL is appropriate vs ORM

---

## 🎉 Congratulations!

You've completed the Advanced ORM section! Check out the **[examples](../examples/)** for complete working code.

---

*Return to: [ORM Overview →](../README.md)*
