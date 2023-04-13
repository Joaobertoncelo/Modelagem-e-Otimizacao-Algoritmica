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

def manhattan_distance(state, goal_state):
    distance = 0
    # Loop pelos elementos do estado atual
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            # Verifica se o valor não é zero (representando o espaço vazio)
            if value != 0:
                # Verifica se o valor está na posição correta no estado objetivo
                if state[i][j] != goal_state[i][j]:
                    distance += 1
                    
    # Retorna a distância de Manhattan
    return distance

def create_priority_queue():
    return []

def add_to_priority_queue(priority_queue, state, priority):
    """
    Adiciona um estado na fila de prioridade.
    """
    # Adiciona o estado na fila de prioridade
    priority_queue.append((state, priority))

def get_from_priority_queue(priority_queue):
    """
    Obtém um estado da fila de prioridade.
    """
    # Obtém o estado com a maior prioridade
    state, priority = max(priority_queue, key=lambda x: x[1])
    # Remove o estado da fila de prioridade
    priority_queue.remove((state, priority))
    # Retorna o estado
    return state

def is_priority_queue_empty(priority_queue):
    """
    Verifica se a fila de prioridade está vazia.
    """
    # Retorna se a fila de prioridade está vazia
    return len(priority_queue) == 0

def update_priority_queue(queue, state, priority):
    """
    Atualiza a fila de prioridade com o estado e a prioridade fornecidos.
    """
    # Loop pela fila de prioridade
    for i in range(len(queue)):
        # Obtém o estado e a prioridade
        current_priority, current_state = queue[i]
        # Verifica se o estado atual é o estado fornecido
        if current_state == state:
            # Verifica se a prioridade atual é maior que a prioridade fornecida
            if current_priority > priority:
                # Atualiza a prioridade
                queue[i] = (priority, state)
                # Reordena a fila de prioridade
                heapq.heapify(queue)
            # Retorna verdadeiro
            return True
    # Retorna falso
    return False

def get_key(state):
    """
    Obtém a chave do estado fornecido.
    """
    # Cria uma lista vazia
    key = []
    # Loop pelos elementos do estado fornecido
    for i in range(3):
        for j in range(3):
            # Adiciona o elemento na lista
            key.append(state[i][j])
    # Retorna a chave
    return tuple(key)

def get_possible_moves(state):
    """
    Obtém os movimentos possíveis do estado fornecido.
    """
    # Cria uma lista vazia
    possible_moves = []
    # Loop pelos elementos do estado fornecido
    for i in range(3):
        for j in range(3):
            # Verifica se o elemento é zero (representando o espaço vazio)
            if state[i][j] == 0:
                # Verifica se o elemento não está na primeira linha
                if i > 0:
                    # Cria uma cópia do estado
                    new_state = [row[:] for row in state]
                    # Troca o elemento com o elemento acima
                    new_state[i][j], new_state[i - 1][j] = new_state[i - 1][j], new_state[i][j]
                    # Adiciona o novo estado na lista de movimentos possíveis
                    possible_moves.append(new_state)
                # Verifica se o elemento não está na última linha
                if i < 2:
                    # Cria uma cópia do estado
                    new_state = [row[:] for row in state]
                    # Troca o elemento com o elemento abaixo
                    new_state[i][j], new_state[i + 1][j] = new_state[i + 1][j], new_state[i][j]
                    # Adiciona o novo estado na lista de movimentos possíveis
                    possible_moves.append(new_state)
                # Verifica se o elemento não está na primeira coluna
                if j > 0:
                    # Cria uma cópia do estado
                    new_state = [row[:] for row in state]
                    # Troca o elemento com o elemento à esquerda
                    new_state[i][j], new_state[i][j - 1] = new_state[i][j - 1], new_state[i][j]
                    # Adiciona o novo estado na lista de movimentos possíveis
                    possible_moves.append(new_state)
                # Verifica se o elemento não está na última coluna
                if j < 2:
                    # Cria uma cópia do estado
                    new_state = [row[:] for row in state]
                    # Troca o elemento com o elemento à direita
                    new_state[i][j], new_state[i][j + 1] = new_state[i][j + 1], new_state[i][j]
                    # Adiciona o novo estado na lista de movimentos possíveis
                    possible_moves.append(new_state)
    # Retorna os movimentos possíveis
    return possible_moves

def reconstruct_path(previous_states, current_state):
    """
    Reconstroi o caminho percorrido a partir do estado atual.
    """
    # Cria uma lista vazia
    path = []
    # Loop enquanto o estado atual não for nulo
    while current_state is not None:
        # Adiciona o estado atual na lista
        path.append(current_state)
        # Obtém a chave do estado atual
        key = get_key(current_state)
        # Obtém o estado anterior
        current_state = previous_states[key]
    # Retorna o caminho percorrido
    return path[::-1]

def print_state(state):
    """
    Imprime o estado fornecido.
    """
    # Loop pelas linhas do estado
    for i in range(3):
        # Loop pelas colunas do estado
        for j in range(3):
            # Imprime o elemento
            print(state[i][j], end=' ')
        # Imprime uma quebra de linha
        print()

def print_path(path):
    """
    Imprime o caminho percorrido.
    """
    # Loop pelo caminho percorrido
    for i in range(len(path)):
        # Imprime o estado atual
        print_state(path[i])
        # Verifica se o estado atual não é o último
        if i < len(path) - 1:
            # Imprime uma linha
            print('---------------------')

def print_solution(path):
    """
    Imprime a solução.
    """
    # Imprime o caminho percorrido
    print_path(path)
    # Imprime o número de movimentos
    print('Número de movimentos:', len(path) - 1)

def get_heuristic(state, goal_state):
    """
    Obtém a heurística do estado fornecido.
    """
    # Cria uma lista vazia
    heuristic = []
    # Loop pelos elementos do estado fornecido
    for i in range(3):
        for j in range(3):
            # Adiciona o elemento na lista
            heuristic.append(state[i][j])
    # Cria uma lista vazia
    goal = []
    # Loop pelos elementos do estado objetivo
    for i in range(3):
        for j in range(3):
            # Adiciona o elemento na lista
            goal.append(goal_state[i][j])
    # Cria uma lista vazia
    heuristic = list(filter(lambda x: x != 0, heuristic))
    # Cria uma lista vazia
    goal = list(filter(lambda x: x != 0, goal))
    # Cria uma lista vazia
    h = []
    # Loop pelos elementos da heurística
    for i in range(len(heuristic)):
        # Adiciona o elemento na lista
        h.append(abs(heuristic[i] - goal[i]))
    # Retorna a heurística
    return sum(h)

def get_successors(state, goal_state):
    """
    Obtém os sucessores do estado fornecido.
    """
    # Cria uma lista vazia
    successors = []
    # Loop pelos movimentos possíveis
    for move in get_possible_moves(state):
        # Cria uma tupla com o estado e a heurística
        successors.append((move, get_heuristic(move, goal_state)))
    # Retorna os sucessores
    return successors

def calculate_cost(state, previous_states, g_score):
    """
    Calcula o custo do estado fornecido.
    """
    # Obtém a chave do estado fornecido
    key = get_key(state)
    # Verifica se o estado já foi visitado
    if key in previous_states:
        # Retorna o custo do estado
        return g_score[key]
    # Retorna 0
    return 0

def a_star(initial_state, goal_state):
    """
    Algoritmo A*.
    """
    # Cria a fila de prioridade
    priority_queue = create_priority_queue()
    # Cria o dicionário de estados visitados
    visited_states = {}
    # Cria o dicionário de estados anteriores
    previous_states = {}
    # Cria o dicionário de custos
    g_score = {}
    # Adiciona o estado inicial na fila de prioridade
    add_to_priority_queue(priority_queue, initial_state, 0)
    # Adiciona o estado inicial no dicionário de estados visitados
    visited_states[get_key(initial_state)] = initial_state
    # Adiciona o estado inicial no dicionário de custos
    g_score[get_key(initial_state)] = 0
    # Loop enquanto a fila de prioridade não estiver vazia
    while not is_priority_queue_empty(priority_queue):
        # Obtém o estado com menor custo
        current_state = get_from_priority_queue(priority_queue)
        # Verifica se o estado atual é o estado objetivo
        if current_state == goal_state:
            # Retorna o caminho percorrido
            return reconstruct_path(previous_states, current_state)
        # Obtém a chave do estado atual
        key = get_key(current_state)
        # Remove o estado atual do dicionário de estados visitados
        del visited_states[key]
        # Obtém os movimentos possíveis do estado atual
        possible_moves = get_possible_moves(current_state)
        # Loop pelos movimentos possíveis
        for move in possible_moves:
            # Obtém a chave do movimento
            move_key = get_key(move)
            # Verifica se o movimento já foi visitado
            if move_key in visited_states:
                # Pula para o próximo movimento
                continue
            # Obtém o custo do movimento
            g = g_score[key] + 1
            # Verifica se o movimento já está na fila de prioridade
            if move_key in g_score:
                # Verifica se o custo do movimento é maior que o custo atual
                if g >= g_score[move_key]:
                    # Pula para o próximo movimento
                    continue
            # Adiciona o movimento no dicionário de estados anteriores
            previous_states[move_key] = current_state
            # Adiciona o movimento no dicionário de custos
            g_score[move_key] = g
            # Adiciona o movimento na fila de prioridade
            add_to_priority_queue(priority_queue, move, g + get_heuristic(move, goal_state))
            # Adiciona o movimento no dicionário de estados visitados
            visited_states[move_key] = move
    # Retorna nulo
    return None

def main():
    print("Algoritmo A*")
    # Cria a fila de prioridade
    priority_queue = create_priority_queue()
    # Cria o dicionário de estados visitados
    visited_states = {}
    # Cria o dicionário de estados anteriores
    previous_states = {}
    # Cria o dicionário de custos
    g_score = {}
    # Adiciona o estado inicial na fila de prioridade
    add_to_priority_queue(priority_queue, initial_state, 0)
    # Adiciona o estado inicial no dicionário de estados visitados
    visited_states[get_key(initial_state)] = initial_state
    # Adiciona o estado inicial no dicionário de custos
    g_score[get_key(initial_state)] = 0
    # Loop enquanto a fila de prioridade não estiver vazia
    while not is_priority_queue_empty(priority_queue):
        print("entrou no while")
        # Obtém o estado com menor custo
        current_state = get_from_priority_queue(priority_queue)
        # Verifica se o estado atual é o estado objetivo
        if current_state == goal_state:
            # Imprime o caminho percorrido
            print_path(previous_states, current_state)
            # Imprime o custo
            print("Custo: ", g_score[get_key(current_state)])
            # Imprime o número de nós visitados
            print("Nós visitados: ", len(visited_states))
            # Imprime o número de nós na fila de prioridade
            print("Nós na fila de prioridade: ", len(priority_queue))
            # Imprime o número de nós expandidos
            print("Nós expandidos: ", len(visited_states) + len(priority_queue))
            # Retorna o estado atual
            return current_state
        # Obtém os estados sucessores
        successors = get_successors(current_state, goal_state)
        # Loop pelos estados sucessores
        for successor in successors:
            # Obtém a chave do estado sucessor
            key = get_key(successor)
            # Verifica se o estado sucessor já foi visitado
            if key not in visited_states:
                # Calcula o custo do estado sucessor
                cost = calculate_cost(successor, goal_state, g_score[get_key(current_state)])
                # Adiciona o estado sucessor na fila de prioridade
                add_to_priority_queue(priority_queue, successor, cost)
                # Adiciona o estado sucessor no dicionário de estados visitados
                visited_states[key] = successor
                # Adiciona o estado sucessor no dicionário de estados anteriores
                previous_states[key] = current_state
                # Adiciona o estado sucessor no dicionário de custos
                g_score[key] = cost
    print_path(previous_states, current_state)
    print_solution(priority_queue, visited_states)
    print_state(current_state)
    # Retorna nulo
    return None
main()