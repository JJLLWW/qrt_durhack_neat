""" ! PROOF OF CONCEPT ONLY ! """
import asyncio
import logging

import websockets

_clients = set()


# yes it is fine to just wait on a websocket's messages forever, can iterate over
# them.
async def conn_handler(websocket: websockets.WebSocketServerProtocol):
    _clients.add(websocket)
    try:
        async for msg in websocket:
            print("next msg")
            print(msg)
    finally:
        _clients.remove(websocket)


async def start_server():
    async with websockets.serve(conn_handler, "localhost", 2357):
        await asyncio.Event().wait()  # stay alive forever


def broadcast_all():
    websockets.broadcast(_clients, "TEST")


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    asyncio.run(start_server())
