import os.path
import pickle
import logging
from datetime import datetime, timedelta

from app.io import IO
from lib.config import config



###############################################################################
class ProcessBase(object):
    PATH = "/tmp/solar_data"
    START_PINS = ["pompa", "ventilator", "incalzitor"]
    STOP_PINS = ["incalzitor", "ventilator", "pompa"]


    #--------------------------------------------------------------------------
    def __init__(self):
        self.required_status = IO.CLOSE_PIN
        self.next_pins = []
        self.next_operation_time = datetime.now()


    @classmethod
    #--------------------------------------------------------------------------
    def load(cls):
        if os.path.exists(cls.PATH):
            try:
                date = datetime.fromtimestamp(os.path.getmtime(cls.PATH))
                expire_date = date + timedelta(seconds=config["class_expire_time"])
                if expire_date > datetime.now():
                    return pickle.load(open(cls.PATH))
            except:
                pass

        return cls()


    #--------------------------------------------------------------------------
    def dump(self):
        pickle.dump(self, open(self.PATH, "wb"))


    #--------------------------------------------------------------------------
    def start(self):
        if self.required_status != IO.OPEN_PIN:
            self.required_status = IO.OPEN_PIN
            self.next_pins = self.START_PINS[:]
        self.run()


    #--------------------------------------------------------------------------
    def stop(self):
        if self.required_status != IO.CLOSE_PIN:
            self.required_status = IO.CLOSE_PIN
            self.next_pins = self.STOP_PINS[:]
            self.run(mandatory=True)
        else:
            self.run()


    #--------------------------------------------------------------------------
    def force_close(self):
        self.required_status = IO.CLOSE_PIN
        self.next_pins = self.STOP_PINS[:]
        self.run(mandatory=True, seconds=config["time_for_force_close"])


    #--------------------------------------------------------------------------
    def run(self, mandatory=False, seconds=config["time_betwen_actions"]):
        if len(self.next_pins) == 0:
            return

        logging.warning(str(self.next_pins))
        if mandatory:
            pin_id = self.next_pins.pop(0)
            IO.change_pin_status(pin_id, self.required_status)
            self.next_operation_time = datetime.now() + timedelta(seconds=seconds)

        elif self.next_operation_time < datetime.now():
            self.run(mandatory=True)

        self.dump()


Process = ProcessBase.load()
