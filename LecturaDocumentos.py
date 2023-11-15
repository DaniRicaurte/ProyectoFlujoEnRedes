import networkx as nx
import matplotlib.pyplot as plt
import gurobipy as gp
import math
import re
from gurobipy import *

# Datos globales del grafo
datos_globales = {}

# Nodos del grafo
nodos = []

# Demanda de potencia activa de los nodos
pd = {}
# Demanda de potencia reactiva de los nodos
qd = {}

# Resistencia de los arcos
r = {}
# Reactancia de los arcos
x = {}
# Arcos
B = []

file_path = "C:\\Users\\danir\\Documents\\GitHub\\ProyectoFlujoEnRedes\\Sistemas_test\\datos33.txt"
#"/Users/juanamejia/Desktop/uni/SVII/FR/ProyectoFlujoEnRedes/datos14.txt"

def calcZbase():
    return 1000* ((datos_globales.get('vbase')**2)/datos_globales.get('sbase'))

def lecturaDocumento():
    
    #Valores globales    
    patterns = {
        'nref': r'nref\s*=\s*([\d.]+);',
        'vref': r'vref\s*=\s*([\d.]+);',
        'vbase': r'vbase\s*=\s*([\d.]+);',
        'sbase': r'sbase\s*=\s*([\d.]+);',
        'tol': r'tol\s*=\s*([\d.^-]+);', 
        'vmin': r'vmin\s*=\s*([\d.]+);',
        'vmax': r'vmax\s*=\s*([\d.]+);',
        'zbase': r'zbase\s*=\s*([\d.]+);',
    }
    
    branch_pattern = r'ramos\s*=\s*\[(.*?)\];'
    bus_demand_pattern = r'barras\s*=\s*\[(.*?)\];'
    
    branches = []
    bus_demand = []
    
    with open(file_path, "r",encoding='latin1') as file:
        text = file.read()
    

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if key == 'tol':
                base, exponent = match.group(1).split('^')
                datos_globales[key] = float(base) * 10 ** int(exponent)

            else:
                datos_globales[key] = float(match.group(1))
    
    datos_globales[key] = calcZbase()
    
    # Datos de ramas      
    match = re.search(branch_pattern, text, re.DOTALL)
    if match:
        branch_data = match.group(1)

        
        branch_lines = branch_data.split('\n')
        branch_lines = [line.strip() for line in branch_lines if not line.strip().startswith('%')]

       
        for line in branch_lines:
            valores = line.split()
            if len(valores) == 4:
                branch = [float(valor) for valor in valores]
                branches.append(branch)
                
    # Datos de la demanda de potencia activa y reactiva en las barras
    match = re.search(bus_demand_pattern, text, re.DOTALL)
    if match:
        bus_demand_data = match.group(1)

       
        bus_demand_lines = bus_demand_data.split('\n')
        bus_demand_lines = [line.strip() for line in bus_demand_lines if not line.strip().startswith('%')]

       
        for line in bus_demand_lines:
            valores = line.split()
            if len(valores) >= 4:
                bus = [int(valores[0]), float(valores[1]), float(valores[2]), float(valores[3])]
                bus_demand.append(bus)
    
    # Editar los valores
    numNodos(datos_globales.get("nref"))
    potencias(bus_demand)
    impedencia(branches)

    
def lecturaDocumento14():
    
    #Valores globales    
    patterns = {
        'nref': r'nref\s*=\s*([\d.]+);',
        'vref': r'vref\s*=\s*([\d.]+);',
        'vbase': r'vbase\s*=\s*([\d.]+);',
        'sbase': r'sbase\s*=\s*([\d.]+);',
        'tol': r'tol\s*=\s*([\d.^-]+);', 
        'vmin': r'vmin\s*=\s*([\d.]+);',
        'vmax': r'vmax\s*=\s*([\d.]+);',
        'zbase': r'zbase\s*=\s*([\d.]+);',
    }
    
    branch_pattern = r'ramos\s*=\s*\[(.*?)\];'
    bus_demand_pattern = r'barras\s*=\s*\[(.*?)\];'
    
    branches = []
    bus_demand = []
    
    
    #input('Ingresar el path del archivo \n')
    
    with open(file_path, "r",encoding='latin1') as file:
        text = file.read()
    

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if key == 'tol':
                base, exponent = match.group(1).split('^')
                datos_globales[key] = float(base) * 10 ** int(exponent)
            else:
                datos_globales[key] = float(match.group(1))
    
    
    
    # Datos de ramas      
    match = re.search(branch_pattern, text, re.DOTALL)
    if match:
        branch_data = match.group(1)

        
        branch_lines = branch_data.split('\n')
        branch_lines = [line.strip() for line in branch_lines if not line.strip().startswith('%')]

       
        for line in branch_lines:
            valores = line.split()
            if len(valores) == 4:
                branch = [float(valor) for valor in valores]
                branches.append(branch)
                
    # Datos de la demanda de potencia activa y reactiva en las barras
    match = re.search(bus_demand_pattern, text, re.DOTALL)
    if match:
        bus_demand_data = match.group(1)

       
        bus_demand_lines = bus_demand_data.split('\n')
        bus_demand_lines = [line.strip() for line in bus_demand_lines if not line.strip().startswith('%')]

       
        for line in bus_demand_lines:
            valores = line.split()
            if len(valores) >= 4:
                bus = [int(valores[0]), float(valores[1]), float(valores[2]), float(valores[3])]
                bus_demand.append(bus)
    
    # Editar los valores
    numNodos(datos_globales.get("nref"))
    potencias(bus_demand)
    impedencia14(branches)
      
        
def impedencia14(branches): 
    for branch in branches:
        from_node = int(branch[0])
        to_node = int(branch[1])
        
        
        B.append( (from_node, to_node))
        B.append( ( to_node, from_node))
        r[( from_node, to_node)] = branch[2]*0.01
        r[( to_node, from_node)] = branch[2]*0.01
        x[( from_node, to_node)] = branch[3]*0.01
        x[( to_node, from_node)] = branch[3]*0.01


    
    

def numNodos(n):
    for i in range (1,int(n)+1):
        nodos.append(i)
    


def potencias(demand):
    for bus in demand:
        pd[(bus[0])] = bus[1]
        qd[( bus[0])] = bus[2]
      
        
def impedencia(branches): 
    for branch in branches:
        from_node = int(branch[0])
        to_node = int(branch[1])
        
        
        B.append( (from_node, to_node))
        B.append( ( to_node, from_node))
        r[( from_node, to_node)] = branch[2]/datos_globales.get('zbase')
        r[( to_node, from_node)] = branch[2]/datos_globales.get('zbase')
        x[( from_node, to_node)] = branch[3]/datos_globales.get('zbase')
        x[( to_node, from_node)] = branch[3]/datos_globales.get('zbase')




def printDatos():
    print("Nodos")
    print(nodos)
    
    print("Datos Globales")
    for key, value in datos_globales.items():
        print(f"{key}: {value}")
    
    print("Demanda de potencia Activa(pd)")
    for key, value in pd.items():
        print(key, value)


    print("Demanda de Potencia Reactiva(qd)")
    for key, value in qd.items():
        print(key, value)
    
    print("Resistencia(r) de los arcos")
    for key, value in r.items():
        print(key, value)
    
    print("Reactancia(x) de los arcos")
    for key, value in x.items():
        print(key, value)
        
    print("Arcos")
    print(B)



def printGrafo():
    # Crear un grafo dirigido
    G = nx.Graph()
    
    # Añadir nodos
    for node in nodos:
        G.add_node(node)
        
    for i, j in B:
        G.add_edge(i,j)
        
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', width=2, font_size=15)
    plt.show()

if file_path.find("datos14")  >-1:
    lecturaDocumento14()
else:
    lecturaDocumento()
    print(datos_globales.get("zbase"))

printDatos()
printGrafo()
    
# Create optimization model
m = gp.Model("RSD")
#Constantes

#tolerancia
tol=datos_globales.get("tol")

# b=lo que genera/consume cada nodo
b_v= 0.1


# tension minimima kV
vmin=float(datos_globales.get("vmin"))*float(datos_globales.get("vbase"))



# tension maxima kV
vmax= float(datos_globales.get("vmax"))*float(datos_globales.get("vbase"))

delV=vmax-vmin

# Potencia base kW
sbase= datos_globales.get("sbase")

print(vmin, vmax)
# Variables
# Estado de la llave del arco i y j
y =  m.addVars(nodos, nodos,  vtype=GRB.BINARY, name="y")

# Flujo de potencia activa entre los nodos i y j 
P =  m.addVars(nodos,nodos, vtype=GRB.CONTINUOUS,lb= 0, ub=1,  name="P")

# Flujo de potencia reactiva entre los nodos i y j 
Q = m.addVars(nodos,nodos,  vtype=GRB.CONTINUOUS,lb= 0, ub=1,  name="Q")

# Flujo de Corriente entre los nodos i y j
I = m.addVars(nodos,nodos,  vtype=GRB.CONTINUOUS, name="I")

# Valor al cuadrado del flujo de Corriente entre los nodos i y j
Isqr = m.addVars(nodos,nodos,  vtype=GRB.CONTINUOUS, lb= 0, ub=1, name="Isqr")

# Voltaje del nodo i
V = m.addVars(nodos,  vtype=GRB.CONTINUOUS, lb=vmin, ub=vmax, name="V")

# Valor al cuadrado del voltaje del nodo i
Vsqr = m.addVars(nodos, vtype=GRB.CONTINUOUS, lb=vmin**2, ub=vmax**2, name="Vsqr")

# Delta del V
deltaV= m.addVars(nodos, nodos, vtype=GRB.CONTINUOUS, lb=-delV, ub=delV, name="deltaV")


FO = LinExpr()
for (i, j) in B:
    FO += I[i,j]**2 * r[i, j]

m.setObjective(FO, GRB.MINIMIZE)
    
for i in nodos:    
    expr1 =0
    expr2 =0
    for k in nodos:
        if ((k,i) in B):
            expr1+=(P[k, i])
    
    for j in nodos:
        if ((i,j) in B):
            expr2+= P[i, j] + r[i, j] * I[i, j]**2
    
    
    r1 = expr1 - expr2 
    
    if(i!=int(datos_globales.get("nref"))):
        m.addConstr(r1 == pd[i]/sbase, name=f"demanda_potencia_activa _{i}")
    else:
        m.addConstr(r1 <= pd[i]/sbase, name=f"demanda_potencia_activa _{i}")

for i in nodos:
    
    expr1 =0
    expr2 =0
    for k in nodos:
        if ((k,i) in B):
            expr1+=(Q[k, i])
    
    for j in nodos:
        if ((i,j) in B):
            expr2+= Q[i, j] + x[i, j] * I[i, j]**2
    

    r1 = expr1 - expr2 
    

    if(i!=int(datos_globales.get("nref"))):
        m.addConstr(r1 == qd[i]/sbase, name=f"demanda_potencia_reactiva _{i}")
    else:
        m.addConstr(r1 <= qd[i]/sbase, name=f"demanda_potencia_reactiva _{i}")


for i,j in B: 
    expr1= 2*(P[(i, j)] * r[i,j] +Q[(i, j)] *x[i,j])
    expr2= (x[i,j]**2 + r[i,j]**2) *I[i,j]**2
    r3= V[(j)]**2 + expr1 - expr2 + deltaV[i,j]
    
    m.addConstr(Vsqr[i]==r3,name=f"limite de magnitud de tensión")
    
for (i,j) in B: 
    expr1= -b_v *(1 - y[i, j])
    m.addConstr(expr1 <= deltaV[(i, j)] ,name=f"regular la magnitud minima de tensión entre los nodos del sistema con respecto a las llaves")
    expr2 = b_v * (1 - y[i, j])
    m.addConstr(deltaV[(i, j)]<= expr2,name=f"regular la magnitud maxima de tensión entre los nodos del sistema con respecto a las llaves")


for (i,j) in B:
    v1=V[j]**2
    v2=I[i, j]**2
    m.addConstr(Vsqr[j] * Isqr[i,j] == P[i, j] * P[i, j] + Q[i, j] * Q[i, j],
                    name=f"restriccion_cuadratica_{i}_{j}")

for i in nodos:
    m.addConstr(vmin**2<= V[i]**2, name =f" Conservación_minima_de_potencia_{i}")
    m.addConstr(Vsqr[i]<=vmax**2, name =f" Conservación_maxima_de_potencia_{i}")


for (i,j) in B:
    m.addConstr(0<=I[i,j]**2, name=f"magnitud_minima_Corriente_{i}_{j}")
    m.addConstr(I[i,j]**2<= (vmax/r[i,j])**2*y[i,j], name=f"magnitud_maxima_Corriente_{i}_{j}")


for (i,j) in B:
    m.addConstr((y[i,j]+y[j,i])<=1, name=f"solo_una_una_direccion_de_flujo_entre_los_nodos_{i}_{j}")

valor=0
print(len(nodos))

for (i,j) in B:
    valor+=y[i,j]
    
m.addConstr(valor ==(len(nodos)-1), name=f"Restriccione_de_radialidad")


for i in nodos: 
    suma=0
    if (i!=int(datos_globales.get("nref"))):
        for j in nodos: 
           if (i,j) in B: 
                suma+=y[j,i]
        m.addConstr(suma >=1, name=f"conexion{i}")
    else:
        for j in nodos: 
           if (i,j) in B: 
                suma+=y[i,j]
        m.addConstr(suma >=1, name=f"conexion{i}")

m.update()

m.setParam("NonConvex",2)

m.optimize()

def getFile():
    valor=file_path.split("\\")
    last=valor[len(valor)-1]
    splitted= last.split('.')
    print(splitted[0])
    return splitted[0]


value=getFile()
if m.Status == GRB.INFEASIBLE:
    m.computeIIS()
    m.write('{value}.ilp')
else:
    m.write('{value}.lp')
    m.write('{value}.sol')

def printGrafo():
    # Crear un grafo dirigido
    G = nx.DiGraph()
    
    # Añadir nodos
    for node in nodos:
        G.add_node(node)
    
    for i, j in B:
        if y[i,j].x>0:
            G.add_edge(i,j)
        
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', width=2, font_size=15)
    plt.show()

printGrafo()
print(m.objval)
