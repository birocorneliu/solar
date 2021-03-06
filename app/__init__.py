from .endpoints import *

ROUTES = (
    (["GET"], "/", home),
    (["GET"], "/reload_pins", reload_pins),
    (["GET"], "/temperatura", temperature),
    (["GET"], "/pin/<pin_id>/open", open_pin),
    (["GET"], "/pin/<pin_id>/close", close_pin),
    (["GET"], "/force_close", force_close),
    (["GET", "POST"], "/edit_pins", edit_pins),

    (["GET"], "/get_temperatures", get_temperatures),
    (["GET", "POST"], "/temperature", temperature),
)


#from app.cron import Cron
#Set CronTab
#Cron.clean_cron()
#Cron.set_times()
