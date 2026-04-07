from log_parser import LogParser
from Source_Code.log_analyzer import LogAnalyzer

def main():
    parser = LogParser("Samples/sample.log")
    entries = parser.parse()

    print(f"Total valid entries: {len(entries)}")
    print(f"Malformed lines: {len(parser.malformed_lines)}\n")

    analyzer = LogAnalyzer(entries)
    counts = analyzer.analyze()

    print("Log counts by type:")
    for level, count in counts.items():
        print(f"{level}: {count}")

    analyzer.save_to_json("Samples/log_summary.json")
    print("\nSummary saved to Samples/log_summary.json")

if __name__ == "__main__":
    main()