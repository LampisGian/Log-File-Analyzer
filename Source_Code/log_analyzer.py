import json
from collections import Counter

class LogAnalyzer:
    def __init__(self, log_entries):
        self.log_entries = log_entries
        self.counts = Counter()

    def analyze(self):
        for entry in self.log_entries:
            self.counts[entry.level] += 1
        return self.counts

    def save_to_json(self, output_file):
        data = {
            "counts": dict(self.counts),
            "total_entries": len(self.log_entries)
        }
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)