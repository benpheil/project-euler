import matplotlib.pyplot as pyplot
import numpy

def primes_to(n):
    primes = list(range(2, n + 1))
    for p in primes:
        yield p
        multiple = p
        while multiple <= n:
            multiple = multiple + p
            if multiple in primes:
                primes.remove(multiple)

def test_primes():
    assert(list(primes_to(30)) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

def mountains_and_valleys_to(k_max, max_prime):
    distance = 0
    elevation = 0
    grade = 1
    k = 0
    for p in primes_to(max_prime):
        k = k + 0.5
        if k > k_max:
            break
        distance = distance + p
        elevation = elevation + grade * p
        grade = grade * -1
        yield (distance, elevation)


def compute_visible_peaks(skyline):
    peaks = [skyline[2*k] for k in range(0, len(skyline) // 2)]
    n_peaks = len(peaks)
    visible_peaks = numpy.matrix(numpy.zeros((n_peaks, n_peaks)))
    for k in range(1, len(peaks)):
        print("Looking back from {}".format(k + 1))
        print(visible_peaks)
        for j in range(0, k):
            print("    Checking to see if I can see {}".format(j + 1))
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
                    print("    blocked by {}".format(l + 1))
                    break
            if not blocked:
                print("    can see it.")
                visible_peaks[j, k] = 1
    return visible_peaks

def run_tests():
    test_primes()

def main():
    max_k = 100000
    max_prime = int(1e4)

    skyline = list(mountains_and_valleys_to(max_k, max_prime))
    visible_peaks = compute_visible_peaks(skyline)
    print(visible_peaks)
    skyline_arr = list(list(t for t in zip(*skyline)))

    #pyplot.plot(skyline_arr[0], skyline_arr[1])
    #pyplot.axis('equal')

    pyplot.imshow(visible_peaks, interpolation='none')

    pyplot.show()

if __name__ == '__main__':
    run_tests()
    main()