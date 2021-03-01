from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, print


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.N:
            self.cnt = 0
            for _ in range(self.N):
                self.turnstile.signal()
        self.mutex.unlock()
        self.turnstile.wait()


def simple_barrier(barrier, thread_id):
    sleep(randint(1, 10) / 10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)


sb = SimpleBarrier(5)
threads = list()

for i in range(10):
    t = Thread(simple_barrier, sb, i)
    threads.append(t)

for t in threads:
    t.join()

