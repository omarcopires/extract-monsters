import re
from pathlib import Path

from patterns import name_regex


def load_creature_list(file_path: str):
	with open(file_path, "r", encoding="utf-8") as f:
		return {line.strip().lower() for line in f if line.strip()}


def extract_monster_name(file_path: str) -> str | None:
	try:
		text = Path(file_path).read_text(encoding="utf-8")
		m = name_regex.search(text)
		if m:
			return m.group(1).strip().lower()
	except Exception:
		return None
	return None


def extract_summon_names(file_path: str):
	"""
	Extract summons STRICTLY inside monster.summon block.

	This guarantees that loot is NOT captured.
	"""
	try:
		text = Path(file_path).read_text(encoding="utf-8")
	except Exception:
		return []

	# Step 1 → find ONLY the summon block
	block_match = re.search(
		r"monster\.summon\s*=\s*\{([\s\S]*?)\}\s*$",
		text,
		re.MULTILINE
	)

	if not block_match:
		return []

	block = block_match.group(1)

	# Step 2 → extract ONLY name="..." inside the summon block
	names = re.findall(
		r'name\s*=\s*"([^"]+)"',
		block
	)

	# Unique + lower
	out = []
	seen = set()
	for n in names:
		nl = n.lower().strip()
		if nl not in seen:
			seen.add(nl)
			out.append(nl)

	return out
