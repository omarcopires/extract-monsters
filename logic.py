import os
import shutil
from tkinter import messagebox

from file_utils import load_creature_list, extract_monster_name, extract_summon_names
from ui_utils import show_scrollable_message


def run_process(monsters_folder, output_folder, list_file, update_progress):
	creatures = load_creature_list(list_file)

	exported_monsters = 0
	exported_summons = 0

	found_monsters = set()
	found_summons = set()

	all_monster_files = {}

	# Index all monster files by name
	for root, dirs, files in os.walk(monsters_folder):
		for file in files:
			if file.lower().endswith(".lua"):
				path = os.path.join(root, file)
				name = extract_monster_name(path)
				if name:
					all_monster_files[name] = path

	total_steps = len(creatures) if len(creatures) > 0 else 1
	current_step = 0

	# Export monsters in the list
	for creature in creatures:
		current_step += 1
		update_progress((current_step / total_steps) * 100)

		if creature in all_monster_files:
			src = all_monster_files[creature]
			relative = os.path.relpath(os.path.dirname(src), monsters_folder)
			dest_dir = os.path.join(output_folder, relative)
			os.makedirs(dest_dir, exist_ok=True)

			shutil.copy2(src, os.path.join(dest_dir, os.path.basename(src)))
			exported_monsters += 1
			found_monsters.add(creature)

			# Extract summons
			summons = extract_summon_names(src)
			for summon in summons:
				if summon in all_monster_files:
					if summon not in found_summons:
						src_s = all_monster_files[summon]
						relative_s = os.path.relpath(os.path.dirname(src_s), monsters_folder)
						dest_s_dir = os.path.join(output_folder, relative_s)
						os.makedirs(dest_s_dir, exist_ok=True)

						shutil.copy2(src_s, os.path.join(dest_s_dir, os.path.basename(src_s)))
						exported_summons += 1
						found_summons.add(summon)
				else:
					found_summons.add(f"[MISSING] {summon}")

	# Missing monsters log
	missing_monsters = sorted(creatures - found_monsters)

	missing_summons = sorted(
		s for s in found_summons if s.startswith("[MISSING]")
	)

	log = (
		f"Export Finished!\n\n"
		f"Monsters exported: {exported_monsters}\n"
		f"Summons exported: {exported_summons}\n\n"
	)

	if missing_monsters:
		log += "Monsters NOT found:\n" + "\n".join(f"- {m}" for m in missing_monsters) + "\n\n"

	if missing_summons:
		log += "Summons NOT found:\n" + "\n".join(f"- {s[10:]}" for s in missing_summons) + "\n\n"

	if log.count("\n") > 15:
		show_scrollable_message("Finished", log)
	else:
		messagebox.showinfo("Finished", log)
