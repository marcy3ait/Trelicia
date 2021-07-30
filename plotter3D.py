from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm


class Posprocess():
    """ 
    Classe destinada ao pos processamento dos dados de treliça tridimensional
    - plotar os graficos
    """

    def __init__(self, model):
        self.nodes = model.nodes
        self.elementos =  model.elementos
        self.contorno = model.contorno
        self.A = model.A
        self.forcas = model.forcas
        

        # material
        self.modYoung = model.E

    def plotDeslocamento3D(self, des):

        fig = plt.figure('Plote das forma deformada')
        #ax = fig.add_subplot(111, projection='3d')
        ax = plt.axes(projection='3d')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        scale =  1./np.max(np.abs(des))
        ax.set_title(f'Deslocamento da estrutura')

        for pontos in self.contorno:
            #print(self.nodes[pontos[0]][1], self.nodes[pontos[0]][2], self.nodes[pontos[0]][3])
            ax.scatter3D(self.nodes[pontos[0]][1], self.nodes[pontos[0]][2], self.nodes[pontos[0]][3], marker = '*', color = 'black')

    
        for elem in self.elementos:

            #ax.scatter3D(  [self.nodes[elem[1]][1], self.nodes[elem[2]][1]], [self.nodes[elem[1]][2],self.nodes[elem[2]][2]], [self.nodes[elem[1]][3],self.nodes[elem[2]][3]])
            # ([Xelem1,Xelem2], [Yelem1,Yelem2], [Zelem1,Zelem2])
            ax.plot3D(  [self.nodes[elem[1]][1], self.nodes[elem[2]][1]],
                        [self.nodes[elem[1]][2], self.nodes[elem[2]][2]],
                        [self.nodes[elem[1]][3],self.nodes[elem[2]][3]], '--k' )

            #ax.text(x = self.nodes[elem[1]][1] , y = self.nodes[elem[1]][2] , z = self.nodes[elem[1]][3] , s = str(self.nodes[elem[1]][0]) )
            #ax.text(x = self.nodes[elem[2]][1] , y = self.nodes[elem[2]][2] , z = self.nodes[elem[2]][3] , s = str(self.nodes[elem[2]][0]) )



            #delocamento 
            ax.plot3D( [ self.nodes[elem[1]][1] + scale*des[3*elem[1]],        self.nodes[elem[2]][1] + scale*des[3*elem[2]]],
                       [ self.nodes[elem[1]][2] + scale*des[ 3*elem[1] + 1 ] , self.nodes[elem[2]][2] + scale*des[ 3*elem[2] + 1 ]],
                       [ self.nodes[elem[1]][3] + scale*des[ 3*elem[1] + 2 ],  self.nodes[elem[2]][3] + scale*des[ 3*elem[2]+ 2 ]],  '--r' )
        #plt.axis('equal')
        plt.show()

    def plotDeslocamento2D(self, des):

        fig = plt.figure('Plote das forma deformada')
        #ax = fig.add_subplot(111, projection='3d')
        ax = plt.axes()

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        

        scale =  1./np.max(np.abs(des))
        ax.set_title(f'Deslocamento da estrutura')

        for pontos in self.contorno:
            #plot cc
            ax.scatter(self.nodes[pontos[0]][1], self.nodes[pontos[0]][2], marker = '*', color = 'black')

   
    
        for elem in self.elementos:

           
            ax.plot(  [self.nodes[elem[1]][1], self.nodes[elem[2]][1]],
                        [self.nodes[elem[1]][2], self.nodes[elem[2]][2]], '--k' )

            #delocamento 
            ax.plot( [ self.nodes[elem[1]][1] + scale*des[3*elem[1]],        self.nodes[elem[2]][1] + scale*des[3*elem[2]]],
                    [ self.nodes[elem[1]][2] + scale*des[ 3*elem[1] + 1 ] , self.nodes[elem[2]][2]+ scale*des[ 3*elem[2] + 1 ]],  '--r' )
        #plt.axis('equal')
        plt.show()

    def plotModoVibra3D(self, phi, mode):
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

        #plt.axis('equal')
        plt.show()

    def plotModoVibra2D(self, phi, mode):
        fig = plt.figure('Plote dos modos de vibrar da estrutura')
        #ax = fig.add_subplot(111, projection='3d')
        ax = plt.axes()

        ax.set_xlabel('x')
        ax.set_ylabel('y')
    
        ax.set_title(f'{mode + 1} ° modo de vibrar da estrutura')

        scale =  3./np.max(np.abs(phi))
    
        for elem in self.elementos:
            #ax.scatter3D(  [self.nodes[elem[1]][1], self.nodes[elem[2]][1]], [self.nodes[elem[1]][2],self.nodes[elem[2]][3]], [self.nodes[elem[1]][3],self.nodes[elem[2]][3]], s = 100)
            # ([Xelem1,Xelem2], [Yelem1,Yelem2], [Zelem1,Zelem2])
            ax.plot(  [self.nodes[elem[1]][1], self.nodes[elem[2]][1]],
                        [self.nodes[elem[1]][2], self.nodes[elem[2]][2]],  color="green", linewidth=2.0, linestyle="-" )

             # modo de vibrar
            ax.plot3D(  [ self.nodes[elem[1]][1] + scale*phi[mode][3*elem[1]],        self.nodes[elem[2]][1] + scale*phi[mode][3*elem[2]] ],
                    [ self.nodes[elem[1]][2] + scale*phi[mode][ 3*elem[1] + 1 ] , self.nodes[ele[2]][2] + scale*phi[mode][ 3*elem[2] + 1 ]],  '--r' )

        #plt.axis('equal')
        plt.show()

    def plotStress3D(self, stress, var=''):
        fig = plt.figure('Plote das tensões')
        #ax = fig.add_subplot(111)
        ax = plt.axes(projection='3d')
        

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')


        ax.set_title(f'Tensão na estrutura')

        for pontos in self.contorno:
            ax.scatter3D(self.nodes[pontos[0]][1], self.nodes[pontos[0]][2], self.nodes[pontos[0]][3], marker = '*', color = 'black')
        
       


        norm = plt.Normalize(np.min(stress), np.max(stress))
        cmap = plt.get_cmap('gist_rainbow')
        c = cmap(norm(stress))

        # plotando as linhas
        for index,elem in enumerate(self.elementos):

            ax.plot3D(  [self.nodes[elem[1]][1], self.nodes[elem[2]][1]], [self.nodes[elem[1]][2],self.nodes[elem[2]][2]], [self.nodes[elem[1]][3],self.nodes[elem[2]][3]], linewidth=(self.A[index]/max(self.A))*5, markersize=5, c=c[index])
            # ([Xelem1,Xelem2], [Yelem1,Yelem2], [Zelem1,Zelem2])

            ax.text(x = self.nodes[elem[1]][1] , y = self.nodes[elem[1]][2] , z = self.nodes[elem[1]][3] , s = str(self.nodes[elem[1]][0]) )
            #ax.text(x = self.nodes[elem[2]][1] , y = self.nodes[elem[2]][2] , z = self.nodes[elem[2]][3] , s = str(self.nodes[elem[2]][0]) )

        cbar = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
        cbar.set_label('Stress '+var)
        #plt.show()  


    def plotStress2D(): 
        pass

if __name__ == '__main__':
    pass
