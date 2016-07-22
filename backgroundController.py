"""
backgroundController.py
"""

import models
import location_api.Args as Args # to deprecate
import location_api.search as search
from peewee import IntegrityError
from time import sleep

WAIT_TIME = 1

def get_webquery():
    return models.WebQuery.get_query()

def single_search_loop(num_steps, position):
    for cell in search.search(position, num_steps, Args.args):
        upsert_parsed_map(cell, position)

def search_loop():
    while True:
        webquery = get_webquery()
        models.cleanup_db()
        single_search_loop(*webquery)
        sleep(WAIT_TIME)

def upsert_parsed_map(parsed_map, source_location):
    source_latitude, source_longitude = source_location
    pokemons = []
    pokestops = []

    mons, stops, _ = parsed_map
    for i in mons:
        pokemons.append(mons[i])

    for i in stops:
        pokestops.append(stops[i])

    for pokemon in pokemons:
        pokemon["source_latitude"] = source_latitude
        pokemon["source_longitude"] = source_longitude

    for pokestop in pokestops:
        pokestop["source_latitude"] = source_latitude
        pokestop["source_longitude"] = source_longitude

    with models.db.atomic():
        for pokemon in pokemons:
            try:
                models.Pokemon.create(**pokemon)
            except IntegrityError:
                pass
        # models.Pokemon.insert_many(pokemons).execute()
        # models.Pokestop.insert_many(pokestops).execute()

    # for pokemon in pokemons:
        # print(pokemon["encounter_id"])
        # models.Pokemon.create(**pokemon)

    # for pokestop in pokestops:
        # print(pokestop["pokestop_id"])
        # models.Pokestop.create(**pokestop)

def test():
    import location_api.search as ps
    import location_api.Args as Args
    ps.login(Args.args, (51,0))
    for cell in ps.search((51,0), 5, Args.args):
        print("Upserting")
        upsert_parsed_map(cell, (51, 0))
