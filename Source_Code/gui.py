import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinterdnd2 import DND_FILES, TkinterDnD

from log_parser import LogParser
from log_analyzer import LogAnalyzer


def get_app_data_dir():
    app_dir = Path.home() / "Library" / "Application Support" / "Log File Analyzer"
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


class LogAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Log File Analyzer")
        self.root.geometry("1380x840")
        self.root.minsize(1100, 700)

        self.file_path = None
        self.frequency_canvas_widget = None
        self.timeline_canvas_widget = None
        self.app_data_dir = get_app_data_dir()

        self.configure_styles()
        self.build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_styles(self):
        self.colors = {
            "bg": "#0B1020",
            "surface": "#121A2B",
            "text": "#E6EEF8",
            "muted": "#94A3B8",
            "accent": "#7C3AED",
            "accent_hover": "#6D28D9",
            "entry_bg": "#F8FAFC",
            "entry_fg": "#111827",
            "results_bg": "#0F172A",
            "results_fg": "#E2E8F0",
            "drop_bg": "#EDE9FE",
            "drop_fg": "#4C1D95",
            "success_bg": "#DCFCE7",
            "success_fg": "#166534",
            "warning_bg": "#FEF3C7",
            "warning_fg": "#92400E",
            "error_bg": "#FEE2E2",
            "error_fg": "#991B1B",
            "info_bg": "#DBEAFE",
            "info_fg": "#1D4ED8",
            "chart_bg": "#F8FAFC",
            "placeholder_fg": "#64748B"
        }

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("App.TFrame", background=self.colors["bg"])

        style.configure(
            "Card.TLabelframe",
            background=self.colors["surface"],
            foreground=self.colors["text"],
            borderwidth=0
        )
        style.configure(
            "Card.TLabelframe.Label",
            background=self.colors["surface"],
            foreground=self.colors["text"],
            font=("Arial", 11, "bold")
        )

        style.configure(
            "TLabel",
            background=self.colors["bg"],
            foreground=self.colors["text"],
            font=("Arial", 10)
        )
        style.configure(
            "Header.TLabel",
            background=self.colors["bg"],
            foreground="#F8FAFC",
            font=("Arial", 20, "bold")
        )
        style.configure(
            "Sub.TLabel",
            background=self.colors["bg"],
            foreground=self.colors["muted"],
            font=("Arial", 10)
        )

        style.configure(
            "Primary.TButton",
            background=self.colors["accent"],
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=10,
            borderwidth=0
        )
        style.map(
            "Primary.TButton",
            background=[("active", self.colors["accent_hover"])]
        )

        style.configure(
            "Secondary.TButton",
            background="#334155",
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=10,
            borderwidth=0
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#475569")]
        )

        style.configure(
            "TNotebook",
            background=self.colors["surface"],
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            background="#E5E7EB",
            foreground="#111827",
            padding=(14, 8),
            font=("Arial", 10, "bold")
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#FFFFFF")],
            foreground=[("selected", "#111827")]
        )

    def build_ui(self):
        self.root.configure(bg=self.colors["bg"])

        main = ttk.Frame(self.root, style="App.TFrame", padding=14)
        main.pack(fill="both", expand=True)

        header = ttk.Frame(main, style="App.TFrame")
        header.pack(fill="x", pady=(0, 10))

        header.columnconfigure(0, weight=1)

        title_wrap = ttk.Frame(header, style="App.TFrame")
        title_wrap.grid(row=0, column=0, sticky="w")

        ttk.Label(title_wrap, text="Log File Analyzer", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            title_wrap,
            text="Analyze log files with search, date filters, report generation, and built-in charts.",
            style="Sub.TLabel"
        ).pack(anchor="w", pady=(2, 0))

        self.status_badge = tk.Label(
            header,
            text="READY",
            bg=self.colors["info_bg"],
            fg=self.colors["info_fg"],
            font=("Arial", 10, "bold"),
            width=14,
            height=2,
            relief="flat",
            bd=0
        )
        self.status_badge.grid(row=0, column=1, sticky="ne", padx=(12, 0))

        top = ttk.LabelFrame(main, text="File Input", style="Card.TLabelframe", padding=12)
        top.pack(fill="x", pady=(0, 10))

        self.drop_area = tk.Label(
            top,
            text="Drag and drop a .log file here",
            bg=self.colors["drop_bg"],
            fg=self.colors["drop_fg"],
            relief="flat",
            bd=0,
            height=4,
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        self.drop_area.pack(fill="x", pady=(0, 10))
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.handle_drop)

        file_row = tk.Frame(top, bg=self.colors["surface"])
        file_row.pack(fill="x")

        self.file_var = tk.StringVar(value="No file selected")
        self.file_entry = tk.Entry(
            file_row,
            textvariable=self.file_var,
            bg=self.colors["entry_bg"],
            fg=self.colors["entry_fg"],
            relief="flat",
            font=("Arial", 11),
            insertbackground=self.colors["entry_fg"],
            bd=8
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        browse_btn = ttk.Button(
            file_row,
            text="Browse",
            style="Primary.TButton",
            command=self.browse_file
        )
        browse_btn.pack(side="left")

        filters = ttk.LabelFrame(main, text="Filters and Search", style="Card.TLabelframe", padding=12)
        filters.pack(fill="x", pady=(0, 10))

        filters.columnconfigure(1, weight=1)
        filters.columnconfigure(3, weight=1)
        filters.columnconfigure(5, weight=1)

        ttk.Label(filters, text="Keyword").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.keyword_entry = tk.Entry(
            filters,
            bg=self.colors["entry_bg"],
            fg=self.colors["entry_fg"],
            relief="flat",
            font=("Arial", 11),
            insertbackground=self.colors["entry_fg"],
            bd=8
        )
        self.keyword_entry.grid(row=0, column=1, sticky="ew", padx=6, pady=6)

        ttk.Label(filters, text="Start Date (YYYY-MM-DD)").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        self.start_entry = tk.Entry(
            filters,
            bg=self.colors["entry_bg"],
            fg=self.colors["entry_fg"],
            relief="flat",
            font=("Arial", 11),
            insertbackground=self.colors["entry_fg"],
            bd=8
        )
        self.start_entry.grid(row=0, column=3, sticky="ew", padx=6, pady=6)

        ttk.Label(filters, text="End Date (YYYY-MM-DD)").grid(row=0, column=4, sticky="w", padx=6, pady=6)
        self.end_entry = tk.Entry(
            filters,
            bg=self.colors["entry_bg"],
            fg=self.colors["entry_fg"],
            relief="flat",
            font=("Arial", 11),
            insertbackground=self.colors["entry_fg"],
            bd=8
        )
        self.end_entry.grid(row=0, column=5, sticky="ew", padx=6, pady=6)

        action_row = tk.Frame(filters, bg=self.colors["surface"])
        action_row.grid(row=1, column=0, columnspan=6, sticky="ew", padx=6, pady=(8, 0))

        analyze_btn = ttk.Button(
            action_row,
            text="Analyze File",
            style="Primary.TButton",
            command=self.analyze_file
        )
        analyze_btn.pack(side="left")

        clear_btn = ttk.Button(
            action_row,
            text="Clear",
            style="Secondary.TButton",
            command=self.clear_fields
        )
        clear_btn.pack(side="left", padx=(8, 0))

        content = ttk.Frame(main, style="App.TFrame")
        content.pack(fill="both", expand=True)

        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        left = ttk.LabelFrame(content, text="Results", style="Card.TLabelframe", padding=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        right = ttk.LabelFrame(content, text="Charts", style="Card.TLabelframe", padding=10)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        left.rowconfigure(0, weight=1)
        left.columnconfigure(0, weight=1)

        self.output_box = ScrolledText(
            left,
            wrap="word",
            font=("Consolas", 10),
            bg=self.colors["results_bg"],
            fg=self.colors["results_fg"],
            insertbackground="white",
            relief="flat",
            padx=12,
            pady=12
        )
        self.output_box.grid(row=0, column=0, sticky="nsew")

        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill="both", expand=True)

        self.freq_tab = tk.Frame(self.notebook, bg=self.colors["chart_bg"])
        self.time_tab = tk.Frame(self.notebook, bg=self.colors["chart_bg"])

        self.notebook.add(self.freq_tab, text="Bar Chart")
        self.notebook.add(self.time_tab, text="Timeline")

        for tab in (self.freq_tab, self.time_tab):
            tab.rowconfigure(0, weight=1)
            tab.columnconfigure(0, weight=1)

        self.freq_placeholder = tk.Label(
            self.freq_tab,
            text="Bar chart will appear here",
            bg=self.colors["chart_bg"],
            fg=self.colors["placeholder_fg"],
            font=("Arial", 11)
        )
        self.freq_placeholder.grid(row=0, column=0)

        self.time_placeholder = tk.Label(
            self.time_tab,
            text="Timeline chart will appear here",
            bg=self.colors["chart_bg"],
            fg=self.colors["placeholder_fg"],
            font=("Arial", 11)
        )
        self.time_placeholder.grid(row=0, column=0)

    def set_status(self, message, status_type="info"):
        colors = {
            "success": (self.colors["success_bg"], self.colors["success_fg"], "SUCCESS"),
            "warning": (self.colors["warning_bg"], self.colors["warning_fg"], "WARNING"),
            "error": (self.colors["error_bg"], self.colors["error_fg"], "ERROR"),
            "info": (self.colors["info_bg"], self.colors["info_fg"], "READY")
        }

        bg, fg, label = colors.get(status_type, colors["info"])
        self.status_badge.config(text=label, bg=bg, fg=fg)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a log file",
            filetypes=[("Log files", "*.log"), ("All files", "*.*")]
        )
        if file_path:
            self.set_file(file_path)

    def handle_drop(self, event):
        file_path = event.data.strip()

        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]

        if not file_path.lower().endswith(".log"):
            self.set_status("Invalid file. Please choose a .log file.", "error")
            messagebox.showerror("Invalid File", "Please choose a .log file.")
            return

        self.set_file(file_path)

    def set_file(self, file_path):
        self.file_path = file_path
        self.file_var.set(file_path)
        self.drop_area.config(text="File loaded successfully", bg=self.colors["success_bg"], fg=self.colors["success_fg"])
        self.set_status("Log file selected successfully.", "success")

    def clear_fields(self):
        self.keyword_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.output_box.delete("1.0", tk.END)
        self.clear_chart_area()
        self.set_status("Fields and charts cleared.", "info")

    def clear_chart_area(self):
        for tab in (self.freq_tab, self.time_tab):
            for widget in tab.winfo_children():
                widget.destroy()

        self.freq_placeholder = tk.Label(
            self.freq_tab,
            text="Bar chart will appear here",
            bg=self.colors["chart_bg"],
            fg=self.colors["placeholder_fg"],
            font=("Arial", 11)
        )
        self.freq_placeholder.grid(row=0, column=0)

        self.time_placeholder = tk.Label(
            self.time_tab,
            text="Timeline chart will appear here",
            bg=self.colors["chart_bg"],
            fg=self.colors["placeholder_fg"],
            font=("Arial", 11)
        )
        self.time_placeholder.grid(row=0, column=0)

        self.frequency_canvas_widget = None
        self.timeline_canvas_widget = None
        plt.close("all")

    def write_line(self, text=""):
        self.output_box.insert(tk.END, text + "\n")
        self.output_box.see(tk.END)

    def render_figure(self, fig, parent, chart_type):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        widget = canvas.get_tk_widget()
        widget.grid(row=0, column=0, sticky="nsew")
        canvas.draw()

        if chart_type == "frequency":
            self.frequency_canvas_widget = canvas
        else:
            self.timeline_canvas_widget = canvas

    def analyze_file(self):
        if not self.file_path:
            self.set_status("Please drag a log file or use Browse first.", "error")
            messagebox.showerror("No File", "Please drag a log file or use Browse.")
            return

        keyword = self.keyword_entry.get().strip() or None
        start_date = self.start_entry.get().strip() or None
        end_date = self.end_entry.get().strip() or None

        try:
            parser = LogParser(self.file_path)
            entries = parser.parse()

            self.output_box.delete("1.0", tk.END)
            self.clear_chart_area()

            self.write_line("=" * 55)
            self.write_line("LOG FILE ANALYSIS REPORT")
            self.write_line("=" * 55)
            self.write_line(f"File: {self.file_path}")
            self.write_line(f"Valid entries: {len(entries)}")
            self.write_line(f"Malformed lines: {len(parser.malformed_lines)}")

            if not entries:
                self.set_status("Analysis failed: no valid log entries were found.", "error")
                self.write_line("")
                self.write_line("No valid log entries were found.")
                self.write_line("Reason: Unsupported log format or fully malformed file.")
                return

            analyzer = LogAnalyzer(entries, len(parser.malformed_lines))
            counts = analyzer.analyze()

            if parser.malformed_lines and entries:
                self.set_status(
                    f"Analysis completed with warnings: {len(parser.malformed_lines)} line(s) could not be parsed.",
                    "warning"
                )
            else:
                self.set_status("Analysis completed successfully.", "success")

            self.write_line("")
            self.write_line("Log counts by type:")
            for level in ["INFO", "WARNING", "ERROR"]:
                self.write_line(f"  {level}: {counts.get(level, 0)}")

            results = analyzer.search(
                keyword=keyword,
                start_date=start_date,
                end_date=end_date
            )

            self.write_line("")
            self.write_line("Search / Filter Results:")
            if results:
                self.write_line(f"  Matching entries: {len(results)}")
                show_limit = 100
                for entry in results[:show_limit]:
                    self.write_line(f"  {entry}")
                if len(results) > show_limit:
                    self.write_line(f"  ... and {len(results) - show_limit} more entries")
            else:
                self.write_line("  No matching log entries found.")

            report = analyzer.generate_report_data()

            self.write_line("")
            self.write_line("Summary Report:")
            self.write_line(f"  Total entries: {report['total_entries']}")
            self.write_line(f"  Malformed lines: {report['malformed_lines']}")
            self.write_line(f"  First log: {report['first_log']}")
            self.write_line(f"  Last log: {report['last_log']}")
            self.write_line("  Common errors:")

            if report["common_errors"]:
                for message, count in report["common_errors"].items():
                    self.write_line(f"    - {message}: {count}")
            else:
                self.write_line("    No error logs found.")

            report_path = self.app_data_dir / "log_report.json"
            analyzer.save_report_to_json(str(report_path))
            self.write_line("")
            self.write_line(f"Report saved to {report_path}")

            freq_fig = analyzer.create_frequency_figure()
            self.render_figure(freq_fig, self.freq_tab, "frequency")

            time_fig = analyzer.create_timeline_figure()
            if time_fig is not None:
                self.render_figure(time_fig, self.time_tab, "timeline")
            else:
                self.write_line("No timeline chart available.")

            self.write_line("=" * 55)

        except Exception as e:
            self.set_status(f"Analysis failed: {str(e)}", "error")
            messagebox.showerror("Error", str(e))

    def on_close(self):
        try:
            plt.close("all")
            self.root.quit()
            self.root.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = LogAnalyzerGUI(root)
    root.mainloop()