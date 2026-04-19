import threading
import time

class ReadWriteLock:
    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0

    def acquire_read(self):
        self._read_ready.acquire()
        try:
            while self._readers < 0:
                self._read_ready.wait()
            self._readers += 1
        finally:
            self._read_ready.release()

    def release_read(self):
        self._read_ready.acquire()
        try:
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()
        finally:
            self._read_ready.release()

    def acquire_write(self):
        self._read_ready.acquire()
        self._readers = -1
        self._read_ready.release()

    def release_write(self):
        self._read_ready.acquire()
        try:
            self._readers = 0
            self._read_ready.notify_all()
        finally:
            self._read_ready.release()


def reader(lock, name):
    lock.acquire_read()
    print(f"{name} started reading")
    time.sleep(2)
    print(f"{name} finished reading")
    lock.release_read()


def writer(lock, name):
    lock.acquire_write()
    print(f"{name} started writing")
    time.sleep(2)
    print(f"{name} finished writing")
    lock.release_write()


lock = ReadWriteLock()

for i in range(3):
    threading.Thread(target=reader, args=(lock, f"Reader {i}")).start()

for i in range(2):
    threading.Thread(target=writer, args=(lock, f"Writer {i}")).start()

for i in range(3, 6):
    threading.Thread(target=reader, args=(lock, f"Reader {i}")).start()

time.sleep(10)