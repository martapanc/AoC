#!/usr/bin/env python3

import utils

utils.setup(2018, 1)

done = False
ans = sum(map(int, utils.get_input()))

utils.submit_answer(1, ans)

seen = set()
seen.add(0)
ans = 0

while not done:
	for d in utils.get_input():
		ans += int(d)

		if ans in seen:
			ans2 = ans
			done = True
			break

		seen.add(ans)

utils.submit_answer(2, ans2)
