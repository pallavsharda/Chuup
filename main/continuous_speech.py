class ContinuousSpeechChecker:
    def __init__(self, pause_tolerance=5):
        self.continuous_time = 0  # Tracks uninterrupted speech time
        self.threshold = 0  # Dynamically updated from the GUI
        self.pause_tolerance = pause_tolerance
        self.current_pause = 0  # Tracks consecutive pauses
        self.session_time = 0  # Tracks overall session time

    def set_threshold(self, threshold):
        """
        Updates the speech threshold dynamically.
        """
        self.threshold = threshold

    def update_continuous_time(self, is_speaking):
        """Updates the continuous speaking time."""
        if is_speaking:
            self.continuous_time += 1
            self.session_time += 1
            self.current_pause = 0
        else:
            self.current_pause += 1
            if self.current_pause >= self.pause_tolerance:
                self.continuous_time = 0

    def reset(self):
        """
        Resets all timers and pause counters.
        """
        self.continuous_time = 0
        self.session_time = 0
        self.current_pause = 0

    def is_threshold_exceeded(self):
        """
        Checks if the speech threshold has been exceeded.
        """
        return self.continuous_time >= self.threshold

    def get_session_time(self):
        """
        Returns the total session time.
        """
        return self.session_time