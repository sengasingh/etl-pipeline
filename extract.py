# extract.py
import time
import requests
from typing import Dict, Iterable, List, Optional

POKEAPI_BASE = "https://pokeapi.co/api/v2"

def _get_json(url: str) -> Dict:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def extract_pokemon_batch(limit: int = 20, offset: int = 0, pause_s: float = 0.2) -> List[Dict]:
    # offset is the pokemon to start at => "extract next 50 (limit) pokemon starting at 200 (offset)"
    list_url = f"{POKEAPI_BASE}/pokemon?limit={limit}&offset={offset}"
    results = _get_json(list_url).get("results", [])
    details: List[Dict] = []
    for item in results:
        details.append(_get_json(item["url"]))
        time.sleep(pause_s)
    return details

def extract_pokemon_by_names(names: Iterable[str], pause_s: float = 0.2) -> List[Dict]:
    details: List[Dict] = []
    for name in names:
        url = f"{POKEAPI_BASE}/pokemon/{name}"
        details.append(_get_json(url))
        time.sleep(pause_s)
    return details
