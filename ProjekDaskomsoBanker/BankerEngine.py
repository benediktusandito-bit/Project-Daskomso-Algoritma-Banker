class BankerEngine:

    # Fungsi pembantu untuk mengalkulasi sisa target kekurangan (Matriks Need)
    # Rumus Dasar Matematika Banker: Need = Maximum - Allocation
    @staticmethod
    def calc_need(allocated, max_):
        need = {}
        # Looping untuk memproses data kekurangan setiap pelanggan satu per satu
        for pid in allocated:
            # Mengurangi nilai matriks Max dengan Alloc pada indeks resource yang bersesuaian
            need[pid] = [max_[pid][i] - allocated[pid][i] for i in range(len(max_[pid]))]
        return need

    # Fungsi inti algoritma Banker untuk mensimulasikan perputaran antrean keselamatan
    # Bertugas mendeteksi apakah sistem berada dalam kondisi aman (Safe) atau buntu (Deadlock)
    @staticmethod
    def check_safe_state(allocated, max_, available, nama_rombongan):
        """Mengecek urutan keselamatan (Safe Sequence)"""
        # Memanggil fungsi calc_need untuk mendapatkan data kekurangan meja terbaru
        need = BankerEngine.calc_need(allocated, max_)
        safe_sequence = []  # Wadah untuk menyimpan urutan rombongan yang berhasil pulang
        not_processed = 0   # Penanda hitungan (counter) jika antrean mengalami jalan buntu
        
        stok_simulasi = list(available)  # Menyalin data sisa meja kosong agar data asli tidak rusak
        processes = list(nama_rombongan)  # Menyalin daftar nama rombongan ke dalam struktur antrean
        total_processes = len(processes)  # Menyimpan jumlah total rombongan awal
        log_simulasi = []                 # Wadah penampung teks log jalannya simulasi untuk GUI

        # Loop terus berjalan selama masih ada antrean DAN belum terjadi kemacetan total
        while not_processed < total_processes and len(safe_sequence) != total_processes:
            pid = processes.pop(0)  # Mengambil rombongan di urutan paling depan (Konsep Queue)
            bisa_makan = True       # Asumsi awal: rombongan tersebut bisa dipenuhi mejanya
            
            # Melakukan komparasi apakah stok sisa meja saat ini cukup untuk menutupi NEED
            for i in range(len(stok_simulasi)):
                if stok_simulasi[i] < need[pid][i]:
                    bisa_makan = False  # Set False jika ada satu jenis meja saja yang tidak cukup
                    break
                    
            if bisa_makan:
                # Jika meja cukup, rombongan sukses diproses dan siap makan hingga selesai
                log_simulasi.append(f"> {pid} sukses dilayani.")
                log_simulasi.append(f"  Kekurangan (Need) {need[pid]} terpenuhi dari sisa meja {stok_simulasi}.")
                log_simulasi.append(f"  {pid} selesai -> Mengosongkan meja lamanya: +{allocated[pid]}")
                
                # Pelanggan pulang dan mengembalikan semua meja lamanya ke stok restoran fisik
                for i in range(len(stok_simulasi)):
                    stok_simulasi[i] += allocated[pid][i]
                    
                log_simulasi.append(f"  [STOK SEKARANG]: {stok_simulasi}\n")
                safe_sequence.append(pid)  # Memasukkan nama rombongan ke daftar selamat
                not_processed = 0          # Reset penanda buntu karena ada kemajuan proses
            else:
                # Jika meja tidak cukup, rombongan ditolak sementara dan dilempar ke belakang
                not_processed += 1         # Naikkan angka indikator kemacetan
                processes.append(pid)      # Masukkan kembali pelanggan ke ekor antrean
                
        # Status dinyatakan aman jika jumlah rombongan yang selamat sama dengan total proses awal
        is_safe = len(safe_sequence) == total_processes
        return is_safe, safe_sequence, log_simulasi