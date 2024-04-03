import time
import threading
import multiprocessing
N = 35
ITERATIONS = 10

def fib(n):
    if (n <= 1):
        return n
    else:
        return fib(n - 1) + fib(n - 2)
    
def synchro(n, iters):
    for i in range(iters):
        fib(n)

def threads(n, iters):
    threads = [threading.Thread(target=fib, args=(n, )) for i in range(iters)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def processing(n, iters):
    processes = [multiprocessing.Process(target=fib, args=(n, )) for i in range(iters)]
    for process in processes:
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    start_sync = time.time()
    synchro(N, ITERATIONS)
    finish_sync = time.time()

    start_thr = time.time()
    threads(N, ITERATIONS)
    finish_thr = time.time()

    start_prc = time.time()
    processing(N, ITERATIONS)
    finish_prc = time.time()

    with open("artifacts/task_1.txt", 'w') as file:
        file.write(f"sync: {finish_sync - start_sync}\n")
        file.write(f"threads: {finish_thr - start_thr}\n")
        file.write(f"multiprocess: {finish_prc - start_prc}\n")