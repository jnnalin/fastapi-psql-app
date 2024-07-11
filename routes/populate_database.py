import random

from database.session import engine as dbengine
from database.session import get_db
from faker import Faker
from fastapi import APIRouter, Depends, HTTPException, status
from models import Base, Customer, DatabaseRequest, Order, OrderItem, Product, CProduct
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from sqlalchemy import select, func, desc, cast, Numeric
database_router = APIRouter(prefix="/database")


# Function to create tables in the database
async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Function to create fake data and populate the database
async def create_fake_data(db: AsyncSession, customer_count: int, order_count: int, product_count: int):
    fake = Faker()

    # Create fake customers
    customers = []
    for _ in range(customer_count):
        customer = Customer(
            customer_name=fake.name(),
            email=fake.email(),
            signup_date=fake.date_this_decade(),
        )
        customers.append(customer)
    db.add_all(customers)
    await db.flush()
    for customer in customers:
        print(f"Customer ID: {customer.customer_id}, Type: {type(customer.customer_id)}")

    # Create fake products
    products = []
    for _ in range(product_count):
        product = Product(product_name=fake.word(), category=fake.word())
        products.append(product)
    db.add_all(products)
    await db.flush()
    for product in products:
        print(f"Product ID: {product.product_id}, Type: {type(product.product_id)}")

    # Create fake orders
    orders = []
    for _ in range(order_count):
        customer = random.choice(customers)
        print(f"Customer ID: {customer.customer_id}, Type: {type(customer.customer_id)}")
        order = Order(
            customer_id=customer.customer_id,  # Ensure this is a UUID
            order_date=fake.date_this_year(),
            total_amount=round(random.uniform(10, 1000), 2),
        )
        orders.append(order)
    db.add_all(orders)
    await db.flush()

    for order in orders:
        print(f"Order ID: {order.order_id}, Type: {type(order.order_id)}")

    # Create fake order items
    order_items = []
    for order in orders:
        for _ in range(random.randint(1, 5)):  # Each order has 1 to 5 items
            product = random.choice(products)
            order_item = OrderItem(
                order_id=order.order_id,  # Ensure this is a UUID
                product_id=product.product_id,  # Ensure this is a UUID
                quantity=random.randint(1, 10),
                price_per_unit=round(random.uniform(1, 100), 2),
            )
            order_items.append(order_item)
    db.add_all(order_items)
    await db.commit()
    # Debugging: Print the types of the UUID fields

# Endpoint to populate the database with fake data
@database_router.put(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": dict,
            "description": "Internal server error",
        },
    },
    summary="Populate the database",
    description="Uses faker to populate the database with fake data.",
    tags=["db"],
)
async def populate_db(request: DatabaseRequest, db: AsyncSession = Depends(get_db)):
    try:
        engine = dbengine
        await create_tables(engine)
        await create_fake_data(db, request.customer_count,request.product_count ,request.order_count)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return {"message": "Database populated successfully"}


async def get_custom_data(db):
    file = "./fake_product_data.csv"
    data = pd.read_csv(file, index_col=None)
    # Ensure that price, quantity_sold, and rating are numeric
    data['price'] = pd.to_numeric(data['price'], errors='coerce')
    data['quantity_sold'] = pd.to_numeric(data['quantity_sold'], errors='coerce')
    data['rating'] = pd.to_numeric(data['rating'], errors='coerce')

    # Replace missing values in price and quantity_sold with the median of their respective columns
    data['price'].fillna(data['price'].median(), inplace=True)
    data['quantity_sold'].fillna(data['quantity_sold'].median(), inplace=True)

    # Replace missing values in rating with the average rating of the respective category
    data['rating'] = data.groupby('category')['rating'].transform(lambda x: x.fillna(x.mean()))
    for index, row in data.iterrows():
        product = CProduct(
            product_id=row['product_id'],
            product_name=row['product_name'],
            category=row['category'],
            price=row['price'],
            quantity_sold=row['quantity_sold'],
            rating=row['rating'],
            review_count=row['review_count']
        )
        db.add(product)

    # Commit the session to save the changes
    await db.commit()

@database_router.put(
    "/custom",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": dict,
            "description": "Internal server error",
        },
    },
    summary="Populate the products database",
    description="Uses faker to populate the database with fake data.",
    tags=["db"],
)
async def populate_custom_db(request: DatabaseRequest, db: AsyncSession = Depends(get_db)):
    try:
        engine = dbengine
        await create_tables(engine)
        await get_custom_data(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return {"message": "Database populated successfully"}

