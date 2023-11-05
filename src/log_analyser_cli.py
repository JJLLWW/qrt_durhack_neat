#!/usr/bin/python3

import logging
from loader.loader import LogLoader

# handling logging config can be quite elaborate

def main():
    logging.basicConfig(filename='cli_log', level=logging.DEBUG)
    log_loader = LogLoader()
    log_loader.load_log_snapshot('../data/frozen_output.log')


if __name__ == '__main__':
    main()