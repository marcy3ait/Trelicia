#%%
# Otimização estrutural
## Pequena otimização estrutural usando elementos de treliça 3d e a biblioteca de algoritmos géneticos DEAP. A inteção aqui era minimizar a tensão maxima de von misses fixando um numero maximo de elementos de area com seção de 0.1 mm^2,simulando um experimento muito comum nas faculdades a ponte de macarrão.
#%%
import random

from Treelicia import Fem3d
import numpy as np
import plotter3D as plott

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 3, 10)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=6)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)




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
    (3,1,-100.0),
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

E2 = 1.2e6#210e9 # n/mm2 
rho =  [2.76e-3, 2.86e-3, 2.96e-3, 2.66e-3, 2.56e-3, 2.46e-3]#2.76e-3



def fitness(individual):

    #crossSection do macarrao 0.01 #mm^2
    try:
        A2 = 0.1*individual
        model1 = Fem3d(nodes,elementos,forcas,contorno,E2,A2,rho)
        Deslocamento, reacoes = model1.solve()
        tensoes = model1.getStress(deslo= Deslocamento)
    except:
        return 1000
    return max(np.abs(tensoes)),

def checkGeometria(individuo):
    
    for index, gene in enumerate(individuo):
        if not(gene >= 3 and gene <=10) or sum(individuo) >= 26:
            return False 
    
    return True

toolbox.register("evaluate", fitness)
toolbox.decorate("evaluate", tools.DeltaPenalty(checkGeometria, [1000]))
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(64)
    
    pop = toolbox.population(n=500)
    hof = tools.HallOfFame(15, similar=np.array_equal)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=100, stats=stats,
                        halloffame=hof)

    return pop, stats, hof



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import plotter3D as plott



    [pop, logger, hof] = main()
    best = hof.items[0]
    print()
    print("Melhor Solucao = ", best, len(best))
    print("Fitness do melhor individuo = ", best.fitness.values[0])
    A2 =   [0.302, 0.729, 0.187, 0.302, 0.729, 0.187] 
    model1 = Fem3d(nodes,elementos,forcas,contorno,E2,A2,rho)
    Deslocamento, reacoes = model1.solve()
    tensoes = model1.getStress(deslo= Deslocamento) 
    pos = plott.Posprocess(model1)
    pos.plotStress3D(tensoes)

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
    model2 = Fem3d(nodes,elementos,forcas,contorno,E2,0.1*np.array(best),rho)
    Deslocamento2, reacoes2 = model2.solve()
    tensoes2 = model2.getStress(deslo= Deslocamento2)
    pos = plott.Posprocess(model2)
    pos.plotStress3D(tensoes2)

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
        print('{0:1.2f}  \t\t {1:4.4f} \t\t {2:4.4f} '.format(index, tensoes2[index], 0.1*best[index]))
   