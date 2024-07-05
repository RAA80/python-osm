#! /usr/bin/env python3

"""Пример использования библиотеки."""

from time import sleep

from osm.client import Client
from osm.device import OSM17

if __name__ == "__main__":
    client = Client(unit=1, port="COM5", baudrate=115200, device=OSM17)
    print(client)

    print(f'Set Enable: {client.set_param("Enable", 1)}')   # Остальные названия параметров в файле 'device.py'
    print(f'Set Current: {client.set_param("Current", 100)}')

    print(f'Move: {client.move(speed=100, steps=200, edge="IN1")}')

    sleep(5)

    print(f'Set Current: {client.set_param("Current", 0)}')
    print(f'Set Enable: {client.set_param("Enable", 0)}')

    # print(f"State: {client.state()}")
    # print(f'Get Enable: {client.get_param("Enable")}')
    # print(f"Reset: {client.reset()}")
