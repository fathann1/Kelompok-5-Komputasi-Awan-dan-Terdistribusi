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

Tim engineering FoodGo menemukan kode yang memiliki asumsi `# network is always reliable, no need for retry`. Selain itu, tidak terdapat mekanisme timeout pada pemanggilan antarservice.

**Kenapa ini keliru:**

Asumsi bahwa jaringan selalu dapat diandalkan tidak sesuai dengan kondisi sistem terdistribusi yang sebenarnya. Komunikasi antarservice dapat mengalami gangguan, kehilangan respons, atau keterlambatan. Permintaan yang dikirim belum tentu mendapatkan respons meskipun service tujuan masih berjalan. Oleh karena itu, sistem perlu memiliki mekanisme untuk menangani kegagalan komunikasi.

**Dampak ke FoodGo:**

Ketika modul pesanan mengirim permintaan ke modul pembayaran dan komunikasi mengalami gangguan, proses pesanan dapat terhambat. Tanpa mekanisme timeout, pemanggilan dapat terus menunggu dan menggunakan resource server. Jika banyak permintaan mengalami kondisi yang sama saat promo berlangsung, permintaan dapat menumpuk dan memperburuk kinerja aplikasi.

**Solusi desain awal:**

FoodGo dapat menerapkan timeout pada komunikasi antarservice dan retry terbatas dengan exponential backoff. Circuit breaker juga dapat digunakan untuk menghentikan sementara permintaan ke service yang terus mengalami kegagalan. Untuk transaksi pembayaran, sistem perlu menggunakan mekanisme idempotency agar pengulangan permintaan tidak menyebabkan pembayaran diproses lebih dari sekali.

**Trade-off:**

Retry dapat membantu mengatasi gangguan sementara, tetapi jika dilakukan terlalu sering, jumlah permintaan justru meningkat ketika server sedang bermasalah. Hal ini dapat memperparah kegagalan berantai atau cascading failure. Karena itu, jumlah retry perlu dibatasi dan jeda antarpercobaan perlu ditingkatkan secara bertahap.

---


## Pitfall 3: Single Point of Failure pada Arsitektur Monolitik — ditulis oleh Dyandra Alifyan Nugroho

**Bukti di skenario:**

Skenario menjelaskan bahwa satu server menangani seluruh modul, yaitu pesanan, pembayaran, dan notifikasi kurir. Semua modul berjalan dalam satu proses monolitik yang kewalahan ketika trafik meningkat. Server juga terkadang mengalami crash total dan harus di-restart secara manual.

**Kenapa ini keliru:**

Ketergantungan seluruh fungsi aplikasi pada satu proses dan satu server dapat menjadi titik kegagalan tunggal atau single point of failure. Ketika proses tersebut mengalami crash, seluruh modul yang berada di dalamnya dapat ikut berhenti. Arsitektur yang menjalankan semua modul dalam satu proses juga membatasi kemampuan untuk meningkatkan kapasitas hanya pada komponen yang sedang membutuhkan resource lebih besar.

Namun, arsitektur monolitik tidak selalu buruk. Masalah utama FoodGo adalah ketergantungan pada satu proses atau instance tanpa isolasi kegagalan dan kapasitas yang memadai.

**Dampak ke FoodGo:**

Ketika trafik pemesanan meningkat, penggunaan CPU dan memori pada server dapat bertambah karena seluruh modul menggunakan resource yang sama. Beban pada proses pesanan dapat memengaruhi pembayaran dan notifikasi kurir. Jika proses mengalami crash, ketiga fungsi tersebut dapat berhenti sekaligus. Pemulihan yang masih mengandalkan restart manual juga memperpanjang waktu gangguan dan menghambat pelayanan pelanggan.

**Solusi desain awal:**

FoodGo dapat memulai dengan memperbaiki pengelolaan resource, menambahkan pemantauan, dan menerapkan restart otomatis ketika proses mengalami kegagalan. Untuk meningkatkan ketersediaan, aplikasi dapat dijalankan pada beberapa instance dengan load balancer jika infrastruktur memungkinkan. Dalam jangka panjang, modul yang memiliki kebutuhan kapasitas atau tingkat kegagalan berbeda, seperti pembayaran dan notifikasi, dapat dipisahkan secara bertahap menjadi service tersendiri.

Pemisahan modul sebaiknya dilakukan berdasarkan kebutuhan, bukan sekadar mengubah semua modul menjadi microservice. Database, komunikasi antarservice, dan mekanisme pemulihan juga harus dirancang dengan baik.

**Trade-off:**

Menjalankan beberapa instance membutuhkan resource dan biaya tambahan. Pemisahan modul menjadi service juga meningkatkan kompleksitas deployment, pemantauan, komunikasi jaringan, dan pengelolaan konsistensi data. Karena itu, FoodGo perlu memprioritaskan komponen yang paling bermasalah terlebih dahulu sebelum memperluas arsitektur.

---

## Kesimpulan Kelompok — ditulis oleh Muhammad Rajwa Al Fathan Koessaputra

Berdasarkan studi kasus FoodGo, terdapat tiga masalah utama, yaitu asumsi bahwa jaringan selalu dapat diandalkan, anggapan bahwa komunikasi antarservice tidak memiliki keterlambatan, serta ketergantungan pada satu proses monolitik sebagai titik kegagalan tunggal.

Ketiga masalah tersebut saling berkaitan. Gangguan komunikasi dapat membuat permintaan tertahan, sedangkan keterlambatan yang tidak ditangani dapat menghabiskan resource server. Ketika seluruh modul bergantung pada satu proses, beban yang meningkat atau crash dapat mengganggu semua fungsi aplikasi sekaligus.

Sebagai langkah awal, FoodGo perlu menerapkan timeout, retry terbatas dengan exponential backoff, circuit breaker, serta pemantauan waktu respons dan penggunaan resource. Untuk meningkatkan skalabilitas dan ketersediaan, FoodGo dapat mempertimbangkan beberapa instance aplikasi dan pemisahan modul secara bertahap sesuai kebutuhan.

Solusi tersebut memiliki trade-off berupa tambahan kompleksitas, kebutuhan resource, dan risiko retry berlebihan. Oleh karena itu, penerapan perlu dilakukan secara bertahap dan dievaluasi berdasarkan hasil pengujian.

Hasil analisis ini dapat menjadi dasar Tugas 2 untuk merancang arsitektur sistem terdistribusi FoodGo yang lebih tangguh, terukur, dan mampu menangani peningkatan jumlah pesanan tanpa menyebabkan seluruh sistem berhenti.
