# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 5

| Nama | NIM | Kontribusi |
|---|---|---|
| Gusti Rifan | 103072400150 | Pitfall 1: The Network Is Reliable |
| Gde Andika Ananta Putra | 103072400161 | Pitfall 2: Latency Is Zero |
| Dyandra Alifyan Nugroho | 103072400014 | Pitfall 3: Single Point of Failure |
| Muhammad Rajwa Al Fathan Koessaputra | 103072400113 | Kesimpulan kelompok dan review silang |

---

## Pitfall 1: The Network Is Reliable — ditulis oleh Gusti Rifan

**Bukti di skenario:**

"Network is always reliable, no need for retry" dan tidak adanya mekanisme timeout pada komunikasi antarservice.

**Kenapa ini keliru:**

[Jelaskan mengapa komunikasi jaringan dapat mengalami gangguan, kehilangan respons, atau kegagalan sementara.]

**Dampak ke FoodGo:**

[Uraikan bagaimana kegagalan komunikasi memengaruhi pemrosesan pesanan dan pembayaran.]

**Solusi desain awal:**

- Menerapkan timeout pada komunikasi antarservice.
- Menggunakan retry terbatas dengan exponential backoff.
- Menerapkan circuit breaker untuk mencegah permintaan terus-menerus ke service yang bermasalah.
- Mempertimbangkan idempotency untuk mencegah transaksi ganda akibat retry.

**Trade-off:**

[Jelaskan bagaimana retry dapat menambah beban sistem dan mengapa jumlah percobaan perlu dibatasi.]

---

## Pitfall 2: Latency Is Zero — ditulis oleh Gde Andika Ananta Putra

**Bukti di skenario:**

Modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu. Saat trafik meningkat, aplikasi menjadi lambat dan beberapa permintaan mengalami timeout.

**Kenapa ini keliru:**

[Jelaskan mengapa komunikasi antarservice membutuhkan waktu dan bagaimana keterlambatan dapat terjadi.]

**Dampak ke FoodGo:**

[Analisis bagaimana thread yang tertahan dapat menyebabkan penumpukan permintaan, penggunaan resource meningkat, dan respons aplikasi melambat.]

**Solusi desain awal:**

- Menetapkan batas waktu tunggu untuk setiap pemanggilan service.
- Menyesuaikan timeout dengan kebutuhan masing-masing operasi.
- Membatasi jumlah permintaan yang diproses secara bersamaan.
- Memantau waktu respons dan jumlah permintaan yang gagal.

**Trade-off:**

[Jelaskan risiko timeout yang terlalu singkat dapat menghentikan operasi yang sebenarnya masih bisa berhasil.]

---

## Pitfall 3: Single Point of Failure pada Arsitektur Monolitik — ditulis oleh Dyandra Alifyan Nugroho

**Bukti di skenario:**

Satu server menangani modul pesanan, pembayaran, dan notifikasi kurir dalam satu proses monolitik. Ketika trafik meningkat, server kewalahan dan terkadang mengalami crash total.

**Kenapa ini keliru:**

[Jelaskan risiko ketergantungan seluruh modul pada satu proses atau server, serta perbedaan skalabilitas dan ketersediaan sistem.]

**Dampak ke FoodGo:**

[Uraikan bagaimana beban tinggi pada satu modul dapat memengaruhi modul lain dan bagaimana crash dapat menghentikan seluruh fungsi aplikasi.]

**Solusi desain awal:**

- Memisahkan modul secara bertahap berdasarkan kebutuhan dan beban.
- Mengisolasi komponen yang paling berat agar gangguannya tidak langsung memengaruhi seluruh aplikasi.
- Mempertimbangkan beberapa instance aplikasi dan load balancing.
- Menambahkan mekanisme pemantauan dan pemulihan otomatis.

**Trade-off:**

[Jelaskan bertambahnya kompleksitas komunikasi jaringan, deployment, pemantauan, dan konsistensi data setelah modul dipisahkan.]

---

## Kesimpulan Kelompok — Muhammad Rajwa Al Fathan Koessaputra

**Ringkasan masalah:**

[Gabungkan hasil analisis ketiga pitfall dan jelaskan hubungan antara asumsi jaringan, keterlambatan komunikasi, dan keterbatasan arsitektur.]

**Rekomendasi arsitektur:**

[Diskusikan apakah FoodGo sebaiknya memperbaiki monolitik terlebih dahulu atau mulai memisahkan modul tertentu. Sertakan alasan berdasarkan hasil diskusi.]

**Hubungan dengan Tugas 2:**

[Jelaskan bagaimana hasil identifikasi masalah ini menjadi dasar untuk menentukan arsitektur, komponen, dan mekanisme komunikasi yang akan dirancang pada tugas berikutnya.]
