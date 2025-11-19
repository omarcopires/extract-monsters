import os

def load_creature_list(file_path):
	with open(file_path, "r", encoding="utf-8") as f:
		return {line.strip().lower() for line in f if line.strip()}


def extract_monster_name(file_path, name_regex):
	try:
		with open(file_path, "r", encoding="utf-8") as f:
			content = f.read()
			match = name_regex.search(content)
			if match:
				return match.group(1).strip().lower()
	except:
		return None
	return None
