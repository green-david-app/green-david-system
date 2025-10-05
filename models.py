from fastapi import FastAPI, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from sqlmodel import Session, select
from database import init_db, get_session
from models import Employee as Zamestnanec, Project as Zakazka, Task as Ukol, Item as Položka, StockMove as Pohyb, Timesheet as Dochazka
from stock_utils import recalc_on_hand

# 🔐 API klíč
API_KEY = "demo-secret-key"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def over_api_klic(x_api_key: str = Depends(api_key_header)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Neplatný nebo chybějící API klíč")

# 🧩 Inicializace aplikace
app = FastAPI(
    title="Systém zakázek, skladu a zaměstnanců",
    description="Interní webové rozhraní pro správu zakázek, úkolů, skladu, zaměstnanců a odpracovaných hodin.",
    version="1.0 (CZ)"
)

@app.on_event("startup")
def inicializace():
    init_db()

@app.get("/stav")
def stav():
    return {"stav": "v pořádku"}


# 🧑‍🤝‍🧑 Zaměstnanci
@app.post("/zamestnanci", dependencies=[Depends(over_api_klic)])
def vytvor_zamestnance(zam: Zamestnanec, session: Session = Depends(get_session)):
    session.add(zam)
    session.commit()
    session.refresh(zam)
    return zam

@app.get("/zamestnanci", dependencies=[Depends(over_api_klic)])
def seznam_zamestnancu(session: Session = Depends(get_session)):
    return session.exec(select(Zamestnanec)).all()


# 🧾 Zakázky
@app.post("/zakazky", dependencies=[Depends(over_api_klic)])
def vytvor_zakazku(zak: Zakazka, session: Session = Depends(get_session)):
    session.add(zak)
    session.commit()
    session.refresh(zak)
    return zak

@app.get("/zakazky", dependencies=[Depends(over_api_klic)])
def seznam_zakazek(session: Session = Depends(get_session)):
    return session.exec(select(Zakazka)).all()


# 📋 Úkoly
@app.post("/ukoly", dependencies=[Depends(over_api_klic)])
def vytvor_ukol(ukol: Ukol, session: Session = Depends(get_session)):
    session.add(ukol)
    session.commit()
    session.refresh(ukol)
    return ukol

@app.get("/ukoly", dependencies=[Depends(over_api_klic)])
def seznam_ukolu(session: Session = Depends(get_session)):
    return session.exec(select(Ukol)).all()


# 📦 Položky (sklad)
@app.post("/polozky", dependencies=[Depends(over_api_klic)])
def vytvor_polozku(pol: Položka, session: Session = Depends(get_session)):
    session.add(pol)
    session.commit()
    session.refresh(pol)
    return pol

@app.get("/polozky", dependencies=[Depends(over_api_klic)])
def seznam_polozek(session: Session = Depends(get_session)):
    return session.exec(select(Položka)).all()


# 🚚 Pohyby skladu
@app.post("/pohyby", dependencies=[Depends(over_api_klic)])
def vytvor_pohyb(poh: Pohyb, session: Session = Depends(get_session)):
    session.add(poh)
    session.commit()
    session.refresh(poh)
    recalc_on_hand(session, poh.item_id)
    return poh

@app.get("/pohyby", dependencies=[Depends(over_api_klic)])
def seznam_pohybu(session: Session = Depends(get_session)):
    return session.exec(select(Pohyb)).all()


# 🕒 Docházka / odpracované hodiny
@app.post("/dochazka", dependencies=[Depends(over_api_klic)])
def zaznam_dochazky(d: Dochazka, session: Session = Depends(get_session)):
    session.add(d)
    session.commit()
    session.refresh(d)
    return d

@app.get("/dochazka", dependencies=[Depends(over_api_klic)])
def seznam_dochazky(session: Session = Depends(get_session)):
    return session.exec(select(Dochazka)).all()
