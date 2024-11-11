#! /usr/bin/env python3

"""Данный файл содержит настройки приборов."""

from typing import TypedDict


class OSM_PARAMS(TypedDict):
    type: str
    address: int
    min: int
    max: int


OSM_DEVICE = dict[str, OSM_PARAMS]


# Таблица настроек контроллеров шагового двигателя OSM-17RA / OSM-42RA / OSM-88RA
OSM17: OSM_DEVICE = {
    "Accel":           {"type": "U16", "address": 0x4003, "min": 0x00,   "max": 0x0BB8},    # Ускорение
    "Address":         {"type": "U16", "address": 0x0000, "min": 0x01,   "max": 0x20},      # Адрес устройства
    "BaudRateIndex":   {"type": "U16", "address": 0x0001, "min": 0x00,   "max": 0x07},      # Скорость обмена
    "Command":         {"type": "U16", "address": 0x0005, "min": 0x00,   "max": 0x13},      # Номер команды
    "Current":         {"type": "U16", "address": 0x4005, "min": 0x00,   "max": 0x1068},    # Ток двигателя
    "Direction":       {"type": "U16", "address": 0x0004, "min": 0x00,   "max": 0x01},      # Направление вращения
    "Enable":          {"type": "U16", "address": 0x0003, "min": 0x00,   "max": 0x01},      # Включение тока в обмотках
    "EncoderPosition": {"type": "I32", "address": 0x800A, "min": -2**32, "max": 2**32},     # Позиция энкодера
    "EnCounter":       {"type": "U16", "address": 0x4009, "min": 0x00,   "max": 2**16},     # Счетчик прерываний по входу EN
    "EndSpeed":        {"type": "U16", "address": 0x4004, "min": 0x00,   "max": 0x0BB8},    # Конечная скорость
    "Inputs":          {"type": "U16", "address": 0x0008, "min": 0x00,   "max": 0x3F},      # Состояние входов
    "IntCounter":      {"type": "U32", "address": 0x8008, "min": 0x00,   "max": 2**32},     # Счетчик прерываний по входу Revers
    "IntEn":           {"type": "U16", "address": 0x000A, "min": 0x00,   "max": 0x03},      # Разрешение прерываний по входам
    "IntMode":         {"type": "U16", "address": 0x000B, "min": 0x00,   "max": 0x03},      # Режим работы прерывания по входу Revers
    "Microstep":       {"type": "U16", "address": 0x0007, "min": 0x01,   "max": 0x10},      # Коэффициент микрошага
    "Output":          {"type": "U16", "address": 0x0006, "min": 0x00,   "max": 0x01},      # Состояние выхода
    "Position":        {"type": "I32", "address": 0x8002, "min": -2**32, "max": 2**32},     # Позиция двигателя
    "RtsDelay":        {"type": "U16", "address": 0x0002, "min": 0x00,   "max": 0xFF},      # Задержка RTS
    "SleepCurrent":    {"type": "U16", "address": 0x0009, "min": 0x00,   "max": 0x64},      # Ток в режиме простоя
    "SleepTime":       {"type": "U16", "address": 0x4008, "min": 0x00,   "max": 0x07D0},    # Время до перехода в спящий режим
    "Speed":           {"type": "U16", "address": 0x4001, "min": 0x01,   "max": 0x4E20},    # Скорость двигателя
    "SpeedCurrent":    {"type": "U16", "address": 0x4006, "min": 0x00,   "max": 2**16},     # Текущая скорость
    "StartSpeed":      {"type": "U16", "address": 0x4002, "min": 0x00,   "max": 0x4E20},    # Стартовая скорость двигателя
    "StepsBefDecel":   {"type": "U16", "address": 0x4007, "min": 0x00,   "max": 2**16},     # Число шагов при замедлении
    "StepsCounter":    {"type": "U32", "address": 0x8004, "min": 0x00,   "max": 2**32},     # Число шагов до завершения команды
    "StepsNumber":     {"type": "U32", "address": 0x8000, "min": 0x00,   "max": 2**32},     # Число шагов
    "SystemId":        {"type": "U16", "address": 0x000C, "min": 0x00,   "max": 0xFF},      # Версия прошивки
    "UartDelay":       {"type": "U16", "address": 0x4000, "min": 0x00,   "max": 2**16},     # Задержка приемопередатчика
}
