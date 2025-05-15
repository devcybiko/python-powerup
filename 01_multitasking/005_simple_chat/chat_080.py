import os
import asyncio
from rando_wisdom import get_advice

async def tail_file(file_path, position):
    """Coroutine to monitor a file for new content."""
    if position == None:
        position = os.path.getsize(file_path)  # Start at the end of the file
    name = file_path.split(".")[0]

    with open(file_path, 'r') as file:
        file.seek(position)
        new_data = file.read()

        if new_data:
            position = file.tell()
            print(name, new_data.strip())
        return position

async def good_chat_bot(name, delay):
    """Coroutine to periodically print advice."""
    print(name, get_advice()["advice"])
    await asyncio.sleep(delay)  # Wait for the specified delay

async def main():
    """Main coroutine to run all tasks."""
    greg_posn = None
    bill_posn = None
    try:
        while True:
            await good_chat_bot("gallant", 10)  # Run GoodChatBot with a 10-second delay
            greg_posn = await tail_file("greg.txt", greg_posn)         # Monitor greg.txt
            bill_posn = await tail_file("bill.txt", bill_posn)          # Monitor bill.txt
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    asyncio.run(main())