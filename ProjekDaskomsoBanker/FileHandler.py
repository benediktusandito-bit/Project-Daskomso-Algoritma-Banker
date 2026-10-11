import pandas as pd

class FileHandler:

    # Fungsi khusus menangani manajemen berkas luar (File Handling)
    # Memanfaatkan dataframe Pandas untuk membaca file eksternal .csv secara efisien
    @staticmethod
    def load_csv_data(filepath):
        try:
            df = pd.read_csv(filepath)  # Membaca file CSV dari jalur penyimpanan pilihan user
            
            # Array validasi untuk memastikan struktur header kolom CSV tidak salah ketik
            required_cols = ['Rombongan', 'Max_Bundar', 'Max_Kotak', 'Max_Bayi', 
                             'Alloc_Bundar', 'Alloc_Kotak', 'Alloc_Bayi']
            # Membandingkan kolom CSV aktual dengan standar template sistem
            if not all(col in df.columns for col in required_cols):
                raise ValueError("Format kolom CSV tidak sesuai standar!")

            # Mengekstrak kolom nama rombongan menjadi sebuah tipe data List Python
            nama_rombongan = df['Rombongan'].astype(str).tolist()
            allocated = {}  # Kamus data penampung alokasi meja saat ini
            max_ = {}       # Kamus data penampung target maksimal meja

            # Iterasi per baris data di dalam dataframe Pandas untuk dikonversi ke struktur Dictionary
            for _, row in df.iterrows():
                pid = str(row['Rombongan'])
                # Mengelompokkan data resource ke array [Bundar, Kotak, Bayi]
                max_[pid] = [int(row['Max_Bundar']), int(row['Max_Kotak']), int(row['Max_Bayi'])]
                allocated[pid] = [int(row['Alloc_Bundar']), int(row['Alloc_Kotak']), int(row['Alloc_Bayi'])]

            return nama_rombongan, allocated, max_
        except Exception as e:
            # Melempar pesan error ke luar jika format file rusak atau gagal baca
            raise Exception(f"Gagal membaca file CSV: {str(e)}")