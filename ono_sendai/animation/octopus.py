from colorama import Style, Fore


from time import sleep
from os import system
import sys


frames = []
for i in range(5):
    with open('animation/'+str(i)+'.txt', 'r') as f:
        content = f.read()
    frames.append(f'{Fore.MAGENTA}'+content+f'{Style.RESET_ALL}')

def animate(n):
    system('clear')
    for i in range(n):
        print(frames[i%5])
        sleep(0.2)
        system('clear')

def intro():
    with open('animation/intro2.txt', 'r') as f:
        anim = f.read()
    system('clear')
    print(f'{Fore.MAGENTA}', end='')
    for ch in anim:
        print(ch, end='')
        sys.stdout.flush()
        sleep(0.01)
    # for i in range(5):
    #     system('clear')
    #     print(anim)
    #     sleep(0.4)
    print(f'{Style.RESET_ALL}')
    

if __name__ == '__main__':
    from sys import argv
    animate(int(argv[1]))
