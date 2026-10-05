import tkinter as tk
from tkinter import messagebox

from timer import PomodoroTimer
from config import (
    WORK_MINUTES,
    SHORT_BREAK_MINUTES,
    LONG_BREAK_MINUTES,
    POMODOROS_BEFORE_LONG_BREAK,
)


class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("420x520")
        self.root.resizable(False, False)

        self.timer = PomodoroTimer(
            work_minutes=WORK_MINUTES,
            short_break_minutes=SHORT_BREAK_MINUTES,
            long_break_minutes=LONG_BREAK_MINUTES,
            pomodoros_before_long_break=POMODOROS_BEFORE_LONG_BREAK,
            on_tick=self.update_display,
            on_session_complete=self.session_complete,
        )

        self.create_widgets()
        self.update_display(
            self.timer.remaining_seconds,
            self.timer.session_type,
        )

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Pomodoro Timer",
            font=("Arial", 28, "bold"),
        )
        title.pack(pady=(30, 10))

        self.session_label = tk.Label(
            self.root,
            text="WORK",
            font=("Arial", 18, "bold"),
        )
        self.session_label.pack(pady=10)

        self.time_label = tk.Label(
            self.root,
            text="25:00",
            font=("Arial", 64, "bold"),
        )
        self.time_label.pack(pady=20)

        self.status_label = tk.Label(
            self.root,
            text="Ready to focus!",
            font=("Arial", 13),
        )
        self.status_label.pack(pady=5)

        self.pomodoro_label = tk.Label(
            self.root,
            text="Completed Pomodoros: 0",
            font=("Arial", 13),
        )
        self.pomodoro_label.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=25)

        self.start_button = tk.Button(
            button_frame,
            text="Start",
            width=10,
            font=("Arial", 12),
            command=self.start_timer,
        )
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(
            button_frame,
            text="Pause",
            width=10,
            font=("Arial", 12),
            command=self.pause_timer,
        )
        self.pause_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            width=10,
            font=("Arial", 12),
            command=self.reset_timer,
        )
        self.reset_button.grid(row=0, column=2, padx=5)

        self.skip_button = tk.Button(
            self.root,
            text="Skip Session",
            width=15,
            font=("Arial", 11),
            command=self.skip_session,
        )
        self.skip_button.pack(pady=5)

    def start_timer(self):
        self.timer.start()
        self.status_label.config(text="Timer is running...")

    def pause_timer(self):
        self.timer.pause()
        self.status_label.config(text="Timer paused.")

    def reset_timer(self):
        self.timer.reset()
        self.status_label.config(text="Timer reset.")

    def skip_session(self):
        self.timer.skip()
        self.status_label.config(text="Session skipped.")

    def update_display(self, remaining_seconds, session_type):
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60

        self.time_label.config(
            text=f"{minutes:02d}:{seconds:02d}"
        )

        if session_type == "work":
            self.session_label.config(text="WORK")
        elif session_type == "short_break":
            self.session_label.config(text="SHORT BREAK")
        else:
            self.session_label.config(text="LONG BREAK")

        self.pomodoro_label.config(
            text=f"Completed Pomodoros: {self.timer.completed_pomodoros}"
        )

        self.root.title(
            f"{minutes:02d}:{seconds:02d} - Pomodoro Timer"
        )

    def session_complete(self, session_type):
        if session_type == "work":
            messagebox.showinfo(
                "Pomodoro Complete",
                "Great job! Time for a break.",
            )
        else:
            messagebox.showinfo(
                "Break Complete",
                "Break finished! Ready for the next Pomodoro?",
            )

        self.status_label.config(text="Session complete!")


def main():
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
