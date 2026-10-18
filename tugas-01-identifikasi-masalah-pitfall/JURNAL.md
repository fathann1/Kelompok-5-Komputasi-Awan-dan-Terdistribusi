# Jurnal Proses — Tugas 1

Jurnal ini digunakan untuk mencatat proses diskusi, pembagian tugas, perubahan pemikiran, dan review silang selama pengerjaan Tugas 1 — Identifikasi Masalah & Pitfall Sistem Terdistribusi pada studi kasus FoodGo.

## [Tanggal diskusi 1]

- **Peserta:** [isi nama anggota yang benar-benar hadir]
- **Poin diskusi:**
  - Membahas masalah yang dialami FoodGo ketika jumlah pesanan meningkat, terutama saat jam makan siang atau promo besar.
  - Mengidentifikasi gejala utama, yaitu aplikasi lambat, permintaan mengalami timeout, server crash, dan perlunya restart manual.
  - Membahas asumsi keliru dalam sistem terdistribusi, khususnya anggapan bahwa jaringan selalu dapat diandalkan dan komunikasi antarservice tidak membutuhkan waktu.
  - Menemukan masalah arsitektur karena modul pesanan, pembayaran, dan notifikasi berjalan pada satu proses monolitik.
  - Menentukan tiga fokus analisis, yaitu The Network Is Reliable, Latency Is Zero, dan Single Point of Failure.
- **Perbedaan pendapat (jika ada):** [catat perbedaan pendapat yang benar-benar muncul selama diskusi]

## [Tanggal diskusi 2]

- **Peserta:** [isi nama anggota yang benar-benar hadir]
- **Poin diskusi:**
  - Membahas solusi awal untuk mengatasi kegagalan komunikasi, seperti timeout, retry terbatas dengan exponential backoff, dan circuit breaker.
  - Membahas pentingnya mengatur timeout agar permintaan tidak menunggu tanpa batas, tetapi juga tidak terlalu cepat dihentikan.
  - Membahas kemungkinan memisahkan modul yang paling bermasalah dan menjalankan beberapa instance untuk meningkatkan kapasitas serta ketersediaan.
  - Menyadari bahwa retry dapat menambah beban ketika server sedang bermasalah dan pemisahan service menambah kompleksitas sistem.
  - Menyusun kesimpulan awal sebagai dasar perancangan arsitektur pada Tugas 2.
- **Perbedaan pendapat (jika ada):** [catat perbedaan pendapat yang benar-benar muncul selama diskusi]

## Pembagian Tugas

| Nama | Bagian yang Dikerjakan |
|---|---|
| Gusti Rifan | Pitfall 1: The Network Is Reliable |
| Gde Andika Ananta Putra | Pitfall 2: Latency Is Zero |
| Dyandra Alifyan Nugroho | Pitfall 3: Single Point of Failure |
| Muhammad Rajwa Al Fathan Koessaputra | Kesimpulan kelompok dan review silang |

## Review Silang

- [Nama reviewer]: meninjau analisis [nama anggota] dan memberikan masukan tentang kesesuaian bukti skenario dengan pitfall yang dipilih.
- [Nama reviewer]: memeriksa hubungan sebab-akibat pada bagian dampak terhadap FoodGo.
- [Nama reviewer]: meninjau solusi desain dan trade-off agar sesuai dengan permasalahan yang ditemukan.
- **Perbaikan setelah review:** [isi masukan dan perubahan yang benar-benar dilakukan kelompok]

## Log Penggunaan AI (Level 2)

AI digunakan untuk membantu brainstorming ide, memahami konsep pitfall sistem terdistribusi, dan menyusun kerangka pengerjaan. Analisis akhir perlu diperiksa, dikembangkan, dan dipahami oleh anggota kelompok.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18 Oktober 2026 | ChatGPT | Membantu mengidentifikasi pitfall sistem terdistribusi pada studi kasus FoodGo dan menyusun pembagian analisis sesuai template kelompok. | Kandidat pitfall meliputi The Network Is Reliable, Latency Is Zero, dan Single Point of Failure. Solusi yang dapat dipertimbangkan meliputi timeout, retry terbatas, circuit breaker, dan pemisahan modul secara bertahap. | Kelompok perlu memeriksa kembali setiap pitfall terhadap kalimat spesifik pada skenario, mendiskusikan mekanisme kegagalan, memilih solusi yang sesuai, serta menulis ulang analisis berdasarkan pemahaman sendiri. |
| 18 Oktober 2026 | ChatGPT | Membantu menyusun struktur README.md dan JURNAL.md berdasarkan template tugas FoodGo. | Saran berupa struktur dokumentasi, pembagian tugas anggota, daftar topik diskusi, dan format pencatatan review silang. | Struktur disesuaikan dengan file yang tersedia di repository GitHub kelompok. Catatan kehadiran, hasil diskusi, perbedaan pendapat, dan review harus diisi sesuai kejadian sebenarnya. |

## Refleksi Kelompok

Melalui tugas ini, kelompok mempelajari bahwa kegagalan sistem terdistribusi tidak hanya disebabkan oleh kapasitas server, tetapi juga oleh asumsi yang keliru tentang jaringan, keterlambatan komunikasi, dan ketergantungan antarkomponen.

Kelompok juga memahami bahwa setiap solusi memiliki trade-off. Timeout dapat membatasi waktu tunggu, retry dapat membantu mengatasi gangguan sementara tetapi berisiko menambah beban, sedangkan pemisahan service dapat meningkatkan isolasi dan skalabilitas tetapi menambah kompleksitas pengelolaan.

Hasil analisis ini akan digunakan sebagai bahan awal untuk merancang sistem yang lebih tangguh pada Tugas 2.
