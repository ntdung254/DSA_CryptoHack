import requests

def fetch_ciphertext():
    endpoint = "http://aes.cryptohack.org/bean_counter/encrypt/"
    response = requests.get(endpoint)
    return response.json()["encrypted"]


def split_blocks(data, size=16):
    """Chia bytes thành các block cố định."""
    return [data[i:i+size] for i in range(0, len(data), size)]


def recover_keystream(first_block, known_header):
    """
    Khôi phục keystream bằng cách XOR block đầu với header đã biết.
    """
    header_bytes = bytes.fromhex("".join(known_header))
    return bytes([a ^ b for a, b in zip(first_block, header_bytes)])


def xor_decrypt(blocks, keystream):
    """Giải mã từng block bằng keystream."""
    plaintext_blocks = []
    for blk in blocks:
        plaintext_blocks.append(bytes([x ^ y for x, y in zip(blk, keystream)]))
    return b"".join(plaintext_blocks)


def save_file(data, path):
    """Ghi dữ liệu nhị phân ra file."""
    with open(path, "wb") as file:
        file.write(data)


def main():
    # PNG magic header
    png_magic = [
        '89','50','4E','47','0D','0A','1A','0A',
        '00','00','00','0D','49','48','44','52'
    ]

    hex_data = fetch_ciphertext()
    raw_bytes = bytes.fromhex(hex_data)

    blocks = split_blocks(raw_bytes)
    ks = recover_keystream(blocks[0], png_magic)

    image_data = xor_decrypt(blocks, ks)

    save_file(image_data, r"C:\Users\Acer\OneDrive\Documents\Kanade\flag.png")


if __name__ == "__main__":
    main()
