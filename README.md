# Task Description

The application takes two optional parameters:

    Int – random seed
    Log output filename – The default file name pattern is qrt_data_extraction_analysis_DD_MM_YYYY_HHMMSS.log

Log entries will be automatically appended to this filename, and your application needs to process this file in as near to real-time as possible.

Our challenge to you is to develop a tool simplify the extraction and analysis of the log output by this and other applications.

Some of the things your analysis tool should do include:

    Analyse multiple log files in parallel
    Option to continuously analyse logs as they are updated
    Filtering for important information (entered by user) – extra points for enabling regex
    Highlighting of information (entered by user) – extra points for enabling regex
    Display time difference between two entered points (rough latency analysis) statistical summary of all the times
    Log will also contain statistical information which should be displayed / summarised in some form (graphical?)
    Being able to save and reload selected options / filters etc…
    Raising ‘alerts’ if a certain type message is found or a condition is met e.g. latency is above threshold for a given amount of time
    Extra Bonus Points and Special Prizes will be awarded for novel and exciting features - nothing is off limits!

Extra points for making the application work via a web browser, any messaging system or some kind of fruit.

Hidden within the log messages are lists of the QRT Team’s favourite movies. If you’ve implemented the features as described above then you should be able to spot these. There’s also three number sequences hidden in the output. The first team that can list all the movies and tell us what the number sequence is will win cool QRT merch!

# Running

The cli and server require Python 3.11+ for certain asyncio features.

## cli
```console
pipx install poetry
make poetry_install_all
python3 src/main.py
```

## server

```console
pipx install poetry
make poetry_install_all
make rmq
make server
```

## ui client

```console
cd client
npm i
npm run start
```

# UI

![image info](./static/ui_image.jpeg)