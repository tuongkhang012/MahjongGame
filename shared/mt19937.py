class MT19937:
    """
    Python implementation of the Mersenne Twister (MT19937)
    specifically matching mt19937ar.c behavior for init_by_array.
    """

    def __init__(self):
        self.N = 624
        self.M = 397
        self.MATRIX_A = 0x9908B0DF
        self.UPPER_MASK = 0x80000000
        self.LOWER_MASK = 0x7FFFFFFF
        self.mt = [0] * self.N
        self.mti = self.N + 1

    def init_genrand(self, s):
        self.mt[0] = s & 0xFFFFFFFF
        for mti in range(1, self.N):
            self.mt[mti] = (
                1812433253 * (self.mt[mti - 1] ^ (self.mt[mti - 1] >> 30)) + mti
            )
            self.mt[mti] &= 0xFFFFFFFF
        self.mti = self.N

    def init_by_array(self, init_key):
        self.init_genrand(19650218)
        i, j, k = 1, 0, 0
        key_length = len(init_key)

        # Determine the number of iterations
        k = max(self.N, key_length)

        for _ in range(k):
            self.mt[i] = (
                (self.mt[i] ^ ((self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) * 1664525))
                + init_key[j]
                + j
            )
            self.mt[i] &= 0xFFFFFFFF
            i += 1
            j += 1
            if i >= self.N:
                self.mt[0] = self.mt[self.N - 1]
                i = 1
            if j >= key_length:
                j = 0

        for _ in range(self.N - 1):
            self.mt[i] = (
                self.mt[i] ^ ((self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) * 1566083941)
            ) - i
            self.mt[i] &= 0xFFFFFFFF
            i += 1
            if i >= self.N:
                self.mt[0] = self.mt[self.N - 1]
                i = 1

        self.mt[0] = 0x80000000

    def genrand_int32(self):
        y = 0
        mag01 = [0x0, self.MATRIX_A]

        if self.mti >= self.N:
            if self.mti == self.N + 1:
                self.init_genrand(5489)

            for kk in range(self.N - self.M):
                y = (self.mt[kk] & self.UPPER_MASK) | (
                    self.mt[kk + 1] & self.LOWER_MASK
                )
                self.mt[kk] = self.mt[kk + self.M] ^ (y >> 1) ^ mag01[y & 0x1]

            for kk in range(self.N - self.M, self.N - 1):
                y = (self.mt[kk] & self.UPPER_MASK) | (
                    self.mt[kk + 1] & self.LOWER_MASK
                )
                self.mt[kk] = (
                    self.mt[kk + (self.M - self.N)] ^ (y >> 1) ^ mag01[y & 0x1]
                )

            y = (self.mt[self.N - 1] & self.UPPER_MASK) | (self.mt[0] & self.LOWER_MASK)
            self.mt[self.N - 1] = self.mt[self.M - 1] ^ (y >> 1) ^ mag01[y & 0x1]

            self.mti = 0

        y = self.mt[self.mti]
        self.mti += 1

        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18

        return y
