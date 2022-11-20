# https://pypi.org/project/bleak/

import asyncio
from bleak import BleakScanner, BleakClient

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

    address = "3A:22:E2:AB:0E:6E"
    MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"

    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

asyncio.run(main())
