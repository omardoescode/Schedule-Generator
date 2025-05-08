from functools import reduce

flatmap = lambda f, xs: reduce(lambda a, b: a + b, map(f, xs), [])
find = lambda f, xs: next((x for x in xs if f(x)), None)
