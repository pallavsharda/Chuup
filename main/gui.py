import tkinter as tk
from speech_detector import SpeechRecognizer
from gui_components import GuiComponents

class SpeechTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chuup - Speech Timer")
        self.root.attributes('-topmost', True)
        
        # Center window
        window_width = 300
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        self.threshold = 60
        self.speech_recognizer = SpeechRecognizer()
        self.gui_components = GuiComponents(root, self.toggle_pause, self.reset_timer, self.stop_timer)
        
        # Connect the threshold
        self.gui_components.threshold = self.threshold
        self.gui_components.set_threshold = self.set_threshold
        
        self.is_running = False
        self.update_id = None

    def toggle_pause(self):
        if not self.is_running:
            self.is_running = True
            self.gui_components.pause_button.config(text="Pause")
            self.start_speech_detection()
        else:
            self.is_running = False
            self.gui_components.pause_button.config(text="Resume")
            if self.update_id:
                self.root.after_cancel(self.update_id)

    def start_speech_detection(self):
        if self.is_running:
            time_value = self.speech_recognizer.get_speech_time()
            self.gui_components.update_time_display(time_value)
            
            if time_value >= self.threshold:
                self.stop_timer()
            else:
                # Update more frequently (every 100ms instead of 1000ms)
                self.update_id = self.root.after(100, self.start_speech_detection)

    def reset_timer(self):
        self.speech_recognizer.stop()
        self.speech_recognizer = SpeechRecognizer()
        self.gui_components.update_time_display(0)
        self.is_running = False
        self.gui_components.pause_button.config(text="Start")
        if self.update_id:
            self.root.after_cancel(self.update_id)

    def stop_timer(self):
        self.speech_recognizer.stop()
        self.root.quit()

    def set_threshold(self):
        try:
            new_threshold = int(self.gui_components.threshold_entry.get())
            if new_threshold > 0:
                self.threshold = new_threshold
                return True
            return False
        except ValueError:
            return False

def main():
    root = tk.Tk()
    app = SpeechTimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()