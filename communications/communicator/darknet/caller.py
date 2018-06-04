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

def obtain_data():
    print('-------DATOS DARKNET------')
    data = execute() #Llama darknet
    # print(data)
    if len(data):
        data = parse_data(data)
        # print(data)
        distances = get_rois_data(data) # Obtiene datos de objetos
        # print(distances)
    else:
        print('---------Nothing detected------------')

def main():
    '''AQUI SE ARMA LA CARNE'''
    while True:
        print("Escribe reto")
        reto = raw_input()
        if reto == "navgps":
            # No usa vision
            continue
        elif reto == "autonav":
            obtain_data()
        elif reto == "speed":
            obtain_data()
        elif reto == "autodock":
            # No usa vision
            continue
        else:
            obtain_data()

main()
