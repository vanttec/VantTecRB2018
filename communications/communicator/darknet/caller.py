import time
from random import randint
from distances import get_distances
from darknet import execute

TIME_DIVIDER = 10.0
MAX_TIME = 30

def generate_data():
    '''Funcion para generar coordenadas aleatorias de objetos'''
    result = []
    for i in range(10):
        identifier = randint(0,1)
        x1 = randint(1, 50)
        y1 = randint(50, 100)
        x2 = randint(50, 100)
        y2 = randint(1, 50)
        result.append([identifier, x1, y1, x2, y2])
    return result

def call():
    '''Realiza llamadas a codigo de red neuronal en C y pasa datos a codigo path.py'''
    start_time = time.time() # Use this for simulation of time
    while (time.time() - start_time) < MAX_TIME:
        # Expect outputs
        # child.expect('.*')
        # Print for debugging
        # print(child.after.decode("utf-8"), end='')
        # Parse data string of child.after
        # data = parse_data(child.after.decode("utf-8"))
        # NOTE x1 < x2, y1 > y2
        # random sleep time for testing
        data = execute()
        print(data)
        time.sleep(randint(1, 10) / TIME_DIVIDER)
        # distances = get_distances(generate_data())
        # print(distances)

call()
