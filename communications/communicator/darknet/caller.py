import time
from random import randint
from distances import get_rois_data
from darknet import execute, execute_test

TIME_DIVIDER = 10.0
MAX_TIME = 60

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

def parse_data(data):
    results = []
    for val in data:
        if val[0] == 'b':
            results.append([1, val[2][0], val[2][1], val[2][2], val[2][3]])
        else:
            results.append([0, val[2][0], val[2][1], val[2][2], val[2][3]])
    return results

def call():
    '''Realiza llamadas a codigo de red neuronal en C y pasa datos a codigo path.py'''
    print('-------DATOS DARKNET------')
    while True:
        data = execute()
        # print(data)
        data = parse_data(data)
        # print(data)
        distances = get_rois_data(data)
        # print(distances)

call()
