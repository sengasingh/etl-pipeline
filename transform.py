# transform.py
from typing import Dict, Optional, Tuple
# slot => ordering hint from PokeAPI; tells which type/ability comes first (primary/regular) vs later (secondary/hidden)

def _types(raw: Dict) -> Tuple[Optional[str], Optional[str]]:
    # types: list of { slot: 1.., type: { name } }
    slots = sorted(raw.get("types", []), key=lambda t: t.get("slot", 999))
    primary = slots[0]["type"]["name"] if len(slots) >= 1 else None
    secondary = slots[1]["type"]["name"] if len(slots) >= 2 else None
    return primary, secondary

def _first_ability(raw: Dict) -> Optional[str]:
    # abilities: list of { slot, ability: { name }, is_hidden }
    abilities = raw.get("abilities", [])
    if not abilities:
        return None
    first = sorted(abilities, key=lambda a: a.get("slot", 999))[0]
    return first.get("ability", {}).get("name")

def _sprite_url(raw: Dict) -> Optional[str]:
    # Prefer official artwork; fallback to front_default
    sprites = raw.get("sprites", {}) or {}
    other = sprites.get("other", {}) or {}
    official = (other.get("official-artwork", {}) or {}).get("front_default")
    return official or sprites.get("front_default")

def _cry_url(raw: Dict) -> Optional[str]:
    cries = raw.get("cries", {}) or {}
    return cries.get("latest") or cries.get("legacy")

def _stats(raw: Dict) -> Dict[str, Optional[int]]:
    # stats: [{ base_stat, stat: { name } }, ...]
    name_map = {
        "hp": "hp",
        "attack": "attack",
        "defense": "defense",
        "special-attack": "special_attack",
        "special-defense": "special_defense",
        "speed": "speed",
    }
    out = {v: None for v in name_map.values()}
    for s in raw.get("stats", []):
        key = s.get("stat", {}).get("name")
        if key in name_map:
            out[name_map[key]] = s.get("base_stat")
    return out

def transform_pokemon(raw: Dict) -> Dict:
    ptype1, ptype2 = _types(raw)
    stats = _stats(raw)
    return {
        "id": raw.get("id"),
        "name": raw.get("name"),
        "height_dm": raw.get("height"),
        "weight_hg": raw.get("weight"),
        "base_experience": raw.get("base_experience"),
        "primary_type": ptype1,
        "secondary_type": ptype2,
        "first_ability": _first_ability(raw),
        "sprite_url": _sprite_url(raw),
        "cry_url": _cry_url(raw),
        **stats,  # hp, attack, defense, special_attack, special_defense, speed
    }
