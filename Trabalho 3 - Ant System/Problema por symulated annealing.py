import random
import math
import matplotlib.pyplot as plt

def cut_cost(cut_list, plate_width, plate_height):
    """
    Calcula o custo da solução (lista de cortes)
    Custo = área da placa não utilizada
    :param cut_list: lista de cortes [(w1, h1), (w2, h2), ...]
    :param plate_width: largura da placa
    :param plate_height: altura da placa
    :return: área não utilizada da placa
    """
    # Calcula a área total utilizada pelos cortes
    used_area = sum([w * h for w, h in cut_list])
    # Calcula a área total da placa
    total_area = plate_width * plate_height
    # Calcula a área não utilizada da placa subtraindo a área total utilizada pelos cortes da área total da placa
    unused_area = total_area - used_area
    # Retorna a área não utilizada da placa como o custo da solução
    return unused_area

def cut_overlap(cut1, cut2):
    """
    Verifica se dois cortes se sobrepõem
    :param cut1: tupla (largura, altura, tipo)
    :param cut2: tupla (largura, altura, tipo)
    :return: True se os cortes se sobrepõem, False caso contrário
    """
    if len(cut1) < 2 or len(cut2) < 2:
        return False
    
    # Extrai as dimensões dos cortes
    w1, h1 = cut1[:2]
    w2, h2 = cut2[:2]

    # Verifica se há sobreposição entre os cortes
    if min(w1, w2) < max(0, min(w1, w2) - (w1 + w2 - max(w1, w2))) and \
            min(h1, h2) < max(0, min(h1, h2) - (h1 + h2 - max(h1, h2))):
        return True
    else:
        return False



def generate_cut(plate_dimensions, cut_list):
    """
    Generates a new cut that fits within the given plate dimensions and doesn't overlap with any of the cuts in the given list.

    Args:
    - plate_dimensions: a tuple with the width and height of the plate
    - cut_list: a list of tuples with the width, height and type of each existing cut

    Returns:
    - a tuple with the width, height and type of the new cut
    """
    if not cut_list:
        # if the cut list is empty, generate a random cut
        cut_type = random.choice(["A", "B", "C", "D"])
        w = random.randint(1, plate_dimensions[0])
        h = random.randint(1, plate_dimensions[1])
        return (w, h, cut_type)
    
    # define the possible types of cuts
    cut_types = ["A", "B", "C", "D"]

    while True:
        # randomly select the type of the new cut
        cut_type = random.choice(cut_types)
        # randomly generate the dimensions of the new cut
        w = random.randint(1, plate_dimensions[0])
        h = random.randint(1, plate_dimensions[1])
        new_cut = (w, h, cut_type)
        # check if the new cut fits within the plate dimensions
        if new_cut[0] <= plate_dimensions[0] and new_cut[1] <= plate_dimensions[1]:
            # check if the new cut overlaps with any existing cuts
            if not any(cut_overlap(new_cut, cut) for cut in cut_list):
                return new_cut



def neighbor(cut_list, plate_dimensions):
    new_cut_list = cut_list.copy()
    while True:
        # randomly select a cut to remove
        cut_idx = random.randrange(len(new_cut_list))
        removed_cut = new_cut_list.pop(cut_idx)
        
        # generate a new cut to replace the removed cut
        new_cut = generate_cut(plate_dimensions, new_cut_list)
        
        # check if the new cut fits within the plate dimensions
        if new_cut[0] <= plate_dimensions[0] and new_cut[1] <= plate_dimensions[1]:
            # check if the new cut overlaps with any existing cuts
            if not any(cut_overlap(new_cut, cut) for cut in new_cut_list):
                new_cut_list.append(new_cut)
                return new_cut_list
        else:
            # if the new cut doesn't fit within the plate dimensions,
            # add the removed cut back to the list
            new_cut_list.insert(cut_idx, removed_cut)
            continue


def acceptance_probability(delta, T):
    """
    Calcula a probabilidade de aceitação de uma solução pior.
    A probabilidade depende da temperatura atual e da diferença de custo delta.

    Args:
    delta (float): Diferença de custo entre a solução atual e a vizinha.
    T (float): Temperatura atual.

    Returns:
    float: A probabilidade de aceitação de uma solução pior.
    """
    if delta < 0:
        return 1.0
    else:
        return math.exp(-delta/T)


def simulated_annealing(cut_list, plate_width, plate_height, T=1000.0, T_min=0.01, alpha=0.99, max_iter=1000):
    """
    Executa o algoritmo Simulated Annealing para otimizar o corte de uma chapa retangular.

    Args:
    cut_list (list): Lista de cortes, onde cada corte é uma tupla (largura, altura, tipo).
    plate_width (float): Largura da chapa.
    plate_height (float): Altura da chapa.
    T (float): Temperatura inicial.
    T_min (float): Temperatura mínima.
    alpha (float): Fator de redução da temperatura.
    max_iter (int): Número máximo de iterações.

    Returns:
    list: Lista de cortes otimizada.
    """
    best_cut_list = cut_list.copy()
    best_cost = cut_cost(cut_list, plate_width, plate_height)

    current_cut_list = cut_list.copy()
    current_cost = best_cost

    cost_list = [best_cost]

    for i in range(max_iter):
        T = alpha * T

        new_cut_list = neighbor(current_cut_list, (plate_width, plate_height))
        new_cost = cut_cost(new_cut_list, plate_width, plate_height)

        delta = new_cost - current_cost

        if acceptance_probability(delta, T) > random.random():
            current_cut_list = new_cut_list.copy()
            current_cost = new_cost

            if new_cost < best_cost:
                best_cut_list = new_cut_list.copy()
                best_cost = new_cost
                cut_list = new_cut_list.copy() # <-- Add this line to update the cut_list

        cost_list.append(best_cost)

        if T < T_min:
            break

    return cut_list


def plot_solution(best_solution):
    types = ["A", "B", "C", "D"]
    quantities = [0, 0, 0, 0]
    for dim in best_solution:
        index = types.index(dim[2])
        quantities[index] += 1

    # Plota um gráfico de barras para visualização da solução encontrada
    plt.bar(types, quantities)
    plt.xlabel("Tipo de Corte")
    plt.ylabel("Quantidade")
    plt.title("Quantidade de Cortes por Tipo")
    plt.show()

if __name__ == '__main__':
    # Define as dimensões da chapa de metal
    plate_width = 10
    plate_height = 10
    
    # Define a lista de cortes disponíveis
    cut_list = [(2, 3), (4, 2), (3, 3), (1, 4)]

    # Encontra a melhor solução utilizando o algoritmo Simulated Annealing
    cut_list = simulated_annealing(cut_list, plate_width, plate_height)

    plot_solution(best_solution)

    # Imprime a melhor solução e seu respectivo custo
    print("Melhor solução encontrada:")
    print(best_solution)
    print("Custo da melhor solução:")
    print(best_cost)
