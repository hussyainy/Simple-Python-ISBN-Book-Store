# 📚 Kedai Buku Python

Skrip **Kedai Buku Python** untuk belajar asas carian & pengurusan data buku dalam terminal.

## 🎯 Fungsi
- Cari buku **ikut ISBN (13 digit)** — jika tak tepat, beri **cadangan ISBN hampir sama** (max 5).
- Senarai buku **ikut harga** (murah → mahal) menggunakan **Merge Sort**.
- Jadual **auto-resize ikut saiz terminal** dan `clear screen` setiap tindakan.

## 🛠 Teknologi
- Python 3.x
- Standard library sahaja (tiada pakej tambahan)

## 📂 Struktur
```
.
├── bookstore.py     # Kod utama (menu, carian, jadual)
├── book_data.py     # 100 ISBN buku Melayu
└── assets/
    ├── screenshot-found.png
    └── screenshot-suggest.png
```

## 🚀 Cara Jalankan
```bash
python bookstore.py
```

## 🖼️ Tangkapan Skrin

**Carian berjaya (ISBN tepat)**
  
![Buku dijumpai](assets/screenshot-found.png)

**Cadangan bila ISBN tak dijumpai**
  
![Cadangan ISBN](assets/screenshot-suggest.png)

## 💡 Nota
- `book_data.py` mengandungi 100 tajuk buku Melayu (fiksyen & bukan fiksyen) dengan harga realistik.
- Carian exact guna **Binary Search** (perlu data disusun ikut ISBN).
- Paparan jadual guna ASCII box dan **auto truncate** teks yang terlalu panjang.

## 📜 Lesen
MIT — bebas guna & ubah suai.
