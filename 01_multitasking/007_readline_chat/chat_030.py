###
### simple chat program, async
### now tail_file() is a generator (uses "yield")
### so it's more "asynchronous"
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

if __name__ == "__main__":
    greg_chat = tail_file("greg.txt")
    bill_chat = tail_file("bill.txt")
    while True:
        greg_says = next(greg_chat)
        if greg_says: print(f"greg: {greg_says}")
        bill_says = next(bill_chat)
        if bill_says: print(f"bill: {bill_says}")
