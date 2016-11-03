import gmpy2
import matplotlib.pyplot as pyplot
import numpy

def primes_to(n):
    # http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in xrange(3,int(n**0.5)+1,2):
        if sieve[i]:
            sieve[i*i::2*i]=[False]*((n-i*i-1)/(2*i)+1)
    return [2] + [i for i in xrange(3,n,2) if sieve[i]]

def test_primes():
    assert(list(primes_to(30)) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

def mountains_and_valleys_to(k_max, max_prime):
    distance = 0
    elevation = 0
    grade = 1
    k = 0
    for p in primes_to(max_prime):
        k = k + 1
        if k // 2 > k_max:
            break
        distance = distance + p
        elevation = elevation + grade * p
        grade = grade * -1
        yield (distance, elevation)


def compute_visible_peaks_brute(skyline):
    peaks = [skyline[2*k] for k in range(0, len(skyline) // 2)]
    n_peaks = len(peaks)
    visible_peaks = numpy.matrix(numpy.zeros((n_peaks, n_peaks)), dtype=int)
    for k in range(1, len(peaks)):
        for j in range(0, k):
            rise = float(peaks[k][1] - peaks[j][1])
            run = float(peaks[k][0] - peaks[j][0])
            slope = rise / run
            assert(rise > 0)
            assert(run > 0)
            blocked = False
            for l in range(j + 1, k):
                dist_from_j = peaks[l][0] - peaks[j][0]
                los_at_l = peaks[j][1] + dist_from_j * slope
                if los_at_l <= peaks[l][1]:
                    blocked = True
                    break
            if not blocked:
                visible_peaks[j, k] = 1
    return visible_peaks

def test_compute_visible_peaks_brute():
    max_k = 9
    max_prime = int(100)
    skyline = list(mountains_and_valleys_to(max_k, max_prime))
    visible_peaks = compute_visible_peaks_brute(skyline)
    visibility_count = numpy.sum(visible_peaks, axis=0)
    assert(visibility_count[0, 0] == 0)
    assert(visibility_count[0, 1] == 1)
    assert(visibility_count[0, 2] == 1)
    assert(visibility_count[0, 8] == 3)

def run_tests():
    test_primes()
    test_compute_visible_peaks_brute()

def main():
    max_k = 100
    max_prime = int(1e7)

    skyline = list(mountains_and_valleys_to(max_k, max_prime))
    visible_peaks = compute_visible_peaks_brute(skyline)
    print(visible_peaks)
    visibility_count = numpy.sum(visible_peaks, axis=0)[0]
    print(visibility_count[0:max_k])
    total = numpy.cumsum(visibility_count)
    print(total)

    assert(total[0, 99] == 227)
    if  total.size < max_k:
        print("Didn't get them all.")

    #skyline_arr = list(list(t for t in zip(*skyline)))
    #pyplot.plot(skyline_arr[0], skyline_arr[1])
    #pyplot.axis('equal')

    pyplot.imshow(visible_peaks, interpolation='none')

    pyplot.show()

if __name__ == '__main__':
    run_tests()
    main()
