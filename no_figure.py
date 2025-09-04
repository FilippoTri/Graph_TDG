import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random




numero_nodi = 1000
zero_uno = 0



def definisci_funzione(x):
    if x<3:
        return 0
    else:
        return x**(-2.5)




def trova_connessioni(funzione, massimo):
    probabilità = np.zeros(massimo)
    for i in range(0,massimo):
        probabilità[i] = funzione(i)    
    numero_connessioni = random.choices(np.arange(0,1000),probabilità,k=numero_nodi)
    return numero_connessioni


def make_graph(lista_non_zero, numero_connessioni):

    matrice_adiacenza = [[] for i in range(0,numero_nodi)]
    while(len(lista_non_zero)>=2):
        a = np.argmax(numero_connessioni)
        b = random.choice(lista_non_zero)

        while(b==a):
            b = random.choice(lista_non_zero)

        matrice_adiacenza[a].append(b)
        matrice_adiacenza[b].append(a)
        numero_connessioni[a] -= 1
        if numero_connessioni[a] == 0:
            lista_non_zero.remove(a)
        numero_connessioni[b] -= 1
        if numero_connessioni[b] == 0:
            lista_non_zero.remove(b)

    for i in lista_non_zero:
        print("numero connessioni ",numero_connessioni[i])
    return matrice_adiacenza


def rho_finder(matrice_adiacenza,effort):

    rho =[]
    fail_safe = 40000
    for _ in range(0,fail_safe):
        check = 0

        a = np.random.choice(range(0,numero_nodi))
        if np.sum(effort[matrice_adiacenza[a]]) == 0:
            effort[a] = 1
        else:
            effort[a] = 0

        i = 0
        while  i< numero_nodi and np.sum(effort[matrice_adiacenza[i]])*effort[i] == 0 :
            if np.sum(effort[matrice_adiacenza[i]]) + effort[i] != 0:
                check += 1
            i += 1
        if check == numero_nodi:
            return rho
        
        rho.append(np.sum(effort))
    
    return rho


def fa_tutto(funzione,zero_uno):

    effort = np.ones(numero_nodi) *zero_uno
    lista_non_zero = []

    numero_connessioni = trova_connessioni(funzione,1000)

    for i in range(0,numero_nodi):
        if numero_connessioni[i]!=0:
            lista_non_zero.append(i)

    matrice_adiacenza = make_graph(lista_non_zero,numero_connessioni)

    rho = rho_finder(matrice_adiacenza,effort)
    
    plt.plot(np.arange(0,len(rho)),rho)
    print("agenti che fanno sforzo ",rho[len(rho)-1])
    print("numero di iterazioni per raggiungere equilibrio ",len(rho))


#Main
#--------------------------------------------------------------------------------------



funzione = lambda x: definisci_funzione(x)


fa_tutto(funzione,0)




plt.show()





