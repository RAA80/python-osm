#! /usr/bin/env python3

"""Реализация класса клиента для управления контроллером шаговых двигателей OSM."""

from __future__ import annotations

from enum import IntEnum

from pymodbus.client.sync import ModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.pdu import ModbusResponse

from .device import OSM17


class OsmError(Exception):
    pass


class CMD(IntEnum):     # Таблица 6.4.2 документации
    """Команды управления."""

    STOP = 0x00
    MOVE = 0x01
    MOVE_N = 0x02
    MOVE_STEP = 0x03
    MOVE_DIR = 0x04
    ADC_SPEED = 0x05
    WL = 0x06
    WH = 0x07
    REVERS = 0x08
    MOVE_IN1 = 0x09
    MOVE_IN2 = 0x0A
    FIND_HOME = 0x0B
    RESET = 0x0C
    MOVE_IN1_N = 0x0D
    MOVE_IN2_N = 0x0E
    FIND_HOME_N = 0x0F
    MOVE_STEP_N = 0x10
    MOVE_DIR_N = 0x11
    MAKE_STEP = 0x12
    SAVE_PARAMETERS = 0x13


class Client:
    """Класс для управления контроллером шаговых двигателей OSM."""

    def __init__(self, port: str, baudrate: int, unit: int,
                       timeout: float = 1.0) -> None:
        """Инициализация класса клиента с указанными параметрами."""

        self.socket = ModbusSerialClient(method="rtu", port=port,
                                         baudrate=baudrate, timeout=timeout)
        self.socket.connect()

        self.port = port
        self.baudrate = baudrate
        self.unit = unit

    def __del__(self) -> None:
        """Закрытие соединения с устройством при удалении объекта."""

        if self.socket:
            self.socket.close()

    def __repr__(self) -> str:
        """Строковое представление объекта."""

        return (f"{type(self).__name__}(port={self.port!r}, "
                f"baudrate={self.baudrate}, unit={self.unit})")

    @staticmethod
    def _check_error(retcode: ModbusResponse) -> bool:
        """Проверка возвращаемого значения на ошибку."""

        if retcode.isError():
            raise OsmError(retcode)
        return True

    @staticmethod
    def _check_name(name: str) -> dict[str, str | int]:
        """Проверка названия параметра."""

        if name not in OSM17:
            msg = f"Unknown parameter '{name}'"
            raise OsmError(msg)

        return OSM17[name]

    def get_param(self, name: str) -> int:
        """Чтение данных из устройства."""

        dev = self._check_name(name)

        count = {"I32": 2, "U32": 2, "U16": 1}[dev["type"]]
        result = self.socket.read_holding_registers(address=dev["address"],
                                                    count=count,
                                                    unit=self.unit)
        self._check_error(result)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big)

        return {"I32": decoder.decode_32bit_int,
                "U32": decoder.decode_32bit_uint,
                "U16": decoder.decode_16bit_uint,
                }[dev["type"]]()

    def set_param(self, name: str, value: int) -> bool:
        """Запись данных в устройство."""

        dev = self._check_name(name)

        if value not in range(dev["min"], dev["max"] + 1):
            msg = f"An '{name}' value of '{value}' is out of range"
            raise OsmError(msg)

        builder = BinaryPayloadBuilder(None, Endian.Big)
        {"I32": builder.add_32bit_int,
         "U32": builder.add_32bit_uint,
         "U16": builder.add_16bit_uint,
        }[dev["type"]](value)

        result = self.socket.write_registers(address=dev["address"],
                                             values=builder.build(),
                                             skip_encode=True,
                                             unit=self.unit)
        return self._check_error(result)

    def move(self, speed: int, steps: int = 0, edge: str = "") -> bool:
        """Запуск движения с постоянной скоростью, по шагам или до ограничителя.
        Знак скорости определяет направление. Если скорость равна 0, движение
        прекращается.
        """

        edges = ("STEP", "DIR", "IN1", "IN2", "HOME")
        if edge and edge not in edges:
            msg = f"Unknown edge. Choose from {edges}"
            raise OsmError(msg)

        args: list[tuple[str, int]] = []
        cmd = CMD.STOP

        if speed:
            args.extend((("Direction", speed < 0), ("Speed", abs(speed))))
            if steps:
                args.append(("StepsNumber", steps))
            cmd = {"DIR": (CMD.MOVE_DIR, CMD.MOVE_DIR_N),
                   "IN1": (CMD.MOVE_IN1, CMD.MOVE_IN1_N),
                   "IN2": (CMD.MOVE_IN2, CMD.MOVE_IN2_N),
                   "HOME": (CMD.FIND_HOME, CMD.FIND_HOME_N),
                   "STEP": (CMD.MOVE_STEP, CMD.MOVE_STEP_N),
                  }.get(edge, (CMD.MOVE, CMD.MOVE_N))[bool(steps)]

        args.append(("Command", cmd))

        for arg in args:
            self.set_param(*arg)

        return True

    def state(self) -> dict[str, bool]:    # Таблица 6.4.3 документации
        """Чтение состояния."""

        val = self.get_param("Inputs")
        return {"STEP": bool(val >> 5 & 1),
                "EN":   bool(val >> 4 & 1),
                "DIR":  bool(val >> 3 & 1),
                "IN2":  bool(val >> 2 & 1),
                "IN1":  bool(val >> 1 & 1),
                "HOME": bool(val >> 0 & 1)}

    def reset(self) -> bool:
        """Все параметры сбрасываются, движение прекращается."""

        return self.set_param("Command", CMD.RESET)


__all__ = ["Client"]
