import tkinter as tk
from tkinter import scrolledtext


def show_scrollable_message(title, text):
	win = tk.Toplevel()
	win.title(title)
	win.geometry("500x400")

	txt = scrolledtext.ScrolledText(win, wrap=tk.WORD)
	txt.pack(expand=True, fill="both")

	txt.insert(tk.END, text)
	txt.config(state="disabled")
