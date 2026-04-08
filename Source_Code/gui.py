import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk

from tkinterdnd2 import DND_FILES, TkinterDnD

from log_parser import LogParser
from log_analyzer import LogAnalyzer


class LogAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Log File Analyzer")
        self.root.geometry("1200x800")

        self.file_path = None
        self.frequency_image = None
        self.timeline_image = None

        os.makedirs("Samples", exist_ok=True)

        self.build_ui()

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)

        top_frame = ttk.LabelFrame(main_frame, text="Log File Input", padding=10)
        top_frame.pack(fill="x", pady=(0, 10))

        self.drop_label = tk.Label(
            top_frame,
            text="Drag and drop a .log file here",
            relief="groove",
            bd=2,
            height=4,
            bg="#f5f5f5",
            font=("Arial", 12)
        )
        self.drop_label.pack(fill="x", pady=(0, 10))
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self.handle_drop)

        self.file_label = ttk.Label(top_frame, text="No file selected")
        self.file_label.pack(anchor="w")

        filter_frame = ttk.LabelFrame(main_frame, text="Filters / Search", padding=10)
        filter_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(filter_frame, text="Keyword:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.keyword_entry = ttk.Entry(filter_frame, width=30)
        self.keyword_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.start_date_entry = ttk.Entry(filter_frame, width=20)
        self.start_date_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(filter_frame, text="End Date (YYYY-MM-DD):").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.end_date_entry = ttk.Entry(filter_frame, width=20)
        self.end_date_entry.grid(row=0, column=5, padx=5, pady=5)

        self.analyze_button = ttk.Button(filter_frame, text="Analyze Log File", command=self.analyze_file)
        self.analyze_button.grid(row=0, column=6, padx=10, pady=5)

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)

        left_frame = ttk.LabelFrame(content_frame, text="Analysis Results", padding=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.output_box = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, font=("Courier New", 10))
        self.output_box.pack(fill="both", expand=True)

        right_frame = ttk.LabelFrame(content_frame, text="Visualizations", padding=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        self.chart_notebook = ttk.Notebook(right_frame)
        self.chart_notebook.pack(fill="both", expand=True)

        self.frequency_tab = ttk.Frame(self.chart_notebook)
        self.timeline_tab = ttk.Frame(self.chart_notebook)

        self.chart_notebook.add(self.frequency_tab, text="Bar Chart")
        self.chart_notebook.add(self.timeline_tab, text="Timeline")

        self.frequency_canvas = tk.Label(self.frequency_tab, text="Bar chart will appear here")
        self.frequency_canvas.pack(fill="both", expand=True)

        self.timeline_canvas = tk.Label(self.timeline_tab, text="Timeline chart will appear here")
        self.timeline_canvas.pack(fill="both", expand=True)

    def handle_drop(self, event):
        file_path = event.data.strip()

        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]

        if not file_path.lower().endswith(".log"):
            messagebox.showerror("Invalid File", "Please drop a .log file.")
            return

        self.file_path = file_path
        self.file_label.config(text=f"Selected file: {self.file_path}")
        self.drop_label.config(text="File loaded successfully")

    def analyze_file(self):
        if not self.file_path:
            messagebox.showerror("No File", "Please drag and drop a .log file first.")
            return

        keyword = self.keyword_entry.get().strip() or None
        start_date = self.start_date_entry.get().strip() or None
        end_date = self.end_date_entry.get().strip() or None

        try:
            parser = LogParser(self.file_path)
            entries = parser.parse()

            self.output_box.delete("1.0", tk.END)

            self.output_box.insert(tk.END, "=" * 50 + "\n")
            self.output_box.insert(tk.END, "LOG FILE ANALYSIS REPORT\n")
            self.output_box.insert(tk.END, "=" * 50 + "\n")
            self.output_box.insert(tk.END, f"File: {self.file_path}\n")
            self.output_box.insert(tk.END, f"Valid entries: {len(entries)}\n")
            self.output_box.insert(tk.END, f"Malformed lines: {len(parser.malformed_lines)}\n")

            if not entries:
                self.output_box.insert(tk.END, "\nNo valid log entries were found.\n")
                self.output_box.insert(tk.END, "Reason: Unsupported log format or fully malformed file.\n")
                self.clear_images()
                return

            analyzer = LogAnalyzer(entries, len(parser.malformed_lines))
            counts = analyzer.analyze()

            self.output_box.insert(tk.END, "\nLog counts by type:\n")
            for level in ["INFO", "WARNING", "ERROR"]:
                self.output_box.insert(tk.END, f"  {level}: {counts.get(level, 0)}\n")

            results = analyzer.search(
                keyword=keyword,
                start_date=start_date,
                end_date=end_date
            )

            self.output_box.insert(tk.END, "\nSearch / Filter Results:\n")
            if results:
                self.output_box.insert(tk.END, f"  Matching entries: {len(results)}\n")
                for entry in results:
                    self.output_box.insert(tk.END, f"  {entry}\n")
            else:
                self.output_box.insert(tk.END, "  No matching log entries found.\n")

            report = analyzer.generate_report_data()

            self.output_box.insert(tk.END, "\nSummary Report:\n")
            self.output_box.insert(tk.END, f"  Total entries: {report['total_entries']}\n")
            self.output_box.insert(tk.END, f"  Malformed lines: {report['malformed_lines']}\n")
            self.output_box.insert(tk.END, f"  First log: {report['first_log']}\n")
            self.output_box.insert(tk.END, f"  Last log: {report['last_log']}\n")
            self.output_box.insert(tk.END, "  Common errors:\n")

            if report["common_errors"]:
                for message, count in report["common_errors"].items():
                    self.output_box.insert(tk.END, f"    - {message}: {count}\n")
            else:
                self.output_box.insert(tk.END, "    No error logs found.\n")

            report_path = "Samples/log_report.json"
            freq_path = "Samples/log_frequency.png"
            timeline_path = "Samples/log_timeline.png"

            analyzer.save_report_to_json(report_path)
            analyzer.visualize_log_frequency(freq_path)
            analyzer.visualize_timeline(timeline_path)

            self.output_box.insert(tk.END, f"\nReport saved to {report_path}\n")
            self.output_box.insert(tk.END, f"Bar chart saved to {freq_path}\n")
            self.output_box.insert(tk.END, f"Timeline chart saved to {timeline_path}\n")
            self.output_box.insert(tk.END, "=" * 50 + "\n")

            self.display_image(freq_path, self.frequency_canvas, "frequency")
            self.display_image(timeline_path, self.timeline_canvas, "timeline")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_image(self, image_path, target_label, image_type):
        if not os.path.exists(image_path):
            target_label.config(text=f"Image not found: {image_path}", image="")
            return

        image = Image.open(image_path)
        image.thumbnail((520, 320))
        photo = ImageTk.PhotoImage(image)

        target_label.config(image=photo, text="")
        target_label.image = photo

        if image_type == "frequency":
            self.frequency_image = photo
        else:
            self.timeline_image = photo

    def clear_images(self):
        self.frequency_canvas.config(image="", text="Bar chart will appear here")
        self.timeline_canvas.config(image="", text="Timeline chart will appear here")
        self.frequency_canvas.image = None
        self.timeline_canvas.image = None


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = LogAnalyzerGUI(root)
    root.mainloop()