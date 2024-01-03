import asyncio

from .file_manager import LogFileManager
from .rmq import get_rmq_connection, rmq_consumer


class ServerManager:
    def __init__(self):
        self.file_manager = LogFileManager()
        self.rmq_consumer = None
        self.connection = None

    async def start(self):
        self.connection = await get_rmq_connection()
        self.rmq_consumer = asyncio.create_task(rmq_consumer(self.file_manager, self.connection))

    def get_all_info(self):
        return self.file_manager.ke

    async def stop(self):
        self.rmq_consumer.cancel()
        self.connection.close()