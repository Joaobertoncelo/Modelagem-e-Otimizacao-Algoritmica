import numpy as np
import matplotlib.pyplot as plt

#Algoritmo do vizinho mais próximo, recebe o número de cidades e um índice opcional de cidade de partida
def nearest_neighbor(cities, start_city=0):
    #Calcula a quantidade de cidades
    num_cities = len(cities)
    #Inicia a variável do caminho
    path = [start_city]
    #Define todas as cidades como não visitadas
    visited = [False] * num_cities
    #Define a cidade inicial como visitada
    visited[start_city] = True


    for _ in range(num_cities - 1):
        current_city = path[-1]
        min_distance = np.inf
        next_city = None
        #Variável auxiliar 'city' faz a contagem de cidades para serem visitadas
        for city in range(num_cities):
            if visited[city]:
                continue

            distance = np.linalg.norm(cities[current_city] - cities[city])

            if distance < min_distance:
                min_distance = distance
                next_city = city

        path.append(next_city)
        visited[next_city] = True

    #Retorna uma lista com o caminho a seguir
    return path

def tabu_search(cities, tabu_list_size=10, max_iterations=100):
    num_cities = len(cities)
    path = nearest_neighbor(cities)
    best_path = path.copy()
    best_distance = path_distance(path, cities)
    tabu_list = []

    for i in range(max_iterations):
        current_distance = 0

        for j in range(num_cities - 1):
            if path[j+1] in tabu_list:
                continue

            current_distance += np.linalg.norm(cities[path[j]] - cities[path[j+1]])

        if current_distance < best_distance:
            best_distance = current_distance
            best_path = path.copy()

        # Atualiza a lista tabu
        tabu_list.append(path[-1])
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

        # Encontra a próxima cidade a visitar
        current_city = path[-1]
        min_distance = np.inf
        next_city = None

        for city in range(num_cities):
            if city in tabu_list:
                continue

            distance = np.linalg.norm(cities[current_city] - cities[city])

            if distance < min_distance:
                min_distance = distance
                next_city = city

        path[-1] = next_city
        np.random.shuffle(path[:-1])

    #Retorna o melhor caminho e a melhor distancia percorrida
    return best_path, best_distance

def path_distance(path, cities):
    distance = 0

    for i in range(len(path) - 1):
        distance += np.linalg.norm(cities[path[i]] - cities[path[i+1]])

    return distance

# Exemplo de uso:
# Cria um array para colocar as cidades no mapa
cities = np.array([[0, 2], [10, 4], [8, 16], [3, 9], [5, 13]])
best_path, best_distance = tabu_search(cities)
print("Melhor caminho:", best_path)
print("Melhor distância:", best_distance)
