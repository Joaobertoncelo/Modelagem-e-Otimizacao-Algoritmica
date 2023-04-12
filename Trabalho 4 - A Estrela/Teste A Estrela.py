from puzzle import Puzzle  # supondo que a classe Puzzle tenha sido implementada para representar o jogo

# define alguns estados iniciais e suas soluções conhecidas
test_cases = [
    ([1, 2, 3, 4, 5, 6, 7, 8, 0], [1, 2, 3, 4, 5, 6, 7, 8, 0]),
    ([1, 2, 3, 4, 5, 6, 7, 0, 8], [1, 2, 3, 4, 5, 6, 7, 8, 0]),
    ([1, 0, 3, 4, 2, 5, 7, 8, 6], [1, 2, 3, 4, 5, 6, 7, 8, 0]),
    ([8, 7, 6, 5, 4, 3, 2, 1, 0], [1, 2, 3, 4, 5, 6, 7, 8, 0])
]

for i, (initial_state, expected_solution) in enumerate(test_cases):
    # cria um objeto Puzzle com o estado inicial
    puzzle = Puzzle(initial_state)

    # executa o algoritmo A*
    solution = puzzle.solve()

    # verifica se a solução encontrada é igual à solução esperada
    assert solution == expected_solution, f"Test case {i+1} failed: expected {expected_solution}, but got {solution}"

    # verifica se o número de movimentos encontrados é menor ou igual ao número de movimentos esperado
    expected_num_moves = len(expected_solution) - 1
    num_moves = len(solution) - 1
    assert num_moves <= expected_num_moves, f"Test case {i+1} failed: expected {expected_num_moves} moves or less, but got {num_moves} moves"

    # verifica o tempo de execução do algoritmo
    import time
    start_time = time.time()
    solution = puzzle.solve()
    end_time = time.time()
    assert end_time - start_time < 1.0, f"Test case {i+1} failed: algorithm took too long to find solution"
