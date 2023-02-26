#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from pymodbus.constants import Endian
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


# Команды движения
CMD_STOP            = 0x00      # Остановка двигателя
CMD_MOVE            = 0x01      # Бесконечное движение
CMD_MOVE_N          = 0x02      # Движение Steps_Number шагов
CMD_MOVE_STEP       = 0x03      # Движение до срабатывания датчика, подключенного ко входу STEP
CMD_MOVE_DIR        = 0x04      # Движение до срабатывания датчика, подключенного ко входу DIR
CMD_ADC_SPEED       = 0x05      # Команда устанавливает текущее значение скорости в соответствии со значением напряжения на аналоговом входе 0..5В от 1Гц до 10кГц
CMD_WL              = 0x06      # Системная команда
CMD_WH              = 0x07      # Системная команда
CMD_REVERS          = 0x08      # Реверс
CMD_MOVE_IN1        = 0x09      # Движение до срабатывания датчика, подключенного ко входу In1
CMD_MOVE_IN2        = 0x0A      # Движение до срабатывания датчика, подключенного ко входу In2
CMD_FIND_HOME       = 0x0B      # Поиск начального положения (движение до сигнала датчика HomeIn)
CMD_RESET           = 0x0C      # Перезагрузка контроллера. Все параметры сбрасываются, движение прекращается
CMD_MOVE_IN1_N      = 0x0D      # Движение до срабатывания датчика, подключенного ко входу In1, но не более Steps_Number шагов
CMD_MOVE_IN2_N      = 0x0E      # Движение до срабатывания датчика, подключенного ко входу In2, но не более Steps_Number шагов
CMD_FIND_HOME_N     = 0x0F      # Поиск начального положения (движение до сигнала датчика HomeIn, но не более Steps_Number шагов)
CMD_MOVE_STEP_N     = 0x10      # Движение до срабатывания датчика, подключенного ко входу STEP, но не более Steps_Number шагов
CMD_MOVE_DIR_N      = 0x11      # Движение до срабатывания датчика, подключенного ко входу DIR, но не более Steps_Number шагов
CMD_MAKE_STEP       = 0x12      # Сделать один шаг
CMD_SAVE_PARAMETERS = 0x13      # Сохранить параметры движения, микрошага и тока в энергонезависимую память


class Client(object):
    ''' Класс для управления шаговыми двигателями OSM '''

    def __init__(self, transport, device, unit):
        self._socket = transport
        self._socket.connect()

        self.device = device
        self.unit = unit

    def __del__(self):
        if self._socket:
            self._socket.close()

    def __repr__(self):
        return "Client(transport={}, unit={})".format(self._socket, self.unit)

    def _errorCheck(self, name, retcode):
        if not retcode:         # for python2 and pymodbus v1.3.0
            _logger.error("Unit %d called '%s' with error: "
                          "Modbus Error: [Input/Output] No Response received "
                          "from the remote unit", self.unit, name)
        elif isinstance(retcode, (ModbusException, ExceptionResponse)):
            _logger.error("Unit %d called '%s' with error: %s", self.unit, name, retcode)
        else:
            return True

    def getParam(self, name):
        ''' Чтение значения параметра по заданному имени '''

        _dev = self.device[name]

        if _dev['type'] in ["I32", "U32"]: count = 2
        elif _dev['type'] in ["U16", "U8"]: count = 1

        result = self._socket.read_holding_registers(address=_dev['address'],
                                                     count=count,
                                                     unit=self.unit)
        if self._errorCheck(name, result):
            decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big)

            if _dev['type'] == "I32":   return decoder.decode_32bit_int()
            elif _dev['type'] == "U32": return decoder.decode_32bit_uint()
            elif _dev['type'] == "U16": return decoder.decode_16bit_uint()
            elif _dev['type'] == "U8":  return decoder.decode_16bit_uint()

    def setParam(self, name, value):
        ''' Запись значения параметра по заданному имени '''

        _dev = self.device[name]

        if value < _dev['min'] or value > _dev['max']:
            raise ValueError("Parameter '{}' out of range ({}, {}) value '{}'".
                             format(name, _dev['min'], _dev['max'], value))

        builder = BinaryPayloadBuilder(None, Endian.Big)

        if _dev['type'] == "I32":   builder.add_32bit_int(value)
        elif _dev['type'] == "U32": builder.add_32bit_uint(value)
        elif _dev['type'] == "U16": builder.add_16bit_uint(value)
        elif _dev['type'] == "U8":  builder.add_16bit_uint(value)

        result = self._socket.write_registers(address=_dev['address'],
                                              values=builder.build(),
                                              skip_encode=True,
                                              unit=self.unit)
        return self._errorCheck(name, result)

    def move(self, speed=None, steps=None, edge=None):
        ''' В зависимости от установленных параметров, происходит движение
            с постоянной скоростью, по шагам или до ограничителя.
            Если скорость не указана или равна 0 происходит остановка движения
        '''

        edges = ("STEP", "DIR", "IN1", "IN2", "HOME")
        if edge and edge not in edges:
            raise ValueError("Unknown edge. Must be 'STEP', 'DIR', 'IN1', 'IN2', 'HOME'")

        args = []
        if speed:
            args.append(("Direction", speed < 0))
            args.append(("Speed", abs(speed)))
            if steps:
                args.append(("StepsNumber", steps))
                if edge in edges:
                    if edge == "STEP": args.append(("Command", CMD_MOVE_STEP_N))
                    if edge == "DIR":  args.append(("Command", CMD_MOVE_DIR_N))
                    if edge == "IN1":  args.append(("Command", CMD_MOVE_IN1_N))
                    if edge == "IN2":  args.append(("Command", CMD_MOVE_IN2_N))
                    if edge == "HOME": args.append(("Command", CMD_FIND_HOME_N))
                else:
                    args.append(("Command", CMD_MOVE_N))
            else:
                if edge in edges:
                    if edge == "STEP": args.append(("Command", CMD_MOVE_STEP))
                    if edge == "DIR":  args.append(("Command", CMD_MOVE_DIR))
                    if edge == "IN1":  args.append(("Command", CMD_MOVE_IN1))
                    if edge == "IN2":  args.append(("Command", CMD_MOVE_IN2))
                    if edge == "HOME": args.append(("Command", CMD_FIND_HOME))
                else:
                    args.append(("Command", CMD_MOVE))
        else:
            args.append(("Command", CMD_STOP))

        for arg in args:
            if not self.setParam(*arg):
                return None

        return True

    def state(self):
        ''' Чтение состояния '''

        val = self.getParam("Inputs")
        if val is not None:
            return {"STEP": bool(val>>5 & 1),
                    "EN":   bool(val>>4 & 1),
                    "DIR":  bool(val>>3 & 1),
                    "IN2":  bool(val>>2 & 1),
                    "IN1":  bool(val>>1 & 1),
                    "HOME": bool(val>>0 & 1)}

    def reset(self):
        ''' Перезагрузка контроллера. Все параметры сбрасываются, движение прекращается '''

        return self.setParam("Command", CMD_RESET)


__all__ = [ "Client" ]
