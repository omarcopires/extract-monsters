import tkinter as tk
from tkinter import ttk


def show_scrollable_message(title, text):
	window = tk.Toplevel()
	window.title(title)
	window.geometry("500x400")

	# Main frame
	frame = ttk.Frame(window)
	frame.pack(fill="both", expand=True)

	# Vertical scrollbar
	scrollbar = ttk.Scrollbar(frame, orient="vertical")
	scrollbar.pack(side="right", fill="y")

	# Read-only text widget
	text_widget = tk.Text(
		frame,
		wrap="word",
		yscrollcommand=scrollbar.set
	)
	text_widget.pack(fill="both", expand=True)

	scrollbar.config(command=text_widget.yview)

	# Insert text and lock editing
	text_widget.insert("1.0", text)
	text_widget.config(state="disabled")
