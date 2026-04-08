import os
import argparse
from log_parser import LogParser
from log_analyzer import LogAnalyzer


def main():
    arg_parser = argparse.ArgumentParser(description="Log File Analyzer")

    arg_parser.add_argument("--file", required=True, help="Path to the log file")
    arg_parser.add_argument("--keyword", default=None, help="Keyword to search in log messages")
    arg_parser.add_argument("--start-date", dest="start_date", default=None, help="Start date in YYYY-MM-DD format")
    arg_parser.add_argument("--end-date", dest="end_date", default=None, help="End date in YYYY-MM-DD format")

    args = arg_parser.parse_args()

    os.makedirs("Samples", exist_ok=True)

    parser = LogParser(args.file)
    entries = parser.parse()

    print("\n" + "=" * 50)
    print("LOG FILE ANALYSIS REPORT")
    print("=" * 50)
    print(f"File: {args.file}")
    print(f"Valid entries: {len(entries)}")
    print(f"Malformed lines: {len(parser.malformed_lines)}")

    if not entries:
        print("\nNo valid log entries were found.")
        print("Reason: Unsupported log format or fully malformed file.")
        print("The program will stop without generating charts or reports.")
        print("=" * 50)
        return

    analyzer = LogAnalyzer(entries, len(parser.malformed_lines))
    counts = analyzer.analyze()

    print("\nLog counts by type:")
    for level in ["INFO", "WARNING", "ERROR"]:
        print(f"  {level}: {counts.get(level, 0)}")

    results = analyzer.search(
        keyword=args.keyword,
        start_date=args.start_date,
        end_date=args.end_date
    )

    print("\nSearch / Filter Results:")
    if results:
        print(f"  Matching entries: {len(results)}")
        for entry in results:
            print(f"  {entry}")
    else:
        print("  No matching log entries found.")

    report = analyzer.generate_report_data()

    print("\nSummary Report:")
    print(f"  Total entries: {report['total_entries']}")
    print(f"  Malformed lines: {report['malformed_lines']}")
    print(f"  First log: {report['first_log']}")
    print(f"  Last log: {report['last_log']}")
    print("  Common errors:")

    if report["common_errors"]:
        for message, count in report["common_errors"].items():
            print(f"    - {message}: {count}")
    else:
        print("    No error logs found.")

    analyzer.save_report_to_json("Samples/log_report.json")
    print("\nReport saved to Samples/log_report.json")

    analyzer.visualize_log_frequency()
    print("Bar chart saved to Samples/log_frequency.png")

    analyzer.visualize_timeline()
    print("Timeline chart saved to Samples/log_timeline.png")

    print("=" * 50)


if __name__ == "__main__":
    main()