#!/usr/bin/env python3

from utils import advent

advent.setup(2018, 1, dry_run=True)
fin = advent.get_input()

deltas = list(map(int, fin.readlines()))
done = False
freq = 0
seen = set()
seen.add(0)

for d in deltas:
	freq += d

	if not done and freq in seen:
		done = True

	seen.add(freq)

assert freq == 435
advent.submit_answer(1, freq)

while not done:
	for d in deltas:
		freq += d

		if freq in seen:
			done = True
			break

		seen.add(freq)

assert freq == 245
advent.submit_answer(2, freq)
