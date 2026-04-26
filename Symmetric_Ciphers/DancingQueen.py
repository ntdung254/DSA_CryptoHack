from binascii import unhexlify

KNOWN_TEXT = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula'

IV1_HEX = 'e42758d6d218013ea63e3c49'
IV2_HEX = 'a99f9a7d097daabd2aa2a235'
MSG_HEX = 'f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c211ef5a52628094f09a30fc692cb25647f'
FLAG_HEX = 'b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0fe622b32732'

# Convert sang bytes
iv1 = unhexlify(IV1_HEX)
iv2 = unhexlify(IV2_HEX)
cipher_msg = unhexlify(MSG_HEX)
cipher_flag = unhexlify(FLAG_HEX)


def to_words(data: bytes):
    """Chuyển bytes -> list 32-bit words (little-endian)."""
    return [int.from_bytes(data[i:i+4], "little") for i in range(0, len(data), 4)]


def to_bytes(words):
    """Chuyển list 32-bit words -> bytes."""
    return b''.join(w.to_bytes(4, "little") for w in words)


def rotl(x, n):
    """Rotate left 32-bit."""
    return ((x << n) & 0xffffffff) | (x >> (32 - n))


def rotr(x, n):
    """Rotate right 32-bit."""
    return ((x >> n) | ((x << (32 - n)) & 0xffffffff)) & 0xffffffff


def add32(x):
    """Giữ giá trị trong 32-bit."""
    return x & 0xffffffff


def bxor(a: bytes, b: bytes):
    """XOR hai chuỗi bytes."""
    return bytes(x ^ y for x, y in zip(a, b))


class ChaChaMini:
    """
    Cài đặt rút gọn của ChaCha20 (10 rounds).
    
    Lưu ý:
    - Không cộng state ban đầu vào cuối (non-standard)
    - Đây chính là lỗ hổng để đảo ngược state
    """

    def __init__(self):
        self.state = []

    def _quarter_round(self, s, a, b, c, d):
        """Quarter round của ChaCha."""
        s[a] = add32(s[a] + s[b]); s[d] ^= s[a]; s[d] = rotl(s[d], 16)
        s[c] = add32(s[c] + s[d]); s[b] ^= s[c]; s[b] = rotl(s[b], 12)
        s[a] = add32(s[a] + s[b]); s[d] ^= s[a]; s[d] = rotl(s[d], 8)
        s[c] = add32(s[c] + s[d]); s[b] ^= s[c]; s[b] = rotl(s[b], 7)

    def _round(self):
        """Một vòng gồm column + diagonal rounds."""
        self._quarter_round(self.state, 0, 4, 8, 12)
        self._quarter_round(self.state, 1, 5, 9, 13)
        self._quarter_round(self.state, 2, 6, 10, 14)
        self._quarter_round(self.state, 3, 7, 11, 15)

        self._quarter_round(self.state, 0, 5, 10, 15)
        self._quarter_round(self.state, 1, 6, 11, 12)
        self._quarter_round(self.state, 2, 7, 8, 13)
        self._quarter_round(self.state, 3, 4, 9, 14)

    def _init_state(self, key, iv, counter):
        """Khởi tạo state ChaCha."""
        self.state = [
            0x61707865, 0x3320646e, 0x79622d32, 0x6b206574
        ]
        self.state += to_words(key)
        self.state.append(counter)
        self.state += to_words(iv)

    def crypt(self, data, key, iv):
        """
        Encrypt/Decrypt (vì stream cipher nên giống nhau).
        """
        out = b''
        counter = 1

        for i in range(0, len(data), 64):
            self._init_state(key, iv, counter)

            for _ in range(10):
                self._round()

            keystream = to_bytes(self.state)
            out += bxor(data[i:i+64], keystream)

            counter += 1

        return out


# ===== Inversion attack =====

def inv_quarter(s, a, b, c, d):
    """Đảo ngược quarter round."""
    a2, b2, c2, d2 = s[a], s[b], s[c], s[d]

    b1 = rotr(b2, 7) ^ c2
    c1 = add32(c2 - d2)
    a1 = add32(a2 - b1)
    d1 = rotr(d2, 8) ^ a2

    b0 = rotr(b1, 12) ^ c1
    c0 = add32(c1 - d1)
    a0 = add32(a1 - b0)
    d0 = rotr(d1, 16) ^ a1

    s[a], s[b], s[c], s[d] = a0, b0, c0, d0


def undo_round(state):
    """Đảo ngược một vòng ChaCha."""
    inv_quarter(state, 3, 4, 9, 14)
    inv_quarter(state, 2, 7, 8, 13)
    inv_quarter(state, 1, 6, 11, 12)
    inv_quarter(state, 0, 5, 10, 15)

    inv_quarter(state, 3, 7, 11, 15)
    inv_quarter(state, 2, 6, 10, 14)
    inv_quarter(state, 1, 5, 9, 13)
    inv_quarter(state, 0, 4, 8, 12)


def extract_key(known_pt, known_ct):
    """
    Khôi phục key từ known plaintext attack.

    Ý tưởng:
    - XOR plaintext và ciphertext → keystream
    - Keystream chính là state sau 10 rounds
    - Đảo ngược 10 rounds → lấy lại state ban đầu
    - Key nằm ở word 4..11
    """
    keystream = bxor(known_ct[:64], known_pt[:64])
    state = to_words(keystream)

    for _ in range(10):
        undo_round(state)

    return to_bytes(state[4:12])


def main():
    key = extract_key(KNOWN_TEXT, cipher_msg)
    print("Recovered key:", key.hex())

    chacha = ChaChaMini()
    flag = chacha.crypt(cipher_flag, key, iv2)

    try:
        print("Flag:", flag.decode())
    except:
        print("Raw flag:", flag)


if __name__ == "__main__":
    main()
