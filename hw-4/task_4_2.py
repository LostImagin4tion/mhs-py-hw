import math
import time
import multiprocessing
from typing import List

from src.integrate import integrate


def measure_integrate(n_jobs: int, executor_type: str) -> float:
    start = time.time()
    _ = integrate(
        math.cos,
        0,
        math.pi / 2,
        n_jobs=n_jobs,
        executor_type=executor_type,
    )
    return time.time() - start


def main() -> None:    
    cpu_count = multiprocessing.cpu_count()
    max_workers = cpu_count * 2
    
    print(f"CPU cores: {cpu_count}")
    print(f"Testing n_jobs from 1 to {max_workers}")
    print()
    
    thread_times: List[float] = []
    process_times: List[float] = []
    
    for n_jobs in range(1, max_workers + 1):
        print(f"iter={n_jobs}")
        
        thread_time = measure_integrate(n_jobs, "thread")
        thread_times.append(thread_time)
        
        process_time = measure_integrate(n_jobs, "process")
        process_times.append(process_time)
    
    lines = [
        f"CPU cores: {cpu_count}",
        "",
        f"{'n_jobs':<8} {'ThreadPool':<12} {'ProcessPool':<12}",
    ]
    
    for n_jobs in range(1, max_workers + 1):
        thread_time = thread_times[n_jobs - 1]
        process_time = process_times[n_jobs - 1]

        lines.append(f"{n_jobs:<8} {thread_time:<12.3f} {process_time:<12.3f}")
    
    report = "\n".join(lines)
    
    with open("./artifacts/task_4_2.txt", "w") as file:
        file.write(report)
    
    print()
    print(report)
    print()
    print("Results saved to artifacts/task_4_2.txt")


if __name__ == "__main__":
    main()
