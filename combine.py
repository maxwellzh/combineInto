# This is a funny brain-exercised game:
# get four cards from poke, which in range
# of A to 10 (A represents 1 here).
# Then try to figure out how to combine
# these four numbers into a specific number
# (24 here) with only + - * / operations.
# And all of four numbers must be involved
# and only for once.

from typing import List, Iterator, Tuple

COMBINEVAL = 24


def solve(nums: List[int]) -> Iterator[List[Tuple[int, str, int, int]]]:
    """return list of tuples, where the elements are
    
    num1 op num2 ans
    """
    L = len(nums)
    if L <= 1:
        print("internal error! solve() received empty list.")
    elif L == 2:
        m, n = nums
        yield [(m, '+', n, m+n)]
        if m == 0 or n == 0:
            return
        if m >= n:
            yield [(m, '-', n, m-n)]
            if m % n == 0:
                yield [(m, '/', n, m//n)]
        else:
            yield [(n, '-', m, n-m)]
            if n % m == 0:
                yield [(n, '/', m, n//m)]
        yield [(m, '*', n, m*n)]
    else:
        for i in range(L):
            for j in range(L):
                if i == j:
                    continue

                m = nums[i] + nums[j]
                res = [nums[k] for k in range(L) if k != i and k != j]
                res.append(m)
                for nl in solve(res):
                    yield [(nums[i], '+', nums[j], m)] + nl

                if nums[i] == 0 or nums[j] == 0:
                    continue

                m = nums[i] * nums[j]
                res[-1] = m
                for nl in solve(res):
                    yield [(nums[i], '*', nums[j], m)] + nl

                m = nums[i] - nums[j]
                if m < 0:
                    continue
                res[-1] = m
                for nl in solve(res):
                    yield [(nums[i], '-', nums[j], m)] + nl

                if nums[i] < nums[j] or (nums[i] % nums[j] != 0):
                    continue
                m = nums[i] // nums[j]
                res[-1] = m
                for nl in solve(res):
                    yield [(nums[i], '/', nums[j], m)] + nl
    return


def display(states: List[Tuple[int, str, int, int]]):
    for n1, op, n2, res in states:
        print(f"{n1:<2} {op} {n2:^3} -> {res:^3}")


def game_loop():
    print("> ", end="")
    geti = input()
    nums = geti.split()
    if len(nums) != 4:
        print("输入不合法!")
        return

    try:
        nums = [int(x) for x in nums]
    except ValueError:
        print("输入不合法!")
        return

    for i in nums:
        if i < 1 or i > 10:
            print("输入不合法!")
            return

    for nl in solve(nums):
        if nl[-1][-1] == COMBINEVAL:
            print("="*15)
            display(nl)
            print("="*15)
            return

    print("没有找到解法")
    return


def main():
    while True:
        try:
            stat = game_loop()
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
