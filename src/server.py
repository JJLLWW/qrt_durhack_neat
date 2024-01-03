""" PROOF OF CONCEPT ONLY! """

import uuid
from contextlib import asynccontextmanager

import fastapi
from loglib.typing import LogFile
from serverlib.lifetime import ServerManager


manager = ServerManager()


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    await manager.start()
    yield
    await manager.stop()


app = fastapi.FastAPI(lifespan=lifespan)


@app.get("/log_files/all_uuids")
async def get_all_uuids():
    return {"uuids": list(manager.file_manager.files.keys())}


@app.get("/log_files/all", response_model=list[LogFile])
async def get_all_files() -> LogFile:
    return manager.file_manager.files.values()


@app.get("/log_files/{uuid}", response_model=LogFile)
async def get_file_by_uuid(uuid: uuid.UUID):
    return manager.file_manager.files[str(uuid)]


@app.post("/log_files/")
async def post_file(log_file: LogFile):
    manager.file_manager.add_file(log_file)