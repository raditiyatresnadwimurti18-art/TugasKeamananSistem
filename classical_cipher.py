"""
=============================================================================
  Implementasi Kriptografi Klasik: Substitusi + Blocking + Permutasi
  Mata Kuliah : Keamanan Sistem
  Deskripsi   : Enkripsi dan Dekripsi teks menggunakan tiga lapisan:
                1. Substitusi monoalfabetik
                2. Blocking (pemblokkan karakter)
                3. Permutasi posisi karakter per blok
=============================================================================
"""

# ===========================================================================
# KONFIGURASI TABEL & PARAMETER
# ===========================================================================

# Tabel Substitusi Monoalfabetik (dari soal):
#
# Asli       : A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 1 2 3 4 5 6 7 8 9 0 - . ,
# Substitusi : B F 1 K Q G A T P J 6 H Y D 2 X 5 M V 7 C 8 4 I 9 N R E U 3 L S W - . , O Z 0

SUBSTITUTION_TABLE: dict[str, str] = {
    'A': 'B', 'B': 'F', 'C': '1', 'D': 'K', 'E': 'Q',
    'F': 'G', 'G': 'A', 'H': 'T', 'I': 'P', 'J': 'J',
    'K': '6', 'L': 'H', 'M': 'Y', 'N': 'D', 'O': '2',
    'P': 'X', 'Q': '5', 'R': 'M', 'S': 'V', 'T': '7',
    'U': 'C', 'V': '8', 'W': '4', 'X': 'I', 'Y': '9',
    'Z': 'N', '1': 'R', '2': 'E', '3': 'U', '4': '3',
    '5': 'L', '6': 'S', '7': 'W', '8': '-', '9': '.',
    '0': ',', '-': 'O', '.': 'Z', ',': '0',
}

# Tabel substitusi terbalik (otomatis di-generate untuk dekripsi)
INVERSE_SUBSTITUTION_TABLE: dict[str, str] = {v: k for k, v in SUBSTITUTION_TABLE.items()}

# Parameter blocking
BLOCK_SIZE: int = 4
PADDING_CHAR: str = '.'

# Pola permutasi 0-based index untuk enkripsi
# [2, 0, 3, 1] berarti: hasil[0]=input[2], hasil[1]=input[0], hasil[2]=input[3], hasil[3]=input[1]
# Ekivalen 1-based: [3, 1, 4, 2]
PERMUTATION_PATTERN: list[int] = [2, 0, 3, 1]

# Pola permutasi terbalik (otomatis di-generate untuk dekripsi)
# inv_perm[perm[i]] = i  ->  digunakan untuk mengembalikan posisi asli
INVERSE_PERMUTATION_PATTERN: list[int] = [
    PERMUTATION_PATTERN.index(i) for i in range(BLOCK_SIZE)
]


# ===========================================================================
# FUNGSI ENKRIPSI
# ===========================================================================

def substitute(text: str) -> str:
    """
    Langkah 1 Enkripsi: Substitusi karakter menggunakan tabel monoalfabetik.

    Setiap karakter pada teks input digantikan oleh karakter padanannya
    yang telah didefinisikan dalam SUBSTITUTION_TABLE.

    Args:
        text (str): Teks plaintext (huruf besar).

    Returns:
        str: Teks setelah substitusi.

    Raises:
        ValueError: Jika terdapat karakter yang tidak ada dalam tabel substitusi.
    """
    result: list[str] = []
    for idx, char in enumerate(text):
        if char not in SUBSTITUTION_TABLE:
            raise ValueError(
                f"Karakter '{char}' pada indeks {idx} tidak terdapat dalam tabel substitusi.\n"
                f"  Karakter yang didukung: {sorted(SUBSTITUTION_TABLE.keys())}"
            )
        result.append(SUBSTITUTION_TABLE[char])
    return "".join(result)


def add_blocking(text: str, block_size: int = BLOCK_SIZE, pad_char: str = PADDING_CHAR) -> list[str]:
    """
    Langkah 2 Enkripsi: Membagi teks menjadi blok-blok berukuran `block_size`.

    Jika panjang teks bukan kelipatan `block_size`, karakter padding
    akan ditambahkan di akhir hingga teks memenuhi kelipatan tersebut.

    Args:
        text       (str): Teks yang akan dibagi ke dalam blok.
        block_size (int): Ukuran setiap blok (default: BLOCK_SIZE).
        pad_char   (str): Karakter pengisi padding (default: PADDING_CHAR).

    Returns:
        list[str]: Daftar blok string masing-masing berukuran `block_size`.
    """
    remainder = len(text) % block_size
    if remainder != 0:
        padding_needed = block_size - remainder
        text += pad_char * padding_needed

    return [text[i:i + block_size] for i in range(0, len(text), block_size)]


def permute_block(block: str, pattern: list[int] = PERMUTATION_PATTERN) -> str:
    """
    Langkah 3 Enkripsi: Mengacak posisi karakter dalam satu blok
    berdasarkan pola permutasi yang diberikan.

    Aturan: karakter hasil[i] = block[pattern[i]]

    Args:
        block   (str)      : Blok karakter dengan panjang == len(pattern).
        pattern (list[int]): Pola permutasi 0-based index.

    Returns:
        str: Blok setelah dipermutasi.

    Raises:
        ValueError: Jika ukuran blok tidak sesuai dengan panjang pola permutasi.
    """
    if len(block) != len(pattern):
        raise ValueError(
            f"Ukuran blok ({len(block)}) tidak cocok dengan panjang pola permutasi ({len(pattern)})."
        )
    return "".join(block[i] for i in pattern)


def encrypt(plaintext: str) -> dict:
    """
    Fungsi utama Enkripsi: Substitusi -> Blocking -> Permutasi.

    Args:
        plaintext (str): Teks asli yang ingin dienkripsi.
                         Akan otomatis dikonversi ke huruf besar.

    Returns:
        dict: Dictionary yang berisi semua hasil antara dan akhir:
              - 'plaintext'       : teks asli (uppercase)
              - 'after_substitute': teks setelah substitusi
              - 'blocks'          : daftar blok (sebelum permutasi, setelah padding)
              - 'permuted_blocks' : daftar blok setelah dipermutasi
              - 'ciphertext'      : ciphertext akhir (gabungan permuted_blocks)

    Raises:
        ValueError: Diteruskan dari substitute() jika ada karakter tidak valid.
    """
    # Normalisasi input ke huruf besar
    plaintext = plaintext.upper()

    # Langkah 1: Substitusi
    after_substitute: str = substitute(plaintext)

    # Langkah 2: Blocking (dengan padding jika perlu)
    blocks: list[str] = add_blocking(after_substitute)

    # Langkah 3: Permutasi setiap blok
    permuted_blocks: list[str] = [permute_block(b) for b in blocks]
    ciphertext: str = "".join(permuted_blocks)

    return {
        "plaintext":        plaintext,
        "after_substitute": after_substitute,
        "blocks":           blocks,
        "permuted_blocks":  permuted_blocks,
        "ciphertext":       ciphertext,
    }


# ===========================================================================
# FUNGSI DEKRIPSI
# ===========================================================================

def inverse_permute_block(block: str, pattern: list[int] = INVERSE_PERMUTATION_PATTERN) -> str:
    """
    Langkah 1 Dekripsi: Membalik permutasi pada satu blok.

    Menggunakan INVERSE_PERMUTATION_PATTERN yang merupakan kebalikan
    dari PERMUTATION_PATTERN yang dipakai saat enkripsi.

    Args:
        block   (str)      : Blok ciphertext.
        pattern (list[int]): Pola permutasi terbalik (0-based index).

    Returns:
        str: Blok setelah permutasi dibalik.
    """
    return permute_block(block, pattern)


def remove_blocking(blocks: list[str], original_length: int) -> str:
    """
    Langkah 2 Dekripsi: Menggabungkan blok-blok dan membuang padding.

    Args:
        blocks          (list[str]): Daftar blok setelah inverse permutasi.
        original_length (int)      : Panjang teks asli sebelum padding ditambahkan.
                                     Digunakan untuk memotong karakter padding.

    Returns:
        str: Teks setelah blok digabungkan dan padding dihapus.
    """
    joined: str = "".join(blocks)
    return joined[:original_length]


def inverse_substitute(text: str) -> str:
    """
    Langkah 3 Dekripsi: Membalik substitusi menggunakan tabel terbalik.

    Args:
        text (str): Teks yang akan di-inverse substitusi.

    Returns:
        str: Plaintext hasil inverse substitusi.

    Raises:
        ValueError: Jika karakter tidak ditemukan dalam tabel substitusi terbalik.
    """
    result: list[str] = []
    for idx, char in enumerate(text):
        if char not in INVERSE_SUBSTITUTION_TABLE:
            raise ValueError(
                f"Karakter '{char}' pada indeks {idx} tidak ada dalam tabel substitusi terbalik."
            )
        result.append(INVERSE_SUBSTITUTION_TABLE[char])
    return "".join(result)


def decrypt(ciphertext: str, original_length: int) -> dict:
    """
    Fungsi utama Dekripsi: Inverse Permutasi -> Unblocking -> Inverse Substitusi.

    Args:
        ciphertext      (str): Teks terenkripsi yang akan didekripsi.
        original_length (int): Panjang plaintext asli (sebelum padding).
                               Diperlukan untuk membuang padding saat unblocking.

    Returns:
        dict: Dictionary yang berisi semua hasil antara dan akhir:
              - 'ciphertext'        : ciphertext input
              - 'blocks'            : ciphertext dibagi menjadi blok
              - 'inv_permuted_blocks': daftar blok setelah inverse permutasi
              - 'after_inv_permute' : teks gabungan setelah inverse permutasi
              - 'after_unblocking'  : teks setelah padding dibuang
              - 'plaintext'         : plaintext hasil dekripsi akhir

    Raises:
        ValueError: Diteruskan dari inverse_substitute() jika ada karakter tidak valid.
    """
    # Langkah 1: Bagi ciphertext kembali menjadi blok-blok
    blocks: list[str] = [
        ciphertext[i:i + BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)
    ]

    # Langkah 2: Inverse permutasi setiap blok
    inv_permuted_blocks: list[str] = [inverse_permute_block(b) for b in blocks]
    after_inv_permute: str = "".join(inv_permuted_blocks)

    # Langkah 3: Unblocking - buang padding menggunakan panjang asli
    after_unblocking: str = remove_blocking(inv_permuted_blocks, original_length)

    # Langkah 4: Inverse substitusi -> plaintext
    plaintext: str = inverse_substitute(after_unblocking)

    return {
        "ciphertext":          ciphertext,
        "blocks":              blocks,
        "inv_permuted_blocks": inv_permuted_blocks,
        "after_inv_permute":   after_inv_permute,
        "after_unblocking":    after_unblocking,
        "plaintext":           plaintext,
    }


# ===========================================================================
# FUNGSI UTILITAS TAMPILAN
# ===========================================================================

def print_separator(char: str = "=", width: int = 65) -> None:
    """Mencetak garis pemisah horizontal."""
    print(char * width)


def print_section_title(title: str) -> None:
    """Mencetak judul seksi dengan bingkai."""
    print_separator("=")
    print(f"  {title}")
    print_separator("-")


def display_encryption_steps(result: dict) -> None:
    """
    Menampilkan setiap langkah proses enkripsi secara terformat dan mudah dibaca.

    Args:
        result (dict): Dictionary output dari fungsi encrypt().
    """
    print_section_title("PROSES ENKRIPSI")
    print(f"  [INPUT]  Plaintext           : {result['plaintext']}")
    print(f"  [Step 1] Setelah Substitusi  : {result['after_substitute']}")
    print(f"  [Step 2] Blok-blok (w/ pad)  : {' | '.join(result['blocks'])}")
    print(f"  [Step 3] Setelah Permutasi   : {' | '.join(result['permuted_blocks'])}")
    print(f"  [OUTPUT] Ciphertext          : {result['ciphertext']}")
    print_separator()


def display_decryption_steps(result: dict) -> None:
    """
    Menampilkan setiap langkah proses dekripsi secara terformat dan mudah dibaca.

    Args:
        result (dict): Dictionary output dari fungsi decrypt().
    """
    print_section_title("PROSES DEKRIPSI")
    print(f"  [INPUT]  Ciphertext              : {result['ciphertext']}")
    print(f"  [Step 1] Blok-blok               : {' | '.join(result['blocks'])}")
    print(f"  [Step 2] Setelah Inv. Permutasi  : {'  | '.join(result['inv_permuted_blocks'])}")
    print(f"  [Step 3] Setelah Unblocking      : {result['after_unblocking']}")
    print(f"  [OUTPUT] Plaintext               : {result['plaintext']}")
    print_separator()


# ===========================================================================
# BLOK DEMONSTRASI UTAMA
# ===========================================================================

if __name__ == "__main__":
    print_separator("=", 65)
    print("   PROGRAM KRIPTOGRAFI KLASIK")
    print("   Substitusi Monoalfabetik + Blocking + Permutasi")
    print("   Mata Kuliah : Keamanan Sistem")
    print_separator("=", 65)

    # --- Tampilkan Konfigurasi yang Digunakan ---
    print("\n  [KONFIGURASI PROGRAM]")
    print(f"  Ukuran Blok           : {BLOCK_SIZE} karakter")
    print(f"  Karakter Padding      : '{PADDING_CHAR}'")
    print(f"  Pola Permutasi (enc)  : {PERMUTATION_PATTERN}  (0-based index)")
    print(f"  Pola Permutasi (dec)  : {INVERSE_PERMUTATION_PATTERN}  (0-based index)")
    print()
    print("  [TABEL SUBSTITUSI]")
    print("  Asli  :", " ".join(SUBSTITUTION_TABLE.keys()))
    print("  Subs  :", " ".join(SUBSTITUTION_TABLE.values()))

    # ------------------------------------------------------------------
    # Test Case: berbagai input teks
    # ------------------------------------------------------------------
    test_cases: list[str] = [
        "NAMA",
        "KEAMANAN",
        "HELLO",
        "PYTHON3",
        "12345",
    ]

    for test_input in test_cases:
        print(f"\n{'#'*65}")
        print(f"  TEST INPUT: \"{test_input}\"")
        print(f"{'#'*65}")

        try:
            # ---- ENKRIPSI ----
            enc_result = encrypt(test_input)
            display_encryption_steps(enc_result)

            # ---- DEKRIPSI ----
            # original_length = panjang plaintext sebelum padding
            original_len: int = len(enc_result["plaintext"])
            dec_result = decrypt(enc_result["ciphertext"], original_length=original_len)
            display_decryption_steps(dec_result)

            # ---- VERIFIKASI ROUND-TRIP ----
            match: bool = enc_result["plaintext"] == dec_result["plaintext"]
            status: str = "✓  BERHASIL (round-trip verified)" if match else "✗  GAGAL"
            print(f"\n  [VERIFIKASI] {status}")
            print(f"               '{enc_result['plaintext']}' == '{dec_result['plaintext']}'")

        except ValueError as e:
            print(f"\n  [ERROR] {e}")

    # ------------------------------------------------------------------
    # Test Case: Demonstrasi penanganan error karakter tidak valid
    # ------------------------------------------------------------------
    print(f"\n{'#'*65}")
    print("  TEST INPUT: \"HELLO!\"  (karakter '!' tidak valid)")
    print(f"{'#'*65}")
    try:
        encrypt("HELLO!")
    except ValueError as e:
        print(f"\n  [ERROR TERTANGKAP]\n  {e}")

    print(f"\n{'='*65}")
    print("  Program selesai.")
    print(f"{'='*65}\n")
