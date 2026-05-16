# Country Info API

A FastAPI-based backend project that provides country statistics using scraped population data.

The API supports searching, ranking, comparing countries, and viewing population-related metrics.

---

## Features

- Scrapes country population data
- Stores data locally using SQLite
- Search countries by name
- Rank countries using different metrics
- Compare two countries
- Cleaned and normalized numeric data
- Typed API responses using Pydantic
- Interactive Swagger documentation

---

## Available Metrics

- population
- yearly_change
- net_change
- density
- land_area
- migrants
- fertility_rate
- median_age
- urban_pop
- world_share

---

## API Endpoints

### Get all countries

```http
GET /countries
```

### Get single country

```http
GET /countries/{name}
```

### Rank countries

```http
GET /countries/rank?metric=population&limit=10
```

### Compare countries

```http
GET /countries/compare?first=India&second=China
```

### Refresh dataset

```http
POST /countries/refresh
```

### API metadata

```http
GET /countries/info
```

---

## Swagger UI

![Swagger UI](assets/swagger.png)

---

## Tech Stack

- FastAPI
- SQLite
- BeautifulSoup
- Requests
- Pydantic

---

## Project Structure

```text
country-info-api/
│
├── main.py
├── db.py
├── scraper.py
├── schemas.py
│
├── routes/
│     └── countries.py
│
├── assets/
│     └── swagger.png
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn main:app --reload
```

Open Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

## Notes

- Data is scraped from Worldometer
- Some fields may contain missing values
- Country data changes very rarely
- Database is created automatically on first run
