import unittest
import tkinter as tk
from unittest.mock import Mock
from main.gui_components import GuiComponents

class TestGuiComponents(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.root = tk.Tk()
        self.mock_timer = Mock()
        self.mock_timer.get_elapsed_time.return_value = 0.0
        
        # Create mock functions for callbacks
        self.mock_toggle_pause = Mock()
        self.mock_reset_timer = Mock()
        self.mock_stop_timer = Mock()
        
        # Initialize GUI components
        self.gui = GuiComponents(
            self.root,
            self.mock_timer,
            self.mock_toggle_pause,
            self.mock_reset_timer,
            self.mock_stop_timer
        )

    def tearDown(self):
        """Clean up after each test"""
        self.root.destroy()

    def test_initialization(self):
        """Test if GUI components are properly initialized"""
        # Check if all components exist
        self.assertIsInstance(self.gui.label, tk.Label)
        self.assertIsInstance(self.gui.cumulative_label, tk.Label)
        self.assertIsInstance(self.gui.pause_button, tk.Button)
        self.assertIsInstance(self.gui.reset_button, tk.Button)
        self.assertIsInstance(self.gui.stop_button, tk.Button)
        self.assertIsInstance(self.gui.threshold_entry, tk.Entry)
        
        # Check initial values
        self.assertEqual(self.gui.continuous_speech_threshold, 0)
        self.assertEqual(self.gui.label['text'], "0.0 seconds")
        self.assertEqual(self.gui.cumulative_label['text'], "Total Time: 0.0 seconds")

    def test_button_callbacks(self):
        """Test if buttons trigger their callbacks"""
        # Test pause button
        self.gui.pause_button.invoke()
        self.mock_toggle_pause.assert_called_once()
        
        # Test reset button
        self.gui.reset_button.invoke()
        self.mock_reset_timer.assert_called_once()
        
        # Test stop button
        self.gui.stop_button.invoke()
        self.mock_stop_timer.assert_called_once()

    def test_threshold_setting(self):
        """Test threshold setting functionality"""
        # Test valid threshold
        self.gui.threshold_entry.insert(0, "5.0")
        self.gui.set_threshold()
        self.assertEqual(self.gui.continuous_speech_threshold, 5.0)
        self.assertIn("Threshold set to: 5.0 seconds", 
                     self.gui.threshold_confirm_label['text'])
        
        # Test invalid threshold
        self.gui.threshold_entry.delete(0, tk.END)
        self.gui.threshold_entry.insert(0, "invalid")
        self.gui.set_threshold()
        self.assertEqual(self.gui.threshold_confirm_label['fg'], "red")
        self.assertEqual(self.gui.threshold_confirm_label['text'], 
                        "Invalid threshold value")

    def test_timer_update(self):
        """Test timer display updates"""
        # Initialize with known values
        self.gui.label = tk.Label(self.root)
        test_time = 8.0  # Use the actual value that's being set
        
        # Update the timer
        self.gui.update_timer(False, test_time, test_time)
        
        # Verify the label text matches the time we set
        expected_text = f"{test_time} seconds"
        self.assertEqual(self.gui.label['text'], expected_text)

    def test_threshold_color_change(self):
        """Test background color changes based on threshold"""
        # Set threshold
        self.gui.continuous_speech_threshold = 5.0
        
        # Test below threshold
        self.gui.update_timer(False, 3.0, 3.0)
        self.assertEqual(self.root.cget('bg'), "#f0f0f0")
        
        # Test above threshold
        self.gui.update_timer(False, 6.0, 6.0)
        self.assertEqual(self.root.cget('bg'), "#ffcccc")
 