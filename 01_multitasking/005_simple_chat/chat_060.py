import os
from rando_wisdom import get_advice
import time
from abc import ABC, abstractmethod
import asyncio

class Coroutine(ABC):
    def __init__(self):
        pass

    def __next__(self):
        pass

    def close(self):
        pass

class TailFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path, 'r')
        self.position = os.path.getsize(file_path)  # Start at end of file
        self.file.seek(self.position)
        self.name = self.file_path.split(".")[0]

    async def run(self):
        while True:
            self.file.seek(self.position)
            new_data = self.file.read()

            if new_data:
                self.position = self.file.tell()
                print(self.name, new_data.strip())
            else:
                # Yield control back to the event loop when no new data is available
                await asyncio.sleep(0.1)  # Small delay to avoid busy-waiting

    def close(self):
        self.file.close()

class GoodChatBot:
    def __init__(self, name, delay):
        self.name = name
        self.delay = delay  # Delay in seconds

    async def run(self):
        while True:
            await asyncio.sleep(self.delay)  # Wait for the specified delay
            print(self.name, get_advice()["advice"])

    def close(self):
        pass

async def main():
    bot = GoodChatBot("gallant", 10)
    greg = TailFile("greg.txt")
    bill = TailFile("bill.txt")

    try:
        await asyncio.gather(
            bot.run(),
            greg.run(),
            bill.run()
        )
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        bot.close()
        greg.close()
        bill.close()

if __name__ == "__main__":
    asyncio.run(main())