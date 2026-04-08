import json
from collections import Counter
import matplotlib.pyplot as plt


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

    def visualize_log_frequency(self, output_file="Samples/log_frequency.png"):
        if not self.counts:
            self.analyze()

        level_order = ["INFO", "WARNING", "ERROR"]
        levels = [level for level in level_order if level in self.counts]
        values = [self.counts[level] for level in levels]

        colors = {
            "INFO": "skyblue",
            "WARNING": "orange",
            "ERROR": "red"
        }

        bar_colors = [colors[level] for level in levels]

        plt.figure(figsize=(9, 5))
        bars = plt.bar(levels, values, color=bar_colors, width=0.45)

        plt.title("Log Frequency by Type", fontsize=16)
        plt.xlabel("Log Level", fontsize=12)
        plt.ylabel("Number of Entries", fontsize=12)
        plt.grid(axis="y", linestyle="--", alpha=0.4)

        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height + 1,
                str(height),
                ha="center",
                va="bottom",
                fontsize=11
            )

        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        plt.show()

    def visualize_timeline(self, output_file="Samples/log_timeline.png"):
        if not self.log_entries:
            print("No log entries available for timeline.")
            return

        timeline_counts = Counter(entry.timestamp[:13] for entry in self.log_entries)

        time_points = sorted(timeline_counts.keys())
        values = [timeline_counts[t] for t in time_points]
        x_positions = list(range(len(time_points)))

        plt.figure(figsize=(12, 5))
        plt.plot(
            x_positions,
            values,
            marker="o",
            linestyle="-",
            linewidth=2,
            markersize=5,
            color="mediumpurple"
        )

        plt.fill_between(x_positions, values, alpha=0.15, color="mediumpurple")

        plt.title("Log Timeline Frequency", fontsize=18, fontweight="bold")
        plt.xlabel("Date and Hour", fontsize=12)
        plt.ylabel("Number of Entries", fontsize=12)

        step = max(1, len(time_points) // 8)
        plt.xticks(
            x_positions[::step],
            [time_points[i] for i in range(0, len(time_points), step)],
            rotation=30,
            ha="right",
            fontsize=10
        )

        plt.yticks(fontsize=10)
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        plt.show()