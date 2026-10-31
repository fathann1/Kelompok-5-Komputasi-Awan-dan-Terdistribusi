import threading
import time

counter = 0
lock = threading.Lock()
jumlah_pesanan = 100
pakai_lock = False

def worker():
    global counter
    if pakai_lock:
        with lock:
            nilai = counter
            time.sleep(0.001)
            counter = nilai + 1
    else:
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

print(f"Pakai lock: {pakai_lock} | Pesanan diproses: {counter} dari {jumlah_pesanan}")