# python-osm #

Библиотека для работы с контроллерами шагового двигателя OSM-17RA / OSM-42RA / OSM-88RA по протоколу Modbus

## 1. Работа с консольной версией ##

    usage: osm-console [-h] --port PORT [--timeout [VALUE]] [--debug] [--scan]
                       [--baudrate BAUDRATE] [--unit UNIT] [--reset | --state | --get KEY |
                       --set KEY VALUE | --move ARG [ARG ...]]

    OSM controllers command-line option

    optional arguments:
      -h, --help            show this help message and exit
      --port PORT           select port name
      --timeout [VALUE]     select timeout in seconds
      --debug               print debug information

    Scanner:
      --scan                scan available modules

    User:
      --baudrate BAUDRATE   select OSM baudrate
      --unit UNIT           select OSM address
      --reset               send RESET request
      --state               read OSM state
      --get KEY             read config value
      --set KEY VALUE       write config value
      --move ARG [ARG ...]  send MOVE command with Speed, Steps, Edge

Программа может работать в двух режимах: **Scanner** и **User**

### Режим Scanner ###

В этом режиме происходит поиск активных модулей, подключенных к порту

Пример использования режима Scanner:

    osm-console --port COM1 --scan

Пример результата работы:

    Unit: 1, Baudrate: 57600 - OK

### Режим User ###

Пример использования режима User:

- Чтение регистра входных сигналов

        osm-console --port COM1 --baudrate 57600 --unit 1 --state

- Чтение значения регистра контроллера

        osm-console --port COM1 --baudrate 57600 --unit 1 --get Enable

- Запись значения в регистр контроллера

        osm-console --port COM1 --baudrate 57600 --unit 1 --set Enable 1

- Движение с постоянной скоростью 100 (или -100 для движения в обратную сторону)

        osm-console --port COM1 --baudrate 57600 --unit 1 --move 100 0 ""

- Движение со скоростью 100, но не более 1000 шагов

        osm-console --port COM1 --baudrate 57600 --unit 1 --move 100 1000 ""

- Движение со скоростью 100 до срабатывания датчика, подключенного ко входу IN1

        osm-console --port COM1 --baudrate 57600 --unit 1 --move 100 0 IN1

- Движение со скоростью 100 до срабатывания датчика, подключенного ко входу IN1, но не более 1000 шагов

        osm-console --port COM1 --baudrate 57600 --unit 1 --move 100 1000 IN1

## 2. Работа с графической версией ##

![OSM Controller](./doc/GUI_1.png)

## 3. Работа с симулятором ##

    usage: osm-simulator [-h] [--port PORT]

    OSM stepper driver simulator command-line option

    optional arguments:
      -h, --help   show this help message and exit
      --port PORT  select port name

Пример использования симулятора:

    osm-simulator --serial COM1
