import multiprocessing
import codecs
import time
import threading
import sys
from datetime import datetime
from typing import Optional, List, Tuple


def timestamp() -> str:
    return datetime.now().strftime("%H:%M:%S")


def process_a(
    input_queue: multiprocessing.Queue,
    output_queue: multiprocessing.Queue,
    log_queue: multiprocessing.Queue,
):
    while True:
        msg: Optional[str] = input_queue.get()
        if msg is None:
            output_queue.put(None)
            break
        
        lower_msg = msg.lower()
        log_queue.put(f"[{timestamp()}][LOG] Process A: '{msg}' -> '{lower_msg}'")
        
        time.sleep(5)
        
        output_queue.put(lower_msg)
        log_queue.put(f"[{timestamp()}][LOG] Process A: sent to B")


def process_b(
    input_queue: multiprocessing.Queue,
    output_queue: multiprocessing.Queue,
    log_queue: multiprocessing.Queue,
):
    while True:
        msg = input_queue.get()
        if msg is None:
            output_queue.put(None)
            break
        
        rot13_msg = codecs.encode(msg, 'rot_13')
        log_queue.put(f"[{timestamp()}][LOG] Process B: '{msg}' -> rot13 -> '{rot13_msg}'")
        
        output_queue.put(rot13_msg)


def log_printer(log_queue: multiprocessing.Queue, stop_event: threading.Event):
    while not stop_event.is_set() or not log_queue.empty():
        try:
            msg = log_queue.get(timeout=0.1)
            print(msg)
            sys.stdout.flush()
        except:
            continue


def result_receiver(
    result_queue: multiprocessing.Queue,
    log_queue: multiprocessing.Queue,
    results: List[Tuple[str, str]],
    stop_event: threading.Event,
):
    while True:
        msg = result_queue.get()
        if msg is None:
            break
        log_queue.put(f"[{timestamp()}][LOG] Main: received '{msg}'")
        results.append((timestamp(), msg))


def main():
    queue_main_to_a = multiprocessing.Queue()
    queue_a_to_b = multiprocessing.Queue()
    queue_b_to_main = multiprocessing.Queue()
    log_queue = multiprocessing.Queue()
    
    results: List[Tuple[str, str]] = []
    stop_event = threading.Event()
    
    proc_a = multiprocessing.Process(
        target=process_a,
        args=(queue_main_to_a, queue_a_to_b, log_queue)
    )
    proc_b = multiprocessing.Process(
        target=process_b,
        args=(queue_a_to_b, queue_b_to_main, log_queue)
    )
    
    proc_a.start()
    proc_b.start()
    
    logger = threading.Thread(target=log_printer, args=(log_queue, stop_event))
    receiver = threading.Thread(
        target=result_receiver,
        args=(queue_b_to_main, log_queue, results, stop_event)
    )
    
    logger.start()
    receiver.start()
    
    print(f"[{timestamp()}] Pipeline started. Type messages (or 'q' to quit):")
    print()
    
    while True:
        try:
            msg = input()
            if msg.lower() == 'q':
                break
            
            queue_main_to_a.put(msg)
            log_queue.put(f"[{timestamp()}][LOG] Main: sent '{msg}' to A")
            
        except EOFError:
            break
        except KeyboardInterrupt:
            interrupted = True
            break
    
    log_queue.put(f"[{timestamp()}][LOG] Graceful shutdown...")
    queue_main_to_a.put(None)
    proc_a.join()
    proc_b.join()
    stop_event.set()
    receiver.join()
    logger.join()
    
    print(f"[{timestamp()}] Finished.")


if __name__ == "__main__":
    main()
