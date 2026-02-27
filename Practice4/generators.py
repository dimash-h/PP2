#1
def squares_up_to_n(n):
    for i in range(n + 1):
        yield i * i
#2
def even_numbers_comma(n):
    return ",".join(str(x) for x in range(0, n + 1) if x % 2 == 0)
#3
def divisible_by_3_and_4(n):
    for x in range(0, n + 1):
        if x % 3 == 0 and x % 4 == 0:
            yield x
#4
def squares(a, b):
    for x in range(a, b + 1):
        yield x * x
#5
def countdown(n):
    for x in range(n, -1, -1):
        yield x

if __name__ == "__main__":
    print(list(squares_up_to_n(5)))
    print(even_numbers_comma(10))
    print(list(divisible_by_3_and_4(50)))
    print(list(squares(3, 7)))
    print(list(countdown(5)))