# Jurnal Proses — Tugas 2

## [tanggal 31 oktober 2026 diskusi 1] — Pemilihan gaya arsitektur dan pembagian tugas
- Peserta: Gusti Rifan, Gde Andika Ananta Putra, Dyandra Alifyan Nugroho, Muhammad Rajwa Al Fathan Koessaputra.
- Media: **[tatap muka]**
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

## Kenapa akhirnya pilih kombinasi SOA + Pub-Sub
- Prinsip yang disepakati: **sinkron hanya untuk langkah yang memang butuh jawaban langsung, sisanya asinkron.**
- Pesanan, Pembayaran, dan Katalog Resto memakai SOA (request-response) karena pelanggan perlu tahu saat itu juga apakah menu tersedia dan pembayaran berhasil.
- Kejadian setelah pesanan dibayar (notifikasi ke resto, penugasan kurir, notifikasi ke pelanggan) memakai event lewat message broker, sehingga pelanggan sudah mendapat konfirmasi tanpa menunggu kurir ditemukan.
- Dengan pembagian ini, tim kurir dan tim resto bisa deploy kapan saja: event tetap menunggu di broker selama service mereka mati.

## [tanggal 31 oktober 2026 diskusi 2] — Penyusunan diagram dan skenario
- Peserta: Gusti Rifan, Gde Andika Ananta Putra, Dyandra Alifyan Nugroho, Muhammad Rajwa Al Fathan Koessaputra.
- Media: **[tatap muka]**
- Poin diskusi:
  - Menetapkan komponen: API Gateway, Service Katalog Resto, Service Pesanan, Service Pembayaran, Service Kurir/Notifikasi, dan Message Broker. Disepakati setiap service punya database sendiri agar perubahan skema atau gangguan satu database tidak merusak service lain.
  - Menetapkan tiga event utama: `PesananDibayar`, `PesananSiap`, dan `KurirDitugaskan`, beserta publisher dan subscriber masing-masing.
  - Menyepakati notasi panah di diagram: garis tegas = request sinkron, putus-putus = balasan atau event asinkron, agar jenis komunikasi terlihat langsung di diagram.
  - Menyusun skenario end-to-end (buat pesanan → bayar → resto menerima notifikasi → kurir ditugaskan) dalam bentuk sequence diagram dan tabel per langkah.

## Revisi Diagram (versi 1 → versi 2
| Versi | Perubahan | Alasan |
|---|---|---|
| v1 → v2 | **[tidak ada** | **[karena sudah lengkap dan bagus]** |

## [tanggal 31 oktober 2026 diskusi 3] — Analisis dan review silang
- Peserta: Gusti Rifan, Gde Andika Ananta Putra, Dyandra Alifyan Nugroho, Muhammad Rajwa Al Fathan Koessaputra.
- Media: **[tatap muka]**
- Poin diskusi:
  - Mengecek bahwa solusi Tugas 1 punya tempat di arsitektur: timeout dan circuit breaker di API Gateway dan panggilan Pesanan → Pembayaran; retry dengan backoff dan *idempotency key* di Service Pembayaran.
  - Mengakui bahwa arsitektur baru membawa masalah baru: message broker dan API Gateway bisa menjadi *single point of failure* baru, event bisa terkirim dua kali (*at-least-once*), dan data menjadi *eventually consistent*. Masing-masing diberi cara mengurangi di tabel trade-off.
  - Menyepakati pemisahan dilakukan bertahap, dimulai dari modul yang paling sering bermasalah (Pembayaran dan Kurir), sejalan dengan kesimpulan Tugas 1.

## Review Silang

* **Gde Andika Ananta Putra mengomentari bagian Gusti Rifan (pemilihan arsitektur):**
  Memberikan masukan agar alasan Pembayaran tetap sinkron dijelaskan lebih tegas, karena di bagian trade-off panggilan sinkron ini disebut sebagai titik lemah. Perlu ditegaskan bahwa pelanggan harus tahu hasil pembayaran saat itu juga, sehingga risiko ini sengaja diterima dan ditangani dengan timeout serta circuit breaker.

* **Dyandra Alifyan Nugroho mengomentari bagian Gde Andika Ananta Putra (komponen dan diagram):**
  Memberikan masukan bahwa Service Katalog Resto punya dua tanggung jawab sekaligus, yaitu menyediakan menu dan meneruskan pesanan ke aplikasi resto, sehingga perlu dijelaskan kenapa tidak dipisah. Diagram komponen juga sebaiknya diberi keterangan bahwa garis putus-putus berarti event asinkron, seperti yang sudah ada di sequence diagram.

* **Muhammad Rajwa Al Fathan Koessaputra mengomentari bagian Dyandra Alifyan Nugroho (skenario end-to-end):**
  Memberikan masukan agar dijelaskan apa yang dilakukan Service Kurir saat menerima `PesananDibayar` (langkah 12) dibanding saat menerima `PesananSiap` (langkah 16), karena keduanya tampak sama-sama memicu pencarian kurir. Skenario juga belum menunjukkan apa yang terjadi jika pembayaran gagal.

* **Gusti Rifan mengomentari bagian Muhammad Rajwa Al Fathan Koessaputra (analisis dan trade-off):**
  Memberikan masukan agar ditambahkan risiko ketika Service Pesanan sudah menyimpan pesanan ke database tetapi crash sebelum sempat mem-publish `PesananDibayar`, sehingga resto dan kurir tidak pernah tahu ada pesanan. Selain itu, tabel kontribusi menyebut "kesimpulan", tetapi README belum punya bagian kesimpulan tersendiri.

## Log Penggunaan AI

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2026-11-01 | Claude | Meminta gambaran poin-poin yang perlu ada di jurnal Tugas 2 berdasarkan README dan format jurnal Tugas 1 | Memberikan kerangka bagian jurnal dan poin diskusi yang relevan (opsi arsitektur, alasan pemilihan, revisi diagram) | Kerangka dipakai sebagai acuan, lalu isi jurnal ditulis ulang dan dilengkapi kelompok sesuai diskusi yang sebenarnya |
