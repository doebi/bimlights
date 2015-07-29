# bimlights

A physical map of 50 LEDs to represent the tram stations in Linz, Upper Austria, which display the location of trams in real time.

![](http://i.imgur.com/zlIwdSP.jpg)

## architecture

### server

A simple webserver written in python based on flask. It simply queries linz.faehrt.at for the location of all trams and calculates their closest station using the mapping file.

### client

The client uses only a ESP8266 module to connect wirelessly to the server, invoke an update of the data every 10s and display the updated data.

## links

[wiki](https://devlol.org/wiki/doebi/BimLights) ⏺ [hackaday](http://hackaday.com/2014/09/15/leds-turn-this-paper-map-into-a-tram-tracker/)

## more pics

![](http://i.imgur.com/YY8QBEy.jpg)
