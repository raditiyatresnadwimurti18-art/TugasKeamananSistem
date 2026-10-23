"""
=============================================================================
  decryption.py - Fungsi Dekripsi (Membalik 5 Langkah Enkripsi)
  Langkah D1: Bagi ciphertext menjadi blok 8 karakter
  Langkah D2: Inverse Key Permutasi
  Langkah D3: Inverse Key Blocking
  Langkah D4: Unblocking (buang padding)
  Langkah D5: Inverse Substitusi
=============================================================================
"""

from config import (
    INVERSE_SUBSTITUTION_TABLE,
    BLOCK_SIZE,
    INVERSE_KEY_BLOCKING,
    INVERSE_KEY_PERMUTATION,
)
from encryption import apply_key


# ---------------------------------------------------------------------------
# LANGKAH D2: INVERSE KEY PERMUTASI
# ---------------------------------------------------------------------------

def inverse_permute(block: str) -> str:
    """
    Balik Key Permutasi menggunakan INVERSE_KEY_PERMUTATION.

    Args:
        block (str): Blok ciphertext (8 karakter).

    Returns:
        str: Blok setelah Key Permutasi dibalik.
    """
    return apply_key(block, INVERSE_KEY_PERMUTATION)


# ---------------------------------------------------------------------------
# LANGKAH D3: INVERSE KEY BLOCKING
# ---------------------------------------------------------------------------

def inverse_blocking(block: str) -> str:
    """
    Balik Key Blocking menggunakan INVERSE_KEY_BLOCKING.

    Args:
        block (str): Blok setelah inverse permutasi (8 karakter).

    Returns:
        str: Blok setelah Key Blocking dibalik (= blok setelah substitusi).
    """
    return apply_key(block, INVERSE_KEY_BLOCKING)


# ---------------------------------------------------------------------------
# LANGKAH D4: UNBLOCKING (buang padding)
# ---------------------------------------------------------------------------

def remove_padding(blocks: list[str], original_length: int) -> str:
    """
    Gabungkan blok-blok dan potong karakter padding di akhir.

    Args:
        blocks          (list[str]): Blok setelah inverse blocking.
        original_length (int)      : Panjang teks sebelum padding (= panjang plaintext asli).

    Returns:
        str: Teks bersih tanpa padding.
    """
    return "".join(blocks)[:original_length]


# ---------------------------------------------------------------------------
# LANGKAH D5: INVERSE SUBSTITUSI
# ---------------------------------------------------------------------------

def inverse_substitute(text: str) -> str:
    """
    Kembalikan setiap karakter ke simbol plaintext aslinya
    menggunakan INVERSE_SUBSTITUTION_TABLE.

    Args:
        text (str): Teks setelah unblocking.

    Returns:
        str: Plaintext hasil dekripsi.

    Raises:
        ValueError: Jika karakter tidak ada di tabel substitusi terbalik.
    """
    result: list[str] = []
    for idx, char in enumerate(text):
        if char not in INVERSE_SUBSTITUTION_TABLE:
            raise ValueError(
                f"Karakter '{char}' (posisi {idx + 1}) tidak ada "
                f"dalam tabel substitusi terbalik."
            )
        result.append(INVERSE_SUBSTITUTION_TABLE[char])
    return "".join(result)


# ---------------------------------------------------------------------------
# FUNGSI DEKRIPSI UTAMA
# ---------------------------------------------------------------------------

def decrypt(ciphertext: str, original_length: int) -> dict:
    """
    Dekripsi teks lengkap - membalik 5 langkah enkripsi:
      D1. Bagi ciphertext menjadi blok 8 karakter
      D2. Inverse Key Permutasi [2 4 1 7 5 8 3 6]
      D3. Inverse Key Blocking  [7 2 6 8 1 4 3 5]
      D4. Unblocking - buang padding
      D5. Inverse Substitusi monoalfabetik

    Args:
        ciphertext      (str): Teks terenkripsi.
        original_length (int): Panjang plaintext asli (untuk membuang padding).

    Returns:
        dict: Semua hasil antara dan akhir:
            - ciphertext         : input ciphertext
            - blocks             : ciphertext dipecah menjadi blok
            - inv_perm_blocks    : blok setelah Inverse Key Permutasi
            - inv_blocked_blocks : blok setelah Inverse Key Blocking
            - after_unblocking   : teks setelah padding dibuang
            - plaintext          : plaintext hasil dekripsi

    Raises:
        ValueError: Diteruskan dari inverse_substitute() jika karakter tidak valid.
    """
    # Langkah D1 - Bagi ciphertext menjadi blok 8 karakter
    blocks: list[str] = [
        ciphertext[i : i + BLOCK_SIZE]
        for i in range(0, len(ciphertext), BLOCK_SIZE)
    ]

    # Langkah D2 - Inverse Key Permutasi
    inv_perm_blocks: list[str] = [inverse_permute(b) for b in blocks]

    # Langkah D3 - Inverse Key Blocking
    inv_blocked_blocks: list[str] = [inverse_blocking(b) for b in inv_perm_blocks]

    # Langkah D4 - Unblocking (buang padding)
    after_unblocking: str = remove_padding(inv_blocked_blocks, original_length)

    # Langkah D5 - Inverse Substitusi
    plaintext: str = inverse_substitute(after_unblocking)

    return {
        "ciphertext":          ciphertext,
        "blocks":              blocks,
        "inv_perm_blocks":     inv_perm_blocks,
        "inv_blocked_blocks":  inv_blocked_blocks,
        "after_unblocking":    after_unblocking,
        "plaintext":           plaintext,
    }
