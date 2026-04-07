from log_parser import LogParser


def main():
    parser = LogParser("Samples/sample.log")
    entries = parser.parse()

    print("Valid log entries:")
    for entry in entries:
        print(entry)

    print("\nMalformed lines:")
    for line in parser.malformed_lines:
        print(line)


if __name__ == "__main__":
    main()