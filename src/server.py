""" PROOF OF CONCEPT ONLY! """

from contextlib import asynccontextmanager

import fastapi
from loglib.json_serialise import encode
from serverlib.lifetime import ServerManager


manager = ServerManager()


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    await manager.start()
    yield
    await manager.stop()


app = fastapi.FastAPI(lifespan=lifespan)


@app.get("/dump_all")
async def dump_all():
    print(manager.file_manager.files)
    as_list = [file.entries for file in manager.file_manager.files.values()]
    # unfortunately its now one giant string
    return encode(as_list)