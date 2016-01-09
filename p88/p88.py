import itertools
import timeit

from operator import mul

# References:
#  [1] -- Kurlandchik and Nowicki. "When the sum equals the product".  

def product_sum_numbers(n):
    for candidate in itertools.combinations_with_replacement(range(1,n+1), n):

        # Condition given in the proof of Theorem 4 of [1]
        if sum(candidate[0:n-2]) >= n*candidate[n-1]:
            break

        if sum(candidate) == reduce(mul, candidate):
            yield candidate

def sum_of_minimal_product_sum_numbers_up_to(kmax):
    minimal_product_sum_numbers = set()
    for k in range(2, kmax + 1):
        Ak = product_sum_numbers(k)
        minimal_product_sum_number = min(sum(a) for a in Ak)
        minimal_product_sum_numbers.add(minimal_product_sum_number)

    return sum(minimal_product_sum_numbers)

def main():
    # Test cases given in the problem.
    assert(sum_of_minimal_product_sum_numbers_up_to(6) == 30)
    assert(sum_of_minimal_product_sum_numbers_up_to(12) == 61)

    sample_sizes = list(range(2, 9)) + [12]
    mps_sums = dict()
    times = dict()
    for kmax in sample_sizes:
        times[kmax] = timeit.timeit(
                "mps_sums[kmax] = sum_of_minimal_product_sum_numbers_up_to(kmax)", number=1)
        print("kmax: {0}, sum: {1}, time: {2}".format(kmax, mps_sums[kmax], times[kmax]))


if __name__ == '__main__':
    main()
