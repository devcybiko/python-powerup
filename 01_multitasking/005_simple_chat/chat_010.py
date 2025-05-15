import time

def tail_file(file_path):
    with open(file_path, 'r') as f:
        # Move to the end of the file
        f.seek(0, 2)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)  # Wait briefly before checking for new content
                continue
            print(line, end='')  # Already includes newline

if __name__ == "__main__":
    tail_file("greg.txt")  # Replace with your target file
