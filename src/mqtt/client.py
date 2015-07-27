#!/usr/bin/env python
# encoding: utf-8
import time
import serial
import urllib
import time
import json
import mosquitto

ser = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 9600,
)

praeambel = "\x00\x00\x00"
praeambel += "\x23\x54\x26\x66"
praeambel += "\x00\x00\x50"

def on_message(client, data, msg):
    actions[msg.topic](msg.payload.replace('0', '\x00').replace('1', '\xC8'))

client = mosquitto.Mosquitto()
client.connect("192.168.7.2")
client.on_message = on_message
client.subscribe("bimlights/#")
client.subscribe("craftui/#")

# def get():
#     url = "http://doebi.at:5000"
#     try:
#         r = urllib.urlopen(url)
#         data = r.read()
#         print data
#     except:
# 	data = ""
#         print("Error: Server not responding")
# 
#     return data.replace('0', '\x00').replace('1', '\xC8')

def show(data):
    print "writing to ser"
    ser.write(praeambel)
    ser.write(data)

def all(data):
    print data
    show(data)

def clear(data):
    print "clearing: " + data
    show(data*50)

def red(data):
    clear("\xFF\x00\00")

def green(data):
    clear("\x00\xFF\00")

def blue(data):
    clear("\x00\x00\xFF")

def demo(data):
    print "demo"

actions = {
    "bimlights/all"               : all,
    "bimlights/clear"             : clear,
    "bimlights/demo"              : demo,
    "craftui/button/button_red"   : red,
    "craftui/button/button_green" : green,
    "craftui/button/button_blue"  : blue
}

clear("\x00\x00\x00")

while True:
    client.loop()

ser.close()
