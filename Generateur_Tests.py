from scipy.stats import  kstest
from Generateur_LCG import PRNG

dices_results = []
for i in range(0,1000):
    dice1 = int(PRNG(1,7))
    dice2 = int(PRNG(1,7))
    dices_results.append(dice1 + dice2)

def countOccurrences(lst, x):
    #Count occurrences to determine observed frequencies
    res = 0
    for i in lst:
        if i == x:
            res += 1
    return res

dices_observed = 11 * [None]
for y in range(0,11):
    dices_observed[y] = countOccurrences(dices_results, 2 + y)

dices_expected = [27, 55, 83, 111, 138, 166, 138, 111, 83, 55, 27]

ks = kstest(dices_observed, dices_expected)

print(dices_observed)
print(ks)


