import re
from typing import TextIO


class LogIterator:
    line_head_regex = r"^\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}.\d+ \w+: .+$"

    def __is_continuation_line(self, line: str) -> bool:
        if line is None:
            return False
        return self.line_head_pattern.match(line) is None

    def __init__(self, logfile: TextIO):
        self.logfile = logfile
        self.cur_entry_head = None
        self.line_head_pattern = re.compile(LogIterator.line_head_regex)

    def __iter__(self):
        return self

    def __next__(self):
        if self.cur_entry_head is None:
            entry_lines = next(self.logfile)
            cur_line = entry_lines
        else:
            entry_lines = self.cur_entry_head
            cur_line = next(self.logfile, None)
        while self.__is_continuation_line(cur_line):
            entry_lines += cur_line
            cur_line = next(self.logfile, None)
        self.cur_entry_head = cur_line
        return entry_lines
