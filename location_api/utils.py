"""
Utilities
"""

def load_pokemon_names(filename):
    pokenames = {}
    for line in open(filename):
        poke_id, name = line.strip().split(", ")
        pokenames[int(poke_id)] = name
    return pokenames

def get_name(pokeid, pokenames):
    return pokenames, pokeid
