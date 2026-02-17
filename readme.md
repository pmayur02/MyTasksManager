# FastAPI Todo App Backend

This is the backend for the Todo App, built with **FastAPI**.  
It provides **user authentication (login/register)** and **task CRUD operations**.

---

## Features

- User signup and login with JWT authentication
- Create, read, update, delete tasks
- Tasks have `title`, `description`, and `status` (`pending` or `completed`)
- CORS configured for frontend integration
- Environment variables support via `.env`

---

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite/PostgreSQL (configurable)
- Uvicorn (ASGI server)
- python-dotenv

---

## Setup

1. Clone the repo:

2. Create virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Create .env file:
DATABASE_URL=sqlite:///./todo.db      # or PostgreSQL URL
SECRET_KEY=your_super_secret_key
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

5.Run the server (development):

