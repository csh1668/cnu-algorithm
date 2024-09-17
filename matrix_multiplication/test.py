import random

from benchmark import measure, print_results
from matrix_multiplication.subjects import *

class Test:
    def __init__(self, size, seed=0):
        self.rand = random.Random(seed)
        self.m1 = [[self.rand.randint(0, 10) for _ in range(size)] for _ in range(size)]
        self.m2 = [[self.rand.randint(0, 10) for _ in range(size)] for _ in range(size)]

    @measure(10)
    def test_naive(self):
        return naive(self.m1, self.m2)

    @measure(10)
    def test_strassen(self, threadhold=64):
        return strassen(self.m1, self.m2, threadhold)

    def test(self):
        naive_result = self.test_naive()
        strassen_result = self.test_strassen()
        assert naive_result == strassen_result



if __name__ == "__main__":
    sz = 256
    test = Test(sz)
    test.test_naive()
    for threshold in [1, 2, 4, 8, 16, 32, 64, 128]:
        test.test_strassen(threshold)
    print_results(f'Matrix Multiplication Benchmark (size={sz})')