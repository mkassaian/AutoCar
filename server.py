import sys
import signal

import logging
logging.basicConfig(level=logging.ERROR)

from flask import Flask
from flask import render_template
from flask import request
import RPi.GPIO as g
import time
from gpiozero import DistanceSensor, LED
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

def sigint_handler(signum, frame):
    print 'Killed...'
    g.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

u = DistanceSensor(echo = 12,trigger = 25)
v = DistanceSensor(echo = 5, trigger = 6)
w = DistanceSensor(echo = 23, trigger = 18)
l = LED(4)
m = LED(24)
m.on()
state = "FullS"
prev = "FullS"
testV = 1.5

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"]=0

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/forward", methods=['POST'])
def asdf():
    global state
    state = "go"
    l.on()
    return "f"

@app.route("/left", methods=['POST'])
def gjk():
    global state
    global prev
    prev = state
    state = "TL"
    l.on()
    return "l"

@app.route("/right", methods=['POST'])
def wety():
    global state
    global prev
    prev = state
    state = "TR"
    l.on()
    return "r"

@app.route("/stop", methods=['POST'])
def csdf():
    global state
    global prev
    state = "FullS"
    prev = "FullS"
    l.on()
    return "s"

@app.route("/reverse", methods=['POST'])
def ldkfgj():
    global state
    state="R"
    l.on()
    return "r"

@app.route("/poll", methods=['POST'])
def kdsjfhg():
    global state
    return "state: "+state+"\nu(front): "+str(u.distance)+"\nv(right): "+str(v.distance)+"\nw(left): "$

def updateCarOrientation():
    global state
    global testV
    global prev
    l.off()
    if state == "STOP":
        off1()
        off2()
        time.sleep(testV)
    if state is "TR":
        reverse1()
        forward2()
        time.sleep(testV)
        state = prev
    if state is "TL":
        reverse2()
        forward1()
        time.sleep(testV)
        state=prev
    if state is "go":
        forward1()
        forward2()
    if state is "FullS":
        off1()
        off2()
    if state is "R":
        reverse1()
        reverse2()

def checkSensors():
    global state
    global timer
    global prev
    prev = state
    print(state)
    if state is "STOP" and u.distance<.2:
        if (v.distance < .2 and u.distance<.2):
            state = "R"
        elif v.distance > w.distance:
            state = "TR"
        else:
            state = "TL"
    if u.distance < .2 and state is "go":
        state = "STOP"
    if u.distance > .2 and state is "STOP":
        state = "go"
    if state is "R":
        if u.distance > .4 and (v.distance > .3 and w.distance >.3):
            if w.distance>v.distance:
                state = "TL"
            else:
                state = "TR"
    updateCarOrientation()
    return "cs"

g.setmode(g.BCM)

motor1A = 13
motor1B = 19
motor1E = 26
motor2A = 16
motor2B = 20
motor2E = 21

g.setup(motor1A, g.OUT)
g.setup(motor1B, g.OUT)
g.setup(motor1E, g.OUT)
g.setup(motor2A, g.OUT)
g.setup(motor2B, g.OUT)
g.setup(motor2E, g.OUT)

def forward1():
    #print("Motor1 FORWARD!")
    g.output(motor1A, g.HIGH)
    g.output(motor1B, g.LOW)
    g.output(motor1E, g.HIGH)

def forward2():
    #print( "Motor2 FORWARD!")
    g.output(motor2A, g.HIGH)
    g.output(motor2B, g.LOW)
    g.output(motor2E, g.HIGH)

def reverse1():
    #print ("Motor1 REVERSE!")
    g.output(motor1A, g.LOW)
    g.output(motor1B, g.HIGH)
    g.output(motor1E, g.HIGH)

def reverse2():
    #print ("Motor2 REVERSE!")
    g.output(motor2E, g.LOW)
    g.output(motor2B, g.HIGH)
    g.output(motor2A, g.HIGH)

def off1():
    #print("Motor1 OFF!")
    g.output(motor1E, g.LOW)
    g.output(motor1B, g.LOW)
    g.output(motor1A, g.LOW)

def off2():
    #print("Motor2 OFF!")
    g.output(motor2E, g.LOW)
    g.output(motor2B, g.LOW)
    g.output(motor2A, g.LOW)

if __name__ == "__main__":
    app.run()
    g.cleanup()

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=checkSensors,
    trigger=IntervalTrigger(seconds=0.25),
    id='sensor_job',
    name='Check sensors every quarter second',
    replace_existing=True)