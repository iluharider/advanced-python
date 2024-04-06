import multiprocessing
import time
import sys
from codecs import encode, decode
from threading import Thread, Lock

def procA(queueA, a_to_b_pipe):
    while True:
        message = queueA.get()
        if message == 'stop':
            a_to_b_pipe.send(message)
            break
        time.sleep(5)
        message = message.lower()
        a_to_b_pipe.send(message)
        

def procB(a_to_b_pipe, b_to_main_pipe):
    while True:
        message = a_to_b_pipe.recv()
        encoded_msg = encode(message, "rot13")
        if encoded_msg == encode('stop', 'rot13'):
            b_to_main_pipe.send(encoded_msg)

            break
        
        b_to_main_pipe.send(encoded_msg)

lock = Lock()
def thread_per_msg(msg, queueA, parent_b_to_main):
    queueA.put(msg)
    with lock:
        decoded_input = decode(parent_b_to_main.recv(), 'rot_13')
        if decoded_input == "stop":
            print("\nthis is the end of this program")
            return
        else:
            print(f"\nmsg {decoded_input} received at {time.ctime()}")

if __name__ == '__main__':
    queue_procA = multiprocessing.Queue()

    parent_a_to_b, child_a_to_b = multiprocessing.Pipe() # A to B processes Pipe
    parent_b_to_main, child_b_to_main = multiprocessing.Pipe() # B to main Pipe

    procA = multiprocessing.Process(target=procA, args=(queue_procA, child_a_to_b))
    procB = multiprocessing.Process(target=procB, args=(parent_a_to_b, child_b_to_main))
    procA.start()
    procB.start()
    msg_sendings = []

    while True:
        message = input("Enter message for process A (or 'stop' to quit): ")
        thread = Thread(target=thread_per_msg, args=(message, queue_procA, parent_b_to_main))
        thread.start()
        msg_sendings.append(thread)

        if message == 'stop':
            break

    procA.join()
    procB.join()
    for thread in msg_sendings:
        thread.join()
    

