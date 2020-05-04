import random
import numpy as np
import time
import matplotlib.pyplot as plt
import pygame

def Max_Fitnes(bord_size):
    max_fitnes = 0
    i = bord_size - 1
    while(i > 0):
        max_fitnes += i
        i -= 1
    return max_fitnes

def Random_solution(bord_size):
    result = []
    for i in range(bord_size):
        result.append(random.randint(0,bord_size-1))
    return result

def Fitnes(solution):
    conflicts = 0
    n = len(solution)
    for i in range(n):
        for j in range(i+1, n):
            if i != j:
                if solution[i] == solution[j]:
                    conflicts += 1
                if abs(solution[i] - solution[j]) == abs(i - j):
                    conflicts += 1
    return conflicts

def Mutate(x):
    neighbour = x[:]
    c = random.randint(0, len(neighbour) - 1)
    m = random.randint(0, len(neighbour) - 1)
    n = len(neighbour)
    neighbour[c] = m
    return neighbour

if __name__ == "__main__":
    n = 10
    best = Random_solution(n)
    best_cost = Fitnes(best)
    counter = 0
    start_time = time.time()
    plot = []
    plt.ion()

    while best_cost != 0:
        T = 1.0
        Tmin = 0.001
        alpha = 0.9
        while T > Tmin:
            i = 1
            if best_cost != 0 and T > Tmin:
                print("T = " + str(T) + " best score: " + str(best_cost))
            while i < 100:
                next_solution = Mutate(best)
                next_cost = Fitnes(next_solution)
                P = np.exp(-(next_cost - best_cost) / T)
                if P > random.random():
                    best = next_solution
                    best_cost = next_cost

                    plot.append(best_cost)

                if best_cost == 0:
                    break
                i += 1
                counter += 1
            T = T * alpha

            plt.clf()
            plt.plot(plot)
            plt.draw()
            plt.pause(0.0001)

    print(best)

    print("{:g} s".format(time.time() - start_time))

    plt.ioff()
    plt.show()

    FPS = 150

    WIN_WIDTH_MIN = 40

    WIN_WIDTH = 500
    WIN_HEIGHT = 500

    if  (WIN_WIDTH / n) < WIN_WIDTH_MIN:
        WIN_WIDTH = WIN_WIDTH_MIN * n
        WIN_HEIGHT = WIN_WIDTH_MIN * n

    WHITE = (255, 255, 255)
    LINE = (0, 0, 0)

    pygame.init()

    clock = pygame.time.Clock()

    logotip = pygame.image.load("123.png")
    pygame.display.set_icon(logotip)

    sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    pygame.display.set_caption("chessboard")

    colour = []

    for i in range(len(best)):
        colour.append((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))

    sc.fill(WHITE)

    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT: exit()

        for i in range(0, WIN_WIDTH, int(WIN_WIDTH/n)):
            pygame.draw.line(sc, LINE, (i, 0), (i, WIN_HEIGHT), 1)
            pygame.display.update()

        for i in range(0, WIN_HEIGHT, int(WIN_HEIGHT/n)):
            pygame.draw.line(sc, LINE, (0, i), (WIN_WIDTH, i), 1)
            pygame.display.update()

        for i in range(len(best)):
            pygame.draw.circle(sc, colour[i], (i * int(WIN_HEIGHT/n) + int((WIN_HEIGHT/n)/2), (n - best[i]) * int(WIN_HEIGHT/n) - int((WIN_HEIGHT/n)/2)), int((WIN_HEIGHT/n)/4))
            pygame.display.update()

        clock.tick(FPS)