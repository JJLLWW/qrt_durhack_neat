import pandas as pd


def main():
    # if pandas can read the timestamp correctly does this mean this can be done
    # in the parsing code instead of the custom code?
    frame_csv = pd.read_csv("frame.csv", parse_dates=['timestamp'])
    pass


if __name__ == "__main__":
    main()