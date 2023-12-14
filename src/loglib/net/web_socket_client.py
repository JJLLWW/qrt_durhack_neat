""" ! PROOF OF CONCEPT ONLY ! """
import asyncio
import logging
import json
import datetime
import dataclasses


import websockets

logger = logging.getLogger(__name__)


class WSEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return json.JSONEncoder.default(self, o)


class WSocketEventForwarder:
    def __init__(self):
        self.events = asyncio.Queue()
        self.client = asyncio.create_task(self.client_main())

    def handle_log_event(self, event):
        self.events.put_nowait(event)

    async def client_main(self):
        async with websockets.connect("ws://localhost:2357") as websocket:
            try:
                while True:  # yuck
                    event = await self.events.get()
                    await websocket.send(json.dumps(event, cls=WSEncoder))
            except websockets.ConnectionClosed:
                pass
