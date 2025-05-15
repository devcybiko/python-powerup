import os

class TailFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path, 'r')
        self.position = os.path.getsize(file_path)  # Start at end of file
        self.file.seek(self.position)

    def __next__(self):
        self.file.seek(self.position)
        new_data = self.file.read()

        if new_data:
            self.position = self.file.tell()
            return new_data
        else:
            return None

    def close(self):
        self.file.close()

import time

def main():
    greg = TailFile("greg.txt")  
    bill = TailFile("bill.txt")

    try:
        while True:
            greg_says = next(greg)
            bill_says = next(bill)
            if greg_says:
                print(f"greg: {greg_says}\n", end='')
            if bill_says:
                print(f"bill: {bill_says}\n", end='')
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        greg.close()
        bill.close()

if __name__ == "__main__":
    main()
