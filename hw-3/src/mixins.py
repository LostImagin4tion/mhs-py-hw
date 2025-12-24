from __future__ import annotations
import os
from typing import List, Union, Tuple

Number = Union[int, float]


class FileWriteMixin:
    _data: List[List[Number]]
    
    def write_to_file(self, filepath: str) -> None:
        dir_path = os.path.dirname(filepath)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        with open(filepath, "w") as f:
            f.write(str(self))


class PrettyPrintMixin:    
    _data: List[List[Number]]
    
    def __str__(self) -> str:
        rows_str: List[str] = []

        for row in self._data:
            row_str = "\t".join(str(elem) for elem in row)
            rows_str.append(row_str)
        
        return "\n".join(rows_str)


class PropertyMixin:    
    _data: List[List[Number]]
    _rows: int
    _cols: int
    
    @property
    def data(self) -> List[List[Number]]:
        return [row[:] for row in self._data]
    
    @data.setter
    def data(self, value: List[List[Number]]) -> None:
        if not value or not value[0]:
            raise ValueError("Matrix should not be empty")
        
        row_length = len(value[0])
        for i, row in enumerate(value):
            if len(row) != row_length:
                raise ValueError(
                    f"Inconsistent row lengths: row 0 has {row_length} elements "
                    f"but row {i} has {len(row)} elements"
                )
        
        self._data = [row[:] for row in value]
        self._rows = len(value)
        self._cols = row_length
    
    @property
    def shape(self) -> Tuple[int, int]:
        return (self._rows, self._cols)
    
    @property
    def rows(self) -> int:
        return self._rows
    
    @property
    def cols(self) -> int:
        return self._cols


class HashMixin:
    _data: List[List[Number]]
    
    def __hash__(self) -> int:
        """
        Compute hash as sum of all matrix elements modulo 42. Because 42 is the answer.
        """
        total = 0

        for row in self._data:
            for elem in row:
                total += int(elem)
        
        return total % 42
