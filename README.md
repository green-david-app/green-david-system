# Zakázky & Sklad API (CZ)

Jednoduché **vše‑v‑jednom** API pro:
- **Zakázky (projekty)**
- **Úkoly**
- **Hodiny (timesheety)**
- **Zaměstnance**
- **Materiál (položky)**
- **Skladové pohyby** (příjem / výdej / přesun)

Postaveno na **FastAPI + SQLModel + SQLite**. Připraveno pro nasazení do cloudu (Render, Fly.io, Railway, apod.).

## Rychlý start (lokálně)

1) Vytvoř a aktivuj virtuální prostředí (volitelné)  
2) Nainstaluj závislosti:
```
pip install -r requirements.txt
```
3) Spusť server:
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
4) Otevři dokumentaci (Swagger):  
`http://localhost:8000/docs`

> **Autorizace:** do každého požadavku přidej HTTP hlavičku `X-API-Key: demo-secret-key`

## Základní entity

- **Employees** `/employees`
- **Projects** `/projects`
- **Tasks** `/tasks`
- **Items** `/items`
- **Stock Moves** `/stock_moves`
- **Timesheets** `/timesheets`

## Seed dat
Pro rychlý test volej:
```
POST /seed
Header: X-API-Key: demo-secret-key
```

## Poznámky
- `on_hand` u položek se přepočítává podle pohybů skladu.
- Pro jednoduchost je sklad bez lokací. Lze rozšířit (sklady, přenosy, rezervace na zakázku).
- Lze přidat autentizaci přes JWT, uživatelské role a detailní oprávnění.

## Nasazení do cloudu
- Lze nasadit na Render/Fly.io/Railway. Potřebuje Python runtime.
- Pro produkci doporučeno PostgreSQL (změnit `DATABASE_URL` v `database.py`).

---

Vytvořil ChatGPT pro rychlý pilot pro zahradnickou firmu.
