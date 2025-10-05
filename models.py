from __future__ import annotations
from typing import Optional, Literal
from datetime import datetime, date, time
from sqlmodel import SQLModel, Field

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    role: Optional[str] = None
    active: bool = True

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    customer: Optional[str] = None
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    status: Literal["nové","probíhá","pozastaveno","dokončeno"] = "nové"
    notes: Optional[str] = None

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    title: str
    description: Optional[str] = None
    assignee_id: Optional[int] = Field(default=None, foreign_key="employee.id")
    due_date: Optional[date] = None
    status: Literal["todo","doing","done"] = "todo"

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sku: str
    name: str
    unit: str = "ks"
    min_stock: float = 0.0
    on_hand: float = 0.0  # denormalized for quick overview (updated via stock movements)

class StockMove(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    move_type: Literal["prijem","vydej","presun"] = "prijem"
    quantity: float
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")  # optional linking to zakázka
    ref: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Timesheet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    project_id: int = Field(foreign_key="project.id")
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    date: date
    hours: float
    notes: Optional[str] = None
