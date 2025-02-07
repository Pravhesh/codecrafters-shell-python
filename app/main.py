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
    else :       
        print(f"{command}: command not found")
    main()
    

if __name__ == "__main__":
    main()
