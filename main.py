import itertools

# credits: Jack Diederich, https://youtu.be/o9pEzgHorH0?t=1163

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


# initial state is a glider
state = set([(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)])
print(state)
# propagate the state
for i in range(2):
    state = advance(state)
    print(state)
