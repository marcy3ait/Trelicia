import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl

def elmCoord(elements,nodes,i):
    idx1=df_index(nodes,elements['n1'][i],'name')
    idx2=df_index(nodes,elements['n2'][i],'name')
    x1=nodes['x'][idx1]
    y1=nodes['y'][idx1]
    x2=nodes['x'][idx2]
    y2=nodes['y'][idx2]
    return x1,x2,y1,y2

def df_index(df,val,col_ID): return df.index[df[col_ID] == val].tolist()[0]

nodes=[['node 1', 3, 0],['node 2', 0, 0],['node 3', 0, 4]]
elements=[['element 1','node 2','node 3'],
          ['element 2','node 1','node 3'],
          ['element 3','node 1','node 2']]
nodes=pd.DataFrame(nodes,columns=['name','x','y'])
nodes=nodes.astype({'x':'float64','y':'float64'})
elements=pd.DataFrame(elements,columns=['name','n1','n2'])

f=[-1000,2000,3000]
fig = plt.figure(figsize = (6,4))
ax = fig.add_subplot(111)
c = np.arange(f[0], f[-1])
norm = plt.Normalize(np.min(f), np.max(f))
cmap = cm.ScalarMappable(norm=norm, cmap=mpl.cm.jet)
cmap.set_array([])
for i in range(len(elements)):
    x1,x2,y1,y2 = elmCoord(elements,nodes,i)
    ax.plot([x1,x2],[y1,y2],'-', linewidth=2, markersize=5, c=cmap.to_rgba(i))
fig.colorbar(cmap, ticks=c)
plt.show()