#!/usr/bin/python3

import logging
from loader.loader import LogLoader
from loader.parser import LogParser

def main():
    logging.basicConfig(filename='cli_log', level=logging.DEBUG)
    log_parser = LogParser()
    with open("../data/frozen_output.log") as f:
        entries = log_parser.parse_static_logfile(f)
        print(entries)


if __name__ == '__main__':
    main()