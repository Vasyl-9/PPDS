from fei.ppds import Mutex, Semaphore


class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(1)

    def lock(self, room_empty):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            room_empty.wait()
        self.mutex.unlock()

    def unlock(self, room_empty):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            room_empty.signal()
        self.mutex.unlock()