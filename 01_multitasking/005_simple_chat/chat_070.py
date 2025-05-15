import os
import asyncio
from rando_wisdom import get_advice

async def tail_file(file_path):
    """Coroutine to monitor a file for new content."""
    position = os.path.getsize(file_path)  # Start at the end of the file
    name = file_path.split(".")[0]

    with open(file_path, 'r') as file:
        file.seek(position)
        while True:
            file.seek(position)
            new_data = file.read()

            if new_data:
                position = file.tell()
                print(name, new_data.strip())
            else:
                # Yield control back to the event loop when no new data is available
                await asyncio.sleep(0.1)

async def good_chat_bot(name, delay):
    """Coroutine to periodically print advice."""
    while True:
        await asyncio.sleep(delay)  # Wait for the specified delay
        print(name, get_advice()["advice"])

async def main():
    """Main coroutine to run all tasks."""
    try:
        await asyncio.gather(
            good_chat_bot("gallant", 10),  # Run GoodChatBot with a 10-second delay
            tail_file("greg.txt"),         # Monitor greg.txt
            tail_file("bill.txt")          # Monitor bill.txt
        )
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    asyncio.run(main())