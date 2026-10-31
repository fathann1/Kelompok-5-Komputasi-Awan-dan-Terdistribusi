# Jurnal Proses — Tugas 2

> Catatan: bagian bertanda **[isi]** perlu dilengkapi kelompok sesuai kejadian sebenarnya (tanggal, peserta, media, dan detail yang hanya kalian yang tahu).

## [isi tanggal diskusi 1] — Pemilihan gaya arsitektur dan pembagian tugas
- Peserta: Gusti Rifan, Gde Andika Ananta Putra, Dyandra Alifyan Nugroho, Muhammad Rajwa Al Fathan Koessaputra. **[sesuaikan jika ada yang tidak hadir]**
- Media: **[tatap muka / online]**
- Poin diskusi:
  - Membaca ulang studi kasus: masalah utama FoodGo adalah semua modul (pesanan, pembayaran, notifikasi kurir, katalog resto) berjalan dalam satu aplikasi monolitik, sehingga satu deploy membuat semua modul ikut restart.
  - Menghubungkan dengan hasil Tugas 1: pitfall *The Network Is Reliable*, *Latency Is Zero*, dan *Single Point of Failure* harus punya tempat penyelesaian yang jelas di arsitektur baru.
- Opsi arsitektur yang dipertimbangkan:
  - **SOA murni (semua sinkron):** setiap modul jadi service sendiri. Kelemahannya, Service Pesanan harus memanggil Resto, Kurir, dan Notifikasi satu per satu dan menunggu semuanya. Jika Service Kurir sedang deploy ulang, pembuatan pesanan ikut gagal, artinya masalah *coupling* dan *latency is zero* dari Tugas 1 terulang.
  - **Publish-Subscribe murni (semua event):** semua modul hanya berkomunikasi lewat event. Kelemahannya, langkah yang butuh jawaban pasti saat itu juga (cek menu, proses pembayaran) menjadi rumit karena pelanggan harus menunggu event balasan tanpa tahu kapan datangnya, dan alur pembayaran sulit dilacak.
  - **Kombinasi SOA + Pub-Sub.**
- Pembagian tugas:
  - Gusti → pemilihan dan analisis arsitektur (bagian 1).
  - Andika → daftar komponen dan diagram arsitektur (bagian 2–3).
  - Dyandra → skenario end-to-end dan tabel jenis komunikasi (bagian 4).
  - Fathan → analisis *coupling*, trade-off, dan kesimpulan (bagian 5–6).
- Perbedaan pendapat: **[isi, atau tulis "tidak ada"]**

## Kenapa akhirnya pilih kombinasi SOA + Pub-Sub
- Prinsip yang disepakati: **sinkron hanya untuk langkah yang memang butuh jawaban langsung, sisanya asinkron.**
- Pesanan, Pembayaran, dan Katalog Resto memakai SOA (request-response) karena pelanggan perlu tahu saat itu juga apakah menu tersedia dan pembayaran berhasil.
- Kejadian setelah pesanan dibayar (notifikasi ke resto, penugasan kurir, notifikasi ke pelanggan) memakai event lewat message broker, sehingga pelanggan sudah mendapat konfirmasi tanpa menunggu kurir ditemukan.
- Dengan pembagian ini, tim kurir dan tim resto bisa deploy kapan saja: event tetap menunggu di broker selama service mereka mati.

## [isi tanggal diskusi 2] — Penyusunan diagram dan skenario
- Peserta: **[isi]**
- Media: **[isi]**
- Poin diskusi:
  - Menetapkan komponen: API Gateway, Service Katalog Resto, Service Pesanan, Service Pembayaran, Service Kurir/Notifikasi, dan Message Broker. Disepakati setiap service punya database sendiri agar perubahan skema atau gangguan satu database tidak merusak service lain.
  - Menetapkan tiga event utama: `PesananDibayar`, `PesananSiap`, dan `KurirDitugaskan`, beserta publisher dan subscriber masing-masing.
  - Menyepakati notasi panah di diagram: garis tegas = request sinkron, putus-putus = balasan atau event asinkron, agar jenis komunikasi terlihat langsung di diagram.
  - Menyusun skenario end-to-end (buat pesanan → bayar → resto menerima notifikasi → kurir ditugaskan) dalam bentuk sequence diagram dan tabel per langkah.

## Revisi Diagram (versi 1 → versi 2)
> **[isi sesuai perubahan yang benar-benar terjadi.]** Riwayat commit hanya menunjukkan diagram ditambahkan sekaligus pada 2026-10-31, jadi detail revisi perlu diisi dari ingatan kelompok. Contoh format:

| Versi | Perubahan | Alasan |
|---|---|---|
| v1 → v2 | **[isi]** | **[isi]** |

## [isi tanggal diskusi 3] — Analisis dan review silang
- Peserta: **[isi]**
- Media: **[isi]**
- Poin diskusi:
  - Mengecek bahwa solusi Tugas 1 punya tempat di arsitektur: timeout dan circuit breaker di API Gateway dan panggilan Pesanan → Pembayaran; retry dengan backoff dan *idempotency key* di Service Pembayaran.
  - Mengakui bahwa arsitektur baru membawa masalah baru: message broker dan API Gateway bisa menjadi *single point of failure* baru, event bisa terkirim dua kali (*at-least-once*), dan data menjadi *eventually consistent*. Masing-masing diberi cara mengurangi di tabel trade-off.
  - Menyepakati pemisahan dilakukan bertahap, dimulai dari modul yang paling sering bermasalah (Pembayaran dan Kurir), sejalan dengan kesimpulan Tugas 1.

## Review Silang
> **[isi isi masukan yang benar-benar diberikan.]** Pasangan reviewer mengikuti pola Tugas 1:

- **Andika mengomentari bagian Gusti (pemilihan arsitektur):** **[isi]**
- **Dyandra mengomentari bagian Andika (komponen dan diagram):** **[isi]**
- **Fathan mengomentari bagian Dyandra (skenario end-to-end):** **[isi]**
- **Gusti mengomentari bagian Fathan (analisis dan trade-off):** **[isi]**

## Log Penggunaan AI

> Dosen telah memberi izin kepada kelompok untuk tidak mengikuti batasan Level 2 pada tugas ini. **[isi tanggal/bentuk izin dosen]**

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2026-11-01 | Claude | Meminta dikerjakan jurnal Tugas 2 berdasarkan isi README Tugas 2 dan format jurnal Tugas 1 | Menyusun draf jurnal: opsi arsitektur, alasan pemilihan, poin diskusi, dan kerangka revisi diagram serta review silang | **[isi: bagian mana yang diperiksa, dilengkapi, atau diubah kelompok]** |
| **[isi jika ada pemakaian AI lain]** | | | | |
