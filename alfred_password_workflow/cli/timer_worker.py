import sys
import time
import tkinter as tk
from tkinter import font


def ring(window, times_left):
    if times_left <= 0:
        return
    window.bell()
    window.after(700, ring, window, times_left - 1)


def main():
    seconds = int(sys.argv[1])
    message = sys.argv[2]

    time.sleep(seconds)

    root = tk.Tk()
    root.title("计时结束")
    root.attributes("-topmost", True)
    root.configure(bg="#fff4d6")
    root.geometry("760x360")
    root.resizable(False, False)

    title_font = font.Font(size=24, weight="bold")
    message_font = font.Font(size=30, weight="bold")
    button_font = font.Font(size=18, weight="bold")

    frame = tk.Frame(root, bg="#fff4d6", padx=30, pady=30)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="计时结束", bg="#fff4d6", fg="#7a3b00", font=title_font).pack(pady=(10, 24))
    tk.Label(
        frame,
        text=message,
        bg="#fff4d6",
        fg="#111111",
        font=message_font,
        wraplength=660,
        justify="center",
    ).pack(expand=True)
    tk.Button(
        frame,
        text="确定",
        command=root.destroy,
        font=button_font,
        bg="#ffb703",
        fg="#111111",
        activebackground="#fb8500",
        relief="flat",
        padx=32,
        pady=12,
    ).pack(pady=(24, 12))

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() - width) // 2
    y = (root.winfo_screenheight() - height) // 3
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.focus_force()
    ring(root, 5)
    root.mainloop()
