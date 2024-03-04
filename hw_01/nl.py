from sys import argv, stdin

def read_from_file(filename: str):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

if __name__ == '__main__':
    cmd_args = argv[1:]
    assert len(cmd_args) <= 1, f'0 or 1 filename expected'

    if len(cmd_args) == 1:
        filename = cmd_args[0] 
    else:
        filename = None

    if filename != None:
        data = read_from_file(filename)
    else:
        data = stdin

    for index, line in enumerate(data):
        print(f'{index + 1}  {line}', end="")
    print('\n')  # it looks nicer in my console with line break
