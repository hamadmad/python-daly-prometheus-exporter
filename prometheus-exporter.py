#!/usr/bin/env python3

import sys
import json
import logging
import asyncio
from dalybms.daly_bms_bluetooth import DalyBMSBluetooth
from prometheus_client import start_http_server, Gauge
from bleak.exc import BleakError
from datetime import datetime

start_http_server(8000)

cv = Gauge("cell_voltages", "Cell voltages", ["cell_number"])


class DalyBMSConnection:
    def __init__(self, mac_address, request_retries=3, logger=None):
        self.bt_bms = DalyBMSBluetooth(request_retries, logger)
        self.mac_address = mac_address
        self.connected = False

    async def connect(self):
        self.connected = await self.bt_bms.connect(mac_address=self.mac_address)

    async def get_all(self):
        if not self.connected:
            await self.connect()
        return await self.bt_bms.get_all()

    async def disconnect(self):
        if not self.connected:
            return
        return await self.bt_bms.disconnect()


log_format = "%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
level = logging.WARNING

logging.basicConfig(level=level, format=log_format, datefmt="%H:%M:%S")

logger = logging.getLogger()

mac_address = sys.argv[1]

bms = DalyBMSConnection(mac_address=mac_address, request_retries=3, logger=logger)

last_output = 0
def print_rarely(data):
    global last_output
    if datetime.now().timestamp() - last_output > 600:
        last_output = datetime.now().timestamp()
        print(json.dumps(data))


while True:
    try:
        result = asyncio.run(bms.get_all())
    except (BleakError, TypeError):
        continue
    for cell_number, cell_voltage in result["cell_voltages"].items():
        cv.labels(cell_number=cell_number).set(cell_voltage)
    print_rarely(result)
