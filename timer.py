class PomodoroTimer:
    def __init__(
        self,
        work_minutes,
        short_break_minutes,
        long_break_minutes,
        pomodoros_before_long_break,
        on_tick=None,
        on_session_complete=None,
    ):
        self.work_seconds = work_minutes * 60
        self.short_break_seconds = short_break_minutes * 60
        self.long_break_seconds = long_break_minutes * 60

        self.pomodoros_before_long_break = (
            pomodoros_before_long_break
        )

        self.on_tick = on_tick
        self.on_session_complete = on_session_complete

        self.session_type = "work"
        self.remaining_seconds = self.work_seconds

        self.completed_pomodoros = 0
        self.running = False
        self._after_id = None

    def start(self):
        if self.running:
            return

        self.running = True
        self._run_timer()

    def pause(self):
        self.running = False

        if self._after_id is not None:
            self._cancel_scheduled_callback()
            self._after_id = None

    def reset(self):
        self.pause()

        self.session_type = "work"
        self.remaining_seconds = self.work_seconds
        self.completed_pomodoros = 0

        self._notify_tick()

    def skip(self):
        self.pause()
        self._finish_session()

    def _run_timer(self):
        if not self.running:
            return

        self._notify_tick()

        if self.remaining_seconds <= 0:
            self._finish_session()
            return

        self.remaining_seconds -= 1

        self._after_id = self._schedule_next_tick()

    def _finish_session(self):
        completed_session = self.session_type

        if completed_session == "work":
            self.completed_pomodoros += 1

        if self.on_session_complete:
            self.on_session_complete(completed_session)

        self._move_to_next_session()

        if self.running:
            self._run_timer()
        else:
            self._notify_tick()

    def _move_to_next_session(self):
        if self.session_type == "work":
            if (
                self.completed_pomodoros
                % self.pomodoros_before_long_break
                == 0
            ):
                self.session_type = "long_break"
                self.remaining_seconds = self.long_break_seconds
            else:
                self.session_type = "short_break"
                self.remaining_seconds = self.short_break_seconds

        else:
            self.session_type = "work"
            self.remaining_seconds = self.work_seconds

    def _notify_tick(self):
        if self.on_tick:
            self.on_tick(
                self.remaining_seconds,
                self.session_type,
            )

    def _schedule_next_tick(self):
        """
        The timer class expects the callback to be supplied
        by the GUI. This method is replaced by the GUI through
        set_scheduler().
        """
        if hasattr(self, "_scheduler"):
            return self._scheduler(self._run_timer)

        return None

    def _cancel_scheduled_callback(self):
        if hasattr(self, "_canceller") and self._after_id is not None:
            self._canceller(self._after_id)

    def set_scheduler(self, scheduler, canceller):
        self._scheduler = scheduler
        self._canceller = canceller
