import threading
import time

class ReadWriteLock:
    def __init__(self):
        self._read_ready = threading.Condition(threading.RLock())
        self._readers = 0
        self._writers = 0

    def acquire_read(self):
        self._read_ready.acquire()
        try:
            while self._writers > 0:
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
        try:
            while self._readers > 0 or self._writers > 0:
                self._read_ready.wait()
            self._writers += 1
        finally:
            self._read_ready.release()

    def release_write(self):
        self._read_ready.acquire()
        try:
            self._writers -= 1
            self._read_ready.notify_all()
        finally:
            self._read_ready.release()

def reader(lock, name):
    print(f"{name} waiting to read")
    lock.acquire_read()
    try:
        print(f"{name} is reading")
        time.sleep(2)
    finally:
        lock.release_read()
    print(f"{name} finished reading")

def writer(lock, name):
    print(f"{name} waiting to write")
    lock.acquire_write()
    try:
        print(f"{name} is writing")
        time.sleep(2)
    finally:
        lock.release_write()
    print(f"{name} finished writing")

lock = ReadWriteLock()
threads = []

for i in range(3):
    t = threading.Thread(target=reader, args=(lock, f"Reader {i+1}"))
    threads.append(t)
    t.start()

for i in range(2):
    t = threading.Thread(target=writer, args=(lock, f"Writer {i+1}"))
    threads.append(t)
    t.start()

for t in threads:
    t.join()