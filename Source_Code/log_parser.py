import re
from log_entry import LogEntry


class LogParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.entries = []
        self.malformed_lines = []

        self.pattern = re.compile(
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|WARNING|ERROR) (.+)"
        )

    def parse(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                match = self.pattern.match(line)

                if match:
                    timestamp, level, message = match.groups()
                    entry = LogEntry(timestamp, level, message)
                    self.entries.append(entry)
                else:
                    self.malformed_lines.append(line)

        return self.entries