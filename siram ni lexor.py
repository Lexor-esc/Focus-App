import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class AlarmRecord:
    def __init__(self):
        self.acknowledged = False

    def acknowledge(self):
        self.acknowledged = True


class FocusAnalyzer:
    def calculate_rate(self, acknowledged, total):
        if total == 0:
            return 0
        return (acknowledged / total) * 100

    def classify(self, rate):
        if rate >= 90:
            return "Highly Focused"
        elif rate >= 70:
            return "Moderately Focused"
        else:
            return "Needs Attention"


class FocusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus App")
        self.root.geometry("450x500")

        self.session_running = False
        self.start_time = None

        self.total_alarms = 0
        self.acknowledged = 0

        title = tk.Label(
            root,
            text="FOCUS APP",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        tk.Label(root, text="Name").pack()
        self.name_entry = tk.Entry(root, width=30)
        self.name_entry.pack()

        tk.Label(root, text="Daily Goal (minutes)").pack()
        self.goal_entry = tk.Entry(root, width=30)
        self.goal_entry.pack()

        self.start_btn = tk.Button(
            root,
            text="Start Session",
            command=self.start_session
        )
        self.start_btn.pack(pady=10)

        self.end_btn = tk.Button(
            root,
            text="End Session",
            command=self.end_session
        )
        self.end_btn.pack()

        self.status_label = tk.Label(
            root,
            text="Session Not Started",
            fg="red"
        )
        self.status_label.pack(pady=10)

        self.report = tk.Text(
            root,
            height=15,
            width=50
        )
        self.report.pack(pady=10)

    def start_session(self):
        if self.session_running:
            return

        self.session_running = True
        self.start_time = datetime.now()

        self.total_alarms = 0
        self.acknowledged = 0

        self.status_label.config(
            text="Session Running",
            fg="green"
        )

        messagebox.showinfo(
            "Focus App",
            "Session Started!"
        )

        # 10 seconds for testing
        self.root.after(10000, self.focus_check)

    def focus_check(self):

        if not self.session_running:
            return

        self.total_alarms += 1

        answer = messagebox.askyesno(
            "Focus Check",
            "Are you still focused?"
        )

        if answer:
            self.acknowledged += 1

        self.root.after(10000, self.focus_check)

    def end_session(self):

        if not self.session_running:
            return

        self.session_running = False

        end_time = datetime.now()

        duration = (
            end_time - self.start_time
        ).total_seconds() / 60

        analyzer = FocusAnalyzer()

        rate = analyzer.calculate_rate(
            self.acknowledged,
            self.total_alarms
        )

        level = analyzer.classify(rate)

        try:
            goal = float(
                self.goal_entry.get()
            )
        except:
            goal = 0

        goal_status = (
            "Goal Achieved"
            if duration >= goal
            else "Goal Not Achieved"
        )

        self.report.delete(
            1.0,
            tk.END
        )

        self.report.insert(
            tk.END,
            f"Name: {self.name_entry.get()}\n\n"
        )

        self.report.insert(
            tk.END,
            f"Duration: {duration:.2f} minutes\n"
        )

        self.report.insert(
            tk.END,
            f"Total Alarms: {self.total_alarms}\n"
        )

        self.report.insert(
            tk.END,
            f"Acknowledged: {self.acknowledged}\n"
        )

        self.report.insert(
            tk.END,
            f"Missed: "
            f"{self.total_alarms - self.acknowledged}\n"
        )

        self.report.insert(
            tk.END,
            f"Response Rate: {rate:.2f}%\n"
        )

        self.report.insert(
            tk.END,
            f"Focus Level: {level}\n"
        )

        self.report.insert(
            tk.END,
            f"Goal Status: {goal_status}\n"
        )

        self.status_label.config(
            text="Session Ended",
            fg="red"
        )


root = tk.Tk()
app = FocusApp(root)
root.mainloop()