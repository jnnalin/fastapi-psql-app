# Test application
A simple fastapi-psql app to test out the concepts covered

## Prerequisites
Ensure you have the following prerequisites:
Docker and Docker Compose installed on your machine.
A PostgreSQL service running and accessible within the same network as the application.

## Settings
place the following file with the name '.env' in the main folder(where main.py is present)
```
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database_name>
POSTGRES_SERVICE=<service_name as per the container>
POSTGRES_PORT=<port as per the psql service>
```
## Running the app
run the following commands
```
docker compose build
docker compose up
```

## Api description
### Authentication
#### Signup
Endpoint: /signup
Method: POST
Description: Registers a new user and returns a JWT token.
Request Body:
```
{
  "username": "string",
  "password": "string"
}
```
Response:
```
{
  "access_token": "string",
  "token_type": "bearer"
}
```
#### Login
Endpoint: /login
Method: POST
Description: Authenticates an existing user and returns a JWT token.
Request Body:
```
{
  "username": "string",
  "password": "string"
}
```
Response:
```
{
  "access_token": "string",
  "token_type": "bearer"
}
```
### Database Operations
#### Populate Database with Fake Data
Endpoint: /database
Method: PUT
Description: Uses Faker to populate the database with fake data for SQL query task(Task 1).
Request Body:
```
{
  "user_count": "integer",
  "item_count": "integer"
}
```
Response:
```
{
  "message": "Database populated successfully"
}
```
#### Populate Database with Custom Product Data
Endpoint: /database/custom
Method: PUT
Description: Loads custom data into the custom_products database from a CSV file.
the currently used file  is test_app/fake_product_data
Response:
```
{
  "message": "Database populated successfully"
}
```
Note : Populating the database is a mututally exclusive event, only one Product_Data/ Task 1 data will be present at a time in the database
### Get Top Products in Each category based on revenue
Endpoint: /database/custom/top-product
Method: PUT
Description: Retrieves the top product in each category along with total revenue.
Response:
```
{
  "data": [
    {
      "category": "string",
      "total_revenue": "float",
      "top_product": "string",
      "top_product_quantity_sold": "integer"
    }
  ]
}
```
