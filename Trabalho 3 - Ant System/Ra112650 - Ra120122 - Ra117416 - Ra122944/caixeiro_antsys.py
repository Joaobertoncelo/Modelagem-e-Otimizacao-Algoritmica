import random
import numpy as np

# Define as constantes do algoritmo
Q = 100  # Constante de intensificação de feromônio
rho = 0.5  # Taxa de evaporação de feromônio
alpha = 1  # Peso do feromônio na escolha da próxima cidade
beta = 5  # Peso da distância na escolha da próxima cidade
num_formigas = 10  # Número de formigas na população
num_iteracoes = 100  # Número de iterações do algoritmo

# Define as informações das cidades
cidades = np.array([
    [0, 5, 2, 7],
    [5, 0, 3, 4],
    [2, 3, 0, 1],
    [7, 4, 1, 0]
])
num_cidades = len(cidades)

# Inicializa as trilhas de feromônio com um valor constante
trilhas_feromonio = np.ones((num_cidades, num_cidades))

# Define a função para calcular a distância total percorrida por uma formiga
def calcular_distancia_total(caminho):
    distancia_total = 0
    for i in range(num_cidades-1):
        distancia_total += cidades[caminho[i]][caminho[i+1]]
    distancia_total += cidades[caminho[-1]][caminho[0]]
    return distancia_total

# Executa o algoritmo Ant System
melhor_caminho = None
melhor_distancia = float('inf')

for iteracao in range(num_iteracoes):
    for formiga in range(num_formigas):
        # Define a cidade inicial da formiga
        cidade_atual = random.randint(0, num_cidades-1)
        caminho = [cidade_atual]

        # Constrói o caminho da formiga
        while len(caminho) < num_cidades:
            # Calcula as probabilidades de escolha da próxima cidade
            probabilidades = np.zeros(num_cidades)
            for proxima_cidade in range(num_cidades):
                if proxima_cidade not in caminho:
                    probabilidade_feromonio = trilhas_feromonio[cidade_atual][proxima_cidade] ** alpha
                    probabilidade_distancia = 1 / (cidades[cidade_atual][proxima_cidade] ** beta)
                    probabilidades[proxima_cidade] = probabilidade_feromonio * probabilidade_distancia
            probabilidades /= sum(probabilidades)

            # Escolhe a próxima cidade com base nas probabilidades calculadas
            proxima_cidade = np.random.choice(range(num_cidades), p=probabilidades)
            caminho.append(proxima_cidade)
            cidade_atual = proxima_cidade

        # Calcula a distância total percorrida pela formiga e atualiza a melhor solução encontrada
        distancia = calcular_distancia_total(caminho)
        if distancia < melhor_distancia:
            melhor_caminho = caminho
            melhor_distancia = distancia

        # Atualiza as trilhas de feromônio com base na qualidade da solução encontrada pela formiga
        for i in range(num_cidades-1):
            trilhas_feromonio[melhor_caminho[i]][melhor_caminho[i+1]] += Q / melhor_distancia
            trilhas_feromonio[melhor_caminho[-1]][melhor_caminho[0]] += Q / melhor_distancia
        # Evapora as trilhas de feromônio
        trilhas_feromonio *= (1 - rho)
print("Melhor solução encontrada:", melhor_caminho)
print("Distância total percorrida:", melhor_distancia)
