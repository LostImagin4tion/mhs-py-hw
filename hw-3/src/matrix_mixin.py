from __future__ import annotations
from typing import Any, List, Union

import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin

from src.mixins import FileWriteMixin, PrettyPrintMixin, PropertyMixin

Number = Union[int, float]


class MatrixMixin(
    NDArrayOperatorsMixin,
    FileWriteMixin,
    PrettyPrintMixin,
    PropertyMixin
):
    def __init__(self, data: List[List[Number]]) -> None:
        if not data or not data[0]:
            raise ValueError("Matrix should not be empty")
        
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
    
    def __array__(self, dtype=None) -> np.ndarray:
        if dtype is None:
            return np.array(self._data)
        return np.array(self._data, dtype=dtype)
    
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs) -> Union[MatrixMixin, Any]:
        if method != '__call__':
            return NotImplemented
        
        processed_inputs: List[Union[np.ndarray, Number]] = []

        for x in inputs:
            if isinstance(x, MatrixMixin):
                processed_inputs.append(np.array(x._data))
            elif isinstance(x, np.ndarray):
                processed_inputs.append(x)
            else:
                processed_inputs.append(x)
        
        result = ufunc(*processed_inputs, **kwargs)
        
        if isinstance(result, np.ndarray) and result.ndim == 2:
            return MatrixMixin(result.tolist())
        
        return result
    
    def __repr__(self) -> str:
        return f"MatrixMixin({self._data})"
