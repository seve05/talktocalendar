import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QIcon

class ScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weekly Schedule")
        self.setGeometry(100, 100, 800, 600)

        # Create web view
        self.webview = QWebEngineView(self)
        self.setCentralWidget(self.webview)

        # Initial HTML content
        self.update_html()
        
        # Set up timer to check for JSON updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_for_updates)
        self.timer.start(5000)  # Check every 5 seconds
        
        self.last_modified = os.path.getmtime('schedule.json')

    def load_schedule(self):
        try:
            with open('schedule.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading schedule: {e}")
            return None

    def generate_html(self):
        data = self.load_schedule()
        if not data or "week" not in data:
            return "<h1>Error loading schedule</h1>"

        week = data["week"]
        
        # Build table rows
        rows = ""
        for hour in range(1, 25):
            row = f"<tr><td>{hour}:00</td>"
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                activity = week[day][str(hour)] or "-"
                row += f"<td>{activity}</td>"
            row += "</tr>"
            rows += row

        # Full HTML with styling
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Planner</title>
            <style>
                body {{
                    font-family: 'Verdana', monospace;
                    margin: 20px;
                        background-color: #000000;
                    color: #e6edf3;
                }}
                h1 {{
                    color: #ffffff;
                    text-align: center;
                    font-weight: 500;
                    margin-bottom: 30px;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                    background-color: #000000;
                    border: 1px solid #30363d;
                }}
                th, td {{
                    border: 1px solid #30363d;
                    padding: 12px;
                    text-align: center;
                }}
                th {{
                    background-color: #000000;
                    color: #e6edf3;
                    font-weight: 600;
                }}
                td {{
                    color: #c9d1d9;
                }}
                tr:nth-child(even) {{
                    background-color: #0000000;
                }}
                tr:hover {{
                    background-color: #30363d;
                    transition: background-color 0.2s ease;
                }}
            </style>
        </head>
        <body>
            <h1>Weekly Schedule</h1>
            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Monday</th>
                        <th>Tuesday</th>
                        <th>Wednesday</th>
                        <th>Thursday</th>
                        <th>Friday</th>
                        <th>Saturday</th>
                        <th>Sunday</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </body>
        </html>
        """
        return html

    def update_html(self):
        html_content = self.generate_html()
        self.webview.setHtml(html_content, QUrl.fromLocalFile(os.path.abspath('schedule.json')))

    def check_for_updates(self):
        try:
            current_modified = os.path.getmtime('schedule.json')
            if current_modified > self.last_modified:
                self.update_html()
                self.last_modified = current_modified
        except Exception as e:
            print(f"Error checking updates: {e}")

def main():
    app = QApplication(sys.argv)
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
