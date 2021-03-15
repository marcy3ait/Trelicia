#%%

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


class Posprocess():
    """ 
    Classe destinada ao pos processamento dos dados de treliça tridimensional
    - plotar os graficos
    """

    def __init__(self, model):
        self.nodes = model.nodes
        self.elementos =  model.elementos

        # material
        self.modYoung = model.E

    def plotDeslocamento(self, des):

        fig = plt.figure('Plote dos deslocamentos')
        #ax = fig.add_subplot(111, projection='3d')
        ax = plt.axes(projection='3d')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        scale =  1./np.max(np.abs(des))
        ax.set_title(f'Deslocamento da estrutura - fator de escala {scale}')
    
        for elem in self.elementos:

            ax.scatter3D(  [self.nodes[elem[1]][1], self.nodes[elem[2]][1]], [self.nodes[elem[1]][2],self.nodes[elem[2]][2]], [self.nodes[elem[1]][3],self.nodes[elem[2]][3]])
            # ([Xelem1,Xelem2], [Yelem1,Yelem2], [Zelem1,Zelem2])
            ax.plot3D(  [self.nodes[elem[1]][1], self.nodes[elem[2]][1]],
                        [self.nodes[elem[1]][2], self.nodes[elem[2]][2]],
                        [self.nodes[elem[1]][3],self.nodes[elem[2]][3]], color="blue", linewidth=2.0, linestyle="-" )

            ax.text(x = self.nodes[elem[1]][1] , y = self.nodes[elem[1]][2] , z = self.nodes[elem[1]][3] , s = str(self.nodes[elem[1]][0]) )
            ax.text(x = self.nodes[elem[2]][1] , y = self.nodes[elem[2]][2] , z = self.nodes[elem[2]][3] , s = str(self.nodes[elem[2]][0]) )



            #delocamento 
            ax.plot3D( [ self.nodes[elem[1]][1] + scale*des[3*elem[1]],        self.nodes[elem[2]][1] + scale*des[3*elem[2]]],
                       [ self.nodes[elem[1]][2] + scale*des[ 3*elem[1] + 1 ] , self.nodes[elem[2]][2] + scale*des[ 3*elem[2] + 1 ]],
                       [ self.nodes[elem[1]][3] + scale*des[ 3*elem[1] + 2 ],  self.nodes[elem[2]][3] + scale*des[ 3*elem[2]+ 2 ]],  '--r' )
        plt.axis('equal')
        plt.show()

    def plotModoVibra(self, phi, mode):
        fig = plt.figure('Plote dos modos de vibrar da estrutura')
        #ax = fig.add_subplot(111, projection='3d')
        ax = plt.axes(projection='3d')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title(f'{mode + 1} ° modo de vibrar da estrutura')

        scale =  3./np.max(np.abs(phi))
    
        for elem in self.elementos:
            #ax.scatter3D(  [self.nodes[elem[1]][1], self.nodes[elem[2]][1]], [self.nodes[elem[1]][2],self.nodes[elem[2]][3]], [self.nodes[elem[1]][3],self.nodes[elem[2]][3]], s = 100)
            # ([Xelem1,Xelem2], [Yelem1,Yelem2], [Zelem1,Zelem2])
            ax.plot3D(  [self.nodes[elem[1]][1], self.nodes[elem[2]][1]],
                        [self.nodes[elem[1]][2], self.nodes[elem[2]][2]],
                        [self.nodes[elem[1]][3],self.nodes[elem[2]][3]],  color="green", linewidth=2.0, linestyle="-" )

             # modo de vibrar
            ax.plot3D(  [ self.nodes[elem[1]][1] + scale*phi[mode][3*elem[1]],        self.nodes[elem[2]][1] + scale*phi[mode][3*elem[2]] ],
                        [ self.nodes[elem[1]][2] + scale*phi[mode][ 3*elem[1] + 1 ] , self.nodes[elem[2]][2] + scale*phi[mode][ 3*elem[2] + 1 ]],
                        [ self.nodes[elem[1]][3] + scale*phi[mode][ 3*elem[1] + 2 ],  self.nodes[elem[2]][3] + scale*phi[mode][ 3*elem[2]+ 2 ]],  '--r' )

        plt.axis('equal')
        plt.show()


# %%
