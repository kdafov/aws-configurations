def log(origin, seq, key, value):
    """
    Function which will print a log in human-readable format
    :param origin: Source of the log file/function_name/line_number
    :param seq: Sequential order of the log in the origin
    :param key: The main information of the log
    :param value: Any values that the key will output
    :return: Prints a log message
    """

    if len(str(value)) == 0:
        print(("LOG origin %s [seq: %s] ---> %s")%(origin,seq,key))
    else:
        print(("LOG origin %s [seq: %s] ---> %s: %s")%(origin,seq,key,value))