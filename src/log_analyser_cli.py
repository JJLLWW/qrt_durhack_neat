#!/usr/bin/python3

import logging
from art import text2art

def help():
    print("""
> press q to quit
> press p or something
> 
""")


def main():
    logging.basicConfig(filename='cli_log', level=logging.DEBUG)
    print(text2art("Log Analyser"))
    help()
    while (line := input("log_analyser> ")) != 'q':
        print(line)


if __name__ == '__main__':
    main()