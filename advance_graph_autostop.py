import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random



numero_nodi = 300
zero_uno = 0

#Funzione per la distribuzione del numero di connessioni
#----------------------------------------------------------------------------------------------------
#scale-free network
def definisci_funzione(x):
    if x<3:
        return 0
    else:
        return x**(-2.5)

#funzione per parti
#mean = 10
#variance = 8
#def definisci_funzione(x):
#    if x == mean + variance:
#        return 0.5
#    if x == mean - variance:
#        return 0.5
#    return 0

#esponenziale
#def definisci_funzione(x):
#    if x<3:
#        return 0
#    else:
#        return np.exp(-x/6)



#Trova il numero di connessioni per ogni nodo
#------------------------------------------------------------------------------------------------------
def trova_connessioni(funzione, minimo, massimo):
    probabilità = np.zeros(massimo)
    for i in range(minimo,massimo):
        probabilità[i] = funzione(i)    
    numero_connessioni = random.choices(np.arange(0,1000),probabilità,k=numero_nodi)
    print(len(numero_connessioni))
    return numero_connessioni



#Crea il grafo
#------------------------------------------------------------------------------------------------------
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
    return (matrice_adiacenza,G)



#continua ad aggiornare lo sforzo di ogni agente fino a che non si raggiunge un equilibrio e stampa
#------------------------------------------------------------------------------------------------------
def stampa(matrice_adiacenza,G):
    my_pos = nx.spring_layout(G, seed = 100)
    rho = []
    fail_safe = 0
    effort = np.ones(numero_nodi)*zero_uno
    while fail_safe < 1000:
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
        check = 0
        color_border = []
        for i in range(0,numero_nodi):
            if np.sum(effort[matrice_adiacenza[i]]) * effort[i] == 0:
                if np.sum(effort[matrice_adiacenza[i]]) + effort[i] != 0:
                    color_border.append(color_map[i])
                    check += 1
                else:
                    color_border.append('red')
            else:
                color_border.append('red')


        rho.append(np.sum(effort))
        plt.clf()
        nx.draw(G, pos=my_pos, node_color=color_map, width=0.15, edgecolors = color_border, node_size = 75)
        if fail_safe>75:
            plt.pause(0.02)
        else:
            plt.pause(0.05)
        if(check == numero_nodi):
            fail_safe = 1000
        fail_safe += 1
        
    plt.figure()
    node_sizes = []
    for i in range(0,numero_nodi):
        node_sizes.append(len(matrice_adiacenza[i])*2.5)

    nx.draw(G, pos=my_pos, node_color=color_map, width=0.15, node_size = node_sizes)

    return rho



#Main

funzione = lambda x: definisci_funzione(x)
numero_connessioni = trova_connessioni(funzione,1000)
aus = make_graph(numero_connessioni)
matrice_adiacenza = aus[0]
G = aus[1]
rho = stampa(matrice_adiacenza,G)



plt.figure()
plt.plot(np.arange(0,len(rho)),rho)
print(rho[len(rho)-1])
plt.show()

