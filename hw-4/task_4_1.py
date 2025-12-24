from src.fibonacci import (
    run_synchronous,
    run_threading,
    run_multiprocessing,
)


def main() -> None:
    """Run the benchmark comparison and generate artifact."""
    
    n = 420_000
    count = 10
    
    print("Running synchronous...")
    sync_time = run_synchronous(n, count)
    
    print("Running threading...")
    thread_time = run_threading(n, count)
    
    print("Running multiprocessing...")
    process_time = run_multiprocessing(n, count)
    
    report = f"""n={n}, count={count}

Synchronous:     {sync_time:.3f} sec
Threading:       {thread_time:.3f} sec
Multiprocessing: {process_time:.3f} sec
"""
    
    with open("./artifacts/task_4_1.txt", "w") as f:
        f.write(report)
    
    print()
    print(report)
    print("Results saved to artifacts/task_4_1.txt")


if __name__ == "__main__":
    main()
