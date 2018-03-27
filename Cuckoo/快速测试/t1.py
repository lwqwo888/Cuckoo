bl = [
    {
        "a": 1,
        "b": 2,
        "c": 3
    },
    {
        "a": 4,
        "b": 5,
        "c": 6
    }
]
al = [
    {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
    },
    {
        "a": 4,
        "b": 5,
        "c": 6,
        "d": 7
    },
    {
        "a": 102,
        "b": 103,
        "c": 6,
        "d": 7
    }
]
# for ls in [al, bl]:
#     for d in ls:
#         print d['a'], d['b']




df = set.difference(*[{d['c'] and d['a'] for d in ls} for ls in [al, bl]])
print df



# dfs = [d for d in al if d['a'] in df]
# print(dfs)