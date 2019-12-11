AoC 2019 walkthrough
====================

Day 1 - The Tyranny of the Rocket Equation
------------------------------------------

[Problem statement][d01-problem] — [Complete solution][d01-solution]

### Part 1

We are given a list of integers as input:

```python
numbers = tuple(map(int, fin.readlines()))
```

We are asked to first apply a function to all of them, and them sum all the
results. The function is `x / 3 - 2`, where the division is an *integer*
division.

We can simply use the built-in [`map()`][py-map] and [`sum()`][py-sum] functions
to solve this in one line:

```python
total = sum(map(lambda n: n // 3 - 2, numbers))
print('Part 1:', total)
```

### Part 2

For the second part, we are asked to repeatedly apply the same function to each
number until it gets to zero (or under zero, in which case we should just treat
is as a zero). Then again, sum every single value we get after applying the
function.

```python
total = 0
for n in numbers:
	while n > 0:
		n = max(n // 3 - 2)
		total += n

print('Part 2:', total)
```

First puzzle of the year, so not really that much of a challenge, but still fun!


Day 2 - 1202 Program Alarm
--------------------------

[Problem statement][d02-problem] — [Complete solution][d02-solution]

### Part 1

Okay, I was not expecting a custom virtual machine for day 2, but here we go I
guess!

We are introduced to "Intcode", machine-code language that only uses integers.
The program source code is a list of integers separated by commas:

```python
program = list(map(int, fin.read().split(',')))
```

We are given instructions on how to interpret the numbers. In particular, there
are three [opcodes](https://en.wikipedia.org/wiki/Opcode):

- The value `1` means *add* together the values at the positions indicated by
  the next two numbers, and store the result at the position indicated by the
  third, then move forward 4 positions to get to the next instruction.
- The value `2` means *multiply*, and it works the same as *add*, except the
  operation is a multiplication.
- The value `99` means *stop*.

We are asked to set `program[0] = 1` and `program[1] = 12` before starting, and
then run the Intcode program until it halts: the output will be at position `0`.

Quite simple, we can just emuate it with a loop. To make it fancier, we can
import [`add`][py-operator-add] and [`mul`][py-operator-mul] from the
[`operator` module][py-operator] and use them instead of a chain of `if/elif`:
`add()` is a function that takes two arguments and performs the same operation
of the `+` operator, while `mul()` does the same for the `*` operator. Using
these might also come in handy if in the future more operations are added (we
could just have a dictionary of `{opcode: operator}`).

```python
from operator import add, mul

def run(program, v0, v1):
	program[0] = v0
	program[1] = v1
	pc = 0

	while program[pc] != 99:
		opcode = program[pc]
		op = add if op == 1 else mul
		program[pc + 1] = op(program[pc + 2], program[pc + 3])
		pc += 4

	return program[0]

output = run(program[:], 1, 12)
print('Part 1:', output)
```

I use `program[:]` here to create a copy of the list, instead of passing the
list itself, which would modify it irrevocably.

### Part 2

For the second part, we are asked to determine which pair of inputs produces the
output `19690720`. Both the input values are between `0` and `99` (included), so
we can just run a brute-force search trying all of them:

```python
for a in range(100):
	for b in range(100):
		if run(program[:], a, b) == 19690720:
			break

print('Part 2:', a * 100 + b)
```


Day 3 - Crossed Wires
---------------------

[Problem statement][d03-problem] — [Complete solution][d03-solution]

### Part 1

We are given two lines, each one is a list of moves in a 2D grid. There are two
wires, and each line represents a wire. Starting from the same position, the
moves describe the path that each wire takes on the grid.

A move is represented as a letter which tells us the direction of the move (`L`,
`R`, `U`, `D`) followed by a number which tells us how many steps to move in
such direction.

The two wires will intersect each other, and we are asked to calculate the
Manhattan distance from the origin to the closest intersection.

First, parse the moves with [`map()`][py-map] and a simple funciton that takes a
string and splits it into direction and number of steps.

```python
def make_move(s):
	return s[0], int(s[1:])

lines = fin.readlines()
moves1 = tuple(map(make_move, line[0].split(',')))
moves2 = tuple(map(make_move, line[1].split(',')))
```

Now, since we need to calculate the intersections of the two paths, a `set`
comes in handy. For each wire, we start from the same arbitrary position, like
`(0, 0)` and then move one step at a time, each time updating the position
adding it to the set of visited positions.

```python
MOVE_DX = {'U': 0, 'D':  0, 'R': 1, 'L': -1}
MOVE_DY = {'U': 1, 'D': -1, 'R': 0, 'L':  0}

def get_visited(moves):
	visited = set()
	p = (0, 0)

	for d, n in moves:
		for _ in range(n):
			p = (p[0] + MOVE_DX[d], p[1] + MOVE_DY[d])
			visited.add(p)

	return visited

visited1 = get_visited(moves1)
visited2 = get_visited(moves2)
```

The two dictionaries `MOVE_DX` and `MOVE_DY` are just a common trick to make it
easier to apply a delta given a direction, instead of writing a long chain of
`if/ifelse` statements with a bunch of different assignments.

We then get the intersection of the two sets, and calculate the Manhattan
distance from each point to the origin, keeping the lowest value. Since the
originis `(0, 0)` the Manhattan distance from a point to the origin is simply
the sum of the absolute values of the two coordinates of the point.

```python
def manhattan(p):
	return abs(p[0]) + abs(p[1])

intersections = visited1 & visited2
min_distance = min(map(manhattan, intersections))
print('Part 1:', min_distance)
```

### Part 2

We are now asked to calculate the shortest cumualative distance (in steps) that
wires must travel to reach an intersection point. If a wire visits the same
position multiple times, we need to use the lowest number of steps it took to
get there.

Counting the steps is easy. For the second requirement we can just use a
dictionary `{position: n_steps}` to remember the lowest number of steps to get
to each position. We can easily modify the previously written function to also
count steps.

```python
def get_visited_and_steps(moves):
	p = (0, 0)
	cur_steps = 0
	visited = set()
	steps = {}

	for d, n in moves:
		for _ in range(n):
			p = (p[0] + MOVE_DX[d], p[1] + MOVE_DY[d])
			visited.add(p)
			cur_steps += 1

			if p not in steps:
				steps[p] = cur_steps

	return visited, steps

visited1, steps1 = get_visited(moves1)
visited2, steps2 = get_visited(moves2)
intersections = visited1 & visited2
best = min(steps1[p] + steps2[p] for p in intersections)
print('Part 2:', best)
```


Day 4 - Secure Container
------------------------

[Problem statement][d04-problem] — [Complete solution][d04-solution]

### Part 1

Bruteforcing passwords! We are given the lower and upper bounds for the value of
a six-digit password, and we need to determine how many valid passwords are in
such range.

A valid password must:

- Have at least two adjacent matching digits.
- Be composed of non-decreasing digits (from left to right).

An iterator over pairs of adjacent characters of a string can be easily obtained
using the [`zip()`][py-zip] build-in functon. If we convert our values in string
form: this will make our life much easier.

```python
digits = str(value)
pairs = tuple(zip(digits, digits[1:]))
```

To check if there are at least two adjavent matching digits, we can iterate over
the pairs of adjacent digits and check if any pair of equal digits exists using
the [`any()`][py-any] build-in function.

```python
has_matching_pair = any(a == b for a, b in pairs)
```

As per the second requirement, to check if a number is only composed of
non-decreasing digits, we can iterate over the pairs of adjacent digits and use
the [`all()`][py-all] build-in function to check if the condition is met for
each pair.

```python
is_non_decreasing = all(a <= b for a, b in pairs)
```

Now that we have the primitives to check if a value is a valid password, we can
simply bruteforce all the possible values in the given range and count how many
of them pass the checks:

```python
lo, hi = map(int, fin.read().split('-'))
n_valid = 0

for pwd in range(lo, hi + 1):
	digits = str(pwd)
	pairs = tuple(zip(digits, digits[1:]))

	is_non_decreasing = all(a <= b for a, b in pairs)
	has_matching_pair = any(a == b for a, b in pairs)

	if is_non_decreasing and has_matching_pair:
		n_valid += 1

print('Part 1:', n_valid)
```

### Part 2

For the second part, another constraint is added for the validity of a password:

- The two adjacent matching digits are not part of a larger group of matching
  digits.

This can be tricky to understand. To make it clearer, we can also say it like
this:

- There is at least one group of exactly two *isolated* adjacent matching
  digits.

To check if a group of two equal digits is isolated, we now need an iterator
over a *quadruplet* of consecutive digits. We can use [`zip()`][py-zip] as
before:

```python
quadruplets = zip(digits, digits[1:], digits[2:], digits[3:])
```

Then, using the same [`any()`][py-any] function as before, we also need to
account for isolated digits at the beginning and at the end of the string. We
can just cheat and add two random characters to the extremes of the string.

```python
digits = 'x' + digits + 'x'
has_isolated = any(a != b and b == c and c != d for a, b, c, d in quadruplets)
```

We can now count the number of valid passwords again:

```python
n_valid = 0

for pwd in range(lo, hi + 1):
	digits = str(pwd)
	pairs = zip(digits, digits[1:])
	quadruplets = zip(digits, digits[1:], digits[2:], digits[3:])

	is_non_decreasing = all(a <= b for a, b in pairs)
	has_isolated = any(a != b and b == c and c != d for a, b, c, d in quadruplets)

	if is_non_decreasing and has_isolated:
		n_valid += 1

print('Part 2:', n_valid)
```

Notice that wrapping `zip(digits, digits[1:])` into `tuple()` is not needed
anymore now, since we only use the iterator once.


Day 5 - Sunny with a Chance of Asteroids
----------------------------------------

[Problem statement][d05-problem] — [Complete solution][d05-solution]

**Disclaimer**: my complete solution for this problem uses an `IntcodeVM` class
that I wrote on day 5 after solving the problem, so it's not the same solution
as described below. The VM will come in handy for future days. It will allow me
to simply do `from lib.intcode import IntcodeVM` to solve Intcode-related
problems. Here's [the Intcode library][lib] I wrote and used.

### Part 1

Second Intcode puzzle of the year. In addition to what we know from day 2, now
two more opcodes are added:

- Opcode `3`: take an integer as *input* and store it in the position indicated
  by the (only) given parameter (length: 2).
- Opcode `4`: *output* the value of the (only) given parameter (length: 2).

In addition to this, now opcode parameters become more complex to handle. In
particular, each opcode is either 1 or 2 digits. Every other more significant
digit is a *parameter mode* for the corresponding parameter.

Parameter modes are:

- `0`: position mode, the parameter refers to a memory address (that is, a
  position). The value to use is the number stored at that address. For
  destination parameters, it is still the location where to write.
- `1`: immediate mode, the parameter itself is interpreted as the value to use.
  This mode is not allowed for destination parameters.

Leading zero digits are left off. So, for example, `1002,2,3,4` now means:
`program[4] = program[2] + 3`, since parameter modes are (from left to right)
`0`, `1` and `0` (implicit leading zero).

The program we are given will only request one input, and we should provide it
with `1` as the only input value. It then outputs a series of numbers, and we
need to get the last one.

This parameter mode thing complicates our solution a fair amount, but it's still
doable. We now need to fetch the modes first, then evaluate them to compute the
needed values. Let's drop the use of the [`operator`][py-operator] module from
day 2, as it didn't turn out to be useful.

To parse opcode and parameter modes, we can just use integer division and
modulo:

```python
modes  = ((op // 100) % 10, (op // 1000) % 10, (op // 10000) % 10)
```

Other than this, we now need to look into memory only if the mode is `0`,
otherwise we can use the parameter value as is. We can just use an `if` for
this.

```python
param1 = prog[pc + 1]
if modes[0] == 0:
	param1 = prog[param1]
```

Our previously written `run()` function now becomes:

```python
def run(prog, input_value):
	pc = 0
	lastout = None

	while prog[pc] != 99:
		op = prog[pc]
		modes = ((op // 100) % 10, (op // 1000) % 10, (op // 10000) % 10)
		op = op % 10

		if op == 1: # add
			a, b, c = prog[pc + 1:pc + 4]
			if modes[0] == 0: a = prog[a]
			if modes[1] == 0: b = prog[b]
			prog[c] = a + b
			pc += 4
		elif op == 2: # mul
			a, b, c = prog[pc + 1:pc + 4]
			if modes[0] == 0: a = prog[a]
			if modes[1] == 0: b = prog[b]
			prog[c] = a * b
			pc += 4
		elif op == 3: # in
			a = prog[pc + 1]
			prog[a] = input_value
			pc += 2
		elif op == 4: # out
			a = prog[pc + 1]
			if modes[0] == 0: a = prog[a]
			lastout = a
			pc += 2

	return lastout
```

Cool, now let's just run it against our input and it's done:

```python
program = list(map(int, fin.read().split(',')))
result = run(program[:], 1)
print('Part 1:', result)
```

### Part 2

Ok, now things starts to get messy... four more opcodes are added:

- Opcode `5` is *jump if true*: if the first parameter is non-zero, it sets the
  instruction pointer to the value from the second parameter. Otherwise, it does
  nothing.
- Opcode `6` is *jump if false*: if the first parameter is zero, it sets the
  instruction pointer to the value from the second parameter. Otherwise, it does
  nothing.
- Opcode `7` is *less than*: if the first parameter is less than the second
  parameter, it stores `1` in the position given by the third parameter.
  Otherwise, it stores `0`.
- Opcode `8` is *equals*: if the first parameter is equal to the second
  parameter, it stores 1 in the position given by the third parameter.
  Otherwise, it stores `0`.

In addition to this, of course the new opcodes all need to support the parameter
modes described in part 1. The program now will need to be run with `5` as its
only input, and we still need to get the last output value.

The good thing is, the code we just wrote can be easily extended to support
these, we just need four more `elif` branches. To implement *less than* and
*equals*, and also for updating the program counter for the jump instructions,
Python [onditional expressions][py-cond-expr] come in handy:

```python
# less than:
prog[param3] = 1 if param1 < param2 else 0
```

Here are the added opcodes (continuing from the last branch in the previous
snippet):

```python
		#...

		elif op == 5: # jnz
			a, b = prog[pc + 1:pc + 3]
			if modes[0] == 0: a = prog[a]
			if modes[1] == 0: b = prog[b]
			pc = b if a != 0 else pc + 3
		elif op == 6: # jz
			a, b = prog[pc + 1:pc + 3]
			if modes[0] == 0: a = prog[a]
			if modes[1] == 0: b = prog[b]
			pc = b if a == 0 else pc + 3
		elif op == 7: # lt
			a, b, c = prog[pc + 1:pc + 4]
			if modes[0] == 0: a = prog[a]
			if modes[1] == 0: b = prog[b]
			prog[c] = 1 if a < b else 0
			pc += 4
		elif op == 8: # eq
			a, b, c = prog[pc + 1:pc + 4]
			if modes[0] == 0: a = prog[a]
			if modes[1] == 0: b = prog[b]
			prog[c] = 1 if a == b else 0
			pc += 4
```

Now we can just run the program with the updated code and the new input to get
the answer:

```python
result = run(program[:], 5)
print('Part 2:', result)
```


[d01-problem]: https://adventofcode.com/2019/day/1
[d02-problem]: https://adventofcode.com/2019/day/2
[d03-problem]: https://adventofcode.com/2019/day/3
[d04-problem]: https://adventofcode.com/2019/day/4
[d05-problem]: https://adventofcode.com/2019/day/5
[d01-solution]: day01_clean.py
[d02-solution]: day02_clean.py
[d03-solution]: day03_clean.py
[d04-solution]: day04_clean.py
[d05-solution]: day05_clean.py

[py-map]: https://docs.python.org/3.7/library/functions.html#map
[py-sum]: https://docs.python.org/3.7/library/functions.html#sum
[py-zip]: https://docs.python.org/3.7/library/functions.html#zip
[py-any]: https://docs.python.org/3.7/library/functions.html#any
[py-all]: https://docs.python.org/3.7/library/functions.html#all
[py-operator]: https://docs.python.org/3.7/library/operator.html
[py-operator-add]: https://docs.python.org/3.7/library/operator.html#operator.add
[py-operator-mul]: https://docs.python.org/3.7/library/operator.html#operator.mul