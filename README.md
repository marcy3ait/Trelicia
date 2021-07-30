# Trelicia
Implementação de númerica de um solver para treliças tridimensionais como projeto final na matéria de introdução a elementos finitos, ministrada na Universidade Estadual Paulista - UNESP (São João da Boa Vista) para curso Engenharia aeronáutica pelo Professor Dr. Murilo Sartorato.

## Estudo de Casos
A implementação realizada permite realizar os calculos dos deslocamentos, tensões, modos de vibrar e frequências naturais da estrutura. Abaixo são apresentados dois resultados parciais decorrentes da implementação, para mais detalhes dos estudos de caso consulte o [relátorio final](https://github.com/marcy3ait/Trelicia/blob/master/Relatorio_Elementos_Finitos.pdf).

### Suporte fixo na parede
Forma deformada de uma estrutura de suporte com três pontos de fixação submetido a uma força na ponta livre.

<p align="center">
  <img src="https://github.com/marcy3ait/Trelicia/blob/master/img/Plote_dos_deslocamentos_hibbler.png" width="650" title="Suporte fixo na parede">
  
</p>

### Cauda do helicóptero BELL 47G-2
Segundo modo de vibrar da cauda treliçada do helicóptero BELL 47G-2.

<p align="center">
  <img src="https://github.com/marcy3ait/Trelicia/blob/master/img/Plote_dos_modos_de_vibrar_da_estrutura-1_bell_modo1.png" width="650" title="Cauda do helicóptero BELL 47G-2">
 
</p>

## Estudo de otimização usando Trelicia
A otimização, área que busca encontrar soluções ótimas ( ou quase ótimas ) para os mais diversos problemas, permeia todas as áreas da engenharia, desde do projeto conceitual até o projeto detalhado parte do projeto conceitual, ainda também é muito usada na remanufatura de projetos, tentado otimizar esse quanto a um dado objetivo(os). 


A ideia aqui é usar um algoritmo genético para otimizar um estrutura treliçada, tendo como variáveis de otimização as área das seções transversais de cada tubo. As funções de avaliação usadas são a tensão no elemento de treliça e o volume da estrutura, buscando minimizar a tensão e o volume da estrutura. Para foi usado a biblioteca de algoritmos géneticos DEAP e o algoritmo multiobjetivo NSGA II.

<p align="left">
  <img src="https://github.com/marcy3ait/Trelicia/blob/master/img/problema.png" width="650" title="estrutura sem otimização">
 
</p>

<p align="right">
  <img src="https://github.com/marcy3ait/Trelicia/blob/master/img/solucao_otima.png" width="650" title="estrutura sem otimização">
 
</p>
