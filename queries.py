# queries.py
from typing import Iterable, Optional
from sqlalchemy import select, func, desc, asc, or_
from sqlalchemy.orm import Session
from load import get_engine
from models import Pokemon

def get_session(db_url: str = "sqlite:///pokemon.db") -> Session:
    engine = get_engine(db_url)
    return Session(engine)

def search_by_name(substring: str, limit: int = 20):
    pattern = f"%{substring}%"
    with get_session() as s:
        stmt = (
            select(Pokemon.id, Pokemon.name, Pokemon.primary_type, Pokemon.secondary_type)
            .where(Pokemon.name.like(pattern))
            .order_by(asc(Pokemon.name))
            .limit(limit)
        )
        return s.execute(stmt).all()

def by_type(type_name: str, limit: int = 50):
    with get_session() as s:
        stmt = (
            select(Pokemon.id, Pokemon.name, Pokemon.speed, Pokemon.primary_type, Pokemon.secondary_type)
            .where(or_(Pokemon.primary_type == type_name, Pokemon.secondary_type == type_name))
            .order_by(desc(Pokemon.speed), asc(Pokemon.id))
            .limit(limit)
        )
        return s.execute(stmt).all()

def fastest(limit: int = 10, only_type: Optional[str] = None):
    with get_session() as s:
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.speed)
        if only_type:
            stmt = stmt.where(or_(Pokemon.primary_type == only_type, Pokemon.secondary_type == only_type))
        stmt = stmt.order_by(desc(Pokemon.speed), asc(Pokemon.id)).limit(limit)
        return s.execute(stmt).all()

def stat_range(min_speed: int = 0, min_attack: int = 0, min_hp: int = 0, limit: int = 50):
    with get_session() as s:
        stmt = (
            select(Pokemon.id, Pokemon.name, Pokemon.hp, Pokemon.attack, Pokemon.speed)
            .where(Pokemon.speed >= min_speed, Pokemon.attack >= min_attack, Pokemon.hp >= min_hp)
            .order_by(desc(Pokemon.speed))
            .limit(limit)
        )
        return s.execute(stmt).all()

def count_by_primary_type():
    with get_session() as s:
        stmt = (
            select(Pokemon.primary_type, func.count().label("n"))
            .group_by(Pokemon.primary_type)
            .order_by(desc("n"))
        )
        return s.execute(stmt).all()

def avg_stats_by_type():
    with get_session() as s:
        stmt = (
            select(
                Pokemon.primary_type.label("type"),
                func.avg(Pokemon.hp).label("avg_hp"),
                func.avg(Pokemon.attack).label("avg_attack"),
                func.avg(Pokemon.speed).label("avg_speed"),
            )
            .group_by(Pokemon.primary_type)
            .order_by(asc("type"))
        )
        return s.execute(stmt).all()
