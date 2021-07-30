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
A otimização, area que busca encontrar soluções otimas para os problemas, permeia todas as areas da engenharia, desde a parte de projeto conceitual onde esta é usada para conceitos conceituais de projetos, mas também é muito usada na remanufatura de projetos, tentado otimizar esse quanto a um dado objetivo. 


A ideia aqui é usar um algoritmo genetico para otimizar um estrutura treliçada, tendo como variaveis de otimização as areas das seções transversais de cada tubo. Tendo como funções de avaliação a tensão no elemento de treliça e o volume da estrutura, buscando minimizar a tensão e o volume da estrutura. Para isso vamos usar a biblioteca de algoritmos géneticos DEAP e o algoritmo multiobjetivo NSGA II.
