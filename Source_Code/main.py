from log_parser import LogParser
from log_analyzer import LogAnalyzer


def main():
    parser = LogParser("Samples/sample.log")
    entries = parser.parse()

    print(f"Total valid entries: {len(entries)}")
    print(f"Malformed lines: {len(parser.malformed_lines)}\n")

    analyzer = LogAnalyzer(entries, len(parser.malformed_lines))
    counts = analyzer.analyze()

    print("Log counts by type:")
    for level, count in counts.items():
        print(f"{level}: {count}")

    keyword = input("Enter keyword (press Enter to skip): ").strip()
    start_date = input("Enter start date YYYY-MM-DD (press Enter to skip): ").strip()
    end_date = input("Enter end date YYYY-MM-DD (press Enter to skip): ").strip()

    results = analyzer.search(
        keyword=keyword if keyword else None,
        start_date=start_date if start_date else None,
        end_date=end_date if end_date else None
    )

    print("\nSearch / Filter Results:")
    if results:
        for entry in results:
            print(entry)
    else:
        print("No matching log entries found.")

    report = analyzer.generate_report_data()

    print("\nSummary Report:")
    print(f"Total entries: {report['total_entries']}")
    print(f"Malformed lines: {report['malformed_lines']}")
    print(f"First log: {report['first_log']}")
    print(f"Last log: {report['last_log']}")
    print("Common errors:")

    if report["common_errors"]:
        for message, count in report["common_errors"].items():
            print(f"- {message}: {count}")
    else:
        print("No error logs found.")

    analyzer.save_report_to_json("Samples/log_report.json")
    print("\nReport saved to Samples/log_report.json")


if __name__ == "__main__":
    main()