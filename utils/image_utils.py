import numpy as np


def decode_rgb565(data, width, height):
    """
    Convert RGB565 (R: 5bits, G: 6bits, B: 5bits) raw bytes into RGB888 image.
    byte1: RRRRRGGG
    byte2: GGGBBBBB
    r : 5 upper bits of byte1 (RRRRRXXX)
    g : 3 lower bits of byte1 (XXXXXGGG) + 3 upper bits of byte2 (GGGXXXXX)
    b : 5 lower bits of byte2 (XXXBBBBB)
    in RGB888 format, bits should be upper
    """
    data = np.frombuffer(data, dtype=np.uint8)
    byte1 = data[0::2]  # even indices
    byte2 = data[1::2]  # odd indices

    r = (byte1 & 0b11111000)
    g = ((byte1 & 0b00000111) << 5) | ((byte2 & 0b11100000) >> 3)
    b = (byte2 & 0b00011111) << 3

    bgr = np.stack((b, g, r), axis=-1).reshape((height, width, 3))
    return bgr