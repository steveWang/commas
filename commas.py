import timeit
import matplotlib.pyplot as plt

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

# Silly regex solution. Shouldn't be faster, or is it...?
def commas_regex(n):
    import re
    s = str(n)[::-1]
    return ','.join(re.findall('..?.?', s))[::-1]

runtimes = {}
MAX_LENGTH = 10000
for f in [commas_format, commas_join, commas_concat, commas_regex]:
    name = f.__name__
    # Sanity check to make sure that all impls yield the same output.
    print(name, ':', f(1234567890))
    runtimes[name] = []
    for L in range(10, MAX_LENGTH, 10):
        n = 10 ** L
        runtimes[name].append(timeit.timeit(
            '%s(%d)' % (name, n),
            setup='from __main__ import %s' % name,
            number=10000 // L))

xs = range(10, MAX_LENGTH, 10)
for fn in runtimes:
    plt.plot(xs, runtimes[fn], label=fn)

plt.legend()
plt.xlabel('digits')
plt.ylabel('time (s)')
plt.show()
