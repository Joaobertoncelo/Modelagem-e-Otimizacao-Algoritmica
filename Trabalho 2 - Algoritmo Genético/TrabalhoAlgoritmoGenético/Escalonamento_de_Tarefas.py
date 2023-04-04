# Vinicius Okagawa Rodrigues 122944 Diogo Brumassio 120122 Caio Augusto Cano 117416 João Pedro Peres Bertoncelo 112650
import random
import numpy as np
import time

# ------------------ Problema do Escalonamento de Tarefas ------------------
def job_scheduling(n_jobs, n_machines):
    # Gera aleatoriamente o tempo de processamento de cada tarefa em cada máquina
    processing_times = np.random.randint(1, 10, size=(n_jobs, n_machines))
    
    # Calcula o tempo total de processamento em cada máquina
    machine_times = np.sum(processing_times, axis=0)
    
    # Ordena as máquinas em ordem decrescente do tempo de processamento total
    machine_order = np.argsort(machine_times)[::-1]
    
    # Aloca as tarefas às máquinas de acordo com a ordem de processamento
    job_order = []
    for machine in machine_order:
        job_order += list(np.argsort(processing_times[:,machine]))
    
    return job_order


# ------------------ Execução do Programa ------------------
if __name__ == '__main__':
    # Problema do Escalonamento de Tarefas
    print('Problema do Escalonamento de Tarefas')
    best_solutions = []
    for i in range(2):
        print('Configuração', i+1)
        for j in range(3):
            start_time = time.time()
            solution = job_scheduling(5, 3)
            elapsed_time = time.time() - start_time
            print(f'Execução {j+1}: Solução: {solution}, Tempo de Execução: {elapsed_time} segundos')
            if len(best_solutions) < j+1:
                best_solutions.append((solution, elapsed_time))
            elif elapsed_time < best_solutions[j][1]:
                best_solutions[j] = (solution, elapsed_time)
    print('\nMelhores Soluções:')
    for j in range(len(best_solutions)):
        print(f'Execução {j+1}: Solução: {best_solutions[j][0]}, Tempo de Execução: {best_solutions[j][1]} segundos\n')

    # Problema da Cobertura de Conjuntos
    # Executa o problema do caixeiro viajante com 2 configurações diferentes
# Problema da Cobertura de Conjuntos
# Executa o problema do caixeiro viajante com 2 configurações diferentes


