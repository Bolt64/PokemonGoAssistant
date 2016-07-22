#!/usr/bin/env python2

import models

def initiate_db():
    models.db.connect()
    models.db.create_tables([models.WebQuery, models.Pokemon, models.Pokestop])

if __name__=="__main__":
    initiate_db()
