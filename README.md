# Book Management Backend Application

## Overview

This is a backend application developed using FastAPI, SQLAlchemy, Alembic, and PostgreSQL for educational purposes. The application provides a platform for managing a collection of books, allowing users to add and view books while utilizing JWT tokens for authorization.

## Features

- **FastAPI**: A modern web framework for building APIs with Python, known for its speed and ease of use.
- **SQLAlchemy**: An ORM (Object-Relational Mapping) tool that simplifies database interactions.
- **Alembic**: A lightweight database migration tool for SQLAlchemy, facilitating version control for the database schema.
- **PostgreSQL**: A powerful open-source relational database system for data storage and management.

## Authentication

- The application uses JWT (JSON Web Tokens) for user authentication. 
- All actions performed by users are authorized through these tokens, ensuring secure access to the application features.

## Functionality

- **Add Books**: Users can add new books to the database, including details.
- **View Books**: The application allows users to view the list of books in the database.
- **Pagination**: Implemented pagination for book listings, enhancing user experience by managing large datasets.
- **ID-Based Access Control**: Users can perform actions based on their access permissions. The application checks user access via ID, allowing or restricting actions accordingly.

## Usage

1. **Installation**:
   - Clone the repository.
   - Install the required dependencies using:
     ```bash
     pip install -r requirements.txt
     ```
   - Set up the PostgreSQL database and configure the connection settings.

2. **Running the Application**:
   - Start the FastAPI application using Uvicorn:
     ```bash
     uvicorn main:app --reload
     ```

3. **Accessing the API**:
   - The API can be accessed at `http://localhost:8000`.

## Conclusion

This backend application serves as an educational project for learning about FastAPI, SQLAlchemy, and PostgreSQL.
