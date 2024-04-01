import sys

def tail(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        last_lines = lines[-10:]
        return last_lines

if __name__ == "__main__":
    if len(sys.argv) > 2:
        for file in sys.argv[1:]:
            print(f"==> {file} <==")
            for line in tail(file):
                print(line, end='')
    elif len(sys.argv) == 2:
        for line in tail(sys.argv[1]):
            print(line, end='')
    else:
        lines = sys.stdin.readlines()
        last_lines = lines[-17:]
        for line in last_lines:
            print(line, end='')
    print('\n') # looks nicer this way