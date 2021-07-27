#%%
# Trabalho final da materia de introdução a elementos finitos
# implementação de um solver de treliça 3d para elementos de area, e material variavel.
# calculo dos deslocamentos, reações, tensões, modo de vibrar e frequencia natural.
# autor: Triplex Aviation
import numpy as np
from scipy.linalg import eigh

class Fem3d:

    def __init__(self, nodesI, elementosI, forcasI, contornoI, Ei, Ai, rhoi):
        ''' definindo os inputs do problema '''

        self.nodes = nodesI
        self.elementos = elementosI
        self.forcas = forcasI
        self.contorno = contornoI

        # determinando graus de liberdade livres
        u_gamma = [] 
        u_val = []
        for cc in self.contorno:
            u_gamma.append(cc[0]*3+cc[1]) # dof no freedom
            u_val.append(cc[2]) # values

        u_livres = [i for i in range(3*len(self.nodes)) if i not in u_gamma]

        self.u_livres = u_livres
        self.u_gamma = u_gamma
        self.u_val = u_val


        # manter como vetor 
        if (type(Ai) == int or type(Ai) == float):
            self.A = [Ai]*len(self.elementos)
        else:
            self.A = Ai

        if (type(Ei) == int or type(Ei) == float):
            self.E = [Ei]*len(self.elementos)
        else:
            self.E = Ei
        
        #self.rho = rho # add matriz como vetor para diferentes materiais

        if (type(rhoi) == int or type(rhoi) == float):
            self.rho = [rhoi]*len(self.elementos)
        else:
            self.rho = rhoi





    def __rididezElement(self, E1, A1, x1, x2): # elemento(x,y,z)
        ''' retorna a matriz elementar de rigidez '''

        L = np.sqrt((x2[0]-x1[0])**2+(x2[1]-x1[1])**2+(x2[2]-x1[2])**2)

        cx = (x2[0]-x1[0])/L
        cy = (x2[1]-x1[1])/L
        cz = (x2[2]-x1[2])/L

        cx2 = cx**2
        cy2 = cy**2
        cz2 = cz**2

        cxcy = cx*cy
        cxcz = cx*cz
        cycz = cy*cz

        K = (A1*E1/L)*np.array((
            (cx2, cxcy, cxcz, -cx2, -cxcy, -cxcz),
            (cxcy, cy2, cycz, -cxcy, -cy2, -cycz),
            (cxcz, cycz, cz2, -cxcz, -cycz, -cz2),
            (-cx2, -cxcy, -cxcz, cx2, cxcy, cxcz),
            (-cxcy, -cy2, -cycz, cxcy, cy2, cycz),
            (-cxcz, -cycz, -cz2, cxcz, cycz, cz2),
           
        ))

        return K

    def __massElement(self, E1, A1, rho1, x1, x2):
        ''' retorna a matriz elementar de massa '''

        L = np.sqrt((x2[0]-x1[0])**2+(x2[1]-x1[1])**2+(x2[2]-x1[2])**2)

        cx = (x2[0]-x1[0])/L
        cy = (x2[1]-x1[1])/L
        cz = (x2[2]-x1[2])/L

        cx2 = cx**2
        cy2 = cy**2
        cz2 = cz**2

        cxcy = cx*cy
        cxcz = cx*cz
        cycz = cy*cz

        Me = (A1*rho1*L/6)*np.array((
            (2*cx2, 2*cxcy, 2*cxcz, cx2, cxcy, cxcz),
            (2*cxcy, 2*cy2, 2*cycz, cxcy, cy2, cycz),
            (2*cxcz, 2*cycz, 2*cz2, cxcz, cycz, cz2),
            (cx2, cxcy, cxcz, 2*cx2,  2*cxcy, 2*cxcz),
            (cxcy, cy2, cycz, 2*cxcy, 2*cy2,  2*cycz),
            (cxcz, cycz, cz2, 2*cxcz, 2*cycz, 2*cz2),
        ))

        return Me

    def matrizGlobal(self):
        ''' retorna a matriz global de rigidez '''

        rigides_global3 = np.zeros((3*len(self.nodes), 3*len(self.nodes)))
        mass_global3 = np.zeros((3*len(self.nodes), 3*len(self.nodes)))

        for elem in self.elementos:

            no1 = elem[1] # esquerda do elemento
            no2 = elem[2] # direita 

            x1 = self.nodes[no1][1:]
            x2 = self.nodes[no2][1:]

            # implementacao para elementos de materiais e areas diferentes.
            rigides_local = self.__rididezElement(self.E[elem[0]], self.A[elem[0]], x1, x2)
            mass_local = self.__massElement(self.E[elem[0]], self.A[elem[0]], self.rho[elem[0]], x1, x2)

            
            A_matriz = np.zeros((6,3*len(self.nodes))) #(gl_elem, gl_total)
            A_matriz[0][3*no1]      += 1
            A_matriz[1][3*no1+1]    += 1
            A_matriz[2][3*no1+2]    += 1
            A_matriz[3][3*no2]      += 1
            A_matriz[4][3*no2+1]    += 1
            A_matriz[5][3*no2+2]    += 1

            rigides_global3 += np.matmul(np.matmul(np.transpose(A_matriz),rigides_local),A_matriz)
            mass_global3 += np.matmul(np.matmul(np.transpose(A_matriz),mass_local),A_matriz)
        
        return rigides_global3, mass_global3

    def forcasGlobais(self):
        ''' retorna o vetor de forças globais - modelando sem peso da treliça'''

        forcas_global = np.zeros(3*len(self.nodes))
        for f in self.forcas:
            forcas_global[3*f[0]+f[1]] += f[2]

        return forcas_global 

    def getmodoVibration(self):

        matrizRig, matrizMass = self.matrizGlobal()

        matrizRig = np.delete(matrizRig,self.u_gamma,0)
        matrizRig = np.delete(matrizRig,self.u_gamma,1)
        
        matrizMass = np.delete(matrizMass,self.u_gamma,0)
        matrizMass = np.delete(matrizMass,self.u_gamma,1)

        omega, phi = eigh(matrizRig, matrizMass)
        freq = omega**0.5
        freq = freq/(2*np.pi)

        number_nodes = len(self.nodes)
       
        for i in self.u_gamma:
            phi = np.insert(phi, i, np.zeros(3*number_nodes - len(self.u_gamma)), axis = 1)

        
        return freq, phi

    
    def getStress(self, deslo):

        """ retorna a tensão nos elementos """

        sigma = []
        for i in self.elementos:
            elemF = np.array([i[1]*3, i[1]*3+1, i[1]*3+2, 
                              i[2]*3, i[2]*3+1, i[2]*3+2 ])

            xa = self.nodes[i[2]][1] - self.nodes[i[1]][1]
            ya = self.nodes[i[2]][2] - self.nodes[i[1]][2]
            za = self.nodes[i[2]][3] - self.nodes[i[1]][3]

            #print(f'elementos: xa = {xa}, ya = {ya}, za = {za}')
            L = np.sqrt( xa**2 + ya**2 + za**2 )
            CXx = xa/L
            CYx = ya/L
            CZx = za/L
            
            T = np.array((-CXx, -CYx, -CZx, CXx, CYx, CZx))

            aux = self.E[i[0]]/L*np.matmul(T , deslo[np.ix_(elemF)] )
            sigma.append(aux)

        return sigma
    

    def solve(self):
        ''' aplica a cc sobre as matrizes e encontra os deslocamentos , reações e tensão '''

        
        # pegar a matriz de rigidez global
        rigidez_global4, __ = self.matrizGlobal()

        k11 = rigidez_global4[np.ix_(self.u_livres, self.u_livres)]
        k12 = rigidez_global4[np.ix_(self.u_gamma,  self.u_livres)]
        k21 = rigidez_global4[np.ix_(self.u_livres, self.u_gamma)]
        k22 = rigidez_global4[np.ix_(self.u_gamma,  self.u_gamma)]

        # pegar o vetor global de forças
        forcas_global4 = self.forcasGlobais()
        

        f1 = forcas_global4[self.u_livres]

        #solve

        u4 = np.linalg.solve(k11, f1 - np.matmul(np.transpose(k12), self.u_val))

        # reações

        f2 = np.matmul(np.transpose(k21), u4) + np.matmul(k22, self.u_val)

        force = np.zeros(3*len(self.nodes))
        deslo  = np.zeros(3*len(self.nodes))
        deslo[np.ix_(self.u_livres)] = u4
        force[np.ix_(self.u_gamma)] = f2
        #tensao = self.stressElement(deslo)

        return deslo, force

   
if __name__ == '__main__':
    # material 
    # validação do codigo - teste com exemplo livro matlab for code FEA - ferreira problema 04 
    nodes = ( # (n_no, x_no,y_no,z_no)
        (0,72.0,0.0,0.0),
        (1,0.0,36.0,0.0),
        (2,0.0,36.0,72.0),
        (3,0.0,0.0,-48.0),
        
    )

    elementos = ( #(n_elemento, no_esquerda, no_direita)
        (0,0,1),
        (1,0,2),
        (2,0,3),
    )
    ## forcas
    forcas = ( #(no, grau_liberdade, forca)
        (0,2,-1000.0),
    )

    ## condicao de contorno
    contorno = ( #(no, grau_liberdade, cc)
           (1,0,0),
           (1,1,0),
           (1,2,0),
           (2,0,0),
           (2,1,0),
           (2,2,0),
           (3,0,0),
           (3,1,0),
           (3,2,0),
    )

    E2 = 1.2e6#210e9 # n/mm2
    A2 = [0.302, 0.729, 0.187]#[10*10**-4, 20*10**-4, 30*10**-4]
    rho = 2.76e-3

    model1 = Fem3d(nodes,elementos,forcas,contorno,E2,A2,rho)
    Deslocamento, reacoes = model1.solve()
    tensoes = model1.getStress(deslo= Deslocamento)
    omega, phi = model1.getmodoVibration()
    
    
    import plotter3D as plott
    # plotando os dados obtidos 

    pos = plott.Posprocess(model1)
    #pos.plotDeslocamento3D(Deslocamento)
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
