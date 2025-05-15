from rando_wisdom import get_advice
import time
import asyncio

###
### simple chat program, with async/await
### finally - we create them as tasks and they run forever
###

async def tail_file(file_path):
    """Read the entire file and return the last line only if it ends with a newline."""
    with open(file_path, 'r') as f:
        original_content = f.read()  # Read the entire file into a string

        while True:
            f.seek(0)  # Go back to the beginning of the file
            new_content = f.read()  # Read the entire file again

            # If the file hasn't changed, continue
            if len(original_content) == len(new_content):
                await asyncio.sleep(0)  # context switch
                continue

            # If the file has changed but doesn't end with a newline, continue
            if not new_content.endswith("\n"):
                await asyncio.sleep(0)  # context switch
                continue

            # Update the original content and return the last line
            original_content = new_content
            lines = new_content.splitlines()  # Split the content into lines
            return lines[-1]  # Return the last line

async def good_wisdom_generator(delay, name):
    while True:
        text = get_advice()["advice"]
        print(f"{name}: {text}")
        await asyncio.sleep(delay) # the right way to behave - cooperation is the best

async def bad_wisdom_generator(delay, name):
    while True:
        text = get_advice()["advice"]
        print(f"{name}: {text}")
        time.sleep(delay) # gonna have a bad time - you're not cooperating
        await asyncio.sleep(0) # context switch

async def chat_task(file_path, name):
    while True:
        text = await tail_file(file_path)
        if text: print(f"{name}: {text}")
        await asyncio.sleep(0) # context switch

async def main():
    asyncio.create_task(chat_task("greg.txt", "greg"))
    asyncio.create_task(chat_task("bill.txt", "bill"))
    asyncio.create_task(good_wisdom_generator(10, "...obi wan"))

    try:
        while True:
            await asyncio.sleep(0) # context switch - to rnn the tasks
    except:
        print("exiting...")

if __name__ == "__main__":
    asyncio.run(main())