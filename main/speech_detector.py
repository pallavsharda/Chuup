import pyaudio
import numpy as np
import time

class SpeechRecognizer:
    def __init__(self):
        self.CHUNK = 2048
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.THRESHOLD = 0.002000
        
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        self.cumulative_speech_time = 0
        self.last_check = time.time()

    def get_speech_time(self):
        try:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            current_level = np.abs(np.frombuffer(data, dtype=np.float32)).mean()
            current_time = time.time()
            
            if current_level > self.THRESHOLD:
                self.cumulative_speech_time += current_time - self.last_check
            
            self.last_check = current_time
            return int(self.cumulative_speech_time)
            
        except IOError:
            return int(self.cumulative_speech_time)

    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()

    def __del__(self):
        self.stop()