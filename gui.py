import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from logic import run_process

CACHE_FILE = "cache.json"


def load_cache():
	if os.path.exists(CACHE_FILE):
		try:
			with open(CACHE_FILE, "r", encoding="utf-8") as f:
				return json.load(f)
		except Exception:
			return {}
	return {}


def save_cache(monsters, output, list_file):
	data = {
		"monsters": monsters,
		"output": output,
		"list_file": list_file
	}
	try:
		with open(CACHE_FILE, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=4)
	except Exception:
		pass


def start_gui():
	root = tk.Tk()
	root.title("Monster Extractor")

	root.geometry("500x300")
	root.resizable(False, False)

	# Load cached directories
	cache = load_cache()

	# Progress bar elements
	progress_var = tk.DoubleVar()

	def update_progress(percent):
		progress_var.set(percent)
		root.update_idletasks()

	def select_monsters_folder():
		path = filedialog.askdirectory()
		if path:
			entry_monsters.delete(0, tk.END)
			entry_monsters.insert(0, path)

	def select_output_folder():
		path = filedialog.askdirectory()
		if path:
			entry_output.delete(0, tk.END)
			entry_output.insert(0, path)

	def select_list_file():
		path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
		if path:
			entry_list.delete(0, tk.END)
			entry_list.insert(0, path)

	def start_process_wrapper():
		monsters = entry_monsters.get().strip()
		output = entry_output.get().strip()
		list_file = entry_list.get().strip()

		if not monsters or not os.path.isdir(monsters):
			return messagebox.showerror("Error", "Select a valid monsters folder.")
		if not output:
			return messagebox.showerror("Error", "Select a valid output folder.")
		if not list_file or not os.path.isfile(list_file):
			return messagebox.showerror("Error", "Select a valid creatures list file.")

		# Save cache
		save_cache(monsters, output, list_file)

		# Run processing
		run_process(monsters, output, list_file, update_progress)

	tk.Label(root, text="Monsters Folder:").pack()
	entry_monsters = tk.Entry(root, width=60)
	entry_monsters.pack()
	entry_monsters.insert(0, cache.get("monsters", ""))
	tk.Button(root, text="Browse", command=select_monsters_folder).pack()

	tk.Label(root, text="Output Folder:").pack()
	entry_output = tk.Entry(root, width=60)
	entry_output.pack()
	entry_output.insert(0, cache.get("output", ""))
	tk.Button(root, text="Browse", command=select_output_folder).pack()

	tk.Label(root, text="Creature List (.txt):").pack()
	entry_list = tk.Entry(root, width=60)
	entry_list.pack()
	entry_list.insert(0, cache.get("list_file", ""))
	tk.Button(root, text="Browse", command=select_list_file).pack()

	tk.Button(root, text="Start", command=start_process_wrapper,
		bg="#4CAF50", fg="white").pack(pady=10)

	# Progress bar widget
	progress_bar = ttk.Progressbar(root, variable=progress_var, length=400)
	progress_bar.pack(pady=10)

	root.mainloop()
