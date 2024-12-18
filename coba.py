import tkinter as tk
from tkinter import messagebox, PhotoImage
from collections import deque  # Untuk menggunakan Queue

# Data soal kuis (list untuk menyimpan soal kuis)
soal_kuis = []

# Stack untuk menyimpan riwayat perubahan soal
soal_stack = []

# Queue untuk menyimpan antrian soal yang belum ditampilkan
soal_queue = deque()

# Fungsi untuk login
def login():
    username = input_username.get()
    password = input_password.get()
    if username == "admin" and password == "admin123":
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
            soal_queue.append(soal_baru)
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
def mulai_kuis():
    if not soal_kuis:
        messagebox.showerror("Error", "Belum ada soal yang tersedia!")
        return
    main_menu_frame.pack_forget()
    tampilkan_soal(0, 0)

# Fungsi untuk menampilkan soal satu per satu
def tampilkan_soal(indeks, skor):
    if len(soal_queue) == 0:  # Jika tidak ada soal yang tersisa di antrian
        messagebox.showinfo("Kuis Selesai", f"Skor Anda: {skor}")
        main_menu_frame.pack()
        return

    # Mengambil soal dari antrian (queue)
    soal_data = soal_queue.popleft()
    soal_text.set(f"Soal {indeks + 1}: {soal_data['soal']}")
    
    # Menampilkan opsi untuk soal
    opsi_1_button.config(text=soal_data['opsi'][0], command=lambda: cek_jawaban(indeks, skor, 0))
    opsi_2_button.config(text=soal_data['opsi'][1], command=lambda: cek_jawaban(indeks, skor, 1))
    opsi_3_button.config(text=soal_data['opsi'][2], command=lambda: cek_jawaban(indeks, skor, 2))

    opsi_1_button.pack(pady=10)
    opsi_2_button.pack(pady=10)
    opsi_3_button.pack(pady=10)  # Menampilkan tombol opsi 3 hanya saat kuis dimulai

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
        try:
            soal_queue.remove(last_soal)  # Hapus soal dari antrian jika ada
        except ValueError:
            pass  # Soal mungkin tidak ada di queue jika belum diproses

        messagebox.showinfo("Undo Sukses", "Soal terakhir telah dihapus!")
    else:
        messagebox.showerror("Undo Gagal", "Tidak ada perubahan yang bisa dibatalkan.")

# Inisialisasi GUI
root = tk.Tk()
root.geometry("600x500")  # Mengatur ukuran window
root.title("Welcome To Quiztopia")  # Judul aplikasi

# Frame Login
login_frame = tk.Frame(root)
login_frame.pack(fill="both", expand=True)

# Tambahkan wallpaper sebagai latar belakang
bg_image = PhotoImage(file="path/to/your/image.png")  # Ganti path gambar
canvas_bg = tk.Canvas(login_frame, width=600, height=500)
canvas_bg.pack(fill="both", expand=True)
canvas_bg.create_image(0, 0, image=bg_image, anchor="nw")

# Widget Login di atas wallpaper
canvas_bg.create_text(300, 50, text="Welcome To Quiztopia", font=("Arial Rounded MT Bold", 20), fill="white")
tk.Label(canvas_bg, text="Username:", font=("Comic Sans MS", 10), bg="white").place(x=200, y=150)
input_username = tk.Entry(canvas_bg, font=("Comic Sans MS", 12))
input_username.place(x=300, y=150)

tk.Label(canvas_bg, text="Password:", font=("Comic Sans MS", 10), bg="white").place(x=200, y=200)
input_password = tk.Entry(canvas_bg, show="*", font=("Comic Sans MS", 12))
input_password.place(x=300, y=200)

tk.Button(canvas_bg, text="Login", command=login, bg="#2980B9", fg="white", font=("Comic Sans MS", 12), width=20).place(x=200, y=250)

# Main Menu
main_menu_frame = tk.Frame(root, bg="#D6EAF8")
# Tombol menu sudah ada di kode awal Anda

# Variabel dan Tombol untuk Kuis
soal_text = tk.StringVar()
tk.Label(root, textvariable=soal_text, font=("Comic Sans MS", 14)).pack(pady=30)
opsi_1_button = tk.Button(root, width=40)
opsi_2_button = tk.Button(root, width=40)
opsi_3_button = tk.Button(root, width=40)

root.mainloop()
