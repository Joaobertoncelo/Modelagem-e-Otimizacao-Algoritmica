import heapq
import matplotlib.pyplot as plt

# Definindo o estado inicial
initial_state = [
    [1, 2, 3],
    [4, 0, 5],
    [6, 7, 8]
]

# Definindo o estado objetivo
goal_state = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]


# Esta função calcula a distância de Manhattan entre o estado atual e o estado objetivo de um quebra-cabeça deslizante de 8 peças.
def manhattan_distance(state, goal_state):
    distance = 0
    # Loop pelos elementos do estado atual
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            # Verifica se o valor não é zero (representando o espaço vazio)
            if value != 0:
                # Verifica se o valor está na posição correta no estado objetivo
                if state[i][j] == goal_state[i][j]:
                    distance += 1
                    
    # Retorna a distância de Manhattan
    return distance


def find_position(state, value):
    for i in range(3):
        for j in range(3):
            if state[i][j] == value:
                return (i, j)

def calculate_cost(state, goal_state, g_score):
    h_score = manhattan_distance(state, goal_state)
    f_score = g_score + h_score
    return f_score

def create_priority_queue():
    return []

def add_to_priority_queue(queue, state, priority):
    heapq.heappush(queue, (priority, state))

def get_from_priority_queue(queue):
    return heapq.heappop(queue)[1]

def is_priority_queue_empty(queue):
    return len(queue) == 0

def update_priority_queue(queue, state, priority):
    """
    Atualiza a fila de prioridade com o estado e a prioridade fornecidos.
    Se o estado já está na fila de prioridade com uma prioridade menor ou igual,
    não faz nada. Caso contrário, atualiza a prioridade do estado na fila de prioridade.

    Args:
        queue (list): uma fila de prioridade, representada como uma lista de tuplas (prioridade, estado)
        state (tuple): o estado a ser adicionado ou atualizado na fila de prioridade
        priority (int): a nova prioridade do estado

    Returns:
        None
    """
    for index, (p, s) in enumerate(queue):
        # verifica se o estado já está na fila de prioridade
        if s == state:
            # se o estado já está na fila de prioridade com uma prioridade menor ou igual, não faz nada
            if p <= priority:
                return
            # se o estado já está na fila de prioridade com uma prioridade maior, remove-o da fila
            del queue[index]
            # reconstrói a fila de prioridade
            heapq.heapify(queue)
            break
    # adiciona o estado com a nova prioridade na fila de prioridade
    heapq.heappush(queue, (priority, state))


def get_successors(current_state):
    successors = []  # inicializa a lista de sucessores
    row, col = find_position(current_state, 0)  # encontra a posição do espaço vazio (zero)

    # move para cima
    if row > 0:
        new_state = [row[:] for row in current_state]  # cria um novo estado copiando o atual
        new_state[row][col] = new_state[row - 1][col]  # move o número acima do espaço vazio para o espaço vazio
        new_state[row - 1][col] = 0  # atualiza o espaço vazio com o número que foi movido
        successors.append(new_state)  # adiciona o novo estado à lista de sucessores

    # move para baixo
    if row < 2:
        new_state = [row[:] for row in current_state]  # cria um novo estado copiando o atual
        new_state[row][col] = new_state[row + 1][col]  # move o número abaixo do espaço vazio para o espaço vazio
        new_state[row + 1][col] = 0  # atualiza o espaço vazio com o número que foi movido
        successors.append(new_state)  # adiciona o novo estado à lista de sucessores

    # move para esquerda
    if col > 0:
        new_state = [row[:] for row in current_state]  # cria um novo estado copiando o atual
        new_state[row][col] = new_state[row][col - 1]  # move o número à esquerda do espaço vazio para o espaço vazio
        new_state[row][col - 1] = 0  # atualiza o espaço vazio com o número que foi movido
        successors.append(new_state)  # adiciona o novo estado à lista de sucessores

    # move para direita
    if col < 2:
        new_state = [row[:] for row in current_state]  # cria um novo estado copiando o atual
        new_state[row][col] = new_state[row][col + 1]  # move o número à direita do espaço vazio para o espaço vazio
        new_state[row][col + 1] = 0  # atualiza o espaço vazio com o número que foi movido
        successors.append(new_state)  # adiciona o novo estado à lista de sucessores

    return successors  # retorna a lista de sucessores


def get_path(goal_state, g_score):
    # Inicializa o estado atual como o estado objetivo e cria uma lista de caminho com o estado atual
    current_state = goal_state  
    path = [current_state]
    
    # Enquanto o estado atual estiver presente na tabela de pontuação
    while current_state in g_score:
        # Define o próximo estado atual como o estado anterior armazenado na tabela de pontuação
        current_state = g_score[current_state][1]
        # Adiciona o estado atual à lista de caminho
        path.append(current_state)

    # Inverte a lista de caminho e retorna
    return list(reversed(path))

def astar(initial_state, goal_state):
    # Conjunto de estados visitados
    visited = set()
    # Cria uma fila de prioridade vazia
    queue = create_priority_queue()
    # Dicionário que armazena os custos até chegar em cada estado
    g_score = {initial_state: 0}
    # Adiciona o estado inicial na fila de prioridade com o custo estimado
    add_to_priority_queue(queue, initial_state, calculate_cost(initial_state, goal_state, 0))
    
    # Enquanto a fila de prioridade não estiver vazia
    while not is_priority_queue_empty(queue):
        # Obtém o estado com menor custo estimado da fila de prioridade
        current_state = get_from_priority_queue(queue)
        
        # Se o estado atual é o estado objetivo, retorna o caminho até ele
        if current_state == goal_state:
            return get_path(current_state, g_score)
        
        # Marca o estado atual como visitado
        visited.add(current_state)
        
        # Para cada sucessor do estado atual
        for successor in get_successors(current_state):
            # Se o sucessor já foi visitado, continua para o próximo
            if successor in visited:
                continue
            
            # Calcula o custo até chegar no sucessor
            tentative_g_score = g_score[current_state] + 1
            
            # Se o sucessor ainda não foi visitado ou o custo até chegar nele é menor do que o custo anteriormente calculado
            if successor not in g_score or tentative_g_score < g_score[successor]:
                # Atualiza o custo até chegar no sucessor
                g_score[successor] = tentative_g_score
                # Calcula o custo estimado total para chegar no objetivo passando pelo sucessor
                f_score = calculate_cost(successor, goal_state, tentative_g_score)
                # Adiciona o sucessor na fila de prioridade com o novo custo estimado
                update_priority_queue(queue, successor, f_score)
    
    # Se não encontrar um caminho, retorna None
    return None

if __name__ == '__main__':

    solution = astar(initial_state, goal_state)
    if solution:
        print("Caminho da solução:")
        for state in solution:
            plt.imshow(state)
            plt.show()
            print(state)
    else:
        print("Não há solução possível para este problema.")
