import threading
import time

counter = 0
lock = threading.Lock()
jumlah_pesanan = 100

def worker():
    global counter
    with lock:
        nilai = counter 
        time.sleep(0.001)
        counter = nilai + 1

daftar_thread = []
for i in range(jumlah_pesanan):
    t = threading.Thread(target=worker)
    daftar_thread.append(t)

for t in daftar_thread:
    t.start()

for t in daftar_thread:
    t.join()

print(f"Nilai ujian: {counter}, target: {jumlah_pesanan}")