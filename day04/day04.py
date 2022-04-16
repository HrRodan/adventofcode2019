x1 = 264793
x2 = 803935

count_correct_pw = 0
count_correct_pw_part2 = 0
for n in range(x1, x2 + 1):
    a, b, c, d, e, f = [int(x) for x in str(n)]
    if a <= b <= c <= d <= e <= f:
        if a == b or b == c or c == d or d == e or e == f:
            count_correct_pw += 1
            if (a == b != c) or (a != b == c != d) or (b != c == d != e) or (c != d == e != f) or (d != e == f):
                count_correct_pw_part2 += 1


print(count_correct_pw)
print(count_correct_pw_part2)
