import timeit
import matplotlib.pyplot as plt

# Parameters of the benchmark.
MAX_LENGTH = 100
ITERATIONS = 10000
START = 1
STEP = 1

# Use built in string formatting.
def commas_format(n):
    return '{:,}'.format(n)

# s += val in a for loop.
def commas_concat(n):
    s = ''
    # Note that here and in join, we stop at n < 1000 to reduce branching.
    while n >= 1000:
        s = ',%03d' % (n % 1000) + s
        n //= 1000
    return str(n) + s

# Build a list, then join at the end.
def commas_join(n):
    lst = []
    while n >= 1000:
        lst.insert(0, '%03d' % (n % 1000))
        n //= 1000
    lst.insert(0, str(n))
    return ','.join(lst)

# String slicing, with string concatenation in a loop.
def commas_concat2(n):
    n = str(n)
    offset = len(n) % 3
    if offset == 0:
        offset = 3

    s = ''
    for i in range(len(n), 3, -3):
        s = ',' + n[i-3:i] + s
    return n[:offset] + s

# String slicing, with string appends instead of prepends.
def commas_concat3(n):
    n = str(n)
    s = ''
    offset = len(n) % 3
    if offset == 0:
        offset = 3
    if offset != 0:
        s = n[:offset]
    for i in range(offset, len(n), 3):
        s += ',' + n[i:i+3]
    return s

# String-slicing, with joined slices.
def commas_join2(n):
    n = str(n)
    lst = []
    offset = len(n) % 3
    if offset == 0:
        offset = 3
    for i in range(len(n), 3, -3):
        lst.insert(0, n[i-3:i])
    lst.insert(0, n[:offset])
    return ','.join(lst)

def commas_join3(n):
    n = str(n)
    offset = len(n) % 3
    if offset == 0:
        offset = 3
    lst = [n[:offset]]
    for i in range(offset, len(n), 3):
        lst.append(n[i:i+3])
    return ','.join(lst)

# String-slicing via list comprehension, with joined slices.
def commas_join4(n):
    n = str(n)
    offset = len(n) % 3
    if offset == 0:
        offset = 3
    lst = [n[i:i+3] for i in range(offset, len(n), 3)]
    lst.insert(0, n[:offset])
    return ','.join(lst)

# Silly regex solution. Shouldn't be faster, or is it...?
def commas_regex(n):
    import re
    s = str(n)[::-1]
    return ','.join(re.findall('..?.?', s))[::-1]

runtimes = {}
for f in [commas_format, commas_regex, commas_concat, commas_concat2, commas_concat3, commas_join, commas_join2, commas_join3, commas_join4]:
    name = f.__name__
    # Sanity check to make sure that all impls yield the same output.
    print(name, ':', f(1234567890))
    runtimes[name] = []
    n = 10 ** (START - STEP)

    for L in range(START, MAX_LENGTH, STEP):
        n *= 10 ** STEP
        runtimes[name].append(timeit.timeit(
            '%s(N)' % name,
            setup='from __main__ import %s; N=%d' % (name, n),
            number=ITERATIONS))

xs = range(START, MAX_LENGTH, STEP)
for fn in runtimes:
    plt.plot(xs, runtimes[fn], label=fn)

plt.legend()
plt.xlabel('digits')
plt.ylabel('time (s)')
plt.show()
