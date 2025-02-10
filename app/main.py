import sys
import os
import shlex
import subprocess

def main():
    PATH = os.getenv("PATH").split(":")
    builtin_cmds = ["echo", "exit", "type", "pwd", "cd"]

    while True:
        # Restore stdout before printing the prompt
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input().strip()
        if not command:
            continue

        parts = shlex.split(command)

        # Check for output redirection (>)
        redirect = False
        output_file = None
        if ">" in parts or "1>" in parts:
            try:
                redir_index = parts.index(">") if ">" in parts else parts.index("1>")
                output_file = parts[redir_index + 1]
                parts = parts[:redir_index]  # Remove redirection part from command
                redirect = True
            except IndexError:
                print("Syntax error: No output file specified")
                continue

        command = parts[0]  # Extract the actual command

        # Handle built-in commands
        if command == "echo":
            output = " ".join(parts[1:])
        
        elif command == "exit" and len(parts) == 2 and parts[1] == "0":
            sys.exit()
        
        elif command == "type":
            cmd_name = parts[1] if len(parts) > 1 else ""
            if cmd_name in builtin_cmds:
                output = f"{cmd_name} is a shell builtin"
            else:
                cmd_path = None
                for path in PATH:
                    full_path = os.path.join(path, cmd_name)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        cmd_path = full_path
                        break
                output = f"{cmd_name} is {cmd_path}" if cmd_path else f"{cmd_name}: not found"
        
        elif command == "pwd":
            output = os.getcwd()
        
        elif command == "cd":
            try:
                target_dir = parts[1] if len(parts) > 1 else os.path.expanduser("~")
                os.chdir(target_dir)
                output = ""  # No output for successful `cd`
            except FileNotFoundError:
                output = f"{parts[1]}: No such file or directory"
            except IndexError:
                output = "cd: missing operand"
        
        else:
            # Handle external commands correctly
            executable_path = None
            for path in PATH:
                full_path = os.path.join(path, command)
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    executable_path = full_path
                    break

            if executable_path:
                try:
                    # Redirect output properly
                    with open(output_file, "w") if redirect else sys.stdout as f:
                        subprocess.run(parts, stdout=f, stderr=sys.stderr)
                    continue  # Skip printing output manually
                except Exception as e:
                    output = f"Error: {e}"
            else:
                output = f"{command}: command not found"

        # Handle output redirection
        if redirect and output_file:
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)  # Create directory if it doesn't exist

            with open(output_file, "w") as f:
                f.write(output + "\n")
        
        else:
            print(output)

if __name__ == "__main__":
    main()
