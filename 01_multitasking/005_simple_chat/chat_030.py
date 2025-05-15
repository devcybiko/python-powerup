import os

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

import time

def main():
    chatters = []
    chatters.append(TailFile("greg.txt")) 
    chatters.append(TailFile("bill.txt"))

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
