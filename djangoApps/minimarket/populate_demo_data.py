"""
populate_demo_data.py

This script populates the database with demo data for testing the minimarket app.
It performs the following actions:
1. Clears existing data from the Category, Product, and Transaction models.
2. Creates 10 unique categories.
3. Creates 50 products with random attributes and assigns them to categories.
4. Creates 100 transactions (either 'IN' or 'OUT') for randomly selected products.
"""

import os
import django
import random
from decimal import Decimal
from faker import Faker
from django.core.exceptions import ValidationError

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minimarket.settings')
django.setup()

from inventory.models import Category, Product, Transaction

# Initialize Faker for generating dummy data
fake = Faker()

# ----- Step 1: Clear existing data -----
print("🧹 Clearing old data...")
Transaction.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()

# ----- Step 2: Create unique categories -----
print("📦 Creating categories...")
categories = []
while len(categories) < 10:
    name = fake.unique.word().capitalize()
    description = fake.sentence()
    try:
        cat = Category.objects.create(name=name, description=description)
        categories.append(cat)
    except:
        continue  # Skip if duplicate (rare case even with Faker.unique)

# ----- Step 3: Create products -----
print("🛒 Creating products...")
products = []
for _ in range(50):
    name = fake.unique.word().capitalize()
    category = random.choice(categories)
    price = round(random.uniform(1.0, 100.0), 2)
    stock_quantity = random.randint(10, 100)
    description = fake.sentence()

    prod = Product.objects.create(
        name=name,
        category=category,
        price=Decimal(price),
        stock_quantity=stock_quantity,
        description=description
    )
    products.append(prod)

# ----- Step 4: Create transactions -----
print("💸 Creating transactions...")
transaction_count = 0
attempts = 0
max_attempts = 1000  # Prevent infinite loops

while transaction_count < 100 and attempts < max_attempts:
    product = random.choice(products)
    transaction_type = random.choice(['IN', 'OUT'])
    quantity = random.randint(1, 20)
    notes = fake.sentence()

    try:
        # Create transaction
        transaction = Transaction(
            product=product,
            transaction_type=transaction_type,
            quantity=quantity,
            notes=notes
        )
        transaction.save()  # This will validate stock and update product
        transaction_count += 1
        print(f"Created transaction {transaction_count}/100: {transaction}")
    except ValidationError as e:
        print(f"Skipping transaction due to: {e}")
        attempts += 1
        continue  # Try a different product or quantity
    except Exception as e:
        print(f"Unexpected error: {e}")
        attempts += 1
        continue

if transaction_count < 100:
    print(f"⚠️ Only created {transaction_count} transactions due to stock constraints or errors - consider increasing initial stock quantities.")
else:
    print("✅ Demo data populated successfully!")