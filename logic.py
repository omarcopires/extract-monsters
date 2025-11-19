import os
import shutil
from tkinter import messagebox

from file_utils import load_creature_list, extract_monster_name
from patterns import name_regex


def run_process(monsters_folder, output_folder, list_file):
	creatures = load_creature_list(list_file)
	exported = 0

	for root, dirs, files in os.walk(monsters_folder):
		for file in files:
			if not file.lower().endswith(".lua"):
				continue

			full_path = os.path.join(root, file)
			monster_name = extract_monster_name(full_path, name_regex)

			if not monster_name:
				continue

			if monster_name in creatures:
				relative_path = os.path.relpath(root, monsters_folder)
				dest_dir = os.path.join(output_folder, relative_path)
				os.makedirs(dest_dir, exist_ok=True)
				dest_path = os.path.join(dest_dir, file)

				shutil.copy2(full_path, dest_path)
				exported += 1

	messagebox.showinfo("Finished", f"Export completed!\nTotal exported: {exported}")
