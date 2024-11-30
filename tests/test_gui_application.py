import unittest
import tkinter as tk
from unittest.mock import Mock, patch
from main.gui import SpeechTimerApp

class TestSpeechTimerApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up any class-level resources"""
        cls.root = tk.Tk()
    
    def setUp(self):
        """Set up test-specific resources"""
        self.app = SpeechTimerApp(root=self.root)
        # Ensure we're not actually running speech recognition
        if hasattr(self.app, 'speech_thread'):
            self.app.speech_thread = None
    
    def test_gui_updates(self):
        """Test GUI updates based on speech detection"""
        try:
            # Set initial state
            self.app.gui.continuous_speech_threshold = 5.0
            self.app.paused = False
            
            # Test below threshold
            self.app.gui.update_timer(False, 3.0, 3.0)
            self.root.update_idletasks()
            self.assertEqual(self.root.cget('bg'), "#f0f0f0", "Background should be default when below threshold")
            
            # Test above threshold
            self.app.gui.update_timer(False, 6.0, 6.0)
            self.root.update_idletasks()
            self.assertEqual(self.root.cget('bg'), "#ffcccc", "Background should be red when above threshold")
            
            # Test paused state
            self.app.gui.update_timer(True, 6.0, 6.0)
            self.root.update_idletasks()
            self.assertEqual(self.root.cget('bg'), "#f0f0f0", "Background should reset when paused")
            
        except Exception as e:
            print(f"Current bg color: {self.root.cget('bg')}")
            print(f"Paused state: {self.app.paused}")
            print(f"Current time values: {self.app.continuous_checker.continuous_time}")
            self.fail(f"Test failed with error: {str(e)}")
    
    def tearDown(self):
        """Clean up test-specific resources"""
        if hasattr(self, 'app'):
            # Stop any running threads
            if hasattr(self.app, 'speech_thread') and self.app.speech_thread:
                self.app.speech_thread = None
    
    @classmethod
    def tearDownClass(cls):
        """Clean up class-level resources"""
        if hasattr(cls, 'root'):
            cls.root.destroy()

if __name__ == '__main__':
    unittest.main()