import sys

def count_lines_words_bytes(filename):
    lines = 0
    words = 0
    bytes_count = 0
    with open(filename, 'r') as file:
        for line in file:
            lines += 1
            words += len(line.split())
            bytes_count += len(line.encode('utf-8'))
    return lines, words, bytes_count

def print_stats(filename, lines, words, bytes_count):
    print(f"{lines} {words} {bytes_count} {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        content = sys.stdin.read()
        lines = content.count('\n')
        words = len(content.split())
        bytes_count = len(content.encode('utf-8'))
        print_stats(lines, words, bytes_count)
    else:
        total_lines = 0
        total_words = 0
        total_bytes = 0
        for filename in sys.argv[1:]:
            lines, words, bytes_count = count_lines_words_bytes(filename)
            print_stats(filename, lines, words, bytes_count)
            total_lines += lines
            total_words += words
            total_bytes += bytes_count
        if len(sys.argv) > 2:
            print_stats(total_lines, total_words, total_bytes)

