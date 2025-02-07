import sys
import os

def main():
    # Uncomment this block to pass the first stage
    
    sys.stdout.write("$ ")

    # Wait for user input
    PATH=os.getenv("PATH").split(":")
    builtin_cmd=["echo","exit","type"]
    command = input()
    if command.startswith("echo"):
        print(command[5:])
    elif(command=="exit 0"):
            sys.exit()    
    elif command.startswith("type"):
        cmd_path=None
        for path in PATH :
            if os.path.isfile(f"{path}/{command[5:]}"):
                    cmd_path=f"{command[5:]} is {path}/{command[5:]}"
        if command[5:] in builtin_cmd:
            print(f"{command[5:]} is a shell builtin")
        elif cmd_path:
            print(cmd_path)
        elif(command.startswith("type invalid")):
            print(f"{command[5:]}: not found")
    else :       
        print(f"{command}: command not found")
    main()
    

if __name__ == "__main__":
    main()
