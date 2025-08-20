import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


numero_punti_grafico = 350
numero_nodi = 300
numero_connessioni = np.zeros(numero_nodi)
zero_uno = 1

def piecewise(x):
    if x == mean + variance:
        return 0.5
    if x == mean - variance:
        return 0.5
    return 0

def esponenziale(x):
    if x<3:
        return 0
    else:
        return np.exp(-x/6)


def trova_connessioni(funzione, minimo, massimo):
    probabilità = np.zeros(massimo)
    for i in range(minimo,massimo):
        probabilità[i] = funzione(i)    
    numero_connessioni = random.choices(np.arange(0,1000),probabilità,k=numero_nodi)
    return numero_connessioni


def make_graph(numero_connessioni):
    
    lista_non_zero = []
    for i in range(0,numero_nodi):
        if numero_connessioni[i]!=0:
            lista_non_zero.append(i)
    G = nx.Graph()
    matrice_adiacenza = [[] for i in range(0,numero_nodi)]
    while(len(lista_non_zero)>=2):
        a = np.argmax(numero_connessioni)
        b = random.choice(lista_non_zero)

        while(b==a):
            b = random.choice(lista_non_zero)

        matrice_adiacenza[a].append(b)
        matrice_adiacenza[b].append(a)
        G.add_edge(a,b)
        numero_connessioni[a] -= 1
        if numero_connessioni[a] == 0:
            lista_non_zero.remove(a)
        numero_connessioni[b] -= 1
        if numero_connessioni[b] == 0:
            lista_non_zero.remove(b)
    for i in lista_non_zero:
        print("numero connessioni ",numero_connessioni[i])
    return (matrice_adiacenza,G)


def stampa(matrice_adiacenza,G):
    my_pos = nx.spring_layout(G, seed = 100)
    rho = np.zeros(numero_punti_grafico)

    effort = np.ones(numero_nodi)*zero_uno
    for s in range(0,numero_punti_grafico):
        for _ in range(0,5):
            a = np.random.choice(range(0,numero_nodi))

            if np.sum(effort[matrice_adiacenza[a]]) == 0:
                effort[a] = 1
            else:
                effort[a] = 0

        color_map = []
        for i in range(0,len(effort)):
            if (effort[i]==0):
                color_map.append('black')
            else:
                color_map.append('yellow')

        color_border = []
        for i in range(0,numero_nodi):
            if np.sum(effort[matrice_adiacenza[i]]) + effort[i] == 0:
                color_border.append('red')
#            elif np.sum(effort[matrice_adiacenza[i]])*effort[i] == 0:
#                color_border.append('blue')
            else:
                color_border.append(color_map[i])


        rho[s] = np.sum(effort)
        plt.clf()
        nx.draw(G, pos=my_pos, node_color=color_map, width=0.15, edgecolors = color_border, node_size = 75)
        if s>75:
            plt.pause(0.02)
        else:
            plt.pause(0.05)

    color_map = []
    for i in range(0,numero_nodi):
        if np.sum(effort[matrice_adiacenza[i]])*effort[i] == 0 and np.sum(effort[matrice_adiacenza[i]])+effort[i]>0:

            color_map.append('green')
        else:
            color_map.append('red')
    plt.figure()
    nx.draw(G, pos=my_pos, node_color=color_map, width=0.15, node_size = 75)

    return rho


x = np.arange(0,1000)
mean = 10
variance = 8

funzione = lambda x: piecewise(x)
#funzione = lambda x: x**(-2.5)
#funzione = lambda x: np.exp(-x/6)



numero_connessioni = trova_connessioni(funzione,1,1000)






aus = make_graph(numero_connessioni)
matrice_adiacenza = aus[0]
G = aus[1]



rho = stampa(matrice_adiacenza,G)



plt.figure()
plt.plot(np.arange(0,numero_punti_grafico),rho)
print(rho[numero_punti_grafico-1])
plt.show()
