import os
import tkinter as tk
from tkinter import filedialog, messagebox

from logic import run_process


def start_gui():
	root = tk.Tk()
	root.title("Monster Extractor")

	root.geometry("500x250")
	root.resizable(False, False)

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

		# run_process already handles message windows
		run_process(monsters, output, list_file)

	tk.Label(root, text="Monsters Folder:").pack()
	entry_monsters = tk.Entry(root, width=60)
	entry_monsters.pack()
	tk.Button(root, text="Browse", command=select_monsters_folder).pack()

	tk.Label(root, text="Output Folder:").pack()
	entry_output = tk.Entry(root, width=60)
	entry_output.pack()
	tk.Button(root, text="Browse", command=select_output_folder).pack()

	tk.Label(root, text="Creature List (.txt):").pack()
	entry_list = tk.Entry(root, width=60)
	entry_list.pack()
	tk.Button(root, text="Browse", command=select_list_file).pack()

	tk.Button(root, text="Start", command=start_process_wrapper,
		bg="#4CAF50", fg="white").pack(pady=10)

	root.mainloop()
