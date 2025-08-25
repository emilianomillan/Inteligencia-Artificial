class Node():
    def __init__(self, state, parent, action):
        self.state = state 
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)
    
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node

# ----------------------------
calendario = [
    ['E', 1, 0, 1, 1, 1, 0],    
    [1, 1, 1, 1, 1, 1, 1],  
    [0, 1, 1, 1, 0, 1, 1],    
    [1, 0, 1, 1, 1, 0, 1]      
]

start = (0, 0)
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def vecinos(state):
    row, col = state
    candidatos = [
        ("derecha", (row, col + 1)),    
        ("abajo", (row + 1, col)),   
        ("izquierda", (row, col - 1)),  
        ("arriba", (row - 1, col)),    
    ]
    result = []
    for action, (r, c) in candidatos:
        if 0 <= r < len(calendario) and 0 <= c < len(calendario[0]):
            result.append((action, (r, c)))
    return result

def etiqueta_dia(pos):
    fila, col = pos
    dia = dias_semana[col]
    semana = fila + 1
    return f"{dia}, Semana {semana}"

def es_transitable(r, c):
    valor = calendario[r][c]
    return True

def buscar_bfs():
    node_start = Node(state=start, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(node_start)
    explored = set()

    while not frontier.empty():
        node = frontier.remove()

        if node.state in explored:
            continue

        r, c = node.state

        if calendario[r][c] == 0 and node.state != start:
            return etiqueta_dia(node.state)

        explored.add(node.state)

        for action, neighbor in vecinos(node.state):
            nr, nc = neighbor
            if neighbor not in explored and not frontier.contains_state(neighbor):
                if es_transitable(nr, nc):
                    child = Node(state=neighbor, parent=node, action=action)
                    frontier.add(child)

    return "No hay días libres disponibles"

def buscar_dfs_diaEspecifico(dia_inicio, dia_columna):
    node_start = Node(state=dia_inicio, parent=None, action=None)
    frontier = StackFrontier()
    frontier.add(node_start)
    explored = set()
    
    while not frontier.empty():
        node = frontier.remove()
        
        if node.state in explored:
            continue
            
        r, c = node.state
        
        if calendario[r][c] == 0 and c == dia_columna:
            return etiqueta_dia(node.state)
        
        explored.add(node.state)
        
        for semana_idx in range(len(calendario)):
            neighbor = (semana_idx, dia_columna)
            if neighbor not in explored and not frontier.contains_state(neighbor):
                if neighbor != node.state: 
                    child = Node(state=neighbor, parent=node, action=f"{dias_semana[dia_columna]}_semana_{semana_idx+1}")
                    frontier.add(child)
    
    return f"No hay {dias_semana[dia_columna].lower()}s libres disponibles"

# ----------------------------
#Ejemplos (aleatorios, no elegí nada específico)
print("Calendario:")
for i, semana in enumerate(calendario):
    dias_formateados = []
    for j, valor in enumerate(semana):
        if valor == 'E':
            dias_formateados.append('E')
        elif valor == 0:
            dias_formateados.append('L')  
        else:
            dias_formateados.append('O')  
    print(f"Semana {i+1}: {dias_formateados}")

#Dia mas cercano (desde lunes, semana 1 = E)
dia_mas_cercano = buscar_bfs()
print(f"\nDía más cercano libre desde inicio: {dia_mas_cercano}")

#Busca en viernes (desde semana 1)
inicio_dfs = (0, 4)
dia_a_buscar = 4  

espacio_libre_dfs = buscar_dfs_diaEspecifico(inicio_dfs, dia_a_buscar)
print(f"\nPrimer espacio libre del -{dias_semana[dia_a_buscar]}-: {espacio_libre_dfs}")

#Buscar en martes (desde semana 3)
dia_martes = 1  
inicio_martes = (2, 1)  

resultado_martes = buscar_dfs_diaEspecifico(inicio_martes, dia_martes)
print(f"Primer espacio libre del -{dias_semana[dia_martes]}-: {resultado_martes}")

#Todos los días libres disponibles
print(f"\nDías libres en el calendario:")
for i in range(len(calendario)):
    for j in range(len(calendario[0])):
        if calendario[i][j] == 0:
            print(f"  - Posición ({i},{j}): {etiqueta_dia((i,j))}")
