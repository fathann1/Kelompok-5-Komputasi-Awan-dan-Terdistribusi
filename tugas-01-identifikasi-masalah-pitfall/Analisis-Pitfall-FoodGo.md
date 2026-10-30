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

Menganggap bahwa jaringan selalu dapat diandalkan adalah kesalahan, ini tidak sesuai dengan kondisi sistem terdistribusi yang sebenarnya. Komunikasi antarservice dapat mengalami gangguan, kehilangan respons, atau keterlambatan karenan kegagalan jaringan bisa saja terjadi seperti paket data hilang, koneksi terputus, dll. Permintaan yang dikirim belum tentu mendapatkan respons meskipun service tujuan masih berjalan. Oleh karena itu, sistem perlu memiliki mekanisme untuk menangani kegagalan komunikasi.

**Dampak ke FoodGo:**

Ketika modul pesanan mengirim permintaan ke modul pembayaran, ada kemungkinan pembayaran bisa berhasil diproses, namun responsnya hilang di jaringan. Karena tidak ada mekanisme pengecekan ulang, modul pesanan tidak mengetahui hasil pembayaran tersebut. Akibatnya, pesanan tidak diteruskan ke restoran, padahal saldo pelanggan sudah terpotong. Pelanggan yang mengira pembayarannya gagal lalu menekan tombol bayar lagi maka berisiko tertagih dua kali. Saat promo, kejadian seperti ini dapat terjadi pada ratusan pesanan sekaligus dan menimbulkan banyak komplain, permintaan refund, dan menurunkan kepercayaan pelanggan terhadap FoodGo.

**Solusi desain awal:**

FoodGo dapat menerapkan retry terbatas dengan exponential backoff, yaitu mencoba ulang permintaan dengan jeda yang semakin panjang, misalnya 1, 2, lalu 4 detik, dan berhenti setelah beberapa kali percobaan. Untuk transaksi pembayaran, sistem perlu menggunakan *idempotency key*: setiap pembayaran diberi ID unik, sehingga jika permintaan dengan ID yang sama dikirim ulang, server cukup mengembalikan hasil sebelumnya tanpa memotong saldo lagi. Circuit breaker juga dapat digunakan untuk menghentikan sementara permintaan ke service yang terus mengalami kegagalan, maka pelanggan segera mendapat informasi dan service yang bermasalah tidak semakin terbebani.

**Trade-off:**

Retry dapat membantu mengatasi gangguan sementara, tetapi jika dilakukan terlalu sering, jumlah permintaan justru meningkat ketika server sedang bermasalah. Karena Ini dapat memperparah kegagalan, jumlah retry perlu dibatasi dan jeda antarpercobaan perlu ditingkatkan secara bertahap. Selain itu, penerapan idempotency membuat server harus menyimpan daftar ID transaksi yang sudah diproses, sehingga membutuhkan tambahan penyimpanan dan logika.

---

## Pitfall 2: Latency Is Zero — ditulis oleh Gde Andika Ananta Putra

**Bukti di skenario:**

Skenario menyebutkan bahwa modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu. Ketika jumlah pesanan meningkat, aplikasi menjadi sangat lambat dan beberapa permintaan mengalami timeout.

**Kenapa ini keliru:**

Dalam sistem terdistribusi, komunikasi antarservice membutuhkan waktu. Permintaan harus dikirim melalui jaringan, diproses oleh service tujuan, lalu hasilnya dikirim kembali. Waktu respons dapat meningkat ketika server sibuk atau jaringan mengalami gangguan. Jika sistem menganggap komunikasi berlangsung seketika, desainnya tidak mampu menangani keterlambatan yang terjadi dalam kondisi nyata.

**Dampak ke FoodGo:**

Ketika modul pembayaran merespons dengan lambat, proses pada modul pesanan ikut tertahan. Thread atau koneksi yang digunakan untuk menangani permintaan tersebut tetap terpakai selama menunggu. Saat banyak pelanggan melakukan pemesanan secara bersamaan, semakin banyak resource yang tertahan sehingga permintaan baru sulit diproses. Akibatnya, waktu respons meningkat, permintaan mengalami timeout, dan server berisiko kehabisan resource.

**Solusi desain awal:**

FoodGo perlu menetapkan timeout pada setiap pemanggilan antarservice agar proses tidak menunggu tanpa batas. Batas waktu tersebut harus disesuaikan dengan kebutuhan setiap operasi. Selain itu, FoodGo dapat membatasi jumlah permintaan yang diproses secara bersamaan dan memantau waktu respons setiap service. Jika suatu operasi dapat dilakukan secara asinkron, proses tersebut juga dapat dipisahkan agar tidak perlu menunggu seluruh pekerjaan selesai dalam satu permintaan.

**Trade-off:**

Timeout yang terlalu singkat dapat membuat permintaan dihentikan meskipun service tujuan sebenarnya masih dapat menyelesaikannya. Sebaliknya, timeout yang terlalu lama membuat resource tetap terpakai ketika service mengalami masalah. Oleh sebab itu, batas waktu perlu ditentukan berdasarkan hasil pengukuran waktu respons dan kebutuhan proses bisnis.

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
