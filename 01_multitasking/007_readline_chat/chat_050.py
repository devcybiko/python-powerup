from rando_wisdom import get_advice
import time

###
### simple chat program, with tasks
### and "wisdom bot"
###

def tail_file(file_path):
    """Read the entire file and return the last line only if it ends with a newline."""
    with open(file_path, 'r') as f:
        original_content = f.read()  # Read the entire file into a string

        while True:
            f.seek(0)  # Go back to the beginning of the file
            new_content = f.read()  # Read the entire file again

            # If the file hasn't changed, continue
            if len(original_content) == len(new_content):
                yield None
                continue

            # If the file has changed but doesn't end with a newline, continue
            if not new_content.endswith("\n"):
                yield None
                continue

            # Update the original content and return the last line
            original_content = new_content
            lines = new_content.splitlines()  # Split the content into lines
            yield lines[-1]  # Return the last line

class TaskManager:
    def __init__(self):
        self.tasks = []

    def register(self, task):
        self.tasks.append(task)
    
    def run(self):
        while len(self.tasks):
            for task in self.tasks:
                task.__await__()

class Task:
    def __init__(self, generator):
        self.generator = generator
    
    def __await__(self):
        return next(self.generator)

class ChatTask(Task):
    def __init__(self, generator, name):
        super().__init__(generator)
        self.name = name
    
    def __await__(self):
        text = next(self.generator)
        if (text): print(f"{self.name}: {text}")

class WisdomBot(ChatTask):
    def __init__(self, delay, name):
        super().__init__(self.wisdom_generator(delay), name)

    def wisdom_generator(self, delay):
        last_time = 0 # immediate printout
        while True:
            if last_time + delay <= int(time.time()):
                last_time = int(time.time()) # time in seconds
                yield get_advice()["advice"]
            else:
                yield None

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.register(ChatTask(tail_file("greg.txt"), "greg"))
    task_manager.register(ChatTask(tail_file("bill.txt"), "bill"))
    task_manager.register(WisdomBot(5, "obi wan"))
    task_manager.run()