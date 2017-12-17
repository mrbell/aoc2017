"""
Code for the 2017 Advent Of Code, day 11
https://adventofcode.com/2017/day/11
Michael Bell
12/16/2017
Solutions passed
"""


def parse_steps(steps):
    if not steps:
        steps = []
    elif isinstance(steps, str):
        steps = steps.replace(' ', '').split(',')
    return steps


def count_min_steps(steps):
    steps = reduce_steps(steps)
    return len(steps)


def balance_steps(steps, dir1, dir2):

    steps_reduced = []

    dir1_steps = [step for step in steps if step == dir1]
    dir2_steps = [step for step in steps if step == dir2]
    other_steps = [
        step for step in steps if step != dir1 and step != dir2
    ]

    if len(dir1_steps) > len(dir2_steps):
        dir1_steps = [dir1 for _ in range(len(dir1_steps) - len(dir2_steps))]
        dir2_steps = []
    else:
        dir2_steps = [dir2 for _ in range(len(dir2_steps) - len(dir1_steps))]
        dir1_steps = []

    other_steps.extend(dir1_steps)
    other_steps.extend(dir2_steps)

    return other_steps


def replace_step_pairs(steps, dir_pair, new_dir):
    dir1_steps = [step for step in steps if step == dir_pair[0]]
    dir2_steps = [step for step in steps if step == dir_pair[1]]

    new_dir_steps = [
        new_dir for dir1, dir2 in zip(dir1_steps, dir2_steps)
    ]

    if len(dir1_steps) > len(dir2_steps):
        dir1_steps = [dir_pair[0]] * (len(dir1_steps) - len(dir2_steps))
        dir2_steps = []
    else:
        dir2_steps = [dir_pair[1]] * (len(dir2_steps) - len(dir1_steps))
        dir1_steps = []

    other_steps = [step for step in steps if step not in dir_pair] 

    other_steps.extend(new_dir_steps)
    other_steps.extend(dir1_steps)
    other_steps.extend(dir2_steps)

    return other_steps

def reduce_steps(steps):

    steps = parse_steps(steps)

    iter = 0

    while True and len(steps) > 0:
        n_steps_start = len(steps)

        steps = balance_steps(steps, 'n', 's')
        steps = balance_steps(steps, 'ne', 'sw')
        steps = balance_steps(steps, 'nw', 'se')

        steps = replace_step_pairs(steps, ['ne', 's'], 'se')
        steps = replace_step_pairs(steps, ['nw', 's'], 'sw')

        steps = replace_step_pairs(steps, ['se', 'n'], 'ne')
        steps = replace_step_pairs(steps, ['sw', 'n'], 'nw')

        steps = replace_step_pairs(steps, ['ne', 'nw'], 'n')
        steps = replace_step_pairs(steps, ['se', 'sw'], 's')
  
        iter += 1

        if len(steps) == n_steps_start:
            break

    return steps


def max_distance_from_start(steps):
    """
    Given a set of steps to take on a hex grid, return the maximum distance
    (in min steps from the origin) that was visited.
    """

    steps = parse_steps(steps)

    max_dist = -1
    # max_dist_steps = -1

    for i, step in enumerate(steps):

        min_steps = count_min_steps(steps[:(i+1)])
        if min_steps > max_dist:
            max_dist = min_steps
            # max_dist_steps = i + 1

    return max_dist

with open('data/day11_input.txt', 'r') as f:
    PUZZLE_INPUT = f.read()


if __name__ == '__main__':
    # TESTS

    assert count_min_steps('') == 0
    assert balance_steps(['n', 'n', 's', 's'], 'n', 's') == []
    assert balance_steps(['n', 'n'], 'n', 's') == ['n', 'n']
    assert replace_step_pairs(['ne', 'ne'], ['ne', 's'], 'se') == ['ne', 'ne']
    assert sorted(
        balance_steps(['n', 's', 'ne', 'sw', 's', 's'], 'n', 's')
    ) == ['ne', 's', 's', 'sw']
    assert sorted(
        replace_step_pairs(['n', 's', 'ne', 'sw', 's', 's'], ['ne', 's'], 'se')
    ) == ['n', 's', 's', 'se', 'sw']

    assert max_distance_from_start('ne,ne,sw,sw') == 2
    assert max_distance_from_start('ne,ne,ne') == 3

    assert count_min_steps('ne,ne,ne') == 3
    assert count_min_steps('ne,ne,sw,sw') == 0
    assert count_min_steps('ne,ne,s,s') == 2
    assert count_min_steps('se,sw,se,sw,sw') == 3

    print('Tests passed!')

    print('Solution 1: {:}'.format(count_min_steps(PUZZLE_INPUT)))
    print('Solution 2: {:}'.format(max_distance_from_start(PUZZLE_INPUT)))
