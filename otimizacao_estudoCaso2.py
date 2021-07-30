#%%
# Otimização estrutural do caso 2
## A otimização, area que busca encontrar soluções otimas para os problemas, permeia todas as areas da engenharia, desde a parte de projeto conceitual onde esta é usada para conceitos conceituais de projetos, mas também é muito usada na remanufatura de projetos, tentado otimizar esse quanto a um dado objetivo. 


## A ideia aqui é usar um algoritmo genetico para otimizar um estrutura treliçada, tendo como variaveis de otimização as areas das seções transversais de cada tubo. Tendo como funções de avaliação a tensão no elemento de treliça e o volume da estrutura, buscando minimizar a tensão e o volume da estrutura. Para isso vamos usar a biblioteca de algoritmos géneticos DEAP e o algoritmo multiobjetivo NSGA II.


# %%
### Definindo o problema
import random

from Treelicia import Fem3d
import numpy as np
import plotter3D as plott
import matplotlib.pyplot as plt

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
 

# montando a geometri
L = 9 # comprimento da cauda
n = 5 # numero de pontos por reta

## direita
y_sup_d = lambda i: (-0.15-i*0.45, L-i*L, 0.6)
nodes1 = ([y_sup_d(i)  for i in np.linspace(0,1,n)])

#y_inf_d = lambda j: (-0.15-j*0.45, L-j*L, 0.3-j*0.9)
#nodes2 = ([y_inf_d(i)  for i in np.linspace(0,1,n)])

## esquerda
y_sup_e = lambda i: (0.6-i*0.45, 0+i*L, 0.6)
nodes3 = ([y_sup_e(i)  for i in np.linspace(1,0,n)])

y_inf_e = lambda j: (0, 0+j*L, -0.6+j*0.9)
nodes4 = ([y_inf_e(i)  for i in np.linspace(1,0,n)])

# ponto final
nodes5 = ([ (0, L+2.4, 0.6+0.1) ])

nodes = []
nodes.extend(nodes1)
#nodes.extend(nodes2)
nodes.extend(nodes3)
nodes.extend(nodes4)
nodes.extend(nodes5)

# add index
nodes = tuple( [ (j, nodes[j][0], nodes[j][1], nodes[j][2]) for j in range(len(nodes))] )

# elementos 
## segmentos retos
elementos1 = ([ (i,i+1) for i in range(n-1)  ] )
elementos2 = ([ (i,i+1) for i in range(n,2*n-1)])
elementos3 = ([ (i,i+1) for i in range(2*n,3*n-1)])
#elementos4 = ([ (i,i+1) for i in range(3*n,4*n-1)])

## elementos triangulares
elementos4 = ([ (i, i+n) for i in range(0,n)])
elementos5 = ([ (i+n,i ) for i in range(n,2*n)])
elementos6 = ([ (i+2*n, i) for i in range(0,n)])

# elemento final 
elementos7 = ( (0,len(nodes)-1),
               (n ,len(nodes)-1),
               (2*n ,len(nodes)-1)
)

# elemento trocados
elementos8 = (
            (14,3),
            (14,8),
            (13,7),
            (13,2),
            (12,6),
            (12,1),
            (11,5),
            (11,0),
            (9,3),
            (8,2),
            (7,1),
            (6,0),
)
               

elementos = []
elementos.extend(elementos1)
elementos.extend(elementos2)
elementos.extend(elementos3)
elementos.extend(elementos4)
elementos.extend(elementos5)
elementos.extend(elementos6)
elementos.extend(elementos7)
elementos.extend(elementos8)

elementos = tuple( [ (j, elementos[j][0], elementos[j][1]) for j in range(len(elementos))] )

F = 100000 #N
forcas = (
    #(15, 0, -F),
    (15, 1, -0.75*F),
    (15, 2, 0.5*F),
)

contorno = (
    (4,0,0),
    (4,1,0),
    (4,2,0),
    (9,0,0),
    (9,1,0),
    (9,2,0),
    (14,0,0),
    (14,1,0),
    (14,2,0)
)

E2 = 73e9#gpa aluminio
A2 =  0.0013# m^2 - diametro de 4 cm
rho =  27000# kg/m^3

MAX_ATRIB = 8
AREA_REF = 0.0013/4.0 #m^2



def stress(individuo):
    individuo = np.array(individuo)
    
    try:
        A2 = AREA_REF*individuo
        model1 = Fem3d(nodes, elementos, forcas, contorno, E2, A2, rho)
        deslocamento, reacoes = model1.solve()
        tensoes = model1.getStress(deslo= deslocamento)
        
    except:
        return 10**12
    return max(np.abs(tensoes)*10**-6)

def volume(individuo):
    individuo = np.array(individuo)
    volu = 0
    ltotal = 0
    for index, elem in enumerate(elementos):
        # index é o elemento
        x = nodes[elem[1]][1] - nodes[elem[2]][1]
        y = nodes[elem[1]][2] - nodes[elem[2]][2]
        z = nodes[elem[1]][3] - nodes[elem[2]][3]
        L = np.sqrt(x**2+y**2+z**2)
        ltotal += L
        volu += AREA_REF*individuo[index]*L
    return volu
    
def fitness(individuo):

    vol = volume(individuo)
    tensao = stress(individuo)

    plt.plot(vol, tensao, '.', color="black")

    return vol, tensao

def crossover(indiA, indiB):
    troca = random.randint(1,len(indiA)-2)
    
    aux = indiA[0:troca]
    indiA[0:troca] = indiB[0:troca]
    indiB[0:troca] = aux
    return indiA, indiB

def checkGeometria(individuo):
    
    for index, gene in enumerate(individuo):

        if not(gene >= 1 and gene <= 8):
            
            return False 
    
    return True


creator.create("FitnessMax", base.Fitness, weights=(-1.0,-1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 1, MAX_ATRIB)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(elementos))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low = 1, up = MAX_ATRIB, indpb = 0.05)
toolbox.register("select", tools.selNSGA2)

def main(max_generations, population_size):


    NGEN = max_generations
    MU = population_size
    LAMBDA = 100
    CXPB = 0.7
    MUTPB = 0.2

    random.seed(64)
    
    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats, halloffame=hof)


    return pop, stats, hof



if __name__ == "__main__":
    import plotter3D as plott

    [pop, logger, hof] = main(300, 100)
    best = hof.items[-1]
    print()
    print("Melhor Solucao = ",best, volume(best))
    print("Fitness do melhor individuo = ", best.fitness.values[0])
    x = []
    y = []
    for ind in hof:
        x.append(volume(ind))
        y.append(stress(ind))
    plt.title('Otimização usando algoritmo NSGA - II')
    plt.plot(x, y, '.', color="green", label = 'Fronteira de pareto')
    plt.ticklabel_format(style="plain")
    plt.grid()
    plt.xlabel("Volume dos tubos")
    plt.ylabel("Stress [Mpa]")
    plt.legend()
    plt.show()
    
    #-------- sem otimizacao
    model2 = Fem3d(nodes,elementos,forcas,contorno,E2,0.0013,rho)
    Deslocamento2, reacoes2 = model2.solve()
    tensoes2 = model2.getStress(deslo= Deslocamento2)
    tensoes2 = np.array(tensoes2)*(10**-6) #mpa
    pos = plott.Posprocess(model2)
    pos.plotStress3D(tensoes2, var='[Mpa]')

    #-------- otimizacao
    model2 = Fem3d(nodes,elementos,forcas,contorno,E2,AREA_REF*np.array(best),rho)
    Deslocamento2, reacoes2 = model2.solve()
    tensoes2 = model2.getStress(deslo= Deslocamento2)
    tensoes2 = np.array(tensoes2)*(10**-6) #mpa
    pos = plott.Posprocess(model2)
    pos.plotStress3D(tensoes2, var='[Mpa]')

    # printando os resultados 
    print('=============================================')
    print('\t\tDeslocamentos')
    print('=============================================')
    print(f'GL \t\t Desl. [mm] \t\t Reacoes [N]')

    for index in range(len(Deslocamento2)):
        print('{0:1.2f} \t\t {1:4.4f} \t\t {2:4.4f}'.format(index, Deslocamento2[index], reacoes2[index]))

    print('=============================================')
    print('\t\tTensões')
    print('=============================================')
    print(f'Elemento \t\t Tensão [Pa] \t\t Area [mm] ')

    for index in range(len(tensoes2)):
        print('{0:1.2f}  \t\t {1:4.4f} \t\t {2:4.4f} '.format(index, tensoes2[index], AREA_REF*best[index]))

    plt.show()

#Volume da estrura:  0.09820291580533828
#Tensão maxima:  368.6936618400466