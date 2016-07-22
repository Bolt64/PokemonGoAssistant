"""
models.py
"""

from peewee import Model, SqliteDatabase, InsertQuery, IntegerField,\
                   CharField, FloatField, BooleanField, DateTimeField
from datetime import datetime

from app import db


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_all(cls):
        return [m for m in cls.select().dicts()]

class WebQuery(BaseModel):
    is_current = BooleanField()
    num_steps = IntegerField()
    source_latitude = FloatField()
    source_longitude = FloatField()

    @classmethod
    def get_query(cls):
        query = WebQuery.select().where(WebQuery.is_current).get()
        return (query.num_steps, (query.source_latitude, query.source_longitude))

    @classmethod
    def set_query(cls, num_steps, position):
        latitude, longitude = position
        with db.atomic():
            WebQuery.delete().execute()
            WebQuery.create(is_current=True,
                            num_steps = num_steps,
                            source_latitude=latitude,
                            source_longitude=longitude)


class Pokemon(BaseModel):
    # We are base64 encoding the ids delivered by the api
    # because they are too big for sqlite to handle
    encounter_id = CharField(primary_key=True)
    source_latitude = FloatField()
    source_longitude = FloatField()
    spawnpoint_id = CharField()
    pokemon_id = IntegerField()
    latitude = FloatField()
    longitude = FloatField()
    disappear_time = DateTimeField()

    @classmethod
    def get_active(cls):
        query = (Pokemon
                 .select()
                 .where(Pokemon.disappear_time > datetime.utcnow())
                 .dicts())

        pokemons = []
        for p in query:
            pokemons.append(p)

        return pokemons

    @classmethod
    def delete_inactive(cls):
        query = (Pokemon
                 .delete()
                 .where(Pokemon.disappear_time <= datetime.utcnow()))

        query.execute()

class Pokestop(BaseModel):
    pokestop_id = CharField(primary_key=True)
    source_latitude = FloatField()
    source_longitude = FloatField()
    enabled = BooleanField()
    latitude = FloatField()
    longitude = FloatField()
    last_modified = DateTimeField()
    lure_expiration = DateTimeField(null=True)
    active_pokemon_id = IntegerField(null=True)


def cleanup_db():
    _, (source_latitude, source_longitude) = WebQuery.get_query()

    # location_query = WebQuery.delete().where(\
                            # (WebQuery.source_latitude, WebQuery.source_longitude) !=\
                            # (source_latitude, source_longitude))
    # location_query.execute()

    pokemon_query = Pokemon.select().execute()
    for pokemon in pokemon_query:
        if (pokemon.source_latitude, pokemon.source_longitude) != (source_latitude, source_longitude):
            pokemon.delete_instance()

    Pokemon.delete_inactive()

    # pokestop_query = Pokestop.delete().where(\
                            # (Pokestop.source_latitude, Pokestop.source_longitude) !=\
                            # (source_latitude, source_longitude))
    # pokestop_query.execute()
