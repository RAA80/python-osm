#! /usr/bin/env python
# -*- coding: utf-8 -*-


# Таблица настроек контроллеров шагового двигателя OSM-17RA / OSM-42RA / OSM-88RA
OSM17 = {'Accel':           {'type': 'U16', 'address': 16387, 'min': 0x00,   'max': 0x0BB8},    # Ускорение
         'Address':         {'type': 'U8',  'address': 0,     'min': 0x01,   'max': 0x20},      # Адрес устройства
         'BaudRateIndex':   {'type': 'U8',  'address': 1,     'min': 0x00,   'max': 0x07},      # Скорость обмена
         'Command':         {'type': 'U8',  'address': 5,     'min': 0x00,   'max': 0x13},      # Номер команды
         'Current':         {'type': 'U16', 'address': 16389, 'min': 0x00,   'max': 0x1068},    # Ток двигателя
         'Direction':       {'type': 'U8',  'address': 4,     'min': 0x00,   'max': 0x01},      # Направление вращения
         'Enable':          {'type': 'U8',  'address': 3,     'min': 0x00,   'max': 0x01},      # Включение тока в обмотках
         'EncoderPosition': {'type': 'I32', 'address': 32778, 'min': -2**32, 'max': 2**32},     # Позиция энкодера
         'EnCounter':       {'type': 'U16', 'address': 16393, 'min': 0x00,   'max': 2**16},     # Счетчик прерываний по входу EN
         'EndSpeed':        {'type': 'U16', 'address': 16388, 'min': 0x00,   'max': 0x0BB8},    # Конечная скорость
         'Inputs':          {'type': 'U8',  'address': 8,     'min': 0x00,   'max': 0x3F},      # Состояние входов
         'IntCounter':      {'type': 'U32', 'address': 32776, 'min': 0x00,   'max': 2**32},     # Счетчик прерываний по входу Revers
         'IntEn':           {'type': 'U8',  'address': 10,    'min': 0x00,   'max': 0x03},      # Разрешение прерываний по входам
         'IntMode':         {'type': 'U8',  'address': 11,    'min': 0x00,   'max': 0x03},      # Режим работы прерывания по входу Revers
         'Microstep':       {'type': 'U8',  'address': 7,     'min': 0x01,   'max': 0x10},      # Коэффициент микрошага
         'Output':          {'type': 'U8',  'address': 6,     'min': 0x00,   'max': 0x01},      # Состояние выхода
         'Position':        {'type': 'I32', 'address': 32770, 'min': -2**32, 'max': 2**32},     # Позиция двигателя
         'RtsDelay':        {'type': 'U8',  'address': 2,     'min': 0x00,   'max': 0xFF},      # Задержка RTS
         'SleepCurrent':    {'type': 'U8',  'address': 9,     'min': 0x00,   'max': 0x64},      # Ток в режиме простоя
         'SleepTime':       {'type': 'U16', 'address': 16392, 'min': 0x00,   'max': 0x07D0},    # Время до перехода в спящий режим
         'Speed':           {'type': 'U16', 'address': 16385, 'min': 0x01,   'max': 0x4E20},    # Скорость двигателя
         'SpeedCurrent':    {'type': 'U16', 'address': 16390, 'min': 0x00,   'max': 2**16},     # Текущая скорость
         'StartSpeed':      {'type': 'U16', 'address': 16386, 'min': 0x00,   'max': 0x4E20},    # Стартовая скорость двигателя
         'StepsBefDecel':   {'type': 'U16', 'address': 16391, 'min': 0x00,   'max': 2**16},     # Число шагов при замедлении
         'StepsCounter':    {'type': 'U32', 'address': 32772, 'min': 0x00,   'max': 2**32},     # Число шагов до завершения команды
         'StepsNumber':     {'type': 'U32', 'address': 32768, 'min': 0x00,   'max': 2**32},     # Число шагов
         'SystemId':        {'type': 'U8',  'address': 12,    'min': 0x00,   'max': 0xFF},      # Версия прошивки
         'UartDelay':       {'type': 'U16', 'address': 16384, 'min': 0x00,   'max': 2**16},     # Задержка приемопередатчика
        }
