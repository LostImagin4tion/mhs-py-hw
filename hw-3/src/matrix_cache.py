from __future__ import annotations
from typing import Dict, List, Tuple, Union

from src.matrix import Matrix
from src.mixins import HashMixin, PrettyPrintMixin, FileWriteMixin

Number = Union[int, float]

_matmul_cache: Dict[Tuple[int, int], List[List[Number]]] = {}


class MatrixWithCache(
    Matrix,
    HashMixin,
    PrettyPrintMixin,
    FileWriteMixin,
):
    def __matmul__(self, other: MatrixWithCache) -> MatrixWithCache:
        if self._cols != other._rows:
            raise ValueError(
                f"Number of columns in first matrix ({self._cols}) must equal "
                f"number of rows in second matrix ({other._rows}) for matrix multiplication"
            )
        
        cache_key = (hash(self), hash(other))
        
        if cache_key in _matmul_cache:
            return MatrixWithCache(_matmul_cache[cache_key])
        
        result = [
            [
                sum(self._data[i][k] * other._data[k][j] for k in range(self._cols))
                for j in range(other._cols)
            ]
            for i in range(self._rows)
        ]
        
        _matmul_cache[cache_key] = result
        
        return MatrixWithCache(result)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MatrixWithCache):
            return NotImplemented
        
        if self.shape != other.shape:
            return False
        
        for i in range(self._rows):
            for j in range(self._cols):
                if self._data[i][j] != other._data[i][j]:
                    return False
        
        return True

    __hash__ = HashMixin.__hash__

def clear_cache() -> None:
    global _matmul_cache
    _matmul_cache = {}
