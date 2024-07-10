# Expense Tracker API

This is a simple Expense Tracker API built with Flask and PostgreSQL. The API allows users to track their expenses, categorize them, and generate reports.

## Features

- User registration and login with JWT authentication.
- CRUD operations for expenses.
- Expense categorization.
- Monthly and annual reports.

## Technologies Used

- Flask
- Flask-RESTful
- Flask-JWT-Extended
- Flask-SQLAlchemy
- PostgreSQL
- Marshmallow

## Prerequisites

- Python 3.8+
- PostgreSQL

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/iajayparihar/Expense-Tracker-flask.git
    cd expense-tracker-api
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the database:**

    Create a PostgreSQL database and update the configuration in `config.py`:

    ```python
    class Config:
        SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/dbname'
        JWT_SECRET_KEY = 'your-secret-key'
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    ```

5. **Initialize the database:**

    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

6. **Run the application:**

    ```bash
    flask run
    ```

## Project Structure
```
expense-tracker-api/
├── app/
│ ├── init.py
│ ├── config.py
│ ├── extensions.py
│ ├── auth/
│ │ ├── init.py
│ │ ├── models.py
│ │ ├── routes.py
│ │ ├── schemas.py
│ ├── expenses/
│ │ ├── init.py
│ │ ├── models.py
│ │ ├── routes.py
│ │ ├── schemas.py
│ ├── reports/
│ │ ├── init.py
│ │ ├── routes.py
├── migrations/
├── requirements.txt
└── README.md
```

## API Endpoints

### Authentication

- **POST** `/auth/register`
  
  Register a new user.
  
  Request body:
  ```json
    {
        "username": "user",
        "password": "password",
        "name": "User Name",
        "email": "user@example.com",
        "mobile": "1234567890"
    }


- **POST** `/auth/login`

    Login a user and receive a JWT token.

    Request body:
    ```json
    {
        "username": "user",
        "password": "password"
    }

- **GET** `/auth/allusers`

    Get all registered users.

    Header:
            Authorization: Bearer <JWT Token>


- **PUT** `/auth/update/<int:id>`

    Update user details.

    Header:
            Authorization: Bearer <JWT Token>
    
    Request body (optional fields):
    ```json
    {
        "name": "Updated Name",
        "email": "updated@example.com",
        "mobile": "0987654321",
        "password": "newpassword"
    }


- **DELETE** ` /auth/delete/<int:id>`

    Delete a user by ID.

    Header:
            Authorization: Bearer <JWT Token>


### Expenses

- **GET** `/expenses`

    Get all expenses for the authenticated user.

    Header:
            Authorization: Bearer <JWT Token>
    

- **POST** `/expenses`

    Add a new expense.

    Header:
            Authorization: Bearer <JWT Token>

    Request body:
    ```json
    {
        "amount": 100.0,
        "description": "Grocery shopping",
        "category": "Food"
    }


- **GET** `/expenses/<int:id>`
    
    Get a specific expense by ID.

    Header:
            Authorization: Bearer <JWT Token>


- **PUT** `/expenses/<int:id>`
    
    Update an existing expense.

    Header:
            Authorization: Bearer <JWT Token>

    Request body:
    ```json
    {
        "amount": 150.0,
        "description": "Grocery shopping updated",
        "category": "Food"
    }


- **DELETE** `/expenses/<int:id>`
    
    Delete an expense by ID.

    Header:
            Authorization: Bearer <JWT Token>


- **GET** `/expenses/summary`
    Get a summary of expenses by category.

    Header:
            Authorization: Bearer <JWT Token>



### Categories
GET 
- **GET** `/categories`
    Get all categories.

    Header:
            Authorization: Bearer <JWT Token>


- **POST** `/categories`
    Add a new category.

    Header:
            Authorization: Bearer <JWT Token>

    Request body:
    ```json
    {
        "name": "New Category"
    }


- **PUT** `/categories/<int:id>`
    Update a category by ID.

    Header:
            Authorization: Bearer <JWT Token>

    Request body:
    ```json
    {
        "name": "Updated Category"
    }


- **DELETE** `/categories/<int:id>`
    
    Delete a category by ID.
    
    Header:
            Authorization: Bearer <JWT Token>
            

### Reports


- **GET** `/reports/monthly/<int:year>/<int:month>`
    Get monthly report for the specified year and month.

    Header:
            Authorization: Bearer <JWT Token>


- **GET** `/reports/annual/<int:year>`

    Get annual report for the specified year.

    Header:
            Authorization: Bearer <JWT Token>
