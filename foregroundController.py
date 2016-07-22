"""
foregroundController.py
"""

import models
from datetime import datetime, timedelta
from app import POKEMON_NAME_LIST
from location_api.utils import load_pokemon_names
from geopy.distance import distance

def set_webquery(num_steps, position):
    models.WebQuery.set_query(num_steps, position)

def generate_location_url(position):
    lat,lng = position
    return "http://www.google.com/maps/place/{0},{1}".format(lat, lng)

def generate_pokemon_list():
    pokemon_name_dict = load_pokemon_names(POKEMON_NAME_LIST)
    to_display = []
    _, current_location = models.WebQuery.get_query()
    for pokemon in models.Pokemon.select():
        if pokemon.disappear_time > datetime.utcnow():
            pokedata = {}
            pokedata["pokemon_id"] = pokemon.pokemon_id
            pokedata["pokemon_name"] = pokemon_name_dict[pokemon.pokemon_id]
            pokedata["location"] = (pokemon.latitude, pokemon.longitude)
            pokedata["disappear_time"] = pokemon.disappear_time + timedelta(hours=5, minutes=30)
            pokedata["distance"] = round(distance(pokedata["location"], current_location).m)
            pokedata["url"] = generate_location_url(pokedata["location"])
            to_display.append(pokedata)
    return to_display

