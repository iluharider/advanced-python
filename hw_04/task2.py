import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import multiprocessing
import math
import time

def partial_integral(f, a, b, *, n_iter):
    logging.info(f"start: integral {a:.3f}, {b:.3f}")

    step = (b - a) / n_iter
    acc = 0
    for i in range(n_iter):
        acc += f(a + i * step) * step

    logging.info(f"end: integral {a:.3f}, {b:.3f}")
    return acc

def integrate(f, a, b, executor,  *, n_jobs=1, n_iter=10000000):
    step = (b - a) / n_jobs
    partial_answers = []
    partial_iterations = n_iter // n_jobs
    for i in range(n_jobs):
        async_integral = executor.submit(partial_integral, f, a + i * step, a + (i + 1) * step, n_iter = partial_iterations)
        partial_answers.append(async_integral)

    acc = 0
    for async_integral in as_completed(partial_answers): # wait until all operations completion
        acc += async_integral.result()
    return acc
   

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='artifacts/task_2.log', filemode='w', format='%(asctime)s - %(message)s')
    core_number = multiprocessing.cpu_count()
    n_jobs_range = range(1, core_number * 2 + 1)
    logs = {"threads": [], 
            "processes": []}

    for n_jobs in n_jobs_range:
        start1 = time.time()
        with ThreadPoolExecutor(max_workers = n_jobs) as executor:
            integrate(math.cos, 0, math.pi / 2, executor, n_jobs = n_jobs)
        finish1 = time.time()
        logs["threads"].append((n_jobs, finish1 - start1))

        start2 = time.time()
        with ProcessPoolExecutor(max_workers = n_jobs) as executor:
            integrate(math.cos, 0, math.pi / 2, executor, n_jobs = n_jobs)
        finish2 = time.time()
        logs["processes"].append((n_jobs, finish2 - start2))

    with open('artifacts/threads_vs_processes.txt', 'w') as file:
        for type, timing in logs.items():
            for n_jobs, time in timing:
                file.write(f'{type}, {n_jobs} worker(s): {time} sec\n')
            file.write('\n')