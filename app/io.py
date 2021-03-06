#!/usr/bin/python
import time
import logging
from RPi import GPIO
from lib.config import config


###################################################################################################
class IO_BASE(object):
    PINS = config["pins"]

    #----------------------------------------------------------------------------------------------
    def __init__(self, GPIO):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.GPIO = GPIO
        self.OPEN_PIN = GPIO.LOW
        self.CLOSE_PIN = GPIO.HIGH


    #----------------------------------------------------------------------------------------------
    def open(self, pin_id):
        self.change_pin_status(pin_id, self.OPEN_PIN)


    #----------------------------------------------------------------------------------------------
    def close(self, pin_id):
        self.change_pin_status(pin_id, self.CLOSE_PIN)


    #----------------------------------------------------------------------------------------------
    def temp_open(self, pin_id, quantity):
        seconds = float(quantity) * self.RESOURCES.get(pin_id, 0)
        self.open(pin_id)
        time.sleep(seconds)
        self.close(pin_id)
        return seconds


    #----------------------------------------------------------------------------------------------
    def change_pin_status(self, pin_id, required_status):
        status = "PORNESTE" if required_status==self.OPEN_PIN else "OPRESTE"
        logging.warning("{} {}".format(status, pin_id))
        pin = self.PINS.get(pin_id)
        if pin is None:
            return

        if self.status(pin) != required_status:
            self.GPIO.output(pin, required_status)
            time.sleep(0.6)


    #----------------------------------------------------------------------------------------------
    def status(self, pin):
        try:
            return self.GPIO.input(pin)
        except:
            self.GPIO.setup(pin, self.GPIO.OUT)
            return self.GPIO.input(pin)


    #----------------------------------------------------------------------------------------------
    def set_pins(self, statuses):
        for pin_id, status in statuses.iteritems():
            self.open(pin_id) if status else self.close(pin_id)


IO = IO_BASE(GPIO)
