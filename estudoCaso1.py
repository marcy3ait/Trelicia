
#%% [markdown] 
# Estudo de caso para válidação da implementação
## Exemplo de estrutura retirada do livro Estática mecânica para engenharia - Hibbler



#%%
from numpy import testing
from Treelicia import Fem3d
import numpy as np
import plotter3D as plott


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

E2 = 1.2e6#210e9 # n/mm2
A2 =   [0.302, 0.729, 0.187, 0.302, 0.729, 0.187] 
rho =  [2.76e-3, 2.86e-3, 2.96e-3, 2.66e-3, 2.56e-3, 2.46e-3]#2.76e-3

model1 = Fem3d(nodes,elementos,forcas,contorno,E2,A2,rho)
Deslocamento, reacoes = model1.solve()
tensoes = model1.getStress(deslo= Deslocamento)
omega, phi = model1.getmodoVibration()

import plotter3D as plott
# plotando os dados obtidos 

pos = plott.Posprocess(model1)

# plotando deslocamento
pos.plotDeslocamento3D(Deslocamento)

# plotando tensao
pos.plotStress3D(tensoes)

# plotando modo de vibrar da estrutura 
pos.plotModoVibra3D(phi, mode = 2)

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
print(f'Elemento \t\t Tensão [Pa] ')

for index in range(len(tensoes)):
    print('{0:1.2f} \t\t {1:4.4f} '.format(index, tensoes[index]))

print('=============================================')
print('\t\tFrequencia naturais')
print('=============================================')
print(f'Modos \t\t Freq. [Hz] ')

for index in range(len(omega)):
    print('{0:1.2f} \t\t {1:4.4f} '.format(index, omega[index]))


# %%
