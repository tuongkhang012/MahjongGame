import random
import struct
import base64


def generate_random_seed():
    """
    Generates a new, valid Tenhou seed string.

    The seed is a base64 encoded representation of 624 random u32 integers,
    which represent the internal state array of the MT19937 PRNG.
    """

    rng = random.SystemRandom()

    mt_state_array = [rng.getrandbits(32) for _ in range(624)]

    byte_sequence = b""
    for value in mt_state_array:
        byte_sequence += struct.pack("<I", value)

    encoded_bytes = base64.b64encode(byte_sequence)

    seed_string = encoded_bytes.decode("utf-8")

    return seed_string
