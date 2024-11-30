import unittest
from main.continuous_speech import ContinuousSpeechChecker

class TestContinuousSpeechChecker(unittest.TestCase):
    def setUp(self):
        """Set up a fresh ContinuousSpeechChecker before each test"""
        self.checker = ContinuousSpeechChecker()

    def test_initialization(self):
        """Test initial state of the checker"""
        self.assertEqual(self.checker.continuous_time, 0)
        self.assertEqual(self.checker.threshold, 0)
        self.assertEqual(self.checker.pause_tolerance, 5)
        self.assertEqual(self.checker.current_pause, 0)
        self.assertEqual(self.checker.session_time, 0)

    def test_set_threshold(self):
        """Test threshold setting"""
        test_threshold = 10
        self.checker.set_threshold(test_threshold)
        self.assertEqual(self.checker.threshold, test_threshold)

    def test_continuous_speech(self):
        """Test continuous speech tracking"""
        # Simulate 3 seconds of continuous speech
        for _ in range(3):
            self.checker.update_continuous_time(is_speaking=True)
        
        self.assertEqual(self.checker.continuous_time, 3)
        self.assertEqual(self.checker.session_time, 3)
        self.assertEqual(self.checker.current_pause, 0)

    def test_pause_tolerance(self):
        """Test pause tolerance handling"""
        # First speak for 3 seconds
        for _ in range(3):
            self.checker.update_continuous_time(is_speaking=True)

        # Then pause for 3 seconds (within tolerance)
        for _ in range(3):
            self.checker.update_continuous_time(is_speaking=False)
        
        # Continuous time should still be 3
        self.assertEqual(self.checker.continuous_time, 3)
        self.assertEqual(self.checker.current_pause, 3)

        # Add more pauses to exceed tolerance
        for _ in range(3):
            self.checker.update_continuous_time(is_speaking=False)
        
        # Continuous time should reset
        self.assertEqual(self.checker.continuous_time, 0)

    def test_threshold_exceeded(self):
        """Test threshold detection"""
        self.checker.set_threshold(3)
        
        # Speak for 2 seconds
        for _ in range(2):
            self.checker.update_continuous_time(is_speaking=True)
        self.assertFalse(self.checker.is_threshold_exceeded())
        
        # Speak for 1 more second
        self.checker.update_continuous_time(is_speaking=True)
        self.assertTrue(self.checker.is_threshold_exceeded())

    def test_reset(self):
        """Test reset functionality"""
        # Add some speech and pauses
        for _ in range(3):
            self.checker.update_continuous_time(is_speaking=True)
        self.checker.update_continuous_time(is_speaking=False)
        
        # Reset everything
        self.checker.reset()
        
        # Check if all values are reset
        self.assertEqual(self.checker.continuous_time, 0)
        self.assertEqual(self.checker.session_time, 0)
        self.assertEqual(self.checker.current_pause, 0)