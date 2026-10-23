"""
=============================================================================
  config.py — Konfigurasi & Tabel Substitusi
  Berisi semua konstanta yang digunakan oleh modul enkripsi & dekripsi.

  Alur enkripsi (5 langkah):
    1. Normalisasi & Substitusi monoalfabetik
    2. Pembentukan Blok 8 karakter + Padding
    3. Key Blocking  : 7 2 6 8 1 4 3 5  (1-based)
    4. Key Permutasi : 2 4 1 7 5 8 3 6  (1-based)
    5. Penggabungan Ciphertext
=============================================================================
"""

# ---------------------------------------------------------------------------
# TABEL SUBSTITUSI MONOALFABETIK
# ---------------------------------------------------------------------------
# Asli       : A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 1 2 3 4 5 6 7 8 9 0 - . , (spasi)
# Substitusi : B F 1 K Q G A T P J 6 H Y D 2 X 5 M V 7 C 8 4 I 9 N R E U 3 L S W - . , O Z 0 (spasi)

SUBSTITUTION_TABLE: dict[str, str] = {
    # Huruf A-Z
    'A': 'B', 'B': 'F', 'C': '1', 'D': 'K', 'E': 'Q',
    'F': 'G', 'G': 'A', 'H': 'T', 'I': 'P', 'J': 'J',
    'K': '6', 'L': 'H', 'M': 'Y', 'N': 'D', 'O': '2',
    'P': 'X', 'Q': '5', 'R': 'M', 'S': 'V', 'T': '7',
    'U': 'C', 'V': '8', 'W': '4', 'X': 'I', 'Y': '9',
    'Z': 'N',
    # Angka 1-9 & 0
    '1': 'R', '2': 'E', '3': 'U', '4': '3',
    '5': 'L', '6': 'S', '7': 'W', '8': '-', '9': '.', '0': ',',
    # Karakter khusus
    '-': 'O', '.': 'Z', ',': '0',
    # Spasi - dipetakan ke dirinya sendiri
    ' ': ' ',
}

# Tabel substitusi terbalik - di-generate otomatis untuk dekripsi
INVERSE_SUBSTITUTION_TABLE: dict[str, str] = {
    v: k for k, v in SUBSTITUTION_TABLE.items()
}

# ---------------------------------------------------------------------------
# PARAMETER BLOCKING
# ---------------------------------------------------------------------------
BLOCK_SIZE:   int = 8       # Ukuran setiap blok (8 karakter)
PADDING_CHAR: str = '.'     # Karakter padding jika teks bukan kelipatan 8

# ---------------------------------------------------------------------------
# KEY BLOCKING (Langkah 3)
# ---------------------------------------------------------------------------
# 1-based  : 7 2 6 8 1 4 3 5
# Konversi ke 0-based: kurangi 1 dari setiap elemen
KEY_BLOCKING_1BASED:  list[int] = [7, 2, 6, 8, 1, 4, 3, 5]
KEY_BLOCKING_PATTERN: list[int] = [k - 1 for k in KEY_BLOCKING_1BASED]
# => [6, 1, 5, 7, 0, 3, 2, 4]

# Inverse Key Blocking - di-generate otomatis untuk dekripsi
INVERSE_KEY_BLOCKING: list[int] = [
    KEY_BLOCKING_PATTERN.index(i) for i in range(BLOCK_SIZE)
]

# ---------------------------------------------------------------------------
# KEY PERMUTASI (Langkah 4)
# ---------------------------------------------------------------------------
# 1-based  : 2 4 1 7 5 8 3 6
# Konversi ke 0-based: kurangi 1 dari setiap elemen
KEY_PERMUTATION_1BASED:  list[int] = [2, 4, 1, 7, 5, 8, 3, 6]
KEY_PERMUTATION_PATTERN: list[int] = [k - 1 for k in KEY_PERMUTATION_1BASED]
# => [1, 3, 0, 6, 4, 7, 2, 5]

# Inverse Key Permutation - di-generate otomatis untuk dekripsi
INVERSE_KEY_PERMUTATION: list[int] = [
    KEY_PERMUTATION_PATTERN.index(i) for i in range(BLOCK_SIZE)
]
