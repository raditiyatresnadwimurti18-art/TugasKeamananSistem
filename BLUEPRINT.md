# Blueprint: Program Kriptografi Klasik
**Mata Kuliah:** Keamanan Sistem
**Bahasa:** Python 3 (pure standard library)

---

## Deskripsi Umum

Program ini mengimplementasikan algoritma kriptografi klasik berbasis tiga metode yang dirangkai secara berlapis:

1. **Substitusi Monoalfabetik** — setiap karakter diganti dengan karakter lain sesuai tabel tetap.
2. **Blocking** — teks dibagi menjadi blok-blok 8 karakter (dengan padding jika perlu).
3. **Key Blocking** — posisi karakter dalam setiap blok diacak menggunakan kunci `7 2 6 8 1 4 3 5`.
4. **Key Permutasi** — posisi karakter diacak kembali menggunakan kunci `2 4 1 7 5 8 3 6`.

---

## Struktur File

```
TugasKeamananSistem/
├── config.py          → Konstanta: tabel substitusi, block size, key blocking, key permutasi
├── encryption.py      → Fungsi enkripsi 5 langkah
├── decryption.py      → Fungsi dekripsi (membalik 5 langkah)
├── display.py         → Fungsi tampilan: banner, separator, langkah-langkah
├── main.py            → Entry point & menu interaktif
├── classical_cipher.py→ Versi monolitik lama (referensi)
└── BLUEPRINT.md       → Dokumen ini
```

---

## Tabel Substitusi Monoalfabetik

| Asli  | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T |
|-------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Subs  | B | F | 1 | K | Q | G | A | T | P | J | 6 | H | Y | D | 2 | X | 5 | M | V | 7 |

| Asli  | U | V | W | X | Y | Z | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | - | . | , | (spasi) |
|-------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---------|
| Subs  | C | 8 | 4 | I | 9 | N | R | E | U | 3 | L | S | W | - | . | , | O | Z | 0 | (spasi) |

> Spasi dipetakan ke dirinya sendiri (dipertahankan dalam ciphertext).

---

## Alur Algoritma Enkripsi (5 Langkah)

```
PLAINTEXT
    |
    v  [Langkah 1] Normalisasi & Substitusi
    |  - Ubah ke huruf kapital
    |  - Ganti tiap karakter sesuai tabel substitusi
    |
    v  [Langkah 2] Pembentukan Blok & Padding
    |  - Hitung panjang teks hasil substitusi
    |  - Tambahkan '.' di akhir jika bukan kelipatan 8
    |  - Bagi menjadi blok-blok 8 karakter
    |
    v  [Langkah 3] Key Blocking [7 2 6 8 1 4 3 5]
    |  - Untuk setiap blok 8 karakter:
    |    hasil[0] = blok[6]  (indeks ke-7, 1-based)
    |    hasil[1] = blok[1]  (indeks ke-2, 1-based)
    |    hasil[2] = blok[5]  (indeks ke-6, 1-based)
    |    hasil[3] = blok[7]  (indeks ke-8, 1-based)
    |    hasil[4] = blok[0]  (indeks ke-1, 1-based)
    |    hasil[5] = blok[3]  (indeks ke-4, 1-based)
    |    hasil[6] = blok[2]  (indeks ke-3, 1-based)
    |    hasil[7] = blok[4]  (indeks ke-5, 1-based)
    |
    v  [Langkah 4] Key Permutasi [2 4 1 7 5 8 3 6]
    |  - Untuk setiap blok perantara (hasil Langkah 3):
    |    final[0] = inter[1]  (indeks ke-2, 1-based)
    |    final[1] = inter[3]  (indeks ke-4, 1-based)
    |    final[2] = inter[0]  (indeks ke-1, 1-based)
    |    final[3] = inter[6]  (indeks ke-7, 1-based)
    |    final[4] = inter[4]  (indeks ke-5, 1-based)
    |    final[5] = inter[7]  (indeks ke-8, 1-based)
    |    final[6] = inter[2]  (indeks ke-3, 1-based)
    |    final[7] = inter[5]  (indeks ke-6, 1-based)
    |
    v  [Langkah 5] Penggabungan
    
CIPHERTEXT
```

---

## Alur Algoritma Dekripsi (Membalik 5 Langkah)

```
CIPHERTEXT
    |
    v  [Langkah D1] Bagi menjadi blok 8 karakter
    |
    v  [Langkah D2] Inverse Key Permutasi [2 0 6 1 4 7 3 5] (0-based)
    |  - Membalik Langkah 4 enkripsi
    |
    v  [Langkah D3] Inverse Key Blocking  [4 1 6 5 7 2 0 3] (0-based)
    |  - Membalik Langkah 3 enkripsi
    |
    v  [Langkah D4] Unblocking - Buang Padding
    |  - Gabungkan semua blok
    |  - Potong sejumlah 'original_length' karakter dari depan
    |
    v  [Langkah D5] Inverse Substitusi
    |  - Kembalikan setiap karakter ke plaintext aslinya
    
PLAINTEXT
```

---

## Kunci Program

| Parameter            | Nilai                           | Keterangan                    |
|----------------------|---------------------------------|-------------------------------|
| Block Size           | 8 karakter                      | Ukuran setiap blok            |
| Padding Char         | `.` (titik)                     | Pengisi jika bukan kelipatan 8|
| Key Blocking (enc)   | `7 2 6 8 1 4 3 5` (1-based)    | Konversi: `[6,1,5,7,0,3,2,4]` |
| Key Blocking (dec)   | `[4,1,6,5,7,2,0,3]` (0-based)  | Auto-generated (inverse)      |
| Key Permutasi (enc)  | `2 4 1 7 5 8 3 6` (1-based)    | Konversi: `[1,3,0,6,4,7,2,5]` |
| Key Permutasi (dec)  | `[2,0,6,1,4,7,3,5]` (0-based)  | Auto-generated (inverse)      |

---

## Contoh Enkripsi Manual: "NAMA"

```
Plaintext        : NAMA
Step 1 (Subst.)  : D B Y B     (N→D, A→B, M→Y, A→B)
Step 2 (Blocking): [D B Y B . . . .] — 1 blok (4 char + 4 padding '.')
Step 3 (Key Blk) : Ambil posisi [6,1,5,7,0,3,2,4] dari blok
                   [.][B][.][.][D][.][Y][B] → [. B . . D . Y B]
Step 4 (Key Perm): Ambil posisi [1,3,0,6,4,7,2,5] dari blok perantara
                   → B . . Y D B . .
Step 5 (Gabung)  : Ciphertext = "B..YD..B"
```

---

## Cara Menjalankan

```bash
# Pastikan semua file .py berada dalam satu folder
python main.py
```

### Menu yang tersedia:
- **[1] Enkripsi** — input teks bebas, tampil 5 langkah secara detail
- **[2] Dekripsi** — input ciphertext + panjang asli, tampil 5 langkah balik
- **[3] Konfigurasi** — tampil tabel substitusi & semua kunci
- **[0] Keluar**

---

## Ketentuan Input

- Karakter yang didukung: `A-Z`, `0-9`, `- . ,` dan **spasi**
- Input huruf kecil akan **otomatis dikonversi** ke huruf besar
- Untuk dekripsi, Anda perlu mengetahui **panjang plaintext asli** (ditampilkan setelah enkripsi)

---

## Catatan Teknis

- **Pure Python 3** — tidak membutuhkan library eksternal
- Inverse key di-generate **otomatis** dari key enkripsi menggunakan:
  ```python
  INVERSE_KEY = [KEY.index(i) for i in range(BLOCK_SIZE)]
  ```
- **Penanganan Padding & `original_length`:**
  Karakter padding `.` berada di dalam tabel substitusi (berpasangan dengan karakter asli `'9'`).
  Jika saat dekripsi `original_length` tidak diisi sesuai panjang teks asli (misal memakai panjang total ciphertext),
  karakter `.` di akhir blok tidak terpotong dan akan di-inverse substitusi menjadi `'999999'`.
  Oleh karena itu, selalu masukkan `original_length` sesuai panjang teks sebelum padding.

---

*Dokumen dibuat otomatis — Keamanan Sistem, 2026*
