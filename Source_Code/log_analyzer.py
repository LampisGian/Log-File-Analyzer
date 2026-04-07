import json
from collections import Counter


class LogAnalyzer:
    def __init__(self, log_entries, malformed_count=0):
        self.log_entries = log_entries
        self.malformed_count = malformed_count
        self.counts = Counter()

    def analyze(self):
        self.counts = Counter(entry.level for entry in self.log_entries)
        return self.counts

    def filter_by_keyword(self, keyword):
        keyword = keyword.lower()
        return [
            entry for entry in self.log_entries
            if keyword in entry.message.lower()
        ]

    def filter_by_date(self, start_date=None, end_date=None):
        filtered_entries = []

        for entry in self.log_entries:
            entry_date = entry.timestamp[:10]

            if start_date and entry_date < start_date:
                continue
            if end_date and entry_date > end_date:
                continue

            filtered_entries.append(entry)

        return filtered_entries

    def search(self, keyword=None, start_date=None, end_date=None):
        filtered_entries = self.log_entries

        if keyword:
            keyword_lower = keyword.lower()
            filtered_entries = [
                entry for entry in filtered_entries
                if keyword_lower in entry.message.lower()
            ]

        if start_date or end_date:
            date_filtered_entries = []

            for entry in filtered_entries:
                entry_date = entry.timestamp[:10]

                if start_date and entry_date < start_date:
                    continue
                if end_date and entry_date > end_date:
                    continue

                date_filtered_entries.append(entry)

            filtered_entries = date_filtered_entries

        return filtered_entries

    def generate_report_data(self):
        if not self.counts:
            self.analyze()

        if not self.log_entries:
            return {
                "counts": {},
                "total_entries": 0,
                "malformed_lines": self.malformed_count,
                "first_log": None,
                "last_log": None,
                "common_errors": {}
            }

        sorted_entries = sorted(self.log_entries, key=lambda entry: entry.timestamp)

        error_messages = [
            entry.message for entry in self.log_entries
            if entry.level == "ERROR"
        ]

        common_errors = dict(Counter(error_messages).most_common(5))

        return {
            "counts": dict(self.counts),
            "total_entries": len(self.log_entries),
            "malformed_lines": self.malformed_count,
            "first_log": str(sorted_entries[0]),
            "last_log": str(sorted_entries[-1]),
            "common_errors": common_errors
        }

    def save_report_to_json(self, output_file):
        data = self.generate_report_data()

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)