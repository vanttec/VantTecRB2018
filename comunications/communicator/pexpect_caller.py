import time
import pexpect
from pexpect import popen_spawn
from random import randint
from Distances import get_distances

TIME_DIVIDER = 10.0
MAX_TIME = 30

def generate_data():
    result = []
    for i in range(10):
        x1 = randint(1, 50)
        y1 = randint(50, 100)
        x2 = randint(50, 100)
        y2 = randint(1, 50)
        result.append([x1, y1, x2, y2])
    return result

def parse_data(data):
    '''Parse data from string to get coordinates in float values'''
    start_index = data.find("(")
    # Cut last 2 characters of data ")}"
    values = data[(start_index + 1):-2]
    coordinates = values.split(",")
    # Parse to float the coordinate values
    float_values = list(map(lambda x: float(x), coordinates))
    return float_values


def call():
    '''Realiza llamadas a codigo de red neuronal en C y pasa datos a codigo path.py'''
    # https://pexpect.readthedocs.io/en/stable/overview.html
    # Spawn process to call neural net
    # child = pexpect.spawn('./darknet') or pexpect.spawn('python darknet.py')
    # Skip first 31 lines of output
    # counter = 0
    # while counter < 31:
    #     child.expect('.*')
    #     counter += 1
    # Expected output from darknet: {b, 0.583, (2.5, 30.58, 78.5, 4.78)}
    start_time = time.time() # Use this for simulation of time
    while (time.time() - start_time) < MAX_TIME:
        # Expect outputs
        # child.expect('.*')
        # Print for debugging
        # print(child.after.decode("utf-8"), end='')
        # TODO Parse data of child.after
        # data = parse_data(child.after.decode("utf-8"))
        # NOTE x1 < x2, y1 > y2
        # random sleep time for testing
        time.sleep(randint(1, 10) / TIME_DIVIDER)
        get_distances(generate_data())

call()
