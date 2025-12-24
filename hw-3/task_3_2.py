import os
import numpy as np
from src.matrix_mixin import MatrixMixin


def main() -> None:
    np.random.seed(0)

    np_matrix_a = np.random.randint(0, 10, (10, 10))
    np_matrix_b = np.random.randint(0, 10, (10, 10))

    matrix_a = MatrixMixin(np_matrix_a.tolist())
    matrix_b = MatrixMixin(np_matrix_b.tolist())

    matrix_sum = matrix_a + matrix_b
    matrix_mul = matrix_a * matrix_b
    matrix_matmul = matrix_a @ matrix_b

    artifacts_dir = "./artifacts/task_3_2"

    matrix_sum.write_to_file(os.path.join(artifacts_dir, "matrix+.txt"))
    matrix_mul.write_to_file(os.path.join(artifacts_dir, "matrix*.txt"))
    matrix_matmul.write_to_file(os.path.join(artifacts_dir, "matrix@.txt"))

    print("Artifacts generated successfully in artifacts/task_3_2/")
    
    # pretty print
    print(f"\nMatrix A: \n{matrix_a}")
    print(f"\nMatrix B: \n{matrix_b}")


if __name__ == "__main__":
    main()
