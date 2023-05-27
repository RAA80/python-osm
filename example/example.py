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

print("Set Enable: {}".format(id_osm.set_param("Enable", 1)))
print("Set Current: {}".format(id_osm.set_param("Current", 100)))

print("Move: {}".format(id_osm.move(speed=100, steps=200, edge="IN1")))

sleep(5)

print("Set Current: {}".format(id_osm.set_param("Current", 0)))
print("Set Enable: {}".format(id_osm.set_param("Enable", 0)))

#print("State: {}".format(id_osm.state()))
#print("Get Enable: {}".format(id_osm.get_param("Enable")))
#print("Reset: {}".format(id_osm.reset()))
