import os
from rando_wisdom import get_advice
import time

class TailFile:
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
            return new_data.strip()
        else:
            return None

    def close(self):
        self.file.close()

class BadChatBot:
    def __init__(self, name, delay):
        self.name = name
        self.delay = delay

    def __next__(self):
        time.sleep(self.delay)
        return get_advice()["advice"]

    def close(self):
        pass

class GoodChatBot:
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
        return get_advice()["advice"]

    def close(self):
        pass

def main():
    chatters = []
    chatters.append(TailFile("greg.txt")) 
    chatters.append(TailFile("bill.txt"))
    # chatters.append(BadChatBot("nimrod", 5))
    chatters.append(GoodChatBot("gallant", 10))

    try:
        while True:
            for chatter in chatters:
                chat_text = next(chatter)
                if chat_text:
                    print(f"{chatter.name}: {chat_text}")

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        for chatter in chatters:
            chatter.close()

if __name__ == "__main__":
    main()
