# HackRadar API

HackRadar is a FastAPI-based API that collects hackathon data from platforms like MLH, Devpost, and Devfolio, storing everything in a PostgreSQL database. It provides endpoints for upcoming hackathons and can be deployed easily with Docker.

---

## 🚀 Features

* Scrapers for multiple hackathon platforms.
* REST API built with FastAPI.
* Uses PostgreSQL as the primary database.
* Automated scraping using background tasks or scheduled jobs.
* Dockerized setup for easy deployment.

---

## 📁 Project Structure

```
hackradar/
├── adapters/                # Scrapers for each platform
│   ├── devpost.py
│   ├── mlh.py
│   └── __init__.py
├── backend/                # FastAPI app
│   ├── main.py
│   ├── models.py           # Pydantic + SQLAlchemy models
│   ├── schemas.py          # Pydantic models for FastAPI responses
│   ├── crud.py             # Database operations
│   ├── db.py               # Database session and engine
│   ├── init_db.py          # Initializes DB schema
│   └── __init__.py
├── tasks/                  # Scheduled scrapers or CLI runners
│   └── fetch_and_store.py
├── docker/entrypoint.sh    # Docker entrypoint script
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml          # Dependency management with uv
├── .env                    # Environment variables
└── README.md
```

---

## ⚡ Quick Start (Docker)

Run the following commands to start everything with Docker and PostgreSQL:

```bash
docker compose build
docker compose up -d
```

Access API at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠 Local Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/hackradar.git
   cd hackradar
   ```

2. **Install dependencies (using uv)**:

   ```bash
   uv pip install -e .
   ```

3. **Set up PostgreSQL**:
   Ensure you have PostgreSQL running locally. Update the `.env` file with your database connection details.

4. **Initialize the database**:

   ```bash
   python -m backend.init_db
   ```

5. **Run the scrapers to fetch initial data**:

   ```bash
   python -m tasks.fetch_and_store
   ```

6. **Start the FastAPI server**:

   ```bash
   uvicorn backend.main:app --reload
   ```

7. Open the interactive API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```
DATABASE_URL=postgresql://hackuser:hackpass@db:5432/hackradar
SCRAPE_ON_START=1
```

---

## 🤝 Contributing

Contributions are welcome! Please check the [Contributing Guide](CONTRIBUTING.md) before submitting pull requests.

---

