from fastapi import FastAPI, Depends, HTTPException
from typing import List, Optional
from sqlmodel import select
from database import init_db, get_session
from sqlmodel import Session
from models import Employee, Project, Task, Item, StockMove, Timesheet
from auth import api_key_guard
from stock_utils import recalc_on_hand

app = FastAPI(title="Zakázky & Sklad API", description="Jednoduché API pro zakázky, úkoly, hodiny, zaměstnance a sklad (CZ)", version="0.1.0")

@app.on_event("startup")
def on_startup():
    init_db()

# Health
@app.get("/health")
async def health():
    return {"status": "ok"}

# --- Employees ---
@app.post("/employees", response_model=Employee, dependencies=[Depends(api_key_guard)])
def create_employee(emp: Employee, session: Session = Depends(get_session)):
    emp.id = None
    session.add(emp)
    session.commit()
    session.refresh(emp)
    return emp

@app.get("/employees", response_model=List[Employee], dependencies=[Depends(api_key_guard)])
def list_employees(session: Session = Depends(get_session)):
    return session.exec(select(Employee)).all()

@app.get("/employees/{emp_id}", response_model=Employee, dependencies=[Depends(api_key_guard)])
def get_employee(emp_id: int, session: Session = Depends(get_session)):
    emp = session.get(Employee, emp_id)
    if not emp:
        raise HTTPException(404, "Employee not found")
    return emp

@app.patch("/employees/{emp_id}", response_model=Employee, dependencies=[Depends(api_key_guard)])
def update_employee(emp_id: int, data: Employee, session: Session = Depends(get_session)):
    emp = session.get(Employee, emp_id)
    if not emp:
        raise HTTPException(404, "Employee not found")
    update = data.model_dump(exclude_unset=True)
    for k, v in update.items():
        setattr(emp, k, v)
    session.add(emp)
    session.commit()
    session.refresh(emp)
    return emp

@app.delete("/employees/{emp_id}", dependencies=[Depends(api_key_guard)])
def delete_employee(emp_id: int, session: Session = Depends(get_session)):
    emp = session.get(Employee, emp_id)
    if not emp:
        raise HTTPException(404, "Employee not found")
    session.delete(emp)
    session.commit()
    return {"ok": True}

# --- Projects ---
@app.post("/projects", response_model=Project, dependencies=[Depends(api_key_guard)])
def create_project(p: Project, session: Session = Depends(get_session)):
    p.id = None
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

@app.get("/projects", response_model=List[Project], dependencies=[Depends(api_key_guard)])
def list_projects(session: Session = Depends(get_session)):
    return session.exec(select(Project)).all()

@app.get("/projects/{pid}", response_model=Project, dependencies=[Depends(api_key_guard)])
def get_project(pid: int, session: Session = Depends(get_session)):
    p = session.get(Project, pid)
    if not p:
        raise HTTPException(404, "Project not found")
    return p

@app.patch("/projects/{pid}", response_model=Project, dependencies=[Depends(api_key_guard)])
def update_project(pid: int, data: Project, session: Session = Depends(get_session)):
    p = session.get(Project, pid)
    if not p:
        raise HTTPException(404, "Project not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

@app.delete("/projects/{pid}", dependencies=[Depends(api_key_guard)])
def delete_project(pid: int, session: Session = Depends(get_session)):
    p = session.get(Project, pid)
    if not p:
        raise HTTPException(404, "Project not found")
    session.delete(p)
    session.commit()
    return {"ok": True}

# --- Tasks ---
@app.post("/tasks", response_model=Task, dependencies=[Depends(api_key_guard)])
def create_task(t: Task, session: Session = Depends(get_session)):
    t.id = None
    session.add(t)
    session.commit()
    session.refresh(t)
    return t

@app.get("/tasks", response_model=List[Task], dependencies=[Depends(api_key_guard)])
def list_tasks(project_id: Optional[int] = None, session: Session = Depends(get_session)):
    q = select(Task)
    if project_id is not None:
        q = q.where(Task.project_id == project_id)
    return session.exec(q).all()

@app.patch("/tasks/{tid}", response_model=Task, dependencies=[Depends(api_key_guard)])
def update_task(tid: int, data: Task, session: Session = Depends(get_session)):
    t = session.get(Task, tid)
    if not t:
        raise HTTPException(404, "Task not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(t, k, v)
    session.add(t)
    session.commit()
    session.refresh(t)
    return t

@app.delete("/tasks/{tid}", dependencies=[Depends(api_key_guard)])
def delete_task(tid: int, session: Session = Depends(get_session)):
    t = session.get(Task, tid)
    if not t:
        raise HTTPException(404, "Task not found")
    session.delete(t)
    session.commit()
    return {"ok": True}

# --- Items ---
@app.post("/items", response_model=Item, dependencies=[Depends(api_key_guard)])
def create_item(i: Item, session: Session = Depends(get_session)):
    i.id = None
    i.on_hand = 0.0
    session.add(i)
    session.commit()
    session.refresh(i)
    return i

@app.get("/items", response_model=List[Item], dependencies=[Depends(api_key_guard)])
def list_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()

@app.patch("/items/{iid}", response_model=Item, dependencies=[Depends(api_key_guard)])
def update_item(iid: int, data: Item, session: Session = Depends(get_session)):
    i = session.get(Item, iid)
    if not i:
        raise HTTPException(404, "Item not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(i, k, v)
    session.add(i)
    session.commit()
    session.refresh(i)
    return i

@app.delete("/items/{iid}", dependencies=[Depends(api_key_guard)])
def delete_item(iid: int, session: Session = Depends(get_session)):
    i = session.get(Item, iid)
    if not i:
        raise HTTPException(404, "Item not found")
    session.delete(i)
    session.commit()
    return {"ok": True}

# --- Stock Moves ---
@app.post("/stock_moves", response_model=StockMove, dependencies=[Depends(api_key_guard)])
def create_stock_move(m: StockMove, session: Session = Depends(get_session)):
    m.id = None
    session.add(m)
    session.commit()
    session.refresh(m)
    # update item on_hand
    recalc_on_hand(session, m.item_id)
    return m

@app.get("/stock_moves", response_model=List[StockMove], dependencies=[Depends(api_key_guard)])
def list_stock_moves(item_id: Optional[int] = None, project_id: Optional[int] = None, session: Session = Depends(get_session)):
    q = select(StockMove)
    if item_id is not None:
        q = q.where(StockMove.item_id == item_id)
    if project_id is not None:
        q = q.where(StockMove.project_id == project_id)
    return session.exec(q).all()

# --- Timesheets ---
@app.post("/timesheets", response_model=Timesheet, dependencies=[Depends(api_key_guard)])
def create_timesheet(t: Timesheet, session: Session = Depends(get_session)):
    t.id = None
    session.add(t)
    session.commit()
    session.refresh(t)
    return t

@app.get("/timesheets", response_model=List[Timesheet], dependencies=[Depends(api_key_guard)])
def list_timesheets(project_id: Optional[int] = None, employee_id: Optional[int] = None, session: Session = Depends(get_session)):
    q = select(Timesheet)
    if project_id is not None:
        q = q.where(Timesheet.project_id == project_id)
    if employee_id is not None:
        q = q.where(Timesheet.employee_id == employee_id)
    return session.exec(q).all()

# --- Seed demo data ---
@app.post("/seed", dependencies=[Depends(api_key_guard)])
def seed(session: Session = Depends(get_session)):
    # add minimal data if empty
    if not session.exec(select(Employee)).first():
        e1 = Employee(name="Zahradník 1", role="technik")
        e2 = Employee(name="Zahradník 2", role="technik")
        e3 = Employee(name="Admin", role="vedoucí")
        session.add_all([e1, e2, e3])
        session.commit()
    if not session.exec(select(Project)).first():
        p1 = Project(name="Výsadba Kunice", customer="Obec Kunice", status="probíhá")
        p2 = Project(name="Rekonstrukce trávníku", customer="SVJ Bělohorská", status="nové")
        session.add_all([p1, p2])
        session.commit()
    if not session.exec(select(Item)).first():
        i1 = Item(sku="M-TRUB-16", name="Kapková hadice 16 mm", unit="m")
        i2 = Item(sku="H-HROT-40", name="Kotvící hrot 40 cm", unit="ks")
        session.add_all([i1, i2])
        session.commit()
    return {"ok": True}
