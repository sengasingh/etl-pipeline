# load.py
from typing import Iterable, Dict
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base, Pokemon

def get_engine(db_url: str = "sqlite:///pokemon.db"):
    return create_engine(db_url, echo=False, future=True)

def init_db(engine):
    Base.metadata.create_all(engine)

def load_pokemon(engine, rows: Iterable[Dict]) -> int:
    count = 0
    with Session(engine) as session:
        for row in rows:
            if not row.get("id") or not row.get("name"):
                continue
            obj = session.get(Pokemon, row["id"])
            if obj is None:
                obj = session.scalar(select(Pokemon).where(Pokemon.name == row["name"]))
            if obj is None:
                # Pokemon(**row) => builds a mapped Python object (keys in row MUST match model attributes)
                # session.add(obj) => marks it “pending”
                session.add(Pokemon(**row))
            else:
                for k, v in row.items():
                    setattr(obj, k, v)
            count += 1
        session.commit()
    return count
