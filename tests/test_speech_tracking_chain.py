import unittest
from main.speech_detector import SpeechRecognizer
from main.continuous_speech import ContinuousSpeechChecker
from main.cumulative_time import CumulativeTimeTracker

class TestSpeechTrackingChain(unittest.TestCase):
    def setUp(self):
        """Set up the complete chain of components"""
        self.speech_checker = ContinuousSpeechChecker(pause_tolerance=2)
        self.cumulative_tracker = CumulativeTimeTracker(self.speech_checker)
        
        # Set thresholds for testing
        self.speech_checker.set_threshold(5)  # 5 seconds continuous threshold
        self.cumulative_tracker.set_cumulative_threshold(10)  # 10 seconds total threshold

    def test_continuous_to_cumulative(self):
        """Test if continuous speech properly updates cumulative time"""
        # Simulate 3 seconds of continuous speech
        for _ in range(3):
            self.speech_checker.update_continuous_time(is_speaking=True)
            self.cumulative_tracker.update_cumulative_time()

        # Check both continuous and cumulative times
        self.assertEqual(self.speech_checker.continuous_time, 3)
        self.assertEqual(self.cumulative_tracker.get_cumulative_time(), 3)

    def test_pause_handling(self):
        """Test how pauses affect both continuous and cumulative time"""
        # Speak for 3 seconds
        for _ in range(3):
            self.speech_checker.update_continuous_time(is_speaking=True)
            self.cumulative_tracker.update_cumulative_time()

        # Pause for 3 seconds (exceeds pause_tolerance of 2)
        for _ in range(3):
            self.speech_checker.update_continuous_time(is_speaking=False)
            self.cumulative_tracker.update_cumulative_time()

        # Continuous time should reset, but cumulative should remain
        self.assertEqual(self.speech_checker.continuous_time, 0)
        self.assertEqual(self.cumulative_tracker.get_cumulative_time(), 3)

    def test_threshold_interactions(self):
        """Test how both continuous and cumulative thresholds interact"""
        # Speak for 6 seconds (exceeds continuous threshold of 5)
        for _ in range(6):
            self.speech_checker.update_continuous_time(is_speaking=True)
            self.cumulative_tracker.update_cumulative_time()

        # Check both threshold exceeded conditions
        self.assertTrue(self.speech_checker.is_threshold_exceeded())
        self.assertFalse(self.cumulative_tracker.is_cumulative_threshold_exceeded())  # Not yet exceeded

        # Speak for 5 more seconds (exceeds cumulative threshold of 10)
        for _ in range(5):
            self.speech_checker.update_continuous_time(is_speaking=True)
            self.cumulative_tracker.update_cumulative_time()

        self.assertTrue(self.cumulative_tracker.is_cumulative_threshold_exceeded())

    def test_reset_propagation(self):
        """Test if reset properly cascades through components"""
        # Add some speech time
        for _ in range(5):
            self.speech_checker.update_continuous_time(is_speaking=True)
            self.cumulative_tracker.update_cumulative_time()

        # Reset both components
        self.speech_checker.reset()
        self.cumulative_tracker.reset()

        # Verify everything is reset
        self.assertEqual(self.speech_checker.continuous_time, 0)
        self.assertEqual(self.speech_checker.session_time, 0)
        self.assertEqual(self.cumulative_tracker.get_cumulative_time(), 0)
