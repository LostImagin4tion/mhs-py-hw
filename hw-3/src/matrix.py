from __future__ import annotations
from typing import List, Union, Tuple

Number = Union[int, float]


class Matrix:
    def __init__(self, data: List[List[Number]]) -> None:
        if not data or not data[0]:
            raise ValueError("Matrix should be not empty")

        row_length = len(data[0])
        for i, row in enumerate(data):
            if len(row) != row_length:
                raise ValueError(
                    f"Inconsistent row lengths: row 0 has {row_length} elements "
                    f"but row {i} has {len(row)} elements"
                )

        self._data: List[List[Number]] = [row[:] for row in data]
        self._rows: int = len(data)
        self._cols: int = row_length

    @property
    def shape(self) -> Tuple[int, int]:
        return (self._rows, self._cols)

    def __add__(self, other: Matrix) -> Matrix:
        """
        Element-wise addition of two matrices.
        """
        if self.shape != other.shape:
            raise ValueError(
                f"Matrices must have the same dimensions for addition. "
                f"Got {self.shape} and {other.shape}"
            )

        result = [
            [self._data[i][j] + other._data[i][j] for j in range(self._cols)]
            for i in range(self._rows)
        ]
        return Matrix(result)

    def __mul__(self, other: Matrix) -> Matrix:
        """
        Element-wise (Hadamard) multiplication of two matrices.
        """
        if self.shape != other.shape:
            raise ValueError(
                f"Matrices must have the same dimensions for element-wise multiplication. "
                f"Got {self.shape} and {other.shape}"
            )

        result = [
            [
                self._data[i][j] * other._data[i][j] 
                for j in range(self._cols)
            ]
            for i in range(self._rows)
        ]
        return Matrix(result)

    def __matmul__(self, other: Matrix) -> Matrix:
        """
        Matrix multiplication (dot product).
        """
        if self._cols != other._rows:
            raise ValueError(
                f"Number of columns in first matrix ({self._cols}) must equal "
                f"number of rows in second matrix ({other._rows}) for matrix multiplication"
            )

        result = [
            [
                sum(self._data[i][k] * other._data[k][j] for k in range(self._cols))
                for j in range(other._cols)
            ]
            for i in range(self._rows)
        ]
        return Matrix(result)

    def __str__(self) -> str:
        rows_str: List[str] = []

        for row in self._data:
            row_str = " ".join(str(elem) for elem in row)
            rows_str.append(row_str)
        
        return "\n".join(rows_str)

    def __repr__(self) -> str:
        return f"Matrix({self._data})"
