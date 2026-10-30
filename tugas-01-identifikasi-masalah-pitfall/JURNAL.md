# Jurnal Proses — Tugas 1

## [Tanggal diskusi 1] — Pembagian tugas
- Peserta: [nama-nama yang hadir]
- Media: [tatap muka]
- Poin diskusi:
  - Membaca studi kasus FoodGo dan menandai gejala utama: aplikasi lambat dan timeout, server crash dan harus di-restart manual, komentar kode `# network is always reliable, no need for retry`, tidak ada timeout antarservice, serta semua modul berjalan dalam satu proses monolitik.
  - Memilih tiga pitfall yang buktinya paling jelas di skenario: *The Network Is Reliable*, *Latency Is Zero*, dan *Single Point of Failure* (arsitektur monolitik).
  - Pembagian tugas: Gusti → Pitfall 1, Andika → Pitfall 2, Dyandra → Pitfall 3, Fathan → kesimpulan kelompok dan review silang.
- Perbedaan pendapat: [isi jika ada, mis. apakah masalah "tidak ada timeout" masuk Pitfall 1 atau Pitfall 2]

## [Tanggal diskusi 2] — Penyusunan dan review draf

* Peserta: Gde Andika Ananta Putra [+ anggota lain jika ikut]
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
- Dikerjakan oleh: Gusti
- Masalah yang ditemukan: Pitfall 1 dan Pitfall 2 tumpang tindih karena memakai bukti dan solusi yang sama (tidak ada timeout), dan dampak Pitfall 1 masih umum.
- Perubahan:
  - Bukti Pitfall 1 difokuskan ke komentar `no need for retry`; pembahasan timeout dirujuk ke Pitfall 2.
  - Bagian "Kenapa keliru" ditambah contoh penyebab kegagalan jaringan (paket hilang, koneksi putus, crash, *network partition*) dan poin bahwa pengirim tidak dapat mengetahui apakah permintaannya sampai.
  - Dampak diganti dengan skenario respons pembayaran hilang yang menyebabkan pesanan menggantung dan risiko pembayaran ganda.
  - Solusi idempotency dijelaskan cara kerjanya; trade-off ditambah biaya penyimpanan ID transaksi.
- Catatan: [apakah kesimpulan Fathan ikut disesuaikan?]

## Review Silang
-  mengomentari analisis Gusti: [...]
-  mengomentari analisis Andika: [...]
-  mengomentari analisis Dyandra: [...]
- [Anggota lain] mengomentari kesimpulan Fathan: [...]

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| [tanggal lain jika ada pemakaian AI sebelumnya] | ... | ... | ... | ... |
| 2026-10-28 | Claude | Meminta bantuan mengisi JURNAL.md Tugas 1 | Memberi kerangka jurnal | Kerangka dipakai sebagai acuan struktur jurnal |
| 2026-10-31 | Claude | Meminta penjelasan studi kasus FoodGo secara sederhana | Penjelasan dengan analogi warung makan | Dipakai untuk memahami konsep, tidak disalin ke laporan |
| 2026-10-31 | Claude | Meminta review analisis terhadap poin-poin soal | Semua poin terpenuhi; Pitfall 1 dan 2 tumpang tindih; dampak Pitfall 1 kurang konkret | Dijadikan dasar keputusan untuk merevisi Pitfall 1 |
| 2026-10-31 | Claude | Meminta perbaikan Pitfall 1 | Outline revisi, review draf Gusti, lalu versi revisi lengkap (atas izin dosen) | Disesuaikan oleh Gusti dengan bahasa sendiri sebelum dimasukkan ke laporan |
| 2026-10-31 | Claude | Meminta pembuatan jurnal | Mengisi bagian jurnal yang faktanya diketahui; bagian diskusi dibiarkan untuk diisi kelompok | Tanggal, peserta, dan review silang diisi sendiri oleh kelompok |
