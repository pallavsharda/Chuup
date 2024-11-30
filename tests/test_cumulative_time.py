import unittest
from unittest.mock import Mock
from main.cumulative_time import CumulativeTimeTracker

class TestCumulativeTimeTracker(unittest.TestCase):
    def setUp(self):
        """Set up a fresh CumulativeTimeTracker with a mock speech checker before each test"""
        self.mock_speech_checker = Mock()
        self.time_tracker = CumulativeTimeTracker(self.mock_speech_checker)

    def test_initialization(self):
        """Test initial state of the tracker"""
        self.assertEqual(self.time_tracker.cumulative_time, 0)
        self.assertIsNotNone(self.time_tracker.speech_checker)

    def test_update_cumulative_time(self):
        """Test updating cumulative time from session time"""
        # Mock the speech checker to return specific session times
        self.mock_speech_checker.get_session_time.return_value = 10
        
        # Update cumulative time
        self.time_tracker.update_cumulative_time()
        self.assertEqual(self.time_tracker.get_cumulative_time(), 10)

        # Test another update
        self.mock_speech_checker.get_session_time.return_value = 15
        self.time_tracker.update_cumulative_time()
        self.assertEqual(self.time_tracker.get_cumulative_time(), 15)

    def test_get_cumulative_time(self):
        """Test getting cumulative time"""
        # Set a known value
        self.time_tracker.cumulative_time = 25
        self.assertEqual(self.time_tracker.get_cumulative_time(), 25)

    def test_reset(self):
        """Test reset functionality"""
        # Set some initial value
        self.time_tracker.cumulative_time = 30
        
        # Reset and verify
        self.time_tracker.reset()
        self.assertEqual(self.time_tracker.get_cumulative_time(), 0)

    def test_cumulative_threshold(self):
        """Test cumulative threshold functionality"""
        # Set threshold
        self.time_tracker.set_cumulative_threshold(30)
        
        # Test below threshold
        self.mock_speech_checker.get_session_time.return_value = 20
        self.time_tracker.update_cumulative_time()
        self.assertFalse(self.time_tracker.is_cumulative_threshold_exceeded())
        
        # Test exceeding threshold
        self.mock_speech_checker.get_session_time.return_value = 35
        self.time_tracker.update_cumulative_time()
        self.assertTrue(self.time_tracker.is_cumulative_threshold_exceeded())

    def test_multiple_sessions_threshold(self):
        """Test threshold across multiple speaking sessions"""
        self.time_tracker.set_cumulative_threshold(25)
        
        # First session: 15 seconds
        self.mock_speech_checker.get_session_time.return_value = 15
        self.time_tracker.update_cumulative_time()
        self.assertFalse(self.time_tracker.is_cumulative_threshold_exceeded())
        
        # Second session: total 30 seconds
        self.mock_speech_checker.get_session_time.return_value = 30
        self.time_tracker.update_cumulative_time()
        self.assertTrue(self.time_tracker.is_cumulative_threshold_exceeded())