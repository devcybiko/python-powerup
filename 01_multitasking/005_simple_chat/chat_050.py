import os
from rando_wisdom import get_advice
import time
from abc import ABC, abstractmethod

class Coroutine(ABC):
    def __init__(self):
        pass

    def __next__(self):
        pass

    def close(self):
        pass

class TailFile(Coroutine):
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path, 'r')
        self.position = os.path.getsize(file_path)  # Start at end of file
        self.file.seek(self.position)
        self.name = self.file_path.split(".")[0]

    def __next__(self):
        self.file.seek(self.position)
        new_data = self.file.read()

        if new_data:
            self.position = self.file.tell()
            print(self.name, new_data.strip())

    def close(self):
        self.file.close()

class GoodChatBot(Coroutine):
    def __init__(self, name, delay):
        self.name = name
        self.delay = delay * 1000
        self.last_time = self._now_ms()

    def _now_ms(self):
        return int(time.time() * 1000)

    def __next__(self):
        if self.last_time + self.delay > self._now_ms():
            return None
        self.last_time = self._now_ms()
        print(self.name, get_advice()["advice"])

    def close(self):
        pass

class EventLoop:
    def __init__(self):
        self.tasks = []
        pass

    def register(self, coro: Coroutine):
        self.tasks.append(coro)

    def run(self):
        try:
            while True:
                for task in self.tasks:
                    next(task)
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            for task in self.tasks:
                task.close()

def main():
    event_loop = EventLoop()
    event_loop.register(TailFile("greg.txt")) 
    event_loop.register(TailFile("bill.txt"))
    event_loop.register(GoodChatBot("gallant", 10))
    event_loop.run()

if __name__ == "__main__":
    main()
