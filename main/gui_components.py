import tkinter as tk
from tkinter import ttk

class GuiComponents:
    def __init__(self, root, toggle_pause, reset_timer, stop_timer):
        self.COLORS = {
            'bg': '#ffffff',           # White background
            'primary': '#2196F3',      # Blue
            'secondary': '#757575',    # Dark gray
            'accent': '#FF4081',       # Pink
            'text': '#212121',         # Almost black
            'warning': '#FF9800',      # Orange
            'danger': '#F44336'        # Red
        }
        
        self.root = root
        root.configure(bg=self.COLORS['bg'])
        
        # Configure ttk styles
        style = ttk.Style()
        for btn_style in ['Pause.TButton', 'Reset.TButton', 'Stop.TButton', 'Set.TButton']:
            style.layout(btn_style,
                        [('Button.padding', {'children':
                            [('Button.label', {'sticky': 'nswe'})],
                            'sticky': 'nswe'})])
        
        # Configure button styles
        for btn_style, bg_color, hover_color in [
            ('Pause.TButton', self.COLORS['primary'], '#1976D2'),
            ('Reset.TButton', self.COLORS['warning'], '#F57C00'),
            ('Stop.TButton', self.COLORS['danger'], '#D32F2F'),
            ('Set.TButton', self.COLORS['primary'], '#1976D2')
        ]:
            style.configure(btn_style,
                          background=bg_color,
                          foreground='white',
                          padding=(15, 8),
                          font=('Helvetica', 11, 'bold'))
            style.map(btn_style,
                     background=[('active', hover_color)],
                     foreground=[('active', 'white')])

        # Main container
        main_frame = tk.Frame(root, bg=self.COLORS['bg'], padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Threshold section
        threshold_frame = tk.LabelFrame(
            main_frame, 
            text="Time Settings", 
            bg=self.COLORS['bg'],
            fg=self.COLORS['primary'],
            font=("Helvetica", 11, "bold")
        )
        threshold_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            threshold_frame, 
            text="Time Limit:", 
            bg=self.COLORS['bg'],
            fg=self.COLORS['text'],
            font=("Helvetica", 11)
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        self.threshold_entry = ttk.Entry(
            threshold_frame,
            width=6,
            style='Custom.TEntry'
        )
        self.threshold_entry.pack(side=tk.LEFT, padx=5)
        self.threshold_entry.insert(0, "60")
        
        self.set_button = ttk.Button(
            threshold_frame,
            text="Set",
            style='Set.TButton',
            command=self.set_threshold
        )
        self.set_button.pack(side=tk.LEFT, padx=5)
        
        self.threshold_label = tk.Label(
            threshold_frame,
            text="(60s)",
            bg=self.COLORS['bg'],
            fg=self.COLORS['secondary'],
            font=("Helvetica", 11)
        )
        self.threshold_label.pack(side=tk.LEFT, padx=5)
        
        # Timer display
        timer_frame = tk.Frame(main_frame, bg=self.COLORS['bg'])
        timer_frame.pack(fill=tk.X, pady=10)
        
        self.time_label = tk.Label(
            timer_frame,
            text="0",
            font=("Helvetica", 48, "bold"),
            bg=self.COLORS['bg'],
            fg=self.COLORS['primary']
        )
        self.time_label.pack()
        
        self.status_label = tk.Label(
            timer_frame,
            text="Ready",
            font=("Helvetica", 12),
            bg=self.COLORS['bg'],
            fg=self.COLORS['secondary']
        )
        self.status_label.pack(pady=(0, 10))
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg=self.COLORS['bg'])
        button_frame.pack(fill=tk.X, pady=5)
        
        self.pause_button = ttk.Button(
            button_frame,
            text="Start",
            command=toggle_pause,
            style='Pause.TButton',
            width=12
        )
        self.pause_button.pack(pady=3)
        
        self.reset_button = ttk.Button(
            button_frame,
            text="Reset",
            command=reset_timer,
            style='Reset.TButton',
            width=12
        )
        self.reset_button.pack(pady=3)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="Stop",
            command=stop_timer,
            style='Stop.TButton',
            width=12
        )
        self.stop_button.pack(pady=3)

    def update_time_display(self, time_value):
        self.time_label.config(text=str(time_value))
        
        if time_value >= 55:
            self.time_label.config(fg=self.COLORS['danger'])
            self.status_label.config(text="Almost done!", fg=self.COLORS['danger'])
        elif time_value >= 45:
            self.time_label.config(fg=self.COLORS['warning'])
            self.status_label.config(text="Time's going by...", fg=self.COLORS['warning'])
        else:
            self.time_label.config(fg=self.COLORS['primary'])
            self.status_label.config(text="Speaking time", fg=self.COLORS['secondary'])

    def set_threshold(self):
        try:
            new_threshold = int(self.threshold_entry.get())
            if new_threshold > 0:
                self.threshold = new_threshold
                self.threshold_label.config(
                    text=f"({new_threshold}s)",
                    fg=self.COLORS['primary']
                )
                # Flash confirmation
                self.threshold_label.config(fg=self.COLORS['accent'])
                self.root.after(1000, lambda: self.threshold_label.config(fg=self.COLORS['secondary']))
            else:
                self.threshold_entry.delete(0, tk.END)
                self.threshold_entry.insert(0, str(self.threshold))
                self.threshold_label.config(
                    text="Invalid input",
                    fg=self.COLORS['danger']
                )
                self.root.after(1500, lambda: self.threshold_label.config(
                    text=f"({self.threshold}s)",
                    fg=self.COLORS['secondary']
                ))
        except ValueError:
            self.threshold_entry.delete(0, tk.END)
            self.threshold_entry.insert(0, str(self.threshold))
            self.threshold_label.config(
                text="Invalid input",
                fg=self.COLORS['danger']
            )
            self.root.after(1500, lambda: self.threshold_label.config(
                text=f"({self.threshold}s)",
                fg=self.COLORS['secondary']
            ))