import asyncio
import aiofiles
import time
from threading import Thread


async def open_files():
    paths = ["output1.log", "output2.log", "output3.log"]
    files = [await aiofiles.open(path) for path in paths]
    return files


async def process_line(file):
    line = await file.readline()
    if line != '' and line != '\n':
        print(line)


async def main():
    files = await open_files()
    while True:
        await asyncio.sleep(0.1)
        read_tasks = []
        for file in files:
            read_tasks.append(asyncio.ensure_future(process_line(file)))
        await asyncio.gather(*read_tasks)

# if I have one thread polling for user input and one thread polling the files.
# how do they communicate - theres an "event" mechanism that could be used.
# if the data frame is constantly being written to, how does another thread read it without
# locking? (it doesn't, just updates the filtering state once.)
# if the filters are being applied in real time operations could be like a pipeline before display.
# how would that work though, suppose there's a backing dataframe being appended to, then a display
# dataframe that gets appended to if new lines get through the filters.
# if the filters change the display dataframe is destroyed and reconstructed. (think there are still threading
# problems here) <- is this data that should be stored in a db? - probably not no.
# how does displaying it work

if __name__ == "__main__":
    io_thread = Thread(target=asyncio.run, args=[main()])
    io_thread.start()
    for i in range(10):
        print(f"{i}")
        time.sleep(1)
    io_thread.join()
