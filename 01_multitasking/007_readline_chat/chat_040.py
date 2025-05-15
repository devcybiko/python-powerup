###
### simple chat program, with tasks
### now tail_file() is a generator (uses "yield")
### so it's more "asynchronous"
### and we add classes for a TaskManager, Task, and ChatTask

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

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.register(ChatTask(tail_file("greg.txt"), "greg"))
    task_manager.register(ChatTask(tail_file("bill.txt"), "bill"))
    task_manager.run()