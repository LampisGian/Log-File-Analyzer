#This class is a simple data structure to represent individual log entries, encapsulating the timestamp, log level, and message. 
#It provides a __str__ method for easy string representation of the log entry, which is useful for displaying entries in the console or GUI. 
#The LogEntry class is used throughout the log parsing and analysis process to maintain a consistent format for log data, making it easier to manipulate and

class LogEntry:
    def __init__(self, timestamp, level, message):
        self.timestamp = timestamp
        self.level = level
        self.message = message

    def __str__(self):
        return f"{self.timestamp} {self.level} {self.message}"