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
        self.entry_first_line = None
        self.first_entry = True
        self.line_head_pattern = re.compile(LogIterator.line_head_regex)

    def __iter__(self):
        return self

    def __next__(self):
        entry_lines = self.entry_first_line
        if self.first_entry:
            entry_lines = next(self.logfile)
            self.first_entry = False
        elif self.entry_first_line is None:
            raise StopIteration
        while (cur_line := next(self.logfile, None)) is not None:
            if not self.__is_continuation_line(cur_line):
                break
            entry_lines += cur_line
        self.entry_first_line = cur_line
        return entry_lines
