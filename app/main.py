import os
import sys
import termios
from pathlib import Path
from subprocess import run
from shlex import split
from contextlib import suppress
from functools import cache

blts = ["echo", "type", "exit", "pwd", "cd"]
paths = [Path(x) for x in os.getenv("PATH", "").split(":")]

@cache
def all_execs():
    execs = []
    for p in paths:
        with suppress(PermissionError):
            for f in p.glob("*"):
                if f.is_file():
                    execs.append(f.name)
    return sorted(execs)

def in_path(cmd):
    for p in paths:
        location = p / cmd
        if location.is_file():
            return location

def pop_redirect(cmd, ops, default):
    for op in ops:
        mode = "a" if op.endswith(">>") else "w"
        with suppress(ValueError):
            idx = cmd.index(op)
            cmd.pop(idx)
            return open(cmd.pop(idx), mode)
    return default

def readchar() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    term = termios.tcgetattr(fd)
    try:
        term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK | termios.BRKINT)
        termios.tcsetattr(fd, termios.TCSAFLUSH, term)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def writechar(ch):
    sys.stdout.write(ch)
    sys.stdout.flush()

def get_input():
    command = ""
    tab_count = 0
    while True:
        try:
            ch = readchar()
            ord_char = ord(ch)
            if ord_char == 10:
                writechar("\n")
                return command
            elif ord_char == 9:
                tab_count += 1
                matches, largest_match = complete(command)
                if not matches:
                    writechar("\a")
                    tab_count = 0
                elif len(matches) == 1:
                    m = matches[0]
                    for c in m[len(command):]:
                        writechar(c)
                    writechar(" ")
                    command = m + " "
                    tab_count = 0
                elif tab_count == 1:
                    if len(command) == len(largest_match):
                        writechar("\a")
                    else:
                        for c in largest_match[len(command):]:
                            writechar(c)
                        command = largest_match
                elif tab_count > 1:
                    matches = "  ".join(matches)
                    writechar(f"\n{matches}\n$ {command}")
            else:
                tab_count = 0
                writechar(ch)
                command += ch
        except KeyboardInterrupt:
            sys.exit(0)

def complete(cmd):
    m = set()
    for c in blts:
        if c.startswith(cmd):
            m.add(c)
    for c in all_execs():
        if c.startswith(cmd):
            m.add(c)
    if not m:
        return [], ""
    m = sorted(m)
    i = len(cmd)
    while True:
        try:
            c = m[0][i]
        except IndexError:
            break
        for x in m:
            if x[i] != c:
                break
        else:
            i += 1
            continue
        break
    return m, m[0][:i]

def main():
    while True:
        print("$", end=" ")
        sys.stdout.flush()
        command = get_input()
        cmd_parts = split(command)
        errfile = pop_redirect(cmd_parts, ["2>>", "2>"], sys.stderr)
        outfile = pop_redirect(cmd_parts, ["1>>", ">>", "1>", ">"], sys.stdout)
        
        match cmd_parts:
            case ["exit"]:
                sys.exit(0)
            case ["exit", code]:
                sys.exit(int(code))
            case ["echo", *msg]:
                outfile.write(" ".join(msg) + "\n")
            case ["pwd"]:
                outfile.write(str(Path().resolve()) + "\n")
            case ["cd", folder]:
                folder = Path(folder).expanduser()
                if folder.is_dir():
                    os.chdir(folder)
                else:
                    errfile.write(f"cd: {folder}: No such file or directory\n")
            case ["type", cmd]:
                if cmd in blts:
                    outfile.write(f"{cmd} is a shell builtin\n")
                elif location := in_path(cmd):
                    outfile.write(f"{cmd} is {location}\n")
                else:
                    errfile.write(f"{cmd}: not found\n")
            case cmd, *args:
                if location := in_path(cmd):
                    # Use the basename of the executable as argv[0]
                    result = run([str(location.name)] + args, stdout=outfile, stderr=errfile, text=True)
                else:
                    errfile.write(f"{cmd}: command not found\n")
        
        # Ensure the prompt is displayed after every command
        outfile.flush()
        errfile.flush()

if __name__ == "__main__":
    main()