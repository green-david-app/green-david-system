from sqlmodel import Session, select
from models import Item, StockMove

def recalc_on_hand(session: Session, item_id: int):
    q = select(StockMove).where(StockMove.item_id == item_id)
    moves = session.exec(q).all()
    total = 0.0
    for m in moves:
        if m.move_type == "prijem":
            total += m.quantity
        elif m.move_type == "vydej":
            total -= m.quantity
        elif m.move_type == "presun":
            total += 0  # no-op for simple demo; could handle warehouse locations later
    item = session.get(Item, item_id)
    if item:
        item.on_hand = total
        session.add(item)
        session.commit()
        session.refresh(item)
    return total
