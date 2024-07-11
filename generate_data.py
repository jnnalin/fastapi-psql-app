import random
import csv
from faker import Faker

# Initialize Faker
fake = Faker()

# Define categories
categories = ['Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Sports', 'Toys']

# Function to generate fake product data
def generate_fake_product_data(num_products):
    products = []

    for i in range(1, num_products + 1):
        product = {
            'product_id': i,
            'product_name': fake.word().capitalize() + ' ' + fake.word().capitalize(),
            'category': random.choice(categories),
            'price': round(random.uniform(5.0, 100.0), 2),
            'quantity_sold': random.randint(1, 100),
            'rating': round(random.uniform(1.0, 5.0), 1),
            'review_count': random.randint(0, 5000)
        }
        products.append(product)

    return products

# Function to save data to a CSV file
def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Generate data for 10 products
fake_product_data = generate_fake_product_data(50000)

# Save the fake product data to a CSV file
save_to_csv(fake_product_data, 'fake_product_data.csv')

print("Fake product data has been saved to 'fake_product_data.csv'")