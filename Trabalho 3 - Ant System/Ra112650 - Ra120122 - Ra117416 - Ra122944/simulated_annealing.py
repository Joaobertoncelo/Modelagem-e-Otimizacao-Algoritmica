import random
import math

def cut_cost(cut_list, plate_width, plate_height):
    # Calcula o custo da solução (lista de cortes)
    # Custo = área da placa não utilizada
    used_area = sum([w*h for w,h in cut_list])
    unused_area = plate_width * plate_height - used_area
    return unused_area

def neighbor(cut_list, plate_width, plate_height):
    # Gera uma solução vizinha aleatória
    # Removendo um corte aleatório e adicionando outro corte aleatório
    new_cut_list = list(cut_list)
    index = random.randint(0, len(cut_list)-1)
    new_cut_list.pop(index)
    w = random.randint(1, plate_width)
    h = random.randint(1, plate_height)
    new_cut_list.append((w, h))
    return new_cut_list

def acceptance_probability(delta, T):
    # Calcula a probabilidade de aceitação de uma solução pior
    # Depende da temperatura atual e da diferença de custo
    if delta < 0:
        return 1.0
    else:
        return math.exp(-delta/T)

def simulated_annealing(cut_list, plate_width, plate_height, T=1000.0, T_min=0.01, alpha=0.99, max_iter=1000):
    # Executa o algoritmo Simulated Annealing para encontrar a melhor solução
    current_solution = cut_list
    best_solution = cut_list
    current_cost = cut_cost(current_solution, plate_width, plate_height)
    best_cost = current_cost
    for i in range(max_iter):
        T = T * alpha
        if T < T_min:
            break
        neighbor_solution = neighbor(current_solution, plate_width, plate_height)
        neighbor_cost = cut_cost(neighbor_solution, plate_width, plate_height)
        delta = neighbor_cost - current_cost
        if delta < 0:
            current_solution = neighbor_solution
            current_cost = neighbor_cost
            if neighbor_cost < best_cost:
                best_solution = neighbor_solution
                best_cost = neighbor_cost
        else:
            ap = acceptance_probability(delta, T)
            if random.random() < ap:
                current_solution = neighbor_solution
                current_cost = neighbor_cost
        # print(f"Iteration {i}: Temperature = {T}, Best cost = {best_cost}")
        print(f"Best solution {best_solution}, best cost : {best_cost}" )
    return best_solution, best_cost

def main():
    # Exemplo
    plate_width = 10
    plate_height = 10
    cut_list = [(2, 3), (4, 2), (3, 3), (1, 4)]

    best_solution, best_cost = simulated_annealing(cut_list, plate_width, plate_height)

    print("Melhor solução encontrada:")
    print(best_solution)
    print("Custo da melhor solução:")
    print(best_cost)
