def parse_single_line_entry(line: str):
    words = line.split(' ')
    timestamp = ' '.join(words[:2])
    status = words[2].strip(':')
    msg: str = ' '.join(words[3:]).strip('\n')

def is_exchange_timing_preamble(line: str):
    return False

def parse_exchange_timing_snapshot(log_file):
    pass

