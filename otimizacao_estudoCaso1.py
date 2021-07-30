#%%
# Otimização estrutural
## Pequena otimização estrutural usando elementos de treliça 3d e a biblioteca de algoritmos géneticos DEAP. A inteção aqui era minimizar a tensão maxima de von misses fixando um numero maximo de elementos de area com seção de 0.1 mm^2,simulando um experimento muito comum nas faculdades a ponte de macarrão.
#%%
from otimizacao_estudoCaso2 import AREA_REF
import random

from Treelicia import Fem3d
import numpy as np
import plotter3D as plott

from deap import algorithms
from deap import base
from deap import creator
from deap import tools





L = 1000
nodes = (
    (0, 0, 0, 0 ),
    (1, -L/2, 0, np.sqrt(3)*L/2 ),
    (2, -L, 0, 0 ),
    (3, -L/2, L, np.sqrt(3)*L/2 ),
)

elementos = (
    (0, 1, 0),
    (1, 1, 2),
    (2, 0, 2),

    (3, 0, 3),
    (4, 1, 3),
    (5, 2, 3),
)

   ## forcas
forcas = ( #(no, grau_liberdade, forca)
    (3,2,-100.0),
    
)

## condicao de contorno
contorno = ( #(no, grau_liberdade, cc)
    (0,0,0),
    (0,1,0),
    (0,2,0),

    (1,0,0),
    (1,1,0),
    (1,2,0),

    (2,0,0),
    (2,1,0),
    (2,2,0),
)

E2 = 3600#Mpa do macarrao 
#rho =  [2.76e-3, 2.86e-3, 2.96e-3, 2.66e-3, 2.56e-3, 2.46e-3]#2.76e-3

rho = 2.66e-3
CargaRuptura = 42.6 #N

MIN_ATRIB = 3
MAX_ATRIB = 10
AREA_REF = 0.2

def fitness(individual):

    #crossSection do macarrao 1.2 #mm^2
    try:
        A2 = AREA_REF*individual
        model1 = Fem3d(nodes,elementos,forcas,contorno,E2,A2,rho)
        Deslocamento, reacoes = model1.solve()
        tensoes = model1.getStress(deslo= Deslocamento)
    except:
        return 1000
    return max(np.abs(tensoes)),

def volume(individuo):
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
    
def checkGeometria(individuo):
    # pacote de macarrao tem 500 fios
    vol = volume(individuo)
    if (vol > 0. and vol <= 7000.):
        return True 
    
    return False

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.uniform, MIN_ATRIB, MAX_ATRIB)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=6)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", fitness)
toolbox.decorate("evaluate", tools.DeltaPenalty(checkGeometria, [10**10]))
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low = MIN_ATRIB, up = MAX_ATRIB, indpb = 0.08)
toolbox.register("select", tools.selTournament, tournsize=5)

def main():
    random.seed(64)
    
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(15, similar=np.array_equal)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50,stats=stats, halloffame=hof, verbose=True)

    return pop, stats, hof



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import plotter3D as plott



    pop, logger, hof = main()

    gen = logger.select("gen")
    fit = logger.select("max")
    avg = logger.select("avg")
    plt.plot(gen,fit, '--r', label = "melhores individuos")
    plt.plot(gen,avg, '--b', label = "media dos individuos")
    plt.xlabel('fitness')
    plt.ylabel('geração')
    plt.legend()
    plt.title('Pontuação dos melhores individuos')
    plt.grid()
    plt.show()

    best = hof.items[0]
    print()
    print("Melhor Solucao = ", best, sum(best))
    print("Fitness do melhor individuo = ", best.fitness.values[0])
    A2 =   [0.302, 0.729, 0.187, 0.302, 0.729, 0.187] 
    model1 = Fem3d(nodes,elementos,forcas,contorno,E2,A2,rho)
    Deslocamento, reacoes = model1.solve()
    tensoes = model1.getStress(deslo= Deslocamento) 
    pos = plott.Posprocess(model1)
    pos.plotStress3D(tensoes, var='[MPa]')

   # printando os resultados 
    print('=============================================')
    print('\t\tDeslocamentos')
    print('=============================================')
    print(f'GL \t\t Desl. [mm] \t\t Reacoes [N]')

    for index in range(len(Deslocamento)):
        print('{0:1.2f} \t\t {1:4.4f} \t\t {2:4.4f}'.format(index, Deslocamento[index], reacoes[index]))

    print('=============================================')
    print('\t\tTensões')
    print('=============================================')
    print(f'Elemento \t\t Tensão [Pa] \t\t Area [mm]')

    for index in range(len(tensoes)):
        print('{0:1.2f} \t\t {1:4.4f} \t\t {2:4.4f} '.format(index, tensoes[index],A2[index]))
    
    #-------- otimizacao
    model2 = Fem3d(nodes,elementos,forcas,contorno,E2,AREA_REF*np.array(best),rho)
    Deslocamento2, reacoes2 = model2.solve()
    tensoes2 = model2.getStress(deslo= Deslocamento2)
    pos = plott.Posprocess(model2)
    pos.plotStress3D(tensoes2,var='[MPa]')

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