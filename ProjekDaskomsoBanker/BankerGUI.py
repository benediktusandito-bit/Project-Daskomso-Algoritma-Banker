import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from PIL import Image, ImageTk  

from BankerEngine import BankerEngine
from FileHandler import FileHandler

class BankerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ALGORITMA BANKER - Deadlock Avoidance Simulator")
        self.root.geometry("1100x650")
        self.root.configure(bg="#0B131F")  
        
        self.nama_rombongan = []
        self.allocated = {}
        self.max_ = {}

        self.setup_styles()
        self.create_widgets()

    # Fungsi untuk mengatur warna komponen internal bawaan Tkinter (Treeview)
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        
        style.configure("Treeview",
                        background="#16222F",
                        foreground="#FFFFFF",
                        fieldbackground="#16222F",
                        rowheight=30,
                        font=("Segoe UI", 10),
                        borderwidth=0)
        
        style.configure("Treeview.Heading",
                        background="#111C28",
                        foreground="#38BDF8",  
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=1)
        
        style.map("Treeview.Heading", background=[('active', '#1F2F41')])
        style.map("Treeview", background=[('selected', '#1E3A8A')])

    def create_widgets(self):
        # ======================================================================
        # COLUMN 1: PANEL KIRI (Input Manual Kapasitas, Upload CSV, Tombol Aksi)
        # ======================================================================

        left_panel = tk.Frame(self.root, bg="#0B131F", width=320)
        left_panel.pack(side="left", fill="y", padx=20, pady=20)
        left_panel.pack_propagate(False)

        # Bagian Logo & Judul Utama Aplikasi
        header_frame = tk.Frame(left_panel, bg="#0B131F")
        header_frame.pack(fill="x", pady=(0, 15))
        
        logo_path = "logo.png"  
        if os.path.exists(logo_path):
            try:
                img_asli = Image.open(logo_path)
                img_resized = img_asli.resize((50, 50), Image.Resampling.LANCZOS)
                self.img_logo = ImageTk.PhotoImage(img_resized)
                
                lbl_logo = tk.Label(header_frame, image=self.img_logo, bg="#0B131F")
                lbl_logo.pack(side="left", padx=(0, 10))
            except Exception as e:
                print(f"Gagal load logo: {e}")
                
        title_frame = tk.Frame(header_frame, bg="#0B131F")
        title_frame.pack(side="left", fill="x")
        
        tk.Label(title_frame, text="Reservasi Restoran", fg="#FFFFFF", bg="#0B131F", font=("Courier New", 14, "bold"), anchor="w").pack(fill="x")
        tk.Label(title_frame, text="Deadlock Avoidance Simulator", fg="#64748B", bg="#0B131F", font=("Segoe UI", 9), anchor="w").pack(fill="x")

        tk.Frame(left_panel, height=1, bg="#1E293B").pack(fill="x", pady=5)

        # Komponen Box "SUMBER DAYA TERSEDIA"
        # Menyediakan 3 kotak input kosong untuk mendefinisikan total kapasitas fisik meja restoran
        lbl_res_title = tk.Label(left_panel, text="SUMBER DAYA TERSEDIA", fg="#94A3B8", bg="#0B131F", font=("Segoe UI", 9, "bold"), anchor="w")
        lbl_res_title.pack(fill="x", pady=(10, 5))
        
        box_res = tk.Frame(left_panel, bg="#111C28", highlightbackground="#1E293B", highlightthickness=1, bd=0)
        box_res.pack(fill="x", pady=5, ipady=8)

        row1 = tk.Frame(box_res, bg="#111C28")
        row1.pack(fill="x", padx=10, pady=4)
        tk.Label(row1, text="Meja Bundar", fg="#94A3B8", bg="#111C28", font=("Segoe UI", 9)).pack(side="left")
        self.ent_tot_bundar = tk.Entry(row1, width=8, bg="#1E293B", fg="#FFFFFF", bd=0, insertbackground="white", justify="center", font=("Segoe UI", 10, "bold"))
        self.ent_tot_bundar.pack(side="right")

        row2 = tk.Frame(box_res, bg="#111C28")
        row2.pack(fill="x", padx=10, pady=4)
        tk.Label(row2, text="Meja Kotak", fg="#94A3B8", bg="#111C28", font=("Segoe UI", 9)).pack(side="left")
        self.ent_tot_kotak = tk.Entry(row2, width=8, bg="#1E293B", fg="#FFFFFF", bd=0, insertbackground="white", justify="center", font=("Segoe UI", 10, "bold"))
        self.ent_tot_kotak.pack(side="right")

        row3 = tk.Frame(box_res, bg="#111C28")
        row3.pack(fill="x", padx=10, pady=4)
        tk.Label(row3, text="Meja Bayi", fg="#94A3B8", bg="#111C28", font=("Segoe UI", 9)).pack(side="left")
        self.ent_tot_bayi = tk.Entry(row3, width=8, bg="#1E293B", fg="#FFFFFF", bd=0, insertbackground="white", justify="center", font=("Segoe UI", 10, "bold"))
        self.ent_tot_bayi.pack(side="right")

        # Komponen Box "UPLOAD DATA"
        # Membuka dialog windows explorer bagi user untuk memuat file manifest data pelanggan (.csv)
        tk.Label(left_panel, text="UPLOAD DATA", fg="#94A3B8", bg="#0B131F", font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x", pady=(10, 2))
        
        box_upload = tk.Frame(left_panel, bg="#111C28", highlightbackground="#1E293B", highlightthickness=1, bd=0)
        box_upload.pack(fill="x", pady=5, ipady=10)
        
        tk.Label(box_upload, text="Silahkan Masukkan \nFile CSV", fg="#38BDF8", bg="#111C28", font=("Segoe UI", 9, "italic"), justify="left", anchor="w").pack(fill="x", padx=12, pady=(8, 8))
        
        self.btn_upload = tk.Button(box_upload, text="⬆ Pilih File CSV", command=self.upload_csv, bg="#1E293B", fg="#FFFFFF", activebackground="#334155", activeforeground="#FFFFFF", bd=0, cursor="hand2", font=("Segoe UI", 9, "bold"), height=2)
        self.btn_upload.pack(fill="x", padx=12)
        
        self.lbl_file_status = tk.Label(box_upload, text="Belum ada data — upload file CSV", fg="#64748B", bg="#111C28", font=("Segoe UI", 8))
        self.lbl_file_status.pack(fill="x", padx=12, pady=(6, 0))

        # Komponen Tombol Kontrol Aksi (Jalankan & Reset)
        # Tombol biru memicu eksekusi utama proses Banker, tombol bawah untuk membersihkan ulang data
        self.btn_hitung = tk.Button(left_panel, text="▶ JALANKAN ALGORITMA", command=self.proses_banker, bg="#1E3A8A", fg="#93C5FD", activebackground="#2563EB", activeforeground="#FFFFFF", bd=0, cursor="hand2", font=("Segoe UI", 10, "bold"), height=2)
        self.btn_hitung.pack(fill="x", pady=(20, 5))
        
        self.btn_reset = tk.Button(left_panel, text="⟳ Reset", command=self.reset_aplikasi, bg="#0B131F", fg="#64748B", activebackground="#1E293B", activeforeground="#94A3B8", bd=1, relief="solid", cursor="hand2", font=("Segoe UI", 9))
        self.btn_reset.pack(fill="x", pady=5)


        # ======================================================================
        # COLUMN 2: PANEL KANAN (Tabel Ringkasan Data & Terminal Log Output Besar)
        # ======================================================================
    
        right_panel = tk.Frame(self.root, bg="#0B131F")
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=20)
        
        right_panel.grid_rowconfigure(1, weight=1) 
        right_panel.grid_rowconfigure(3, weight=3) # Mengatur pembesaran proporsi vertikal area Log Output
        right_panel.grid_columnconfigure(0, weight=1)

        # Komponen "TABEL DATA PELANGGAN" 
        tk.Label(right_panel, text="TABEL DATA PELANGGAN", fg="#94A3B8", bg="#0B131F", font=("Segoe UI", 9, "bold"), anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        table_frame = tk.Frame(right_panel, bg="#16222F", highlightbackground="#1E293B", highlightthickness=1)
        table_frame.grid(row=1, column=0, sticky="nsew")

        columns = ("Nama", "Max", "Alloc", "Need")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        headers = {"Nama": "Nama Pelanggan", "Max": "Maximum", "Alloc": "Allocation", "Need": "Need"}
        for col, txt in headers.items():
            self.tree.heading(col, text=txt)
            self.tree.column(col, anchor="center", width=150 if col != "Nama" else 180)
            
        self.tree.pack(fill="both", expand=True)

        self.lbl_placeholder = tk.Label(self.tree, text="Belum ada data — upload file CSV untuk memulai", fg="#64748B", bg="#16222F", font=("Segoe UI", 11, "italic"))
        self.lbl_placeholder.place(relx=0.5, rely=0.5, anchor="center")

        # Komponen "LOG TERMINAL OUTPUT" 
        tk.Label(right_panel, text="OUTPUT", fg="#94A3B8", bg="#0B131F", font=("Segoe UI", 9, "bold"), anchor="w").grid(row=2, column=0, sticky="w", pady=(15, 5))
        
        self.txt_log = tk.Text(right_panel, bg="#111C28", fg="#10B981", insertbackground="white", bd=0, font=("Consolas", 12), padx=10, pady=10, highlightbackground="#1E293B", highlightthickness=1)
        self.txt_log.grid(row=3, column=0, sticky="nsew")

    # ======================================================================
    # FUNGSI INTERAKSI LOGIKA INTERFACE (CONTROLLER)
    # ======================================================================
    
    # Fungsi perantara untuk mengunggah CSV, mendistribusikan data ke state, dan me-refresh tabel
    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            nama, alloc, mx = FileHandler.load_csv_data(file_path)
            self.nama_rombongan = nama
            self.allocated = alloc
            self.max_ = mx

            self.lbl_file_status.config(text=f"✓ Berhasil memuat {len(nama)} rombongan.", fg="#10B981")
            self.lbl_placeholder.place_forget()
            self.refresh_table()

        except Exception as e:
            messagebox.showerror("Error File CSV", str(e))

    # Fungsi untuk memperbarui tampilan baris tabel Treeview ke format matriks ringkas [B, K, By]
    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        need_matrix = BankerEngine.calc_need(self.allocated, self.max_)

        for pid in self.nama_rombongan:
            self.tree.insert("", "end", values=(
                pid, 
                f"[{self.max_[pid][0]}, {self.max_[pid][1]}, {self.max_[pid][2]}]", 
                f"[{self.allocated[pid][0]}, {self.allocated[pid][1]}, {self.allocated[pid][2]}]", 
                f"[{need_matrix[pid][0]}, {need_matrix[pid][1]}, {need_matrix[pid][2]}]"
            ))

    # Fungsi penarik data input GUI, memvalidasi ambang batas logika, lalu menembakkan perhitungan ke core engine
    def proses_banker(self):
        if not self.nama_rombongan:
            messagebox.showwarning("Peringatan", "Silakan upload file CSV data rombongan terlebih dahulu!")
            return

        try:
            tot_b = int(self.ent_tot_bundar.get())
            tot_k = int(self.ent_tot_kotak.get())
            tot_by = int(self.ent_tot_bayi.get())
            total_restoran = [tot_b, tot_k, tot_by]
        except ValueError:
            messagebox.showerror("Kapasitas Error", "Input kapasitas meja harus berupa angka bulat positif!")
            return

        sum_alloc = [0, 0, 0]
        for pid in self.nama_rombongan:
            if any(self.max_[pid][i] > total_restoran[i] for i in range(3)):
                messagebox.showerror("Validasi Gagal", f"Target maksimum {pid} melebihi total kapasitas fisik restoran!")
                return
            for i in range(3):
                sum_alloc[i] += self.allocated[pid][i]

        meja_kosong = [total_restoran[i] - sum_alloc[i] for i in range(3)]

        if any(kursi < 0 for kursi in meja_kosong):
            messagebox.showerror("Overallocated", f"Alokasi meja aktif saat ini melebihi kapasitas restoran fisik!\nSisa: {meja_kosong}")
            return

        is_safe, sequence, log_jalannya_simulasi = BankerEngine.check_safe_state(
            self.allocated, self.max_, meja_kosong, self.nama_rombongan
        )

        self.txt_log.delete("1.0", tk.END)
        self.txt_log.insert(tk.END, f"[AVAILABLE REAL-TIME]: Bundar:{meja_kosong[0]} | Kotak:{meja_kosong[1]} | Bayi:{meja_kosong[2]}\n")
        self.txt_log.insert(tk.END, "=====================================================================\n")
        
        for baris_log in log_jalannya_simulasi:
            self.txt_log.insert(tk.END, baris_log + "\n")
            
        self.txt_log.insert(tk.END, "============================== HASIL ================================\n")
        if is_safe:
            self.txt_log.insert(tk.END, "STATUS SISTEM: SAFE STATE (Aman Dari Deadlock)\n")
            self.txt_log.insert(tk.END, f"URUTAN AMAN KESELAMATAN: {' ➔ '.join(sequence)}\n")
        else:
            self.txt_log.insert(tk.END, "[!] KEBUNTUAN (DEADLOCK) TERDETEKSI / UNSAFE STATE\n")

    # Fungsi untuk mengosongkan seluruh komponen teks input, menghapus tabel, dan me-reset status log
    def reset_aplikasi(self):
        self.nama_rombongan = []
        self.allocated = {}
        self.max_ = {}
        self.ent_tot_bundar.delete(0, tk.END)
        self.ent_tot_kotak.delete(0, tk.END)
        self.ent_tot_bayi.delete(0, tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.lbl_placeholder.place(relx=0.5, rely=0.5, anchor="center")
        self.lbl_file_status.config(text="Belum ada data — upload file CSV", fg="#64748B")
        self.txt_log.delete("1.0", tk.END)
        self.txt_log.insert(tk.END, "[Sistem Reset] Data dikosongkan. Silakan upload file CSV kembali.")