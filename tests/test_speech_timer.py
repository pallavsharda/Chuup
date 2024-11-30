import unittest
import tkinter as tk
from main.gui import SpeechTimerApp

class TestSpeechTimer(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.root = tk.Tk()
        self.app = SpeechTimerApp(root=self.root)
    
    def test_initial_state(self):
        """Test initial state of the application"""
        self.assertFalse(self.app.paused)
        self.assertEqual(self.app.continuous_checker.continuous_time, 0)
        self.assertEqual(self.app.continuous_checker.session_time, 0)
    
    def test_speech_detection(self):
        """Test speech detection and timing functionality"""
        initial_continuous = self.app.continuous_checker.continuous_time
        initial_session = self.app.continuous_checker.session_time
        
        # Simulate 2 seconds of continuous speech
        self.app.continuous_checker.update_continuous_time(is_speaking=True)
        self.app.continuous_checker.update_continuous_time(is_speaking=True)
        
        self.assertEqual(self.app.continuous_checker.continuous_time, initial_continuous + 2)
        self.assertEqual(self.app.continuous_checker.session_time, initial_session + 2)
        self.assertEqual(self.app.continuous_checker.current_pause, 0)
    
    def test_pause_detection(self):
        """Test pause detection and continuous time reset"""
        PAUSE_THRESHOLD = 5  # Define the expected pause threshold
        
        # Initial speaking period
        self.app.continuous_checker.update_continuous_time(is_speaking=True)
        self.app.continuous_checker.update_continuous_time(is_speaking=True)
        initial_continuous = self.app.continuous_checker.continuous_time
        
        # Simulate pause period
        for i in range(PAUSE_THRESHOLD + 1):
            self.app.continuous_checker.update_continuous_time(is_speaking=False)
            if i < PAUSE_THRESHOLD - 1:
                # Check continuous time before threshold
                self.assertEqual(self.app.continuous_checker.continuous_time, initial_continuous,
                               f"Continuous time should remain {initial_continuous} before threshold")
            else:
                # Check continuous time is reset after threshold
                self.assertEqual(self.app.continuous_checker.continuous_time, 0,
                               "Continuous time should reset to 0 after threshold")

    def tearDown(self):
        """Clean up after each test"""
        if hasattr(self, 'root'):
            self.root.destroy()

if __name__ == '__main__':
    unittest.main() 