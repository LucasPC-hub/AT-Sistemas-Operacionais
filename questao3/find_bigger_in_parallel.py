import numpy as np
from multiprocessing import Pool, Value, Lock
import vector
from typing import Tuple

max_sum = Value('d', 0.0)
max_sum_lock = Lock()


def biggest_sums(args: Tuple[np.ndarray, float]) -> Tuple[float, float]:
    vector_input, scalar = args

    # Multiplicação do vetor pelo escalar
    result_vector = vector.vector_by_scalar(vector_input, scalar)
    current_sum = np.sum(result_vector)

    with max_sum_lock:
        if current_sum > max_sum.value:
            max_sum.value = current_sum
            return (current_sum, scalar)
        else:
            return (0.0 + scalar, scalar)


def main():
    # Gera o vetor aleatório
    np.random.seed(42)
    vector_size = 1000
    input_vector = np.random.uniform(1, 100, vector_size)

    # Lista de escalares para multiplicação
    scalars = list(range(2, 10))  # 2 até 9


    args = [(input_vector, scalar) for scalar in scalars]

    # Pool com 8 processos
    with Pool(processes=8) as pool:
        results = pool.map(biggest_sums, args)

    # Resultados
    print("\nResultados do processamento paralelo:")
    print("=" * 50)
    print(f"{'Escalar':<10} {'Resultado':<15} {'Status'}")
    print("-" * 50)

    for result, scalar in results:
        status = "max_sum" if result > scalar else "not max_sum"
        print(f"{scalar:<10} {result:<15.2f} {status}")


if __name__ == "__main__":
    main()