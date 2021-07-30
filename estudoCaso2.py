#%%
from operator import lt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 
import numpy as np

from Treelicia import Fem3d
import plotter3D as plott


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

'''

fig = plt.figure('Plote dos modos de vibrar da estrutura')
#ax = fig.add_subplot(111, projection='3d')
ax = plt.axes(projection='3d')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

for elem in elementos:

    ax.plot3D(  [nodes[elem[1]][1], nodes[elem[2]][1]],
                [nodes[elem[1]][2],  nodes[elem[2]][2]],
                [nodes[elem[1]][3],  nodes[elem[2]][3]], '--k' )

for node in nodes:
    ax.plot3D( [node[1]],[node[2]],[node[3]], 'or' )
    ax.text(x = node[1] , y = node[2] , z = node[3] , s = str(node[0]) )
    #ax.text(x = nodes[elem[2]][1] , y = nodes[elem[2]][2] , z = nodes[elem[2]][3] , s = str(nodes[elem[2]][0]) )
plt.show()
'''
F = 10000 #N
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

model1 = Fem3d(nodes,elementos,forcas,contorno,E2,A2,rho)
Deslocamento, reacoes = model1.solve()
tensoes = model1.getStress(deslo= Deslocamento)
omega, phi = model1.getmodoVibration()

tensoes = np.array(tensoes)*(10**-6) #Mpa
import plotter3D as plott
# plotando os dados obtidos 

pos = plott.Posprocess(model1)

# plotando deslocamento
#pos.plotDeslocamento3D(Deslocamento)
pos.plotStress3D(tensoes, var='[Mpa]')
plt.show()

# plotando modo de vibrar da estrutura 
#pos.plotModoVibra3D(phi, mode = 0)

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

volu = 0
ltotal = 0
for index, elem in enumerate(elementos):
    # index é o elemento
    area =  0.0013
    x = nodes[elem[1]][1] - nodes[elem[2]][1]
    y = nodes[elem[1]][2] - nodes[elem[2]][2]
    z = nodes[elem[1]][3] - nodes[elem[2]][3]
    L = np.sqrt(x**2+y**2+z**2)
    ltotal+=L
    volu += area*L

print('Volume da estrura: ',volu)
print('Tensão maxima: ', max(np.abs(tensoes)))

# %%
