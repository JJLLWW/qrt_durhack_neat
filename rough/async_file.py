# to track file creation/deletion in a directory, watchdog is recommended - seems to work ok
# is it possible
import asyncio

import aiofiles


# is there a way to avoid polling the file with an interval?
# how to cancel this coroutine when doing cleanup? - send event? <- no, needs to be awaited
# (there's just a cancel method)
# - this will continue running if the underlying file is deleted, so could be a
# resource leak.
async def file_coro(filename: str):
    async with aiofiles.open(filename, mode='r') as f:
        while True:
            line = await f.readline()
            if line:
                print(f"{filename}: {line}", end='')
            else:
                await asyncio.sleep(1)


async def main():
    # asyncio.timeout() is 3.11+ only
    try:
        await asyncio.wait_for(file_coro("rough.log"), 2)
    except asyncio.TimeoutError:
        print("waited for timeout") # love using exceptions as control flow


# if multiple running in parallel how do I timeout all?
# more interestingly how can 2 coroutines communicate? <- global ):,
# shared object parameter ):
async def main2():
    coros = [file_coro("rough.log"), file_coro("rough2.log")]
    await asyncio.gather(*coros)


async def test1(L):
    L.append('oh no')
    await asyncio.sleep(2)
    print(L)

async def test2(L):
    await asyncio.sleep(1)
    print(L)
    L.append("oh no 2")

# surely mutable function parameter is a recipe for disaster
# there are also events with wait() and set() and clear()
# asyncio queues <- all of these objects are passed as mutable function parameters.
# lgtm
async def main3():
    L = []
    coros = [test1(L), test2(L)]
    await asyncio.gather(*coros)


if __name__ == "__main__":
    asyncio.run(main2())