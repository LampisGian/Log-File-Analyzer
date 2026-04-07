from datetime import datetime, timedelta
import random


class SampleLogGenerator:
    def __init__(self, output_file, num_lines=200):
        self.output_file = output_file
        self.num_lines = num_lines
        self.levels = ["INFO", "WARNING", "ERROR"]

        self.info_messages = [
            "User logged in",
            "User logged out",
            "Backup started",
            "Backup completed",
            "Configuration loaded successfully",
            "Scheduled task started",
            "Scheduled task completed",
            "Connection established",
            "File uploaded successfully",
            "Application started",
            "Application restarted",
            "Cache cleared",
            "New session created",
            "Settings updated successfully",
            "Service started successfully"
        ]

        self.warning_messages = [
            "Disk usage is high",
            "CPU temperature is above normal",
            "Memory usage is high",
            "Unusual login attempt detected",
            "API response is slower than expected",
            "Deprecated API call detected",
            "Low available storage space",
            "Temporary network instability detected",
            "Multiple failed login attempts",
            "Large response time recorded"
        ]

        self.error_messages = [
            "Failed to connect to database",
            "Timeout while contacting server",
            "Could not open configuration file",
            "Access denied for admin panel",
            "Failed to save user settings",
            "Database query failed",
            "Network connection lost",
            "Authentication failed",
            "File not found",
            "Unexpected server error occurred"
        ]

    def get_random_message(self, level):
        if level == "INFO":
            return random.choice(self.info_messages)
        elif level == "WARNING":
            return random.choice(self.warning_messages)
        else:
            return random.choice(self.error_messages)

    def generate_logs(self):
        start_time = datetime(2026, 3, 24, 14, 0, 0)

        with open(self.output_file, "w", encoding="utf-8") as file:
            current_time = start_time

            for i in range(self.num_lines):
                level = random.choice(self.levels)
                message = self.get_random_message(level)

                log_line = f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} {level} {message}\n"
                file.write(log_line)

                if i % 25 == 0 and i != 0:
                    file.write("Malformed log line example\n")
                    file.write("2026/03/24 ERROR Wrong date format\n")

                current_time += timedelta(seconds=random.randint(5, 120))

        print(f"Sample log file created successfully: {self.output_file}")


def main():
    generator = SampleLogGenerator("Samples/sample.log", 300)
    generator.generate_logs()


if __name__ == "__main__":
    main()