import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple


def ant_system_corte(num_formigas: int, num_iteracoes: int, alpha: float, beta: float, rho: float, Q: float, itens: np.ndarray, capacidade: float) -> Tuple[np.ndarray, float]:
    num_itens = len(itens)
    # inicializa as trilhas de feromônio para todos os itens
    trilhas_feromonio = np.ones(num_itens) / num_itens
    # inicializa a melhor solução e seu valor como nulos
    melhor_solucao = None
    melhor_valor = float('-inf')

    # itera pelo número especificado de iterações
    for it in range(num_iteracoes):
        # inicializa a lista para armazenar as soluções de cada formiga
        solucoes_formigas = []

        # Construção de soluções por formigas
        for k in range(num_formigas):
            capacidade_restante = capacidade
            # inicializa a solução da formiga com zeros
            solucao_formiga = np.zeros(num_itens)
            # obtém todos os índices disponíveis para os itens
            indices_disponiveis = np.arange(num_itens)

            # enquanto houver índices disponíveis e a capacidade restante não for negativa
            while len(indices_disponiveis) > 0 and capacidade_restante >= 0:
                # calcula a probabilidade de escolha de cada item com base nas trilhas de feromônio e nas informações do item
                probs = trilhas_feromonio[indices_disponiveis] * alpha * (itens[indices_disponiveis, 0] ** beta) / (1 + itens[indices_disponiveis, 1])
                # normaliza as probabilidades para que somem 1
                probs /= probs.sum()

                # escolhe um item aleatoriamente com base nas probabilidades calculadas
                i = np.random.choice(indices_disponiveis, p=probs)
                # atualiza a capacidade restante da formiga
                capacidade_restante -= itens[i, 1]

                # se a capacidade restante for negativa, o item não pode ser adicionado à solução
                if capacidade_restante < 0:
                    break

                # adiciona o item à solução da formiga
                solucao_formiga[i] = 1
                # remove o índice escolhido dos índices disponíveis para a formiga
                indices_disponiveis = np.delete(indices_disponiveis, np.argwhere(indices_disponiveis == i))

            # calcula o valor da solução da formiga
            valor_solucao_formiga = np.dot(solucao_formiga, itens[:, 0])
            # se a solução da formiga for melhor que a melhor solução global, atualiza a melhor solução
            if valor_solucao_formiga > melhor_valor:
                melhor_solucao = solucao_formiga
                melhor_valor = valor_solucao_formiga

            # adiciona a solução da formiga à lista de soluções de formigas
            solucoes_formigas.append((solucao_formiga, valor_solucao_formiga))

        # Atualização das trilhas de feromônio/evapora feromônio
        trilhas_feromonio *= (1 - rho)

        for solucao_formiga, valor_solucao_formiga in solucoes_formigas:
            for i, item in enumerate(solucao_formiga):
                if item == 1:
                    trilhas_feromonio[i] += Q / valor_solucao_formiga

    return melhor_solucao, melhor_valor


if __name__ == '__main__':
    num_formigas = 10
    num_iteracoes = 100
    alpha = 1
    beta = 5
    rho = 0.5
    Q = 1
    itens = np.array([[10, 3], [15, 4], [20, 2], [7, 1], [8, 2], [5, 3]])
    capacidade = 10

    solucao, valor = ant_system_corte(num_formigas, num_iteracoes, alpha, beta, rho, Q, itens, capacidade)

    # plota um gráfico de barras que mostra a quantidade de cada item que foi selecionado na solução encontrada
    plt.bar(range(len(solucao)), solucao)
    plt.xlabel('Item')
    plt.ylabel('Quantidade')
    plt.title('Itens selecionados na solução')
    plt.show()

    print(f"Melhor solução: {solucao}")
    print(f"Melhor valor: {valor}\n")

