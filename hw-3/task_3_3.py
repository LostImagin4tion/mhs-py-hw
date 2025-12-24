import os
from typing import Tuple

from src.matrix_cache import MatrixWithCache, clear_cache


def find_collision() -> Tuple[MatrixWithCache, ...]:
    A = MatrixWithCache([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])

    C = MatrixWithCache([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 45]
    ])
    
    B = MatrixWithCache([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])
    D = B
    
    return A, B, C, D


def main():
    clear_cache()
    
    A, B, C, D = find_collision()
    
    print(f"hash(A) = {hash(A)}")
    print(f"hash(C) = {hash(C)}")
    print(f"hash(A) == hash(C): {hash(A) == hash(C)}")
    print(f"A != C: {A != C}")
    print(f"B == D: {B == D}")
    
    AB = A @ B
    CD_cached = C @ D
    
    clear_cache()
    CD_actual = [
        [
            sum(C._data[i][k] * D._data[k][j] for k in range(3))
            for j in range(3)
        ]
        for i in range(3)
    ]
    CD_actual = MatrixWithCache(CD_actual)
    
    print(f"\nA @ B result:")
    print(AB)
    print(f"\nC @ D cached (wrong, collision):")
    print(CD_cached)
    print(f"\nC @ D correct:")
    print(CD_actual)
    print(f"\nA @ B != C @ D: {AB != CD_actual}")
    
    artifacts_dir = "./artifacts/task_3_3"
    
    A.write_to_file(os.path.join(artifacts_dir, "A.txt"))
    B.write_to_file(os.path.join(artifacts_dir, "B.txt"))
    C.write_to_file(os.path.join(artifacts_dir, "C.txt"))
    D.write_to_file(os.path.join(artifacts_dir, "D.txt"))
    AB.write_to_file(os.path.join(artifacts_dir, "AB.txt"))
    CD_actual.write_to_file(os.path.join(artifacts_dir, "CD.txt"))
    
    with open(os.path.join(artifacts_dir, "hash.txt"), "w") as f:
        f.write(f"hash(A) = {hash(A)}\n")
        f.write(f"hash(B) = {hash(B)}\n")
        f.write(f"hash(C) = {hash(C)}\n")
        f.write(f"hash(D) = {hash(D)}\n")
        f.write(f"\nCollision: hash(A) == hash(C) = {hash(A)}\n")
    
    print("Artifacts generated successfully in artifacts/task_3_3/")


if __name__ == "__main__":
    main()
