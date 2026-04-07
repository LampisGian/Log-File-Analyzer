from log_parser import LogParser
from log_analyzer import LogAnalyzer


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

    keyword = input("Enter keyword (press Enter to skip): ").strip()
    start_date = input("Enter start date YYYY-MM-DD (press Enter to skip): ").strip()
    end_date = input("Enter end date YYYY-MM-DD (press Enter to skip): ").strip()

    results = analyzer.search(
        keyword=keyword if keyword else None,
        start_date=start_date if start_date else None,
        end_date=end_date if end_date else None
    )

    print("\nFiltered results:")
    if results:
        for entry in results:
            print(entry)
    else:
        print("No matching log entries found.")


if __name__ == "__main__":
    main()