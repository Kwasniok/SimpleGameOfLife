import sys
import time
import random
import itertools

# credits for the idea: Jack Diederich, https://youtu.be/o9pEzgHorH0?t=1163

# returns min, max of iterable
def min_max(iterable):
    return min(iterable), max(iterable)


# elementwise addition of two iterables
def add(lhs, rhs):
    return type(lhs)(sum(e) for e in zip(lhs, rhs))


# returns interable rhs where each element is shifted by lhs
def shift(lhs, rhs):
    return ((add(e, lhs)) for e in rhs)


def dye_red(str):
    return "".join(["\033[31m", str, "\033[0m"])


# get all neighbours of a coordinate
def neighbours_of(coord):
    x, y = coord
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1
    yield x + 1, y + 1
    yield x + 1, y - 1
    yield x - 1, y + 1
    yield x - 1, y - 1


# advance the board state (set of alive coordinates)
def advance(state):
    next_state = set()
    relevant_coords = state | set(itertools.chain(*map(neighbours_of, state)))
    for coord in relevant_coords:
        count = sum((neighbour in state) for neighbour in neighbours_of(coord))
        if count == 3 or (count == 2 and coord in state):
            next_state.add(coord)
    return next_state


def propagate(state):
    i = 0
    yield i, state
    while True:
        i += 1
        state = advance(state)
        yield i, state


SYMBOL_ALIVE = dye_red("#")
SYMBOL_DEAD = "."


def get_symbol(state, coords):
    if coords in state:
        return SYMBOL_ALIVE
    return SYMBOL_DEAD


def display(i, state):
    xs, ys = zip(*state)
    x_min, x_max = min_max(xs)
    y_min, y_max = min_max(ys)
    print("i = ", i)
    for y in range(y_max, y_min - 1, -1):
        for x in range(x_min, x_max + 1, +1):
            sys.stdout.write(get_symbol(state, (x, y)))
            sys.stdout.write(" ")
        print()


# initial state is a glider
glider = set([(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)])
state = set(glider) | set(shift((5, -5), glider))
randint = lambda: random.randint(-15, 15)
state |= set(
    zip(
        tuple(randint() for i in range(110)),
        tuple(randint() for i in range(110)),
    )
)

# propagate the state
for i, state in propagate(state):
    input()
    display(i, state)
