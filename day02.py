# Code for the 2017 Advent Of Code, day 2
# http://adventofcode.com/2017
# Michael Bell
# 12/9/2017
# Solutions valid

def checksum(spreadsheet, mode='minmax'):
    """
    Given a string SPREADSHEET with multiple lines of numbers separated by
    spaces, and each line ending with a newline character, return the 
    sum of the difference between the max and min values of each line.
    """

    rows = spreadsheet.split('\n')

    diffs = []
    for i, row in enumerate(rows):
        if len(row) == 0:
            continue
        vals = [int(n) for n in row.strip('\n').split()]
        if mode == 'minmax':
            diffs.append(max(vals) - min(vals))
        elif mode == 'div':
            pair_found = False
            for v in vals:
                for w in vals:
                    num = max([v, w])
                    den = min([v, w])

                    if num > den and num % den == 0:
                        diffs.append(num // den)
                        pair_found = True
                        break
                if pair_found:
                    break
            if not pair_found:
                raise ValueError('No pairs found in line {:}'.format(i))

    return sum(diffs)


if __name__ == "__main__":
    test_input1 = """5 1 9 5
7 5 3
2 4 6 8"""
    test_input2 = """5 9 2 8
9 4 7 3
3 8 6 5"""

    assert checksum(test_input1) == 18
    assert checksum(test_input2, 'div') == 9
    print('All tests pass')
    
    real_input = open('day02_input.txt', 'r').read()

    print("Checksum 1: {:}".format(checksum(real_input)))
    print("Checksum 2: {:}".format(checksum(real_input, 'div')))
