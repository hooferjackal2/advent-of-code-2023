def find_symmetry(lists, part):
    symsum = 0
    length = len(lists)
    for i in range(1, length):
        dist = min(i, length - i)
        asymmetric = 0
        fixable = 0
        for j in range(dist):
            if lists[i + j] != lists[i - j - 1]:
                asymmetric += 1
                strs = zip(lists[i + j], lists[i - j - 1])
                smudges = len([1 for x, y in strs if x != y])
                if smudges == 1:
                    fixable += 1
        if part == 1 and asymmetric == 0:
            symsum += i
        if part == 2 and asymmetric == 1 and fixable == 1:
            symsum += i
    return symsum


def day13(filename, part):
    with open(filename) as f: patterns = ''.join(f.readlines()).strip().split('\n\n')
    colsum = 0
    rowsum = 0
    for pattern in patterns:
        rows = pattern.split('\n')
        cols = [''.join([row[i] for row in rows]) for i in range(len(rows[0]))]
        rowsum += find_symmetry(rows, part)
        colsum += find_symmetry(cols, part)
    return 100*rowsum + colsum


print(day13('input', 1))
print(day13('input', 2))
