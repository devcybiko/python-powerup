###
### simple chat program, again
### showing how the chat alternates between users
### because the tail_file_blocking() blocks
###

def tail_file_blocking(file_path):
    """Read the entire file and return the last line only if it ends with a newline."""
    with open(file_path, 'r') as f:
        original_content = f.read()  # Read the entire file into a string

        while True:
            f.seek(0)  # Go back to the beginning of the file
            new_content = f.read()  # Read the entire file again

            # If the file hasn't changed, continue
            if len(original_content) == len(new_content):
                continue

            # If the file has changed but doesn't end with a newline, continue
            if not new_content.endswith("\n"):
                continue

            # Update the original content and return the last line
            original_content = new_content
            lines = new_content.splitlines()  # Split the content into lines
            return lines[-1]  # Return the last line

if __name__ == "__main__":
    while True:
        greg_says = tail_file_blocking("greg.txt")
        print(f"greg: {greg_says}")
        bill_says = tail_file_blocking("bill.txt")
        print(f"bill: {bill_says}")