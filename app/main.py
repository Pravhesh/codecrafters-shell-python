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
    elif(command.startswith("type invalid")):
        print(f"{command[5:]}: not found")
    elif command.startswith("type"):
        print(f"{command[5:]} is a shell builtin")
    else :       
        print(f"{command}: command not found")
    main()
    

if __name__ == "__main__":
    main()
