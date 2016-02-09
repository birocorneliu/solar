import time
import requests
from flask import request, redirect, url_for

from app.io import IO
from app.cron import Cron
from app.temperature import read_temp
from lib.config import config
from lib.helpers import get_statuses, get_times
from lib.db import TempCommands, session, ConfigTemperatura

#-------------------------------------------------------------------------------------------------
def home():
    return "<h1 style='color:blue'>Hello There!</h1>"


#-------------------------------------------------------------------------------------------------
def open_pin(pin_id):

    obj = TempCommands.add_entry({pin_id: True})
    IO.open(pin_id)
    return "<h1 style='color:blue'>Hello There, {}</h1>".format(pin_id)


#-------------------------------------------------------------------------------------------------
def close_pin(pin_id):
    obj = TempCommands.add_entry({pin_id: False})
    IO.close(pin_id)
    return "<h1 style='color:blue'>Hello There, {}</h1>".format(pin_id)


#-------------------------------------------------------------------------------------------------
def set_times_to_cron():
    times = Cron.set_times()
    return str(times)


#-------------------------------------------------------------------------------------------------
def temperature():
    if request.method == "GET":
        return str(read_temp())
    else:
        temp = read_temp()
        data = {"temperature": temp}
        response = requests.post("http://aquanet.ro/temperature", data=data )

        return response.content


#-------------------------------------------------------------------------------------------------
def get_temperatures():
    response = requests.get("http://aquanet.ro/temperature")
    return response.content


#--------------------------------------------------------------------------------------------------
def doser(pin_id, quantity):
    seconds = IO.temp_open(pin_id, quantity)
    return "just dosed '{}' for {} seconds".format(pin_id, seconds)


#--------------------------------------------------------------------------------------------------
def reload_pins():
    Procedure.run()
    statuses = get_statuses()
    obj = TempCommands.get()
    if obj is not None:
        statuses.update(obj.statuses)
    IO.set_pins(statuses)

    return str(statuses)


#-------------------------------------------------------------------------------------------------
def edit_pins():
    if request.method == "GET":
        values = ConfigTemperatura.get_all()
        return """
            <h1 style='color:blue'>Hello There!</h1>
            <form action="/edit_pins" method="post">
                Temperatura Ziua: <input type="text" name="t_am" value="{}"><br>
                Temperatura Noaptea: <input type="text" name="t_pm" value="{}"><br>
                <input type="submit" value="Salveaza">
            </form>
        """.format(values.get("t_am", ""), values.get("t_pm", ""))
    else:
        params = request.values.to_dict()
        ConfigTemperatura.save(params)

        return redirect(url_for('edit_pins'))





