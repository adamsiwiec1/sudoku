import random as rn

# 45

s = [1,0,3,0,0,0,0,0,0]
m = max(s)
while 0 in s:
    missing_i = []
    [missing_i.append(i) if value == 0 and i is not None else None for i, value in enumerate(s)]
    not_in_s = rn.choice([x for x in range(10) if x not in s])
    s[missing_i[0]] = not_in_s

