from datetime import datetime
import pandas as pd


def correct_time_nanos(timestamp: str):
    time_fields = timestamp.split('.')
    if len(time_fields[1]) == 8:
        time_fields[1] = "0" + time_fields[1][:5]
    else:
        time_fields[1] = time_fields[1][:6]
    return '.'.join(time_fields)


def parse_single_line_entry(line: str):
    line_dict = {}
    words = line.split(' ')
    words[1] = correct_time_nanos(words[1])
    timestamp_str: str = ' '.join(words[:2])
    timestamp = datetime.strptime(timestamp_str, '%m-%d-%Y %H:%M:%S.%f')
    line_dict['Timestamp'] = [timestamp]
    line_dict['Status'] = [words[2].strip(':')]
    line_dict['Message'] = [' '.join(words[3:]).strip('\n')]
    return pd.DataFrame.from_dict(line_dict)


def is_exchange_timing_preamble(line: str):
    words = line.strip('\n').rstrip().split(' ')
    return len(words) < 4


def parse_exchange_timing_snapshot(log_file):
    pass
