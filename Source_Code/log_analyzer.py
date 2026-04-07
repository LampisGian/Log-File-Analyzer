import json
from collections import Counter


class LogAnalyzer:
    def __init__(self, log_entries):
        self.log_entries = log_entries
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

    def save_to_json(self, output_file):
        data = {
            "counts": dict(self.counts),
            "total_entries": len(self.log_entries)
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)