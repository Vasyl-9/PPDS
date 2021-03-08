import matplotlib.pyplot as plt
from fei.ppds import Mutex, Semaphore, randint, Thread
from time import sleep


class Lightswitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0
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


def statistics(thread_id):
    if threadCount.get(thread_id):
        threadCount[thread_id] += 1
    else:
        threadCount[thread_id] = 1


def reading(thread_id):
    statistics(thread_id)
    print(f"Vlakno {thread_id} zacalo citat")
    sleep(randint(0, 10) / 10)
    print(f"Vlakno {thread_id} ukoncilo citanie")
    print("------------------------------------")


def writing(thread_id):
    statistics(thread_id)
    print(f"Vlakno {thread_id} zacalo zapisovat")
    sleep(randint(0, 10) / 10)
    print(f"Vlakno {thread_id} ukoncilo zapisovanie")
    print("------------------------------------")


def light_switch_for_readers(light_switch, empty_room, reader_id):
    for _ in range(count_reading):
        light_switch.turnstile.wait()
        light_switch.turnstile.signal()
        light_switch.lock(empty_room)
        reading(reader_id)
        light_switch.unlock(empty_room)


def light_switch_for_writers(light_switch, empty_room, writer_id):
    for _ in range(count_writing):
        light_switch.turnstile.wait()
        empty_room.wait()
        writing(writer_id)
        empty_room.signal()
        light_switch.turnstile.signal()
        sleep(0)


def plotly(x, y, x1, y1):
    plt.bar(x, y, color="#1e8a2e")
    plt.bar(x1, y1, color="#0b2073")
    plt.xlabel('Thread ID (Green are read threads, '
               'Blue are write threads)')
    plt.ylabel('Count of executions by the thread')
    plt.title('Graph')
    plt.show()


def create_and_draw_graph(thread_count):
    x, y, x1, y1 = list(), list(), list(), list()
    for thread_id, count_of_executions_thread in thread_count.items():
        if thread_id < count_reading:
            x.append(thread_id)
            y.append(count_of_executions_thread)
        else:
            x1.append(thread_id)
            y1.append(count_of_executions_thread)

    plotly(x, y, x1, y1)


if __name__ == '__main__':
    light_switch = Lightswitch()
    empty_room = Semaphore(1)
    threads = list()
    threadCount = dict()
    count_reading = 50
    count_writing = 50
    for i in range(count_reading):
        threads.append(Thread(light_switch_for_readers,
                              light_switch, empty_room, i))
    for i in range(count_writing):
        threads.append(Thread(light_switch_for_writers, light_switch,
                              empty_room, i + count_reading))

    for t in threads:
        t.join()

    create_and_draw_graph(threadCount)
