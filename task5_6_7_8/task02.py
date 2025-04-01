from collections.abc import Sequence

"""
Given a cell with "it's a fib sequence" from slideshow,
    please write function "check_fib", which accepts a Sequence of integers, and
    returns if the given sequence is a Fibonacci sequence

We guarantee, that the given sequence contain >= 0 integers inside.

"""

def check_fibonacci(data: Sequence[int]) -> bool:

    if len(data) < 3:
        return True
    for i in range(2, len(data)):
        if data[i] != data[i - 1] + data[i - 2]:
            return False
    return True

if __name__ == "__main__":
    seq1 = [0, 1, 1, 2, 3, 5, 8]
    print(f"Последовательность {seq1} является Фибоначчи: {check_fibonacci(seq1)}")
    
    seq2 = [3, 5, 8, 13, 21]
    print(f"Последовательность {seq2} является Фибоначчи: {check_fibonacci(seq2)}")
    
    seq3 = [1, 2, 4, 7, 11]
    print(f"Последовательность {seq3} является Фибоначчи: {check_fibonacci(seq3)}")
    
    seq4 = [7]
    seq5 = []
    print(f"Последовательность {seq4} является Фибоначчи: {check_fibonacci(seq4)}")
    print(f"Последовательность {seq5} является Фибоначчи: {check_fibonacci(seq5)}")
