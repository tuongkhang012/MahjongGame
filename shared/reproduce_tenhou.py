import hashlib
import base64
import struct
from shared.mt19937 import MT19937


def reproduce_tenhou(seed_str, num) -> list[tuple[list[int], list[int]]]:
    """
    Reproduces Tenhou wall generation.
    :param seed_str: Base64 encoded seed string.
    :param num: Number of games/walls to generate.
    :return: List of tuples (wall_tiles, dice_rolls)
    """

    # 1. Base64 Decode
    decoded_seed = base64.b64decode(seed_str)

    # 2. Convert to Integers (Seed Preparation)
    # The C++ code constructs Big-Endian ints then bswaps them.
    # This is equivalent to reading the bytes as Little-Endian uint32.
    # Since the seed is 624 * 4 bytes, we unpack 624 integers.
    if len(decoded_seed) < 624 * 4:
        raise ValueError("Seed length is too short")

    rt_seed = list(struct.unpack("<" + "I" * 624, decoded_seed[: 624 * 4]))

    # 3. Initialize MT19937
    mt = MT19937()
    mt.init_by_array(rt_seed)

    results = []

    SHA512_DIGEST_LENGTH = 64  # bytes

    # Calculate array sizes based on C++ logic
    # rnd size: (64 / 4 * 9) = 144 uint32s
    rnd_size = (SHA512_DIGEST_LENGTH // 4) * 9

    # src size: 144 * 2 = 288 uint32s
    src_size = rnd_size * 2

    for _ in range(num):
        # 4. Generate Random Noise (src)
        src = [mt.genrand_int32() for _ in range(src_size)]

        # 5. Hash Noise to get Wall RNG (rnd)
        rnd = []

        # We process 'src' in chunks of (SHA512_DIGEST_LENGTH * 2) bytes
        # which is 64 * 2 = 128 bytes (32 uint32s)
        chunk_size_ints = (SHA512_DIGEST_LENGTH * 2) // 4

        for i in range(9):
            # Extract chunk from src
            start_idx = i * chunk_size_ints
            chunk_ints = src[start_idx : start_idx + chunk_size_ints]

            # Convert ints to bytes (Little Endian) to mimic C++ memory casting
            chunk_bytes = struct.pack("<" + "I" * len(chunk_ints), *chunk_ints)

            # Perform SHA512
            sha_hash = hashlib.sha512(chunk_bytes).digest()

            # Convert hash back to uint32s (Little Endian)
            hash_ints = struct.unpack("<" + "I" * (len(sha_hash) // 4), sha_hash)
            rnd.extend(hash_ints)

        # 6. Shuffle Wall
        # 0-135 tiles
        wall = list(range(136))

        for i in range(136 - 1):
            # Swap logic: std::swap(wall[i], wall[i + (rnd[i] % (136 - i))])
            swap_idx = i + (rnd[i] % (136 - i))
            wall[i], wall[swap_idx] = wall[swap_idx], wall[i]

        # 7. Get Dice
        # rnd[135] and rnd[136] are used for dice
        dice1 = (rnd[135] % 6) + 1
        dice2 = (rnd[136] % 6) + 1

        results.append((wall, [dice1, dice2]))

    return results
