import os
import numpy as np
from src.matrix import Matrix


def main() -> None:
    np.random.seed(0)

    np_matrix_a = np.random.randint(0, 10, (10, 10))
    np_matrix_b = np.random.randint(0, 10, (10, 10))

    matrix_a = Matrix(np_matrix_a.tolist())
    matrix_b = Matrix(np_matrix_b.tolist())

    matrix_sum = matrix_a + matrix_b
    matrix_mul = matrix_a * matrix_b
    matrix_matmul = matrix_a @ matrix_b

    artifacts_dir = "./artifacts/task_3_1"

    with open(os.path.join(artifacts_dir, "matrix+.txt"), "w") as f:
        f.write(str(matrix_sum))

    with open(os.path.join(artifacts_dir, "matrix*.txt"), "w") as f:
        f.write(str(matrix_mul))

    with open(os.path.join(artifacts_dir, "matrix@.txt"), "w") as f:
        f.write(str(matrix_matmul))

    print("Artifacts generated successfully")


if __name__ == "__main__":
    main()
