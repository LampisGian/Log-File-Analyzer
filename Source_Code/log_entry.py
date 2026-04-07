class LogEntry:
    def __init__(self, timestamp, level, message):
        self.timestamp = timestamp
        self.level = level
        self.message = message

    def __str__(self):
        return f"{self.timestamp} {self.level} {self.message}"