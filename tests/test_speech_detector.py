import unittest
from unittest.mock import Mock, patch
from main.speech_detector import SpeechRecognizer
import speech_recognition as sr

class TestSpeechRecognizer(unittest.TestCase):
    def setUp(self):
        self.recognizer = SpeechRecognizer()

    def test_initialization(self):
        """Test if recognizer is properly initialized"""
        self.assertIsInstance(self.recognizer.recognizer, sr.Recognizer)

    @patch('speech_recognition.Recognizer.recognize_google')
    def test_is_speech_with_audio(self, mock_recognize):
        """Test speech detection with mock audio"""
        # Mock audio object
        mock_audio = Mock()
        
        # Test case 1: Speech detected
        mock_recognize.return_value = {'result': [{'alternative': [{'transcript': 'test'}]}]}
        self.assertTrue(self.recognizer.is_speech(mock_audio))

        # Test case 2: No speech detected
        mock_recognize.return_value = {}
        self.assertFalse(self.recognizer.is_speech(mock_audio))

    def test_is_speech_with_none(self):
        """Test speech detection with None audio"""
        self.assertFalse(self.recognizer.is_speech(None))

    @patch('speech_recognition.Recognizer.recognize_google')
    def test_is_speech_with_errors(self, mock_recognize):
        """Test speech detection error handling"""
        mock_audio = Mock()

        # Test UnknownValueError
        mock_recognize.side_effect = sr.UnknownValueError()
        self.assertFalse(self.recognizer.is_speech(mock_audio))

        # Test RequestError
        mock_recognize.side_effect = sr.RequestError("Test error")
        self.assertFalse(self.recognizer.is_speech(mock_audio)) 