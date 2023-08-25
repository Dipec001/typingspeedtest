import tkinter as tk
import random
import time


class TypingSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")

        # Load previous typing speed from file
        self.previous_speed = self.load_typing_speed()

        self.sample_text = "The quick brown fox jumps over the lazy dog."
        self.current_text = tk.StringVar()

        self.label = tk.Label(root, text="Type the following text:")
        with open('typing_speed.txt') as score_file:
            data = score_file.read()
        self.label1 = tk.Label(root, text=f'Highest score recorded is {data}')
        self.text_widget = tk.Label(root, textvariable=self.current_text, wraplength=300, justify="center")
        self.entry = tk.Entry(root)
        self.start_button = tk.Button(root, text="Start Test", command=self.start_test)
        self.result_label = tk.Label(root, text="Your typing speed: ")

        self.label.pack(pady=10)
        self.label1.pack(pady=10)
        self.text_widget.pack(pady=10)
        self.entry.pack(pady=5)
        self.start_button.pack(pady=10)
        self.result_label.pack(pady=5)

    def start_test(self):
        self.start_button.config(state=tk.DISABLED)

        # Display sample text
        self.current_text.set(self.sample_text)

        # Enable typing and record start time
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.entry.bind("<KeyRelease>", self.check_typing_speed)
        self.start_time = time.time()

    def check_typing_speed(self, event):
        typed_text = self.entry.get()
        if typed_text == self.sample_text:
            self.calculate_typing_speed()
        elif self.sample_text.startswith(typed_text):
            self.current_text.set(self.sample_text[len(typed_text):])
        else:
            self.entry.delete(0, tk.END)

    def calculate_typing_speed(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        words_typed = len(self.sample_text.split())
        typing_speed_wpm = int(words_typed / (elapsed_time / 60))

        self.result_label.config(text=f"Your typing speed: {typing_speed_wpm} WPM")

        # Compare with previous speed and update if needed
        if self.previous_speed is None or typing_speed_wpm > self.previous_speed:
            self.save_typing_speed(typing_speed_wpm)

        self.entry.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)

    def load_typing_speed(self):
        try:
            with open("typing_speed.txt", "r") as file:
                return int(file.readline())
        except (FileNotFoundError, ValueError):
            return None

    def save_typing_speed(self, speed):
        with open("typing_speed.txt", "w") as file:
            file.write(str(speed))


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()
