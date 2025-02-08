import sys
import os
import subprocess
from typing import Optional



def main():
    # Uncomment this block to pass the first stage
    
    sys.stdout.write("$ ")
    sys.stdout.flush()


    # Wait for user input
    PATH=os.getenv("PATH").split(":")
    builtin_cmd=["echo","exit","type"]
    command= input().strip()
    args= command.strip()
    executable = args[0]
    
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
    else:
        args = command.split()
        executable = args[0]
        executable_path = None

        # Locate the executable in PATH
        for path in PATH:
            full_path = os.path.join(path, executable)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                executable_path = full_path
                break

        if executable_path:
            try:
                # Run the external command and pass arguments
                subprocess.run([executable_path, *args[1:]])
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"{executable}: command not found")

    main()
    

if __name__ == "__main__":
    main()
