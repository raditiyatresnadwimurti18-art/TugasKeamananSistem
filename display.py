"""
=============================================================================
  display.py - Fungsi Tampilan & Utilitas
  Mengelola semua output ke layar: banner, separator, dan
  tampilan langkah-langkah enkripsi/dekripsi.
=============================================================================
"""

from config import (
    BLOCK_SIZE,
    PADDING_CHAR,
    KEY_BLOCKING_1BASED,
    KEY_BLOCKING_PATTERN,
    INVERSE_KEY_BLOCKING,
    KEY_PERMUTATION_1BASED,
    KEY_PERMUTATION_PATTERN,
    INVERSE_KEY_PERMUTATION,
    SUBSTITUTION_TABLE,
)

DISPLAY_WIDTH: int = 70


# ---------------------------------------------------------------------------
# UTILITAS DASAR
# ---------------------------------------------------------------------------

def sep(char: str = "=", width: int = DISPLAY_WIDTH) -> None:
    """Cetak garis pemisah horizontal."""
    print(char * width)


def header(title: str) -> None:
    """Cetak judul seksi dengan bingkai."""
    sep("=")
    print(f"  {title}")
    sep("-")


def clear_screen() -> None:
    """Bersihkan layar konsol (cross-platform)."""
    import os
    os.system("cls" if os.name == "nt" else "clear")


def fmt_blocks(blocks: list[str]) -> str:
    """Format daftar blok menjadi string yang mudah dibaca."""
    return "  ".join(f"[{b}]" for b in blocks)


# ---------------------------------------------------------------------------
# BANNER & INFO PROGRAM
# ---------------------------------------------------------------------------

def print_banner() -> None:
    """Tampilkan banner pembuka program."""
    sep("=")
    print("  ██████╗██████╗ ██╗██████╗ ████████╗ ██████╗ ")
    print(" ██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝██╔═══██╗")
    print(" ██║     ██████╔╝██║██████╔╝   ██║   ██║   ██║")
    print(" ██║     ██╔══██╗██║██╔═══╝    ██║   ██║   ██║")
    print(" ╚██████╗██║  ██║██║██║        ██║   ╚██████╔╝")
    print("  ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝    ╚═════╝")
    sep("-")
    print("  KRIPTOGRAFI KLASIK  |  Mata Kuliah: Keamanan Sistem")
    print("  Substitusi + Blocking (8 char) + Key Blocking + Key Permutasi")
    sep("=")


def print_config() -> None:
    """Tampilkan konfigurasi cipher yang sedang digunakan."""
    header("KONFIGURASI CIPHER")
    print(f"  Ukuran Blok          : {BLOCK_SIZE} karakter")
    print(f"  Karakter Padding     : '{PADDING_CHAR}'")
    print()
    kb1 = " ".join(str(k) for k in KEY_BLOCKING_1BASED)
    kb0 = " ".join(str(k) for k in KEY_BLOCKING_PATTERN)
    print(f"  Key Blocking (enc)   : [{kb1}]  (1-based)")
    print(f"                       : [{kb0}]  (0-based, dipakai program)")
    ikb = " ".join(str(k) for k in INVERSE_KEY_BLOCKING)
    print(f"  Key Blocking (dec)   : [{ikb}]  (inverse, 0-based)")
    print()
    kp1 = " ".join(str(k) for k in KEY_PERMUTATION_1BASED)
    kp0 = " ".join(str(k) for k in KEY_PERMUTATION_PATTERN)
    print(f"  Key Permutasi (enc)  : [{kp1}]  (1-based)")
    print(f"                       : [{kp0}]  (0-based, dipakai program)")
    ikp = " ".join(str(k) for k in INVERSE_KEY_PERMUTATION)
    print(f"  Key Permutasi (dec)  : [{ikp}]  (inverse, 0-based)")
    print()
    sep("-")
    print("  TABEL SUBSTITUSI:")
    keys = list(SUBSTITUTION_TABLE.keys())
    vals = list(SUBSTITUTION_TABLE.values())
    chunk = 13
    for i in range(0, len(keys), chunk):
        k_row = " ".join(f"{c:>2}" for c in keys[i:i+chunk])
        v_row = " ".join(f"{c:>2}" for c in vals[i:i+chunk])
        print(f"  Asli  : {k_row}")
        print(f"  Subs  : {v_row}")
        if i + chunk < len(keys):
            sep(".")
    sep("=")


# ---------------------------------------------------------------------------
# TAMPILAN HASIL ENKRIPSI (5 Langkah)
# ---------------------------------------------------------------------------

def display_encryption_steps(result: dict) -> None:
    """
    Cetak setiap langkah proses enkripsi secara terformat.

    Args:
        result (dict): Output dari encryption.encrypt().
    """
    header("HASIL ENKRIPSI - LANGKAH DEMI LANGKAH")
    print(f"  [INPUT ]  Plaintext              : {result['plaintext']}")
    sep(".")
    print(f"  [Step 1]  Setelah Substitusi     : {result['after_substitute']}")
    sep(".")
    print(f"  [Step 2]  Blok 8-char (+ padding):")
    print(f"            {fmt_blocks(result['blocks'])}")
    sep(".")
    kb = " ".join(str(k) for k in KEY_BLOCKING_1BASED)
    print(f"  [Step 3]  Key Blocking [{kb}]:")
    print(f"            {fmt_blocks(result['blocked_blocks'])}")
    sep(".")
    kp = " ".join(str(k) for k in KEY_PERMUTATION_1BASED)
    print(f"  [Step 4]  Key Permutasi [{kp}]:")
    print(f"            {fmt_blocks(result['permuted_blocks'])}")
    sep(".")
    print(f"  [OUTPUT]  Ciphertext             : {result['ciphertext']}")
    sep("=")


# ---------------------------------------------------------------------------
# TAMPILAN HASIL DEKRIPSI (Kebalikan 5 Langkah)
# ---------------------------------------------------------------------------

def display_decryption_steps(result: dict) -> None:
    """
    Cetak setiap langkah proses dekripsi secara terformat.

    Args:
        result (dict): Output dari decryption.decrypt().
    """
    header("HASIL DEKRIPSI - LANGKAH DEMI LANGKAH")
    print(f"  [INPUT ]  Ciphertext             : {result['ciphertext']}")
    sep(".")
    print(f"  [Step 1]  Blok 8-char:")
    print(f"            {fmt_blocks(result['blocks'])}")
    sep(".")
    ikp = " ".join(str(k) for k in INVERSE_KEY_PERMUTATION)
    print(f"  [Step 2]  Inv. Key Permutasi [{ikp}]:")
    print(f"            {fmt_blocks(result['inv_perm_blocks'])}")
    sep(".")
    ikb = " ".join(str(k) for k in INVERSE_KEY_BLOCKING)
    print(f"  [Step 3]  Inv. Key Blocking [{ikb}]:")
    print(f"            {fmt_blocks(result['inv_blocked_blocks'])}")
    sep(".")
    print(f"  [Step 4]  Setelah Unblocking     : {result['after_unblocking']}")
    sep(".")
    print(f"  [OUTPUT]  Plaintext              : {result['plaintext']}")
    sep("=")


# ---------------------------------------------------------------------------
# TAMPILAN VERIFIKASI
# ---------------------------------------------------------------------------

def display_verification(original: str, decrypted: str) -> None:
    """Tampilkan hasil verifikasi round-trip."""
    match = original == decrypted
    icon  = "v" if match else "x"
    label = "BERHASIL - teks asli terpulihkan!" if match else "GAGAL - teks tidak cocok."
    sep("-")
    print(f"  [{icon}] VERIFIKASI: {label}")
    if not match:
        print(f"      Asli     : '{original}'")
        print(f"      Dekripsi : '{decrypted}'")
    sep("=")
