import unittest
import tkinter as tk
from main.gui import SpeechTimerApp

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SpeechTimerApp(root=self.root)
    
    def test_full_cycle(self):
        """Test complete cycle of speech detection and timing"""
        # Initial state
        self.assertEqual(self.app.continuous_checker.continuous_time, 0)
        self.assertEqual(self.app.continuous_checker.session_time, 0)
        
        # Simulate speech detection
        self.app.continuous_checker.update_continuous_time(is_speaking=True)
        self.assertEqual(self.app.continuous_checker.continuous_time, 1)
        
        # Simulate pause
        self.app.continuous_checker.update_continuous_time(is_speaking=False)
        
        # Verify final state
        self.assertEqual(self.app.continuous_checker.session_time, 1)
    
    def tearDown(self):
        if hasattr(self, 'root'):
            self.root.destroy()

if __name__ == '__main__':
    unittest.main()
