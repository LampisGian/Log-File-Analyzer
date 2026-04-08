# Log File Analyzer

## Description
## Description
A Python-based Log File Analyzer that parses and analyzes `.log` files from multiple common log formats, not only generated sample logs. The application can read log entries, identify their timestamp, log level, and message content, and then produce useful summaries and visualizations for easier inspection of system or application activity.

The project supports both Command Line Interface (CLI) and Graphical User Interface (GUI) usage. Users can load a log file, search by keyword, filter entries by date range, and view analysis results in a structured and user-friendly way. The program also generates summary reports including total valid entries, malformed lines, first and last log entry, common errors, and log counts by type.

In addition, the analyzer creates visualizations such as bar charts and timeline graphs using `matplotlib`, helping users better understand log frequency and event distribution over time. Unsupported or malformed log lines are handled safely without crashing the program, making the tool robust for working with both clean and imperfect log datasets.
## Getting Started

There are two ways to run the application:

### 1) macOS app (`.app`)

- Download the provided **Log File Analyzer.zip**
- Unzip the file
- Open the generated **Log File Analyzer.app**
- Use the graphical interface to drag and drop a `.log` file or browse for one manually
- Enter optional filters such as keyword, start date, and end date
- Run the analysis directly from the GUI

> **Note:** The macOS application is intended for direct use without running Python manually. The generated reports and visualization files are stored in the application's standard data location on macOS.

---

### 2) Run from source (Python)

- Download or clone the full project folder
- Open a terminal in the project directory
- Move into the `Source_Code` folder
- Run the application from the command line

```bash
python main.py --file path/to/logfile.log
# or
python3 main.py --file path/to/logfile.log
```
> **Note:** The application also supports optional CLI arguments for search and filtering:
```python main.py --file path/to/logfile.log --keyword error --start-date 2026-03-24 --end-date 2026-03-24 ```


## Tasks
- Understand `.log` file formats. Use sample logs. Plan regex for extracting levels and timestamps.
- Implement log parser with support for `INFO`, `ERROR`, `WARNING`.
- Count and display logs per type. Save results to JSON.
- Add search/filter by keyword and date.
- Generate summary report (total entries, first/last log, common errors).
- Visualize log frequency using matplotlib (bar chart or timeline).
- Add CLI arguments for automation, GUI for log analysis.
- Test with large logs, handle malformed lines.
- Final testing. Create README with instructions and screenshots. Submit as Git repo.

## Estimated time to work 2 weeks
