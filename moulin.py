import datetime
import os
import subprocess
import sys
import time
import tomllib

BIN = None
BASE_TIMEOUT = None
SILENT = False

class Result(object):
    def __init__(self, timedout=None) -> None:
        self.timedout = timedout
        self.procdata = None

    def __format__(self, fmt) -> str:
        return f"Result(timedout={self.timedout}, " +\
            f"procdata={self.procdata})"

def dispatch(args, secs):
    result = Result(timedout=False)

    try:
        result.procdata =\
        subprocess.run(args, timeout=secs,\
                       capture_output=True)
    except subprocess.TimeoutExpired:
        result.timedout = True

    return result

def mouline(test):
    if not test:
        return

    args = [BIN]

    if test.get('args'):
        args += test['args']

    secs = test.get('timeout')

    if secs:
        secs = datetime.timedelta(\
            hours=secs.hour,\
            minutes=secs.minute,\
            seconds=secs.second).total_seconds()

    result = dispatch(args, secs)

    print(args)
    print(f"{result}")

    return

if __name__ == '__main__':
    data = None
    filename = 'test.toml'

    with open(filename, 'rb') as file:
        data = tomllib.load(file)

    glob = data.get('global')

    if not glob:
        raise Exception(f"{filename}: missing global section")

    data.pop('global')

    BIN = glob.get('bin')
    BASE_TIMEOUT = glob.get('timeout')

    if not BIN:
        raise Exception(f"{filename}: missing binary")

    for sample in data:
        print(f"-- running {sample} --")

        if type(data[sample]) is list:
            for test in data[sample][0]:
                mouline(data[sample][0][test])
        else:
            mouline(data[sample])
