#  FastAPI Ticket Booking System with Pessimistic Locking

A demonstration of a **ticket booking system** built with **FastAPI** and **PostgreSQL**, focusing on **safe concurrency control**.

It uses **pessimistic locking** (`SELECT ... FOR UPDATE`) to enforce **row-level locks**, ensuring data consistency when multiple users attempt to reserve the same ticket at the same time.

## 🚀 Features
- FastAPI backend with RESTful endpoints
- SQLModel + PostgreSQL for database modeling
- Pessimistic locking to handle concurrent reservations safely
- Ticket expiration logic (reserved tickets expire after 5 minutes if unpaid)
- Enum-based ticket statuses: `Available`, `Reserved`, `Booked`
- Alembic migrations included for schema evolution
- Concurrency testing script (`run_concurrent.py`) to simulate multiple users

## 🛠️ Tech Stack
- **FastAPI** (Python web framework)
- **SQLModel / SQLAlchemy** (ORM + database interaction)
- **PostgreSQL** (relational database)
- **Alembic** (database migrations)
- **Docker Compose** (for easy setup)

## 📂 Project Structure
```bash
project-root/
├── alembic/                 # Database migration scripts
├── app/
│   ├── models/              # SQLModel table definitions
│   │   └── event.py, ticket.py
│   ├── services/            # Business logic & DB operations using SQLModel
│   │   └── ticket_service.py
│   ├── utils/               # Helper utilities (db_engine, formatting etc.)
│   │   └── create_db_engine.py
│   ├── validation_schemas/  # Request validation models
│   └── main.py              # FastAPI entrypoint
```

## ⚡ Quick Start
1. Clone the repo
```bash
git clone https://github.com/rkvlorenzo/fastapi-ticket-booking-system-with-locking.git
cd fastapi-ticket-booking-system-with-locking
```
2. Create Environment Files
#### Create environment files
- Create `db.env` file in root folder.
    These environment variables will be used by PostgreSQL inside Docker.
    ```bash
        POSTGRES_USER=dev_user        # database username
        POSTGRES_PASSWORD=dev_password # database password
        POSTGRES_DB=db_bookings            # database name
        POSTGRES_HOST=localhost       # database host (if running locally)
        POSTGRES_PORT=5432            # database port
    ```
- Create `.env` file in root folder. These environment variables will be used by FastAPI to connect to the database.
    ```bash
        POSTGRES_USER=dev_user        # must match db.env
        POSTGRES_PASSWORD=dev_password # must match db.env
        POSTGRES_DB=db_bookings            # must match db.env
        POSTGRES_HOST=db              # container name in docker-compose
        POSTGRES_PORT=5432            # must match db.env
    ```
    >NOTE:
    >- When Running Locally (Without Docker), set POSTGRES_HOST=localhost.
    >- When Running Locally Using Docker, use POSTGRES_HOST=db since that matches the service name in docker-compose.yml.

3. Start services
```bash
docker-compose up --build
```
4. Run migrations
```bash
docker-compose exec api alembic upgrade head
```
5. Access the API
```bash
Swagger UI: http://localhost:8000/docs
```
6. Test concurrency
```bash
python run_concurrent.py
```
## 🔗 Related Projects
https://github.com/rkvlorenzo/fastapi-docker-postgresql-template