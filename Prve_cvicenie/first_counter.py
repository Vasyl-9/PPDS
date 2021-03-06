"""
The first multi-threading solution using a Mutex object
The first solution is to block two threads from using the function
at the same time.
Not the most effective option, but it works.
"""
from fei.ppds import Thread, Mutex
from time import time


class Shared:
    """
    Creating object that will be shared between threads
    """

    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end


def counter(shared, mutex):
    """
    Function which fills 1 array with 2 threads
    """
    # In the beginning of function close it for changes of another
    # thread.
    mutex.lock()
    while True:
        if shared.counter >= shared.end:
            break
        shared.array[shared.counter] += 1
        shared.counter += 1
    mutex.unlock()
    # At the end we unlock access to function


class Histogram(dict):
    """
    Additional class for tracking the state of the array values.
    """
    def __init__(self, seq=[]):
        super().__init__()
        for item in seq:
            self[item] = self.get(item, 0) + 1


def current_milli_time():
    return round(time() * 1000)


# Start time of the function to calculate running time
start_time = current_milli_time()

# Creating a locking object
mutex = Mutex()

"""
In the loop, we start filling millionth array with 2 threads and display 
state of the array.
"""
for i in range(10):
    shared = Shared(1_000_000)
    t1 = Thread(counter, shared, mutex)
    t2 = Thread(counter, shared, mutex)
    t1.join()
    t2.join()
    print(Histogram(shared.array))

# Calculation of program runtime
end_time = (current_milli_time() - start_time)
print("\nProgram runtime: %s ms", end_time)
