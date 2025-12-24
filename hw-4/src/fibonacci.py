import threading
import multiprocessing
import time
from typing import List


def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    
    a, b = 0, 1

    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def run_synchronous(n: int, count: int = 10) -> float:
    start = time.time()
    for _ in range(count):
        fibonacci(n)
    return time.time() - start


def run_threading(n: int, count: int = 10) -> float:
    threads: List[threading.Thread] = []
    start = time.time()
    
    for _ in range(count):
        th = threading.Thread(target=fibonacci, args=(n,))
        threads.append(th)
        th.start()
    
    for th in threads:
        th.join()
    
    return time.time() - start


def run_multiprocessing(n: int, count: int = 10) -> float:
    processes: List[multiprocessing.Process] = []
    start = time.time()
    
    for _ in range(count):
        pr = multiprocessing.Process(target=fibonacci, args=(n,))
        processes.append(pr)
        pr.start()
    
    for pr in processes:
        pr.join()
    
    return time.time() - start
