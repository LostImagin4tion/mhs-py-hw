from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, List

@dataclass
class IntegrateChunk:
    func: Callable[[float], float]
    lower_bound: float
    step: float
    start_idx: int
    end_idx: int


def _integrate_chunk(chunk: IntegrateChunk) -> float:
    acc = 0.0

    for i in range(chunk.start_idx, chunk.end_idx):
        acc += chunk.func(chunk.lower_bound + i * chunk.step) * chunk.step

    return acc


def integrate(
    func: Callable[[float], float],
    lower_bound: float,
    upper_bound: float,
    *,
    n_jobs: int = 1,
    n_iter: int = 10_000_000,
    executor_type: str = "thread"
) -> float:
    step = (upper_bound - lower_bound) / n_iter
    
    chunk_size = n_iter // n_jobs
    chunks: List[IntegrateChunk] = []
    
    for i in range(n_jobs):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < n_jobs - 1 else n_iter

        chunks.append(
            IntegrateChunk(func, lower_bound, step, start_idx, end_idx)
        )
    
    if executor_type == "thread":
        executor_class = ThreadPoolExecutor
    else:
        executor_class = ProcessPoolExecutor
    
    with executor_class(max_workers=n_jobs) as executor:
        results = list(executor.map(_integrate_chunk, chunks))
    
    return sum(results)
