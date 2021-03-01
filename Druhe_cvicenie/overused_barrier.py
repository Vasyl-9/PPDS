from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, print


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(1)

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:
            self.turnstile2.wait()
            self.turnstile1.signal()
        self.mutex.unlock()
        self.turnstile1.wait()
        self.turnstile1.signal()

        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            self.turnstile1.wait()
            self.turnstile2.signal()
        self.mutex.unlock()
        self.turnstile2.wait()
        self.turnstile2.signal()


def rendezvous(thread_name):
    sleep(randint(1, 10) / 10)
    print("vlakno {%d} pred barierou" % thread_name)


def ko(thread_name):
    print("vlakno {%d} po bariere" % thread_name)
    sleep(randint(1, 10) / 10)


def overused_barrier(barrier, thread_name):
    while True:
        rendezvous(thread_name)
        barrier.wait()
        ko(thread_name)


threads = list()
sb = SimpleBarrier(5)
for i in range(5):
    thread = Thread(overused_barrier, sb, i)
    threads.append(thread)

for t in threads:
    t.join()
