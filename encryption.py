"""
=============================================================================
  encryption.py - Fungsi Enkripsi (5 Langkah)
  Langkah 1: Normalisasi & Substitusi
  Langkah 2: Pembentukan Blok 8 karakter + Padding
  Langkah 3: Key Blocking  [7 2 6 8 1 4 3 5]
  Langkah 4: Key Permutasi [2 4 1 7 5 8 3 6]
  Langkah 5: Penggabungan Ciphertext
=============================================================================
"""

from config import (
    SUBSTITUTION_TABLE,
    BLOCK_SIZE,
    PADDING_CHAR,
    KEY_BLOCKING_PATTERN,
    KEY_PERMUTATION_PATTERN,
)


# ---------------------------------------------------------------------------
# LANGKAH 1: SUBSTITUSI
# ---------------------------------------------------------------------------

def substitute(text: str) -> str:
    """
    Ganti setiap karakter plaintext dengan padanannya di SUBSTITUTION_TABLE.

    Args:
        text (str): Teks plaintext (huruf besar).

    Returns:
        str: Teks setelah substitusi.

    Raises:
        ValueError: Jika ada karakter di luar tabel substitusi.
    """
    result: list[str] = []
    for idx, char in enumerate(text):
        if char not in SUBSTITUTION_TABLE:
            valid = sorted(SUBSTITUTION_TABLE.keys())
            raise ValueError(
                f"Karakter '{char}' (posisi {idx + 1}) tidak ada dalam tabel substitusi.\n"
                f"  Karakter yang didukung: {valid}"
            )
        result.append(SUBSTITUTION_TABLE[char])
    return "".join(result)


# ---------------------------------------------------------------------------
# LANGKAH 2: BLOCKING & PADDING
# ---------------------------------------------------------------------------

def add_blocking(
    text: str,
    block_size: int = BLOCK_SIZE,
    pad_char:   str = PADDING_CHAR,
) -> list[str]:
    """
    Bagi teks menjadi blok-blok berukuran `block_size` (default 8).
    Tambahkan padding di akhir jika panjang teks bukan kelipatan blok.

    Args:
        text       (str): Teks yang akan dibagi.
        block_size (int): Ukuran setiap blok (default: 8).
        pad_char   (str): Karakter padding (default: '.').

    Returns:
        list[str]: Daftar blok masing-masing berukuran `block_size`.
    """
    remainder = len(text) % block_size
    if remainder != 0:
        text += pad_char * (block_size - remainder)
    return [text[i : i + block_size] for i in range(0, len(text), block_size)]


# ---------------------------------------------------------------------------
# LANGKAH 3 & 4: PERMUTASI GENERIK (dipakai untuk blocking & permutasi)
# ---------------------------------------------------------------------------

def apply_key(block: str, pattern: list[int]) -> str:
    """
    Terapkan pola kunci (key) pada satu blok karakter.
    Aturan: hasil[i] = block[pattern[i]]

    Args:
        block   (str)      : Blok karakter dengan panjang == len(pattern).
        pattern (list[int]): Pola kunci 0-based index.

    Returns:
        str: Blok setelah kunci diterapkan.

    Raises:
        ValueError: Jika ukuran blok tidak sesuai panjang pola kunci.
    """
    if len(block) != len(pattern):
        raise ValueError(
            f"Ukuran blok ({len(block)}) != panjang pola kunci ({len(pattern)})."
        )
    return "".join(block[i] for i in pattern)


# ---------------------------------------------------------------------------
# FUNGSI ENKRIPSI UTAMA
# ---------------------------------------------------------------------------

def encrypt(plaintext: str) -> dict:
    """
    Enkripsi teks lengkap menggunakan 5 langkah:
      1. Normalisasi (uppercase) & Substitusi monoalfabetik
      2. Pembentukan Blok 8 karakter + Padding
      3. Penerapan Key Blocking  [7 2 6 8 1 4 3 5]
      4. Penerapan Key Permutasi [2 4 1 7 5 8 3 6]
      5. Penggabungan seluruh blok menjadi ciphertext

    Args:
        plaintext (str): Teks asli (akan otomatis diubah ke huruf besar).

    Returns:
        dict: Semua hasil antara dan akhir:
            - plaintext        : teks asli (uppercase)
            - after_substitute : teks setelah substitusi
            - blocks           : daftar blok 8-char (setelah padding)
            - blocked_blocks   : daftar blok setelah Key Blocking
            - permuted_blocks  : daftar blok setelah Key Permutasi
            - ciphertext       : ciphertext akhir

    Raises:
        ValueError: Diteruskan dari substitute() jika karakter tidak valid.
    """
    # Langkah 1 - Normalisasi & Substitusi
    plaintext = plaintext.upper()
    after_substitute: str = substitute(plaintext)

    # Langkah 2 - Pembentukan Blok 8 karakter + Padding
    blocks: list[str] = add_blocking(after_substitute)

    # Langkah 3 - Key Blocking [7 2 6 8 1 4 3 5]
    blocked_blocks: list[str] = [apply_key(b, KEY_BLOCKING_PATTERN) for b in blocks]

    # Langkah 4 - Key Permutasi [2 4 1 7 5 8 3 6]
    permuted_blocks: list[str] = [apply_key(b, KEY_PERMUTATION_PATTERN) for b in blocked_blocks]

    # Langkah 5 - Gabungkan
    ciphertext: str = "".join(permuted_blocks)

    return {
        "plaintext":       plaintext,
        "after_substitute": after_substitute,
        "blocks":          blocks,
        "blocked_blocks":  blocked_blocks,
        "permuted_blocks": permuted_blocks,
        "ciphertext":      ciphertext,
    }
