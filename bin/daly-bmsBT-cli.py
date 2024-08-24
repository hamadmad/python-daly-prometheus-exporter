#!/usr/bin/python3
import argparse
import json
import logging
import asyncio
from daly_bms_bluetooth import DalyBMSBluetooth

class DalyBMSConnection():
    def __init__(self, mac_address,request_retries=3, logger=None):
        self.bt_bms = DalyBMSBluetooth(request_retries,logger)
        self.mac_address = mac_address
        self.connected = False

    async def connect(self):
        self.connected = await self.bt_bms.connect(mac_address=self.mac_address)

    async def get_soc(self):
        if not self.connected:
           await self.connect()
        return await self.bt_bms.get_soc()

    async def get_cell_voltage_range(self):
        if not self.connected:
           await self.connect()
        return await self.bt_bms.get_cell_voltage_range()

    async def get_temperature_range(self):
        if not self.connected:
           await self.connect()
        return await self.bt_bms.get_temperature_range()

    async def get_mosfet_status(self):
        if not self.connected:
           await self.connect()
        return await self.bt_bms.get_mosfet_status()

    async def get_status(self):
        if not self.connected:
           await self.connect()
        return await self.bt_bms.get_status()

    async def get_cell_voltages(self):
        if not self.connected:
           await self.connect()
        return await self.bt_bms.get_cell_voltages()

    async def get_temperatures(self):
        if not self.connected:
           await self.connect()
        return await self.bt_bms.get_temperatures()

    async def get_balancing_status(self):
        if not self.connected:
           await self.connect()
        return await self.bt_bms.get_balancing_status()

    async def get_errors(self):
        if not self.connected:
           await self.connect()
        return await self.bt_bms.get_errors()

    async def get_all(self):
        if not self.connected:
           await self.connect()
        return await self.bt_bms.get_all()

    async def disconnect(self):
        if not self.connected:
           return
        return await self.bt_bms.disconnect()

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--device",
                    help="MAC address, e.g. 88:99:AA:BB:CC",
                    type=str)
parser.add_argument("--status", help="show status", action="store_true")
parser.add_argument("--soc", help="show voltage, current, SOC", action="store_true")
parser.add_argument("--mosfet", help="show mosfet status", action="store_true")
parser.add_argument("--cell-voltages", help="show cell voltages", action="store_true")
parser.add_argument("--cell-voltage-range", help="show cell voltage range", action="store_true")
parser.add_argument("--temperatures", help="show temperature sensor values", action="store_true")
parser.add_argument("--temperature-range", help="show temperature sensor values", action="store_true")
parser.add_argument("--balancing", help="show cell balancing status", action="store_true")
parser.add_argument("--errors", help="show BMS errors", action="store_true")
parser.add_argument("--all", help="show all", action="store_true")
parser.add_argument("--verbose", help="Verbose output", action="store_true")

args = parser.parse_args()

log_format = '%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
if args.verbose:
    level = logging.DEBUG
else:
    level = logging.WARNING

logging.basicConfig(level=level, format=log_format, datefmt='%H:%M:%S')

logger = logging.getLogger()

bms = DalyBMSConnection(mac_address=args.device,request_retries=3, logger=logger )

result = False

def print_result(result):
    print(json.dumps(result, indent=2))

while True:
    if args.status:
        result = asyncio.run(bms.get_status())
        print_result(result)
    if args.soc:
        result = asyncio.run(bms.get_soc())
        print_result(result)
    if args.mosfet:
        result = asyncio.run(bms.get_mosfet_status())
        print_result(result)
    if args.cell_voltages:
        result = asyncio.run(bms.get_cell_voltages())
        print_result(result)
    if args.cell_voltage_range:
        result = asyncio.run(bms.get_cell_voltage_range())
        print_result(result)
    if args.temperatures:
        result = asyncio.run(bms.get_temperatures())
        print_result(result)
    if args.temperature_range:
        result = asyncio.run(bms.get_temperature_range())
        print_result(result)
    if args.balancing:
        result = asyncio.run(bms.get_balancing_status())
        print_result(result)
    if args.errors:
        result = asyncio.run(bms.get_errors())
        print_result(result)
    if args.all:
        result = asyncio.run(bms.get_all())
        print_result(result)
