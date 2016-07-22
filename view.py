"""
views.py
"""

from flask import render_template, request, redirect, url_for

from app import app
import models as md
from forms import CombinedForm
import foregroundController as fc

@app.route("/nearby")
def show_status():
    pokedata = fc.generate_pokemon_list()
    return render_template("nearby.html", pokedata=pokedata)

@app.route('/parameters', methods=['GET', 'POST'])
def adjust_search_parameters():
    try:
        current_num_steps, (current_latitude, current_longitude) = md.WebQuery.get_query()
    except md.WebQuery.DoesNotExist:
        current_num_steps, (current_latitude, current_longitude) = None, (None, None)
    errors = None
    form = CombinedForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            num_steps = request.form["step_num"]
            latitude = request.form["latitude"]
            longitude = request.form["longitude"]
            fc.set_webquery(num_steps, (latitude, longitude))
            return redirect(url_for('adjust_search_parameters'))
        else:
            return render_template("parameters.html",
                                   form=form,
                                   num_steps=current_num_steps,
                                   latitude=current_latitude,
                                   longitude=current_longitude,
                                   errors=errors)

    return render_template("parameters.html",
                           form=form,
                           num_steps=current_num_steps,
                           latitude=current_latitude,
                           longitude=current_longitude,
                           errors=errors)
