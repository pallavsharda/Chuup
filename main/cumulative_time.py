class CumulativeTimeTracker:
    def __init__(self, speech_checker):
        """
        Tracks cumulative speaking time across multiple sessions.
        """
        self.cumulative_time = 0  # Total speaking time
        self.speech_checker = speech_checker  # Reference to `continuous_speech.py`
        self.cumulative_threshold = 0  # New: threshold for cumulative time

    def set_cumulative_threshold(self, threshold):
        """
        Sets the threshold for cumulative speaking time.
        """
        self.cumulative_threshold = threshold

    def update_cumulative_time(self):
        """
        Adds session time to cumulative time when speech ends.
        """
        self.cumulative_time = self.speech_checker.get_session_time()

    def is_cumulative_threshold_exceeded(self):
        """
        Checks if total speaking time exceeds the cumulative threshold.
        """
        return self.cumulative_threshold > 0 and self.cumulative_time >= self.cumulative_threshold

    def get_cumulative_time(self):
        """
        Returns the cumulative speaking time.
        """
        return self.cumulative_time

    def reset(self):
        """
        Resets cumulative time.
        """
        self.cumulative_time = 0