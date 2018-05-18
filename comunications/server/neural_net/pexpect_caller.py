import pexpect
from pexpect import popen_spawn
from Distances import get_distances

def call():
    '''Realiza llamadas a codigo de red neuronal en C y pasa datos a codigo path.py'''
    # Spawn process to call neural net
    # child = popen_spawn.PopenSpawn('./a.out')
    while True:
        # Expect outputs
        # child.expect('.*')
        # Print for debugging
        # print(child.after.decode("utf-8"), end='')
        # TODO Parse data of child.after
        get_distances([1, 2, 3, 4, 5])

call()