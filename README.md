# FastAPI Postgres Smart Library System

This project is a Smart Library System built with **FastAPI** and **PostgreSQL**. It provides APIs for managing users, books, and loans. The application uses **uvicorn** as the ASGI server.

## Features

- **User Management**: Add, update, delete, and retrieve user information.
- **Book Management**: Add, update, delete, and retrieve book details.
- **Loan Management**: Manage book loans, including issuing and returning books.
- **Database**: PostgreSQL is used for data storage.
- **FastAPI**: High-performance API framework for building RESTful APIs.
- **Uvicorn**: Lightning-fast ASGI server for running the application.

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/your-username/fastapi-postgres-smart-library.git
  cd fastapi-postgres-smart-library
  ```

2. Install `uv` package manager globally if not already installed:
  ```bash
  pip install uv
  ```

3. Configure the database:
  - Create a PostgreSQL database.
  - Update the `DATABASE_URL` in the `.env` file with your database credentials.

4. Install project dependencies using `uv`:
  ```bash
  uv install
  ```

5. Run database migrations:
  ```bash
  uv db upgrade
  ```

6. Start the application:
  ```bash
  uv run fastapi dev
  ```

## API Endpoints

### Users
- `GET /users/`: Retrieve all users.
- `POST /users/`: Create a new user.
- `GET /users/{user_id}/`: Retrieve a specific user.
- `PUT /users/{user_id}/`: Update a user.
- `DELETE /users/{user_id}/`: Delete a user.

### Books
- `GET /books/`: Retrieve all books.
- `POST /books/`: Add a new book.
- `GET /books/{book_id}/`: Retrieve a specific book.
- `PUT /books/{book_id}/`: Update a book.
- `DELETE /books/{book_id}/`: Delete a book.

### Loans
- `GET /loans/`: Retrieve all loans.
- `POST /loans/`: Issue a new loan.
- `PUT /loans/{loan_id}/`: Return a loan.

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
```

## Running Tests

Run the test suite using `pytest`:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
