from fei.ppds import Thread

"""
1) Aký je najmenší počet synchronizačných objektov (semafory, mutexy, udalosti) potrebných na riešenie tejto úlohy?
- Po preskúšaniu rôznych možnosti som našiel spôsob, pri ktorom vôbec nepotrebujeme synchronizačne objekty, čiže 0.
2) Ktoré z prebratých synchronizačných vzorov (vzájomné vylúčenie, signalizácia, rendezvous, bariéra) 
sa dajú (rozumne) využiť pri riešení tejto úlohy?
- Pre riešenie danej úlohy rozumne je vôbec nepoužívať ani synchronizačne objekty ani viacvláknový výpočet pretože v
úlohách kde ďalší výpočet potrebuje výsledok predchádzajúceho výpočtu multithreading stráca význam.
"""


class SharedObject:
    """
    Dany objekt obsahuje premennu fibonacci_size ktorá symbolizuje počet prvkov fibonacci + 2
    fib_seq je pole do ktoreho vkladame vypočitane prvky fibonacci postupnosti.
    """
    def __init__(self, fibonacci_size):
        self.fibonacci_seq_size = fibonacci_size
        self.fib_seq = [0, 1] + [0] * fibonacci_size


def count_fibonacci_sequence(shared_stuff, thread_id):
    """
    Aby sme umožnili viac vláknam prístup k výpočtu danej funkcie bez synchronizácie
    musíme ju volať pre každý prvok fibonacci postupnosti.
    """
    shared_stuff.fib_seq[thread_id + 2] = shared_stuff.fib_seq[thread_id] + shared_stuff.fib_seq[thread_id + 1]
    thread_id += 2


if __name__ == '__main__':
    threads = list()
    number_of_threads = 10
    fibonacci_seq_size = 25
    shared_stuff = SharedObject(fibonacci_seq_size)
    for i in range(fibonacci_seq_size):
        for j in range(number_of_threads):
            t = Thread(count_fibonacci_sequence, shared_stuff, i)
            threads.append(t)

        for t in threads:
            t.join()

    print(shared_stuff.fib_seq)
