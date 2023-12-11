import logging
import time


def main():
    # apparently python logging doesn't support microseconds naturally ):
    # its not just the default formatter, LogRecords only store the milliseconds not anything more
    # precise so you can't even solve it with a formatter subclass.
    # further, even time.time() doesn't support microseconds. <- there is time_ns() though.

    # suppose this isn't something you normally want.
    logging.basicConfig(filename='rough.log', level=logging.DEBUG)
    for i in range(1000):
        logging.debug("timing")


if __name__ == "__main__":
    main()