# Jurnal Proses — Tugas 1

## [Tanggal diskusi 1] — Pembagian tugas
- Peserta: Gusti Rifan, Gde Andika Ananta Putra, Muhammad Rajwa Al Fathan Koessaputra, Dyandra Alifyan Nugroho.
- Media: tatap muka
- Poin diskusi:
  - Membaca studi kasus FoodGo dan menandai gejala utama: aplikasi lambat dan timeout, server crash dan harus di-restart manual, komentar kode `# network is always reliable, no need for retry`, tidak ada timeout antarservice, serta semua modul berjalan dalam satu proses monolitik.
  - Memilih tiga pitfall yang buktinya paling jelas di skenario: *The Network Is Reliable*, *Latency Is Zero*, dan *Single Point of Failure* (arsitektur monolitik).
  - Pembagian tugas: Gusti → Pitfall 1, Andika → Pitfall 2, Dyandra → Pitfall 3, Fathan → kesimpulan kelompok dan review silang.
- Perbedaan pendapat: tidak ada

## [Tanggal diskusi 2] — Penyusunan dan review draf

* Peserta: Gde Andika Ananta Putra, Gusti Rifan, Muhammad Rajwa Al Fathan Koessaputra, Dyandra Alifyan Nugroho.
* Media: tatap muka
* Poin diskusi:
   * Draf ketiga pitfall dan kesimpulan digabungkan ke `Analisis-Pitfall-FoodGo.md`.
   * Pitfall 3 diberi catatan bahwa arsitektur monolitik tidak selalu buruk;
     masalah utamanya adalah ketergantungan pada satu proses tanpa isolasi kegagalan.
   * Solusi pemisahan modul diarahkan bertahap sesuai kebutuhan, bukan langsung
     mengubah semua modul menjadi microservice.
   * Menguji klaim Pitfall 3 rolling deploy menghilangkan downtime saat
     deploy, tetapi tidak mengatasi bug/memory leak satu modul yang tetap
     menjatuhkan semua instance jadwal rilis yang tetap harus
     bersamaan antar-tim, dan scaling yang tidak bisa per modul.

## 2026-10-31 — Revisi Pitfall 1
- Peserta: Gusti Rifan, Gde Andika Ananta Putra, Muhammad Rajwa Al Fathan Koessaputra, Dyandra Alifyan Nugroho.
- Media: tatap muka
- Perubahan:
  - Bukti Pitfall 1 difokuskan ke komentar `no need for retry`; pembahasan timeout dirujuk ke Pitfall 2.
  - Bagian "Kenapa keliru" ditambah contoh penyebab kegagalan jaringan (paket hilang, koneksi putus, crash, *network partition*) dan poin bahwa pengirim tidak dapat mengetahui apakah permintaannya sampai.
  - Dampak diganti dengan skenario respons pembayaran hilang yang menyebabkan pesanan menggantung dan risiko pembayaran ganda.
  - Solusi idempotency dijelaskan cara kerjanya; trade-off ditambah biaya penyimpanan ID transaksi.

## Review Silang
-  mengomentari analisis Gusti: [...]
-  mengomentari analisis Andika: [...]
-  mengomentari analisis Dyandra: [...]
- [Anggota lain] mengomentari kesimpulan Fathan: [...]

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah menjadi tulisan sendiri |
|---|---|---|---|---|
| 2026-10-28 | Claude | Meminta gambaran struktur jurnal untuk Tugas 1 | Memberikan gambaran susunan dan bagian-bagian jurnal yang perlu diperhatikan | Digunakan sebagai acuan awal, kemudian struktur dan isi jurnal disusun sendiri oleh kelompok. |
| 2026-10-31 | Claude | Meminta penjelasan sederhana mengenai studi kasus FoodGo | Menjelaskan konsep dan permasalahan pada studi kasus menggunakan analogi sehari-hari | Penjelasan digunakan untuk memahami materi sebelum melakukan diskusi dan analisis secara mandiri. |
