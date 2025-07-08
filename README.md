# 🚀 HackRadar

**HackRadar** is an open-source API service that aggregates and serves upcoming hackathons from various platforms like Devpost and MLH. It scrapes hackathon details, stores them in a database, and exposes a clean FastAPI endpoint to consume this data.


## 📦 Features

* 🔎 Scrapes hackathons from multiple sources (MLH, Devpost)
* 🗃️ Stores events in a local SQLite database
* 🧠 Automatic duplicate handling using upsert logic
* ⚡ FastAPI-powered REST API to fetch upcoming events



## 🧪 Quick Start

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/yourusername/hackradar.git
cd hackradar
python3 -m venv .venv
source .venv/bin/activate
uv sync
```

### 2. Run scraper to populate the DB

```bash
python tasks/fetch_and_store.py
```

### 3. Launch the API server

```bash
uvicorn backend.main:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


## 📖 API Docs

### `GET /hackathons`

Returns a list of upcoming hackathons.

#### Query Params:

* `from_date`: (optional) Filter by start date
* `to_date`: (optional) Filter by end date

#### Response:

```json
[
  {
    "id": "hack1",
    "title": "Hack the Future",
    "start_date": "2025-08-01",
    "end_date": "2025-08-03",
    "location": "Remote",
    "url": "https://devpost.com/hackthefuture",
    "source": "devpost",
    "tags": ["AI", "Web", "Blockchain"]
  }
]
```


## 🛣️ Roadmap

* ⏳ Add MLH, Unstop, Devfolio scrapers
* 📅 Add periodic cron scraping
* 📤 Deploy API to Render/Railway
* 🤖 Integrate with WhatsApp bot (HackAlertBot)

## 🤝 Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) guide to get started.

---

