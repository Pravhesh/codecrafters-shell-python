import sys


def main():
    # Uncomment this block to pass the first stage
    command = input
    print(f"{command}: command not found")
    sys.stdout.write("$ ")

    # Wait for user input
    input()


if __name__ == "__main__":
    main()
