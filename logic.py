import os
import shutil
from tkinter import messagebox

from file_utils import load_creature_list, extract_monster_name
from patterns import name_regex
from ui_utils import show_scrollable_message


def run_process(monsters_folder, output_folder, list_file):
	creatures = load_creature_list(list_file)

	exported_count = 0
	found_monsters = set()

	for root, dirs, files in os.walk(monsters_folder):
		for file in files:
			if not file.lower().endswith(".lua"):
				continue

			full_path = os.path.join(root, file)
			monster_name = extract_monster_name(full_path, name_regex)

			if not monster_name:
				continue

			if monster_name in creatures:
				found_monsters.add(monster_name)

				relative_path = os.path.relpath(root, monsters_folder)
				dest_dir = os.path.join(output_folder, relative_path)
				os.makedirs(dest_dir, exist_ok=True)
				dest_path = os.path.join(dest_dir, file)

				shutil.copy2(full_path, dest_path)
				exported_count += 1

	missing_monsters = sorted(creatures - found_monsters)

	if missing_monsters:
		msg = (
			f"Export completed!\n"
			f"Total exported: {exported_count}\n\n"
			f"Monsters NOT found:\n\n" +
			"\n".join(f"- {m}" for m in missing_monsters)
		)

		# If list is long, show scrollable window
		if len(missing_monsters) > 8:
			show_scrollable_message("Finished", msg)
		else:
			messagebox.showinfo("Finished", msg)

	else:
		messagebox.showinfo(
			"Finished",
			f"Export completed!\n"
			f"Total exported: {exported_count}\n\n"
			f"All monsters from the list were found!"
		)
