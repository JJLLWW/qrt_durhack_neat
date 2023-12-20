from loglib.datamodel.log_file import LogFile
from loglib.loader.entry_parse import parse_log_entry


def test_log_file_single_thread():
    log_file = LogFile()
    lines = """04-11-2023 21:04:29.87573000 DEBUG: Recreating message with new code NEWC-61803
04-11-2023 21:04:29.87576000 INFO: Starting processing of order [additional_info]
04-11-2023 21:04:30.29640000 OTHER: Nature hides her secrets because of her essential loftiness, but not by means of ruse - Einstein, Albert
04-11-2023 21:04:30.29694000 ERROR: Unable to find order ORD-398 sent to exchange (Rook)
04-11-2023 21:04:30.29711000 OTHER: If you give a github repo in your CV make sure to have someone review the code, recruiters will look at the code
04-11-2023 21:04:30.29720000 WARN: Received out of order message from exchange {Rook}
04-11-2023 21:04:30.29734000 DEBUG: Received heartbeat from exchange *Rook*
04-11-2023 21:04:30.29750000 DEBUG: Exiting unimportant code area"""
    entries = [parse_log_entry(line) for line in lines.split("\n")]
    for entry in entries:
        log_file.add_entry(entry)
