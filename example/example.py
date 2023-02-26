#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from time import sleep

from pymodbus.client.sync import ModbusSerialClient
from osm.client import Client
from osm.device import OSM17        # Для OSM-17RA, OSM-42RA, OSM-88RA параметры одинаковые

logging.basicConfig(level=logging.INFO)


transport = ModbusSerialClient(method='rtu',
                               port="COM5",
                               baudrate=115200,
                               timeout=0.2,
                               retry_on_empty=True)
id_osm = Client(transport=transport, device=OSM17, unit=1)
print(id_osm)

print("State: {}".format(id_osm.state()))
print("Set Enable: {}".format(id_osm.setParam("Enable", 1)))
print("Get Enable: {}".format(id_osm.getParam("Enable")))
print("Set Current: {}".format(id_osm.setParam("Current", 100)))
print("Get Current: {}".format(id_osm.getParam("Current")))

print("Move: {}".format(id_osm.move(speed=100, steps=200, edge="IN1")))

sleep(5)

print("Set Current: {}".format(id_osm.setParam("Current", 0)))
print("Set Enable: {}".format(id_osm.setParam("Enable", 0)))

#print("Reset: {}".format(id_osm.reset()))
