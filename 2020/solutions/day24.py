#!/usr/bin/env python3

from utils import advent
import re

MOVEMAP = {
	'e' : ( 1,  0),
	'w' : (-1,  0),
	'se': ( 1,  1),
	'sw': ( 0,  1),
	'ne': ( 0, -1),
	'nw': (-1, -1)
}

def walk(moves):
	x, y = 0, 0

	for move in moves:
		dx, dy = MOVEMAP[move]
		x += dx
		y += dy

	return x, y

def black_adjacent(grid, x, y):
	deltas = ((1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1))
	return sum((x + dx, y + dy) in grid for dx, dy in deltas)

def all_neighbors(grid):
	deltas = ((1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1))
	return set((x + dx, y + dy) for x, y in grid for dx, dy in deltas)

def evolve(grid):
	new = set()

	for p in all_neighbors(grid):
		n = black_adjacent(grid, *p)

		if n == 2 or (n == 1 and p in grid):
			new.add(p)

	return new


advent.setup(2020, 24)
fin = advent.get_input()

grid = set() # coords of tiles with black side up
rexp = re.compile(r'e|w|se|sw|ne|nw')

for line in fin:
	moves = rexp.findall(line)
	p = walk(moves)

	if p in grid:
		grid.remove(p)
	else:
		grid.add(p)

n_black = len(grid)
advent.print_answer(1, n_black)


for _ in range(100):
	grid = evolve(grid)

n_black = len(grid)
advent.print_answer(2, n_black)