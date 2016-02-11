import time
import requests
from datetime import datetime
from flask import request, redirect, url_for

from app.io import IO
from app.temperature import read_temp
from lib.config import config
from lib.helpers import Process
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
def force_close():
    Process.force_close()
    return "Inchis fortat"


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
    return str(read_temp())


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
    am = ConfigTemperatura.get("am")
    pm = ConfigTemperatura.get("pm")
    date = datetime.now()
    este_zi = date.replace(hour=am.ora) < date < date.replace(hour=pm.ora)
    if este_zi:
        temp = am.temperature
    else:
        temp = pm.temperature

    senzor_temp = read_temp()

    if senzor_temp < temp - 0.2:
        Process.start()
    elif senzor_temp > temp - 0.2:
        Process.stop()
    else:
        Process.run()

    return "pins reloaded"

#-------------------------------------------------------------------------------------------------
def edit_pins():
    if request.method == "GET":
        values = ConfigTemperatura.get_all()
        return """
            <h1 style='color:blue'>Hello Simon!</h1>
            <form action="/edit_pins" method="post">
                <table>
                <tr>
                    <td>Temperatura Ziua: </td>
                    <td><input type="number" name="t_am" value="{}"></td>
                </tr>
                <tr>
                    <td>Ziua incepe la:</td>
                    <td><input type="number" name="h_am" value="{}"></td>
                </tr>
                <tr>
                </tr>
                <tr>
                    <td>Temperatura Noaptea:</td>
                    <td><input type="number" name="t_pm" value="{}"></td>
                </tr>
                <tr>
                    <td>Noaptea incepe la:</td>
                    <td><input type="number" name="h_pm" value="{}"></td>
                </tr>
                </table>
                <input type="submit" value="Salveaza">
            </form>
        """.format(values.get("am", {}).get("temp", ""),
                   values.get("am", {}).get("ora", ""),
                   values.get("pm", {}).get("temp", ""),
                   values.get("pm", {}).get("ora", ""))
    else:
        params = request.values.to_dict()
        ConfigTemperatura.save(params)

        return redirect(url_for('edit_pins'))





