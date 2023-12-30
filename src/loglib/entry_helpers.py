import asyncio
import re

import aiofiles


async def get_next_line(file: str, watch: bool = True):
    async with aiofiles.open(file) as f:
        while True:
            line = await f.readline()
            if line:
                yield line
            elif watch:
                await asyncio.sleep(1)
            else:
                return


_default_line_regex = r"^(?P<timestamp>\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}.\d+) (?P<status>\w+:) (?P<message>.*)$"
_default_line_pattern = re.compile(_default_line_regex)


async def get_next_entry_lines(
        file: str,
        watch: bool = True,
        pattern: re.Pattern = _default_line_pattern
):
    next_entry = ""
    async for line in get_next_line(file, watch):
        if pattern.match(line) and next_entry != "":
            yield next_entry
            next_entry = line
        else:
            next_entry += line
    if next_entry:
        yield next_entry
