# bimlights

A physical map of 50 LEDs to represent the tram stations in Linz, Upper Austria, which display the location of trams in real time.

## architecture

### server

A simple webserver written in python based on flask. It simply queries linz.faehrt.at for the location of all trams and calculates their closest station using the mapping file.

### client

The client uses only a ESP8266 module to connect wirelessly to the server, invoke an update of the data every 10s and display the updated data.
