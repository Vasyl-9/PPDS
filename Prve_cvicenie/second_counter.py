"""
The second way of filling array with 2 threads. During local
testing this variant was the fastest.
A detailed description of the program is in the first version.
"""
from time import time
from fei.ppds import Thread, Mutex


class Shared:
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end


def counter(shared, mutex):
    """
    In this case, we are blocking only filling each element of the
    array. This is the fastest way to lock because the array is filled
    with two threads, but they do not conflict with each other because
    each thread fills the other element.
    """
    while True:
        mutex.lock()
        if shared.counter >= shared.end:
            mutex.unlock()
            break
        shared.array[shared.counter] += 1
        shared.counter += 1
        mutex.unlock()


class Histogram(dict):
    def __init__(self, seq=[]):
        super().__init__()
        for item in seq:
            self[item] = self.get(item, 0) + 1


def current_milli_time():
    return round(time() * 1000)


start_time = current_milli_time()
mutex = Mutex()

for i in range(10):
    shared = Shared(1_000_000)
    t1 = Thread(counter, shared, mutex)
    t2 = Thread(counter, shared, mutex)
    t1.join()
    t2.join()
    print(Histogram(shared.array))

end_time = (current_milli_time() - start_time)
print("\nProgram runtime: %s ms", end_time)
