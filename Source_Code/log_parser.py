import re
from datetime import datetime
from log_entry import LogEntry


class LogParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.entries = []
        self.malformed_lines = []

        self.standard_patterns = [
            re.compile(
                r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
                r"(?P<level>INFO|WARNING|ERROR)\s+"
                r"(?P<message>.+)$",
                re.IGNORECASE
            ),
            re.compile(
                r"^\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+"
                r"(?P<level>INFO|WARNING|ERROR):\s+"
                r"(?P<message>.+)$",
                re.IGNORECASE
            ),
            re.compile(
                r"^(?P<level>INFO|WARNING|ERROR)\s+"
                r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
                r"(?P<message>.+)$",
                re.IGNORECASE
            )
        ]

        self.apache_pattern = re.compile(
            r"^\[(?P<timestamp>[A-Za-z]{3}\s+[A-Za-z]{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2}\s+\d{4})\]\s+"
            r"\[(?P<level>[A-Za-z]+)\]\s+"
            r"(?P<message>.+)$"
        )

        self.health_pattern = re.compile(
            r"^(?P<timestamp>\d{8}-\d{2}:\d{2}:\d{2}:\d{3})\|"
            r"(?P<tag>[^|]+)\|"
            r"(?P<pid>[^|]+)\|"
            r"(?P<message>.+)$"
        )

        self.syslog_pattern = re.compile(
            r"^(?P<month>[A-Za-z]{3})\s+"
            r"(?P<day>\d{1,2})\s+"
            r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
            r"(?P<host>\S+)\s+"
            r"(?P<source>.+?):\s*"
            r"(?P<message>.+)$"
        )

        self.windows_pattern = re.compile(
            r"^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}),\s*"
            r"(?P<level>[A-Za-z]+)\s+"
            r"(?P<component>\S+)\s+"
            r"(?P<message>.+)$"
        )

    def normalize_level(self, level, message=""):
        level_upper = level.upper()

        mapping = {
            "INFO": "INFO",
            "INFORMATION": "INFO",
            "NOTICE": "INFO",
            "DEBUG": "INFO",
            "TRACE": "INFO",

            "WARN": "WARNING",
            "WARNING": "WARNING",

            "ERR": "ERROR",
            "ERROR": "ERROR",
            "CRIT": "ERROR",
            "CRITICAL": "ERROR",
            "ALERT": "ERROR",
            "EMERG": "ERROR",
            "FATAL": "ERROR",
            "SEVERE": "ERROR"
        }

        if level_upper in mapping:
            return mapping[level_upper]

        msg = message.lower()
        if any(word in msg for word in ["error", "failure", "failed", "exception", "fatal", "critical"]):
            return "ERROR"
        if any(word in msg for word in ["warn", "warning"]):
            return "WARNING"

        return "INFO"

    def parse_standard(self, line):
        for pattern in self.standard_patterns:
            match = pattern.match(line)
            if match:
                timestamp = match.group("timestamp")
                level = self.normalize_level(match.group("level"), match.group("message"))
                message = match.group("message")
                return LogEntry(timestamp, level, message)
        return None

    def parse_apache(self, line):
        match = self.apache_pattern.match(line)
        if not match:
            return None

        raw_timestamp = match.group("timestamp")
        level = self.normalize_level(match.group("level"), match.group("message"))
        message = match.group("message")

        dt = datetime.strptime(raw_timestamp, "%a %b %d %H:%M:%S %Y")
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

        return LogEntry(timestamp, level, message)

    def parse_health(self, line):
        match = self.health_pattern.match(line)
        if not match:
            return None

        raw_timestamp = match.group("timestamp")
        tag = match.group("tag")
        pid = match.group("pid")
        message = match.group("message")

        dt = datetime.strptime(raw_timestamp, "%Y%m%d-%H:%M:%S:%f")
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

        full_message = f"[{tag}] [PID:{pid}] {message}"
        level = self.normalize_level("INFO", full_message)

        return LogEntry(timestamp, level, full_message)

    def parse_syslog(self, line):
        match = self.syslog_pattern.match(line)
        if not match:
            return None

        month = match.group("month")
        day = match.group("day")
        time_part = match.group("time")
        host = match.group("host")
        source = match.group("source")
        message = match.group("message")

        current_year = datetime.now().year
        raw_timestamp = f"{current_year} {month} {day} {time_part}"
        dt = datetime.strptime(raw_timestamp, "%Y %b %d %H:%M:%S")
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

        full_message = f"[{host}] [{source}] {message}"
        level = self.normalize_level("INFO", full_message)

        return LogEntry(timestamp, level, full_message)

    def parse_windows(self, line):
        match = self.windows_pattern.match(line)
        if not match:
            return None

        raw_timestamp = match.group("timestamp")
        level = self.normalize_level(match.group("level"), match.group("message"))
        component = match.group("component")
        message = match.group("message")

        dt = datetime.strptime(raw_timestamp, "%Y-%m-%d %H:%M:%S")
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

        full_message = f"[{component}] {message}"
        return LogEntry(timestamp, level, full_message)

    def parse_line(self, line):
        line = line.strip()

        if not line:
            return None

        parsers = [
            self.parse_standard,
            self.parse_apache,
            self.parse_health,
            self.parse_syslog,
            self.parse_windows
        ]

        for parser in parsers:
            entry = parser(line)
            if entry:
                return entry

        self.malformed_lines.append(line)
        return None

    def parse(self):
        self.entries = []
        self.malformed_lines = []

        with open(self.file_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                entry = self.parse_line(line)
                if entry:
                    self.entries.append(entry)

        return self.entries