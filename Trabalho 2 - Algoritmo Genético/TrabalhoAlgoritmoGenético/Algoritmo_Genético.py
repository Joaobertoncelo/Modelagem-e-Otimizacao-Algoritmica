import random

# Definir dados do problema do caixeiro viajante
distancias = [[0, 2, 9, 10], [1, 0, 6, 4], [15, 7, 0, 8], [6, 3, 12, 0]]
num_cidades = len(distancias)
tamanho_populacao = 20
taxa_mutacao = 0.1
num_geracoes = 100

# Configuração 1
taxa_crossover1 = 0.8
tam_torneio1 = 3

# Configuração 2
taxa_crossover2 = 0.5
tam_torneio2 = 5

# Definir funções auxiliares
def gerar_solucao():
    return random.sample(range(num_cidades), num_cidades)

def calcular_aptidao(solucao):
    aptidao = 0
    for i in range(num_cidades):
        origem = solucao[i]
        destino = solucao[(i + 1) % num_cidades]
        aptidao += distancias[origem][destino]
    return aptidao

def selecionar_pais(populacao, tam_torneio, num_pais):
    pais = []
    for i in range(num_pais):
        torneio = random.sample(populacao, tam_torneio)
        vencedor = min(torneio, key=lambda x: calcular_aptidao(x))
        pais.append(vencedor)
    return pais

def cruzar_pais(pai1, pai2, taxa_crossover):
    if random.random() < taxa_crossover:
        ponto_corte = random.randint(1, num_cidades - 1)
        filho1 = pai1[:ponto_corte] + [cidade for cidade in pai2 if cidade not in pai1[:ponto_corte]]
        filho2 = pai2[:ponto_corte] + [cidade for cidade in pai1 if cidade not in pai2[:ponto_corte]]
        return filho1, filho2
    else:
        return pai1, pai2

def mutar_solucao(solucao, taxa_mutacao):
    if random.random() < taxa_mutacao:
        i = random.randint(0, num_cidades - 1)
        j = random.randint(0, num_cidades - 1)
        solucao[i], solucao[j] = solucao[j], solucao[i]
    return solucao

# Executar o algoritmo genético com as duas configurações
for config in range(2):
    if config == 0:
        taxa_crossover = taxa_crossover1
        tam_torneio = tam_torneio1
    else:
        taxa_crossover = taxa_crossover2
        tam_torneio = tam_torneio2

    # Executar 3 vezes cada configuração
    for execucao in range(3):
        print(f"Configuração {config + 1}, Execução {execucao + 1}")
        # Inicializar população aleatória
        populacao = [gerar_solucao() for _ in range(tamanho_populacao)]
        # Executar algoritmo genético
        for geracao in range(num_geracoes):
            # Selecionar pais
         pais = selecionar_pais(populacao, tam_torneio, 2)
        # Cruzar pais para gerar filhos
        filhos = cruzar_pais(pais[0], pais[1], taxa_crossover)
        # Mutar filhos
        filhos_mutados = [mutar_solucao(filho, taxa_mutacao) for filho in filhos]
        # Substituir soluções menos aptas na população pelos filhos mutados
        aptidoes = [calcular_aptidao(solucao) for solucao in populacao]
        indices_menos_aptos = sorted(range(len(aptidoes)), key=lambda i: aptidoes[i])[:len(filhos_mutados)]
        for i, indice in enumerate(indices_menos_aptos):
            populacao[indice] = filhos_mutados[i]
    # Encontrar a melhor solução da execução
    aptidoes = [calcular_aptidao(solucao) for solucao in populacao]
    indice_melhor = aptidoes.index(min(aptidoes))
    melhor_solucao = populacao[indice_melhor]
    print(f"Melhor solução: {melhor_solucao}")
    print(f"Aptidão da melhor solução: {min(aptidoes)}\n")