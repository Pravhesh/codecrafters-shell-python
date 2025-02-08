import sys
import os
import subprocess
from typing import Optional



def main():
    # Uncomment this block to pass the first stage
    
    sys.stdout.write("$ ")

    # Wait for user input
    PATH=os.getenv("PATH").split(":")
    builtin_cmd=["echo","exit","type"]
    command= input().split(" ")
    
    if command[0]==("echo"):
        print(command[5:])
    if os.path.isfile(command[0]):
                    os.system(command)
    elif(command=="exit 0"):
            sys.exit()    
    elif command[0]==("type"):
        cmd_path=None
        for path in PATH :
            if os.path.isfile(f"{path}/{command[5:]}"):
                    cmd_path=f"{command[5:]} is {path}/{command[5:]}"
        if command[5:] in builtin_cmd:
            print(f"{command[5:]} is a shell builtin")
        elif cmd_path:
            print(cmd_path)
        elif(command[0]==("type invalid")):
            print(f"{command[5:]}: not found")
    else :       
        print(f"{command}: command not found")
    main()
    

if __name__ == "__main__":
    main()
