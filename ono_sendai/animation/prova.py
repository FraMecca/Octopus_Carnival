from colorama import Style, Fore


from time import sleep
from os import system


frames = []
for i in range(5):
    with open(str(i)+'.txt', 'r') as f:
        content = f.read()
    frames.append(f'{Fore.MAGENTA}'+content+f'{Style.RESET_ALL}')

def animate(n):
    for i in range(n):
        print(frames[i%5])
        sleep(0.2)
        system('clear')

if __name__ == '__main__':
    from sys import argv
    animate(int(argv[1]))
