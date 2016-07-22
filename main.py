#!/usr/bin/env python2

import app.search as ps
import app.utils as utils
import app.Args as Args
from geopy.distance import distance

def get_nearby_pokemon(position, num_steps, logged_in = False):
    if not logged_in:
        ps.login(Args.args, position)
    map_details = ps.search(position, num_steps, Args.args)
    observed_pokemon = []
    for cell in map_details:
        pokemon_cell, _, _ = cell
        if pokemon_cell:
            for key in pokemon_cell:
                observed_pokemon.append(pokemon_cell[key])
    return observed_pokemon

def get_distance_to_pokemon(position, pokemon):
    pokemon_position = pokemon["latitude"], pokemon["longitude"]
    return distance(position, pokemon_position).m

def print_listing(observed_pokemon, position, pokenames):
    for pokemon in observed_pokemon:
        pokeid = pokemon["pokemon_id"]
        name = pokenames[pokeid]
        print("{0}: {1}".format(pokeid, name))
        print("{0} m".format(get_distance_to_pokemon(position, pokemon)))
        print("")

def main():
    pokenames = utils.load_pokemon_names("static/pokemon_names.data")
    position = (51, 0, 0)
    num_steps = 5
    observed_pokemon = get_nearby_pokemon(position, num_steps)
    print_listing(observed_pokemon, position, pokenames)

if __name__=="__main__":
    main()
