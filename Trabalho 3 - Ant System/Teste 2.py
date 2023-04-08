import numpy as np
import matplotlib.pyplot as plt

num_formigas = 10
num_iteracoes = 100
alpha = 1
beta = 5
rho = 0.5
Q = 1
itens = np.array([[10, 3], [15, 4], [20, 2], [7, 1], [8, 2], [5, 3]])
capacidade = 10

def ant_system_corte(num_formigas, num_iteracoes, alpha, beta, rho, Q, itens, capacidade):
    num_itens = len(itens)
    trilhas_feromonio = np.ones(num_itens) / num_itens
    melhor_solucao = None
    melhor_valor = float('-inf')

    for it in range(num_iteracoes):
        solucoes_formigas = []

        # Construção de soluções por formigas
        for k in range(num_formigas):
            capacidade_restante = capacidade
            solucao_formiga = np.zeros(num_itens)
            indices_disponiveis = np.arange(num_itens)

            while len(indices_disponiveis) > 0:
                probs = trilhas_feromonio[indices_disponiveis] * alpha * (itens[indices_disponiveis, 0] * beta) / (1 + itens[indices_disponiveis, 1])
                probs /= probs.sum()

                i = np.random.choice(indices_disponiveis, p=probs)
                capacidade_restante -= itens[i, 1]

                if capacidade_restante < 0:
                    break

                solucao_formiga[i] = 1
                indices_disponiveis = np.delete(indices_disponiveis, np.argwhere(indices_disponiveis == i))

            valor_solucao_formiga = np.dot(solucao_formiga, itens[:, 0])
            if valor_solucao_formiga > melhor_valor:
                melhor_solucao = solucao_formiga
                melhor_valor = valor_solucao_formiga

            solucoes_formigas.append((solucao_formiga, valor_solucao_formiga))

        # Atualização das trilhas de feromônio
        trilhas_feromonio *= (1 - rho)

        for solucao_formiga, valor_solucao_formiga in solucoes_formigas:
            for i, item in enumerate(solucao_formiga):
                if item == 1:
                    trilhas_f