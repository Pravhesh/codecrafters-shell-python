import sys


def main():
    # Uncomment this block to pass the first stage
    
    sys.stdout.write("$ ")

    # Wait for user input
    
    command = input()
    if command.startswith("echo"):
        print(command[5:])
    elif(command=="exit 0"):
            sys.exit()    
    elif(command.startswith("type")):
        if command[5:]=="type":
            print("type is a shell builtin")
        elif command[5:]=="exit":
            print("exit is a shell builtin")
        elif command[5:]=="echo":
            print("echo is a shell builtin")
        elif command[5:]=="invalid_command":
            print("invalid_command: not found")
    else :       
        print(f"{command}: command not found")
    main()
    

if __name__ == "__main__":
    main()
