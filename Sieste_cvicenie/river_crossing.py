from random import randint
from time import sleep
from fei.ppds import Semaphore, print, Thread, Mutex


class Barrier:
    def __init__(self, count):
        self.N = count
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


class Shared(object):
    def __init__(self):
        self.hackers = 0
        self.serfs = 0
        self.hackers_q = Semaphore(0)
        self.serfs_q = Semaphore(0)
        self.mutex = Mutex()
        self.barrier = Barrier(4)


def board(passenger, thread_id):
    print("%s #%s nastupil na lod." % (passenger, thread_id))
    sleep(0.2 + randint(0, 3) / 10)


def row_boat(captain, thread_id):
    print("---------------------------------------------------")
    print("%s #%s, riadi prepravu lode." % (captain, thread_id))
    print("---------------------------------------------------")
    sleep(0.5 + randint(0, 3) / 10)


def hacker_joins_the_board(thread_id, shared):
    while True:
        is_captain = False
        shared.mutex.lock()
        shared.hackers += 1
        if shared.hackers == 4:
            is_captain = True
            shared.hackers = 0
            shared.hackers_q.signal(4)
        elif shared.hackers == 2 and shared.serfs >= 2:
            is_captain = True
            shared.hackers = 0
            shared.hackers_q.signal(2)
            shared.serfs -= 2
            shared.serfs_q.signal(2)
        else:
            shared.mutex.unlock()

        shared.hackers_q.wait()

        board("Hacker", thread_id)
        shared.barrier.wait()

        if is_captain:
            row_boat("Hacker", thread_id)
            print("Koniec prepravy lode.")
            print("---------------------------------------------------")
            print("---------------------------------------------------")
            shared.mutex.unlock()


def serfs_joins_the_board(thread_id, shared):
    while True:
        is_captain = False
        shared.mutex.lock()
        shared.serfs += 1
        if shared.serfs == 4:
            is_captain = True
            shared.serfs = 0
            shared.serfs_q.signal(4)
        elif shared.serfs == 2 and shared.hackers >= 2:
            is_captain = True
            shared.serfs = 0
            shared.serfs_q.signal(2)
            shared.hackers -= 2
            shared.hackers_q.signal(2)
        else:
            shared.mutex.unlock()

        shared.serfs_q.wait()

        board("Serfs", thread_id)
        shared.barrier.wait()

        if is_captain:
            row_boat("Serfs", thread_id)
            print("Koniec prepravy lode.")
            print("---------------------------------------------------")
            print("---------------------------------------------------")
            shared.mutex.unlock()


def init():
    threads = list()
    shared = Shared()
    for i in range(0, 10):
        threads.append(Thread(hacker_joins_the_board, i, shared))
        threads.append(Thread(serfs_joins_the_board, i, shared))

    for t in threads:
        t.join()


if __name__ == "__main__":
    init()
