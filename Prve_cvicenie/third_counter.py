# This is the third option using the local variable temp
# but local testing has shown that this is the slowest option.
from time import time
from fei.ppds import Thread, Mutex


class Shared:
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end


# With the blocked local variable temp, which stores the current index value in the array,
# we fill the array with only 1 thread at a time, which writes its value into this variable.
def counter(shared, mutex):
    while True:
        mutex.lock()
        temp = shared.counter
        shared.counter += 1
        mutex.unlock()
        if temp >= shared.end:
            break
        shared.array[temp] += 1


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
