# models.py
from typing import Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Pokemon(Base):
    __tablename__ = "pokemon"
    # adding indexes for faster querying:
    '''
    __table_args__ = (
        Index("ix_pokemon_primary_type", "primary_type"),
        Index("ix_pokemon_secondary_type", "secondary_type"),
        Index("ix_pokemon_speed", "speed"),
    )
    '''

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), index=True, unique=True)

    # raw units from PokeAPI (decimeters / hectograms)
    height_dm: Mapped[Optional[int]]
    weight_hg: Mapped[Optional[int]]

    base_experience: Mapped[Optional[int]]

    primary_type: Mapped[Optional[str]] = mapped_column(String(30))
    secondary_type: Mapped[Optional[str]] = mapped_column(String(30))
    first_ability: Mapped[Optional[str]] = mapped_column(String(50))

    sprite_url: Mapped[Optional[str]] = mapped_column(String(300))
    cry_url: Mapped[Optional[str]] = mapped_column(String(300))

    # core stats
    hp: Mapped[Optional[int]] = mapped_column(Integer)
    attack: Mapped[Optional[int]] = mapped_column(Integer)
    defense: Mapped[Optional[int]] = mapped_column(Integer)
    special_attack: Mapped[Optional[int]] = mapped_column(Integer)
    special_defense: Mapped[Optional[int]] = mapped_column(Integer)
    speed: Mapped[Optional[int]] = mapped_column(Integer)
