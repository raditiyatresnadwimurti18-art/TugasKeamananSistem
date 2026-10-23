"""
=============================================================================
  main.py - Entry Point & Menu Interaktif
  Jalankan file ini untuk memulai program kriptografi klasik.

  Cara menjalankan:
      python main.py
=============================================================================
"""

from encryption import encrypt
from decryption import decrypt
from display import (
    print_banner,
    print_config,
    display_encryption_steps,
    display_decryption_steps,
    display_verification,
    sep,
    header,
)
from config import SUBSTITUTION_TABLE, BLOCK_SIZE


# ===========================================================================
# FUNGSI MENU
# ===========================================================================

def get_menu_choice() -> str:
    """
    Tampilkan menu utama dan minta pilihan pengguna.

    Returns:
        str: '1' (enkripsi), '2' (dekripsi), '3' (info), atau '0' (keluar).
    """
    print()
    sep("=")
    print("  MENU UTAMA")
    sep("-")
    print("  [1]  Enkripsi teks")
    print("  [2]  Dekripsi teks")
    print("  [3]  Lihat konfigurasi & tabel substitusi")
    print("  [0]  Keluar")
    sep("=")
    return input("  Pilih menu (0-3): ").strip()


def ask_continue() -> bool:
    """
    Tanya pengguna apakah ingin kembali ke menu utama.

    Returns:
        bool: True jika lanjut, False jika keluar.
    """
    sep("-")
    jawab = input("  Kembali ke menu utama? (y/n): ").strip().lower()
    return jawab in ("y", "yes", "ya", "")


# ===========================================================================
# SESSION STATE (Menyimpan hasil enkripsi terakhir untuk kemudahan dekripsi)
# ===========================================================================

SESSION_STATE: dict = {
    "last_result": None,
}


# ===========================================================================
# HANDLER: ENKRIPSI
# ===========================================================================

def handle_encrypt() -> None:
    """Proses enkripsi interaktif: minta input, tampilkan 5 langkah."""
    header("ENKRIPSI TEKS")

    supported = " ".join(sorted(SUBSTITUTION_TABLE.keys()))
    print(f"  Karakter yang didukung:\n  {supported}")
    print(f"  (Input akan otomatis diubah ke HURUF BESAR)")
    sep("-")

    raw = input("  Masukkan teks yang akan dienkripsi: ").strip()
    if not raw:
        print("  [!] Input tidak boleh kosong.")
        return

    try:
        result = encrypt(raw)
        display_encryption_steps(result)

        original_len = len(result["plaintext"])
        SESSION_STATE["last_result"] = result

        print(f"  [i] Panjang plaintext   : {original_len} karakter")
        print(f"  [i] Simpan nilai ini    : original_length = {original_len}")
        print(f"      (PENTING: Masukkan angka {original_len} saat dekripsi agar")
        print(f"       karakter padding dibuang dan teks kembali seperti semula!)")
        sep("=")

        # Opsi langsung tes dekripsi untuk membuktikan round-trip
        quick_test = input(
            "  Ingin langsung dekripsi ciphertext ini untuk verifikasi? (y/n) [y]: "
        ).strip().lower()

        if quick_test in ("", "y", "ya", "yes"):
            handle_decrypt(
                prefilled_cipher=result["ciphertext"],
                prefilled_len=original_len,
                expected_plaintext=result["plaintext"],
            )

    except ValueError as e:
        sep("-")
        print(f"  [ERROR] {e}")
        sep("=")


# ===========================================================================
# HANDLER: DEKRIPSI
# ===========================================================================

def handle_decrypt(
    prefilled_cipher: str | None = None,
    prefilled_len: int | None = None,
    expected_plaintext: str | None = None,
) -> None:
    """Proses dekripsi interaktif: minta ciphertext & panjang asli."""
    header("DEKRIPSI TEKS")
    print(f"  Masukkan ciphertext (harus kelipatan {BLOCK_SIZE} karakter).")
    print(f"  Panjang plaintext asli diperlukan untuk membuang padding.")
    sep("-")

    last_res = SESSION_STATE.get("last_result")

    # Ambil Ciphertext
    if prefilled_cipher:
        cipher = prefilled_cipher
        print(f"  Ciphertext (otomatis) : {cipher}")
    else:
        if last_res:
            default_cipher = last_res["ciphertext"]
            cipher_input = input(
                f"  Masukkan ciphertext [Enter untuk memakai hasil terakhir]: "
            ).strip()
            cipher = cipher_input if cipher_input else default_cipher
            if cipher == default_cipher:
                expected_plaintext = last_res["plaintext"]
        else:
            cipher = input("  Masukkan ciphertext  : ").strip()

    if not cipher:
        print("  [!] Ciphertext tidak boleh kosong.")
        return

    if len(cipher) % BLOCK_SIZE != 0:
        print(
            f"  [ERROR] Panjang ciphertext ({len(cipher)}) bukan kelipatan "
            f"ukuran blok ({BLOCK_SIZE}).\n"
            f"          Pastikan ciphertext tidak terpotong."
        )
        return

    max_len = len(cipher)

    # Ambil Panjang Plaintext Asli
    if prefilled_len is not None:
        original_length = prefilled_len
        print(f"  Panjang asli (otomatis) : {original_length}")
    else:
        suggested_len = None
        if last_res and cipher == last_res.get("ciphertext"):
            suggested_len = len(last_res["plaintext"])

        if suggested_len is not None:
            raw_len = input(
                f"  Panjang plaintext asli (1-{max_len}, Enter={suggested_len}): "
            ).strip()
            if raw_len == "":
                original_length = suggested_len
            else:
                try:
                    original_length = int(raw_len)
                    if not (1 <= original_length <= max_len):
                        raise ValueError
                except ValueError:
                    print(f"  [ERROR] Masukkan angka antara 1 dan {max_len}.")
                    return
        else:
            raw_len = input(
                f"  Panjang plaintext asli sebelum padding (1-{max_len}): "
            ).strip()
            if raw_len == "":
                print(
                    "  [!] Panjang plaintext asli harus diisi untuk membuang padding.\n"
                    f"      (Ketik angka antara 1 dan {max_len})."
                )
                return
            try:
                original_length = int(raw_len)
                if not (1 <= original_length <= max_len):
                    raise ValueError
            except ValueError:
                print(f"  [ERROR] Masukkan angka antara 1 dan {max_len}.")
                return

    try:
        result = decrypt(cipher, original_length)
        display_decryption_steps(result)

        if expected_plaintext is not None:
            display_verification(expected_plaintext, result["plaintext"])
        else:
            sep("-")
            print("  [i] Dekripsi selesai!")
            sep("=")

    except ValueError as e:
        sep("-")
        print(f"  [ERROR] {e}")
        sep("=")


# ===========================================================================
# LOOP UTAMA
# ===========================================================================

def main() -> None:
    """Fungsi utama: tampilkan banner lalu jalankan loop menu interaktif."""
    print_banner()

    while True:
        choice = get_menu_choice()

        if choice == "1":
            handle_encrypt()
            if not ask_continue():
                break

        elif choice == "2":
            handle_decrypt()
            if not ask_continue():
                break

        elif choice == "3":
            print_config()
            if not ask_continue():
                break

        elif choice == "0":
            break

        else:
            sep("-")
            print("  [!] Pilihan tidak valid. Masukkan angka 0-3.")

    sep("=")
    print("  Terima kasih telah menggunakan program ini. Sampai jumpa!")
    sep("=")


# ===========================================================================
# ENTRY POINT
# ===========================================================================

if __name__ == "__main__":
    main()
