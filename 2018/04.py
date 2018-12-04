#!/usr/bin/env python3

import utils
from collections import defaultdict

def get_min(event):
	return int(e[1][e[1].find(':')+1:-1])

def sum_intervals(intervals):
	return sum(b-a for a, b in intervals)

def times_slept(guard_id, minute):
	return sum(a <= minute < b for a, b in guards[guard_id])

utils.setup(2018, 4, dry_run=True)
fin = utils.get_input()

events = list(map(str.split, sorted(fin.readlines())))
assert 'begins' in events[0]

guards = defaultdict(list)

for e in events:
	if 'begins' in e:
		gid = int(e[3][1:])
		lastw = get_min(e)
	elif 'wakes' in e:
		lastw = get_min(e)
		guards[gid].append((lasts, lastw))
	elif 'falls' in e:
		lasts = get_min(e)

worst_guard = max(guards, key=lambda g: sum_intervals(guards[g]))
worst_guard_min = max(range(60), key=lambda m: times_slept(worst_guard, m))

ans = worst_guard * worst_guard_min
# assert ans == 106710

utils.submit_answer(1, ans)

worst_guard = max(guards, key=lambda g: max(times_slept(g, m) for m in range(60)))
worst_guard_min = max(range(60), key=lambda m: times_slept(worst_guard, m))

ans2 = worst_guard * worst_guard_min
# assert ans2 == 10491

utils.submit_answer(2, ans2)
