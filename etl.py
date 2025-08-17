# etl_pokemon.py
from extract import extract_pokemon_batch, extract_pokemon_by_names
from transform import transform_pokemon
from load import get_engine, init_db, load_pokemon

def run_batch(limit=30, offset=0):
    raw_list = extract_pokemon_batch(limit=limit, offset=offset)
    rows = [transform_pokemon(raw) for raw in raw_list]
    engine = get_engine("sqlite:///pokemon.db")
    init_db(engine)
    print(f"Upserted {load_pokemon(engine, rows)} rows")

def run_names(names):
    raw_list = extract_pokemon_by_names(names)
    rows = [transform_pokemon(raw) for raw in raw_list]
    engine = get_engine("sqlite:///pokemon.db")
    init_db(engine)
    print(f"Upserted {load_pokemon(engine, rows)} rows")

if __name__ == "__main__":
    # Example: just Greninja
    run_names(["greninja"])
    # Or: a page
    # run_batch(limit=50, offset=0)
