# EventHub

Web app full-stack per gestione eventi culturali con backend Flask e frontend Angular.

## Stack
- Backend: Flask, SQLAlchemy, Flask-Migrate, JWT, Marshmallow
- Frontend: Angular standalone + routing lazy + guard + interceptor
- DB: SQLite (sviluppo), facilmente estendibile a PostgreSQL
- Async: threading per email conferma prenotazione

## Funzionalità incluse
- Area pubblica: lista eventi, ricerca base per categoria/città, dettaglio evento
- Auth JWT: register/login/refresh token
- Area utente: iscrizione evento con controllo posti, tickets con payload QR, recensioni post-evento
- Area organizer/admin: CRUD base evento (create + listing), dashboard metriche, export iscritti CSV
- Area admin: gestione utenti + promozione organizer + recensioni segnalate

## Setup Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app run.py db init
flask --app run.py db migrate -m "init"
flask --app run.py db upgrade
python run.py
```
API: `http://localhost:5000`

## Setup Frontend
```bash
cd frontend
npm install
npm start
```
UI: `http://localhost:4200`

## Docker Compose
```bash
cp .env.example .env
docker compose up --build
```

## Test backend (pytest)
```bash
cd backend
pytest -q
```

## OpenAPI
Spec disponibile in `backend/openapi.yaml`.

## Note sicurezza
- Usa `.env` locale (non committare segreti)
- JWT con token access + refresh
- Guardie ruolo lato frontend e decoratori ruolo lato backend
