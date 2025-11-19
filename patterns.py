import re

name_regex = re.compile(r'Game\.createMonsterType\("([^"]+)"\)')
summon_regex = re.compile(r'name\s*=\s*"([^"]+)"')
