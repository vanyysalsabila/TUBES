import tkinter as tk
from tkinter import  Label, Button, messagebox
from collections import deque  # Untuk menggunakan Queue



# Data soal kuis (list untuk menyimpan soal kuis)
soal_kuis = [
    {
        "soal": "Apa kepanjangan dari SQL dalam basis data?",
        "opsi": ["Simple Query Language", "Structured Query Language", "Sequential Query Language"],
        "jawaban": 1
    },
    {
        "soal": "Apa fungsi utama dari algoritma Dijkstra?",
        "opsi": ["Mencari lintasan terpendek", "Mengurutkan data", "Menghitung probabilitas"],
        "jawaban": 0
    },
    {
        "soal": "Apa kegunaan dari library NumPy dalam Python?",
        "opsi": ["Manipulasi array dan komputasi numerik", "Visualisasi data", "Manajemen basis data"],
        "jawaban": 0
    },
    {
        "soal": "Manakah yang termasuk struktur data linier?",
        "opsi": ["Tree", "Graph", "Linked List"],
        "jawaban": 2
    }
]

# Stack untuk menyimpan riwayat perubahan soal
soal_stack = [
    {"soal": "Apa kepanjangan dari SQL dalam basis data?", "opsi": ["Simple Query Language", "Structured Query Language", "Sequential Query Language"], "jawaban": 1},
    {"soal": "Apa fungsi utama dari algoritma Dijkstra?","opsi": ["Mencari lintasan terpendek", "Mengurutkan data", "Menghitung probabilitas"], "jawaban": 0},
    {"soal": "Apa kegunaan dari library NumPy dalam Python?", "opsi": ["Manipulasi array dan komputasi numerik", "Visualisasi data", "Manajemen basis data"], "jawaban": 0}
]

# Queue untuk menyimpan antrian soal yang belum ditampilkan
soal_queue = deque()

# Fungsi untuk login
def login():
    username = input_username.get()
    password = input_password.get()
    if username == "kelompok6" and password == "123456":
        # Login berhasil, arahkan ke menu utama
        login_frame.pack_forget()
        main_menu_frame.pack()
    else:
        messagebox.showerror("Login Gagal", "Username atau password salah!")

# Fungsi untuk tambah/edit soal
def tambah_edit_soal():
    soal = input_soal.get()
    opsi = [input_opsi1.get(), input_opsi2.get(), input_opsi3.get()]
    jawaban = var_jawaban.get()
    indeks_edit = input_indeks.get()

    if not soal or not all(opsi) or jawaban == "":
        messagebox.showerror("Error", "Semua field harus diisi!")
        return

    try:
        jawaban = int(jawaban)
        if jawaban < 0 or jawaban > 2:
            raise ValueError

        if indeks_edit:  # Jika indeks edit diisi, berarti kita ingin mengedit soal yang ada
            indeks = int(indeks_edit)
            if indeks < 0 or indeks >= len(soal_kuis):
                raise IndexError
            soal_kuis[indeks] = {"soal": soal, "opsi": opsi, "jawaban": jawaban}
            messagebox.showinfo("Sukses", "Soal berhasil diedit!")
        else:  # Jika tidak ada indeks, berarti menambah soal baru
            soal_baru = {"soal": soal, "opsi": opsi, "jawaban": jawaban}
            soal_kuis.append(soal_baru)
            soal_stack.append(soal_baru)
            messagebox.showinfo("Sukses", "Soal berhasil ditambahkan!")

        bersihkan_form_soal()
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Indeks tidak valid atau jawaban benar harus berupa indeks 0, 1, atau 2!")

# Fungsi untuk menghapus soal
def hapus_soal():
    try:
        indeks = int(input_indeks.get())
        if indeks < 0 or indeks >= len(soal_kuis):
            raise IndexError
        soal_kuis.pop(indeks)
        messagebox.showinfo("Sukses", "Soal berhasil dihapus!")
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Indeks soal tidak valid!")

# Fungsi untuk membersihkan form tambah soal
def bersihkan_form_soal():
    input_soal.delete(0, tk.END)
    input_opsi1.delete(0, tk.END)
    input_opsi2.delete(0, tk.END)
    input_opsi3.delete(0, tk.END)
    var_jawaban.set("")
    input_indeks.delete(0, tk.END)  # Bersihkan indeks setelah operasi selesai

# Fungsi untuk mulai kuis
# Fungsi untuk mulai kuis
def mulai_kuis():
    if not soal_kuis:
        messagebox.showerror("Error", "Belum ada soal yang tersedia!")
        return
    
    # Reset soal_queue dengan semua soal dari soal_kuis
    soal_queue.clear()
    soal_queue.extend(soal_kuis)

    main_menu_frame.pack_forget()
    tampilkan_soal(0, 0)

# Fungsi untuk kembali ke Menu Utama
def kembali_ke_menu_utama():
    # Sembunyikan semua widget yang ada
    for widget in root.winfo_children():
        widget.pack_forget()
    
    # Tampilkan kembali frame menu utama
    main_menu_frame.pack()

# Fungsi untuk menampilkan halaman skor
def tampilkan_halaman_skor(skor):
    # Sembunyikan semua widget terlebih dahulu
    for widget in root.winfo_children():
        widget.pack_forget()
    
    # Buat label untuk menampilkan skor
    skor_label = Label(root, text=f"Skor Anda: {skor}", font=("Arial", 20))
    skor_label.pack(pady=20)
    
    # Tombol untuk kembali ke Menu Utama
    tombol_kembali = Button(root, text="Kembali ke Menu Utama", command=kembali_ke_menu_utama)
    tombol_kembali.pack(pady=10)

# Fungsi untuk menampilkan soal satu per satu
def tampilkan_soal(indeks, skor):
    # Jika tidak ada soal tersisa
    if len(soal_queue) == 0:
        tampilkan_halaman_skor(skor)  # Tampilkan halaman skor terlebih dahulu
        return

    # Ambil soal dari antrian (queue)
    soal_data = soal_queue.popleft()
    soal_text.set(f"Soal {indeks + 1}: {soal_data['soal']}")

    # Konfigurasi tombol opsi dengan jawaban yang tersedia
    opsi_1_button.config(text=soal_data['opsi'][0], command=lambda: cek_jawaban(indeks, skor, 0))
    opsi_2_button.config(text=soal_data['opsi'][1], command=lambda: cek_jawaban(indeks, skor, 1))
    opsi_3_button.config(text=soal_data['opsi'][2], command=lambda: cek_jawaban(indeks, skor, 2))

    # Tampilkan tombol opsi
    opsi_1_button.pack(pady=10)
    opsi_2_button.pack(pady=10)
    opsi_3_button.pack(pady=10)


# Fungsi untuk cek jawaban
def cek_jawaban(indeks, skor, pilihan):
    if pilihan == soal_kuis[indeks]["jawaban"]:
        skor += 1
    tampilkan_soal(indeks + 1, skor)

# Fungsi untuk undo perubahan soal terakhir
def undo_soal():
    if soal_stack:
        last_soal = soal_stack.pop()  # Mengambil soal terakhir dari stack
        soal_kuis.remove(last_soal)  # Menghapus soal tersebut dari soal_kuis
        # Menghapus soal dari queue juga
        try:
            soal_queue.remove(last_soal)  # Hapus soal dari antrian jika ada
        except ValueError:
            pass  # Soal mungkin tidak ada di queue jika belum diproses

        messagebox.showinfo("Undo Sukses", "Soal terakhir telah dihapus!")
    else:
        messagebox.showerror("Undo Gagal", "Tidak ada perubahan yang bisa dibatalkan.")

# Inisialisasi GUI
root = tk.Tk()
root.geometry("600x320")  # Ukuran window
root.configure(bg="#2C2C2C", highlightthickness=0, bd=0)# Background abu-abu tua

# Frame Login
login_frame = tk.Frame(root, bg="#2C2C2C")  # Warna latar belakang 
tk.Label(login_frame, text="Welcome To Quiztopia", font=("Arial Rounded MT Bold", 16), fg="#87CEEB", bg="#2C2C2C").pack(pady=10)
tk.Label(login_frame, text="Login here", font=("Comic Sans MS", 12), fg="white", bg="#2C2C2C").pack(pady=5)
tk.Label(login_frame, text="Username:", font=("Comic Sans MS", 10), fg="#87CEEB", bg="#2C2C2C").pack()
input_username = tk.Entry(login_frame, font=("Comic Sans MS", 12))
input_username.pack()
tk.Label(login_frame, text="Password:", font=("Comic Sans MS", 10), fg="#87CEEB", bg="#2C2C2C").pack()
input_password = tk.Entry(login_frame, show="*", font=("Comic Sans MS", 12))
input_password.pack()
tk.Button(login_frame, text="Login", command=login, bg="#2980B9", fg="white", font=("Comic Sans MS", 12), width=20).pack(pady=10)
login_frame.pack(padx=20, pady=20)

# Frame Menu Utama
main_menu_frame = tk.Frame(root, bg="#2C2C2C")  # Hilangkan highlight  
tk.Label(main_menu_frame, text="Menu Utama", font=("Arial Rounded MT Bold", 16), fg="#2980b9", bg="#2C2C2C").pack(pady=10)
tk.Button(main_menu_frame, text="Mulai Kuis", command=mulai_kuis, bg="#2980b9", fg="white", font=("Comic Sans MS", 12), width=20).pack(pady=5)  
tk.Button(main_menu_frame, text="Edit Soal", command=lambda: [main_menu_frame.pack_forget(), tambah_soal_frame.pack()], bg="#2980b9", fg="white", font=("Comic Sans MS", 12), width=20).pack(pady=5)  
tk.Button(main_menu_frame, text="Keluar", command=root.quit, bg="#d90429", fg="white", font=("Comic Sans MS", 12), width=20).pack(pady=5)  

main_menu_frame.pack(pady=(0, 50)) 
main_menu_frame.pack_forget()

# Frame Tambah/Edit Soal dengan Scrollbar
tambah_soal_frame = tk.Frame(root, bg="#2C2C2C", bd=0, relief='flat')  # Frame utama
tambah_soal_frame.pack_forget()

# Canvas dan Scrollbar untuk Scrollable Frame
canvas = tk.Canvas(tambah_soal_frame, bg="#2C2C2C")
scrollbar = tk.Scrollbar(tambah_soal_frame, orient="vertical", command=canvas.yview) 
scrollable_frame = tk.Frame(canvas, bg="#2C2C2C", bd=0, relief='flat')

# Binding scroll ke area frame
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Menambahkan scrollable frame ke dalam canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Layout Canvas dan Scrollbar di Frame Tambah/Edit Soal
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Widget Tambah/Edit Soal di dalam Scrollable Frame
tk.Label(scrollable_frame, text="Silahkan Edit Soal", font=("Comic Sans MS", 16), fg="#2980b9", bg="#d6eaf8").pack(pady=10)
tk.Label(scrollable_frame, text="Masukkan Soal:", font=("Comic Sans MS", 12), fg="#2980b9", bg="#d6eaf8").pack()
input_soal = tk.Entry(scrollable_frame, font=("Comic Sans MS", 12))
input_soal.pack(pady=5)
tk.Label(scrollable_frame, text="Opsi 1:", font=("Comic Sans MS", 12), fg="#2980b9", bg="#d6eaf8").pack()
input_opsi1 = tk.Entry(scrollable_frame, font=("Comic Sans MS", 12))
input_opsi1.pack(pady=5)
tk.Label(scrollable_frame, text="Opsi 2:", font=("Comic Sans MS", 12), fg="#2980b9", bg="#d6eaf8").pack()
input_opsi2 = tk.Entry(scrollable_frame, font=("Comic Sans MS", 12))
input_opsi2.pack(pady=5)
tk.Label(scrollable_frame, text="Opsi 3:", font=("Comic Sans MS", 12), fg="#2980b9", bg="#d6eaf8").pack()
input_opsi3 = tk.Entry(scrollable_frame, font=("Comic Sans MS", 12))
input_opsi3.pack(pady=5)
tk.Label(scrollable_frame, text="Jawaban Benar (0/1/2):", font=("Comic Sans MS", 12), fg="#2980b9", bg="#d6eaf8").pack()
var_jawaban = tk.StringVar()
tk.Entry(scrollable_frame, textvariable=var_jawaban, font=("Comic Sans MS", 12)).pack(pady=5)

# Indeks untuk edit soal
tk.Label(scrollable_frame, text="Indeks Soal untuk Edit (kosongkan untuk tambah soal baru):", font=("Comic Sans MS", 12), fg="#2980b9", bg="#d6eaf8").pack()
input_indeks = tk.Entry(scrollable_frame, font=("Comic Sans MS", 12))
input_indeks.pack(pady=5)

# Tombol untuk tambah soal, hapus soal, dan undo
tk.Button(scrollable_frame, text="Tambah Soal", command=tambah_edit_soal, bg="#2980b9", fg="white", font=("Comic Sans MS", 12), width=20).pack(pady=5)
tk.Label(scrollable_frame, text="Indeks Soal untuk Dihapus:", font=("Comic Sans MS", 12), fg="#2980B9", bg="#d6eaf8").pack()
input_indeks_hapus = tk.Entry(scrollable_frame, font=("Comic Sans MS", 12))
input_indeks_hapus.pack(pady=5)
tk.Button(scrollable_frame, text="Hapus Soal", command=hapus_soal, bg="#2980B9", fg="white", font=("Comic Sans MS", 12), width=20).pack(pady=5)

# Tombol Undo Soal di halaman tambah soal
undo_button = tk.Button(scrollable_frame, text="Undo Soal", command=undo_soal, bg="#d90429", fg="white", font=("Comic Sans MS", 12), width=20)
undo_button.pack(pady=10)

tk.Button(scrollable_frame, text="Kembali", command=lambda: [tambah_soal_frame.pack_forget(), main_menu_frame.pack()], bg="#2980B9", fg="white", font=("Comic Sans MS", 12), width=20).pack(pady=10)

# Variabel dan Tombol untuk Kuis
soal_text = tk.StringVar()
tk.Label(root, textvariable=soal_text, font=("Comic Sans MS", 14)).pack(pady=30)  # Menambahkan padding vertikal untuk mengatur posisi
opsi_1_button = tk.Button(root, width=40)
opsi_2_button = tk.Button(root, width=40)
opsi_3_button = tk.Button(root, width=40)

# Isi queue dengan soal awal
soal_queue.extend(soal_kuis)

root.mainloop()