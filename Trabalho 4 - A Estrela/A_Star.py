# Definindo o estado inicial
initial_state = [
    [2, 8, 3],
    [1, 6, 4],
    [7, 5, 0]
]

# Definindo o estado objetivo
goal_state = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
]

# Calcula o custo h
def heuristic(state, goal_state):
    distance = 0
    # Loop pelos elementos do estado atual
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            # Verifica se o valor está na posição correta no estado objetivo
            if state[i][j] != goal_state[i][j]:
                distance += 1
    return distance

# Calcula o custo f
def f(state, goal_state, g_score):
    h_score = heuristic(state, goal_state)
    f_score = g_score + h_score
    return f_score

# Obtém os sucessores do estado atual
def move_zero(state, move,zero_x,zero_y):
    new_state = [row[:] for row in state]
    if move == "up":
        new_state[zero_x][zero_y] = new_state[zero_x - 1][zero_y]
        new_state[zero_x - 1][zero_y] = 0
    elif move == "down":
        new_state[zero_x][zero_y] = new_state[zero_x + 1][zero_y]
        new_state[zero_x + 1][zero_y] = 0
    elif move == "left":
        new_state[zero_x][zero_y] = new_state[zero_x][zero_y - 1]
        new_state[zero_x][zero_y - 1] = 0
    elif move == "right":
        new_state[zero_x][zero_y] = new_state[zero_x][zero_y + 1]
        new_state[zero_x][zero_y + 1] = 0
    return new_state

# Obtém os sucessores do estado atual
def get_successors(state):
    zero_x = 0
    zero_y = 0
    for i in range(3):
        for j in range(3):
            if(state[i][j] == 0):
                zero_x = i
                zero_y = j

    moves = possible_moves(state, zero_x, zero_y)
    successors = []
    for move in moves:
        new_state = move_zero(state, move, zero_x, zero_y)
        successors.append(new_state)
    return successors

def possible_moves(state, zero_x, zero_y):
    moves = []
    # Verifica se o espaço vazio está na primeira linha
    if zero_x != 0:
        moves.append("up")
    # Verifica se o espaço vazio está na última linha
    if zero_x != 2:
        moves.append("down")
    # Verifica se o espaço vazio está na primeira coluna
    if zero_y != 0:
        moves.append("left")
    # Verifica se o espaço vazio está na última coluna
    if zero_y != 2:
        moves.append("right")
    return moves

# Seleciona o melhor estado da fila de prioridade
def select_best(queue):
    best = queue[0]
    for i in range(len(queue)):
        if queue[i][1] < best[1]:
            best = queue[i]
    return best

def main():
    # Definindo o estado atual
    current_state = initial_state

    # Definindo o custo g
    g_score = 0

    # Definindo o custo f
    f_score = f(current_state, goal_state, g_score)

    # Definindo a fila de prioridade
    queue = []

    # Definindo o conjunto de estados visitados
    visited = []

    # Definindo o conjunto de estados que não foram visitados
    not_visited = []

    print("Estado inicial: ", current_state)
    print("Custo g: ", g_score)
    print("Heurística: ", heuristic(current_state, goal_state))
    
    while current_state != goal_state:
        # Adiciona o estado atual na lista de estados visitados
        visited.append(current_state)

        # Obtém os sucessores do estado atual
        successors = get_successors(current_state)

        # Loop pelos sucessores
        for successor in successors:
            # Verifica se o sucessor não foi visitado
            if successor not in visited:
                # Adiciona o sucessor na lista de estados que não foram visitados
                not_visited.append(successor)

                # Calcula o custo g do sucessor
                g_score = g_score + 1

                # Calcula o custo f do sucessor
                f_score = f(successor, goal_state, g_score)

                # Adiciona o sucessor na fila de prioridade
                queue.append((successor, f_score))

        # Seleciona o melhor estado da fila de prioridade
        best = select_best(queue)

        # Atualiza o estado atual
        current_state = best[0]

        # Atualiza o custo g
        g_score = best[1] - heuristic(current_state, goal_state)
        f_score = f(current_state, goal_state, g_score) 

        # Remove o melhor estado da fila de prioridade
        queue.remove(best)

        print("Estado atual: ", current_state)
        print("Custo g: ", g_score)
        print("Heurística: ", heuristic(current_state, goal_state))

    # Imprime o estado atual
    print("Estado final: ",current_state)

if __name__ == "__main__":
    main()