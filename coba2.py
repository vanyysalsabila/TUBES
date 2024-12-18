import tkinter as tk
from tkinter import messagebox
from collections import deque

# Data soal kuis
soal_kuis = [
    {"soal": "Apa ibu kota Indonesia?", "opsi": ["Jakarta", "Surabaya", "Bandung"], "jawaban": 0},
    {"soal": "Berapa hasil 5 + 3?", "opsi": ["6", "8", "10"], "jawaban": 1},
    {"soal": "Siapa penemu lampu pijar?", "opsi": ["Nikola Tesla", "Albert Einstein", "Thomas Edison"], "jawaban": 2},
]

# Stack dan Queue
soal_stack = []
soal_queue = deque(soal_kuis)

# Fungsi login
def login():
    username = input_username.get()
    password = input_password.get()
    if username == "admin" and password == "admin123":
        login_frame.pack_forget()
        main_menu_frame.pack()
    else:
        messagebox.showerror("Error", "Username atau password salah!")

# Fungsi tambah/edit soal
def tambah_edit_soal():
    soal = input_soal.get()
    opsi = [input_opsi1.get(), input_opsi2.get(), input_opsi3.get()]
    jawaban = var_jawaban.get()

    if not soal or not all(opsi) or jawaban == "":
        messagebox.showerror("Error", "Semua field harus diisi!")
        return

    try:
        jawaban = int(jawaban)
        if jawaban not in [0, 1, 2]:
            raise ValueError

        indeks_edit = input_indeks.get()
        if indeks_edit:  # Edit soal
            indeks = int(indeks_edit)
            soal_kuis[indeks] = {"soal": soal, "opsi": opsi, "jawaban": jawaban}
            messagebox.showinfo("Sukses", "Soal berhasil diedit!")
        else:  # Tambah soal
            soal_baru = {"soal": soal, "opsi": opsi, "jawaban": jawaban}
            soal_kuis.append(soal_baru)
            soal_queue.append(soal_baru)
            soal_stack.append(soal_baru)
            messagebox.showinfo("Sukses", "Soal berhasil ditambahkan!")
        bersihkan_form_soal()
    except ValueError:
        messagebox.showerror("Error", "Jawaban harus 0, 1, atau 2!")

# Fungsi hapus soal
def hapus_soal():
    try:
        indeks = int(input_indeks.get())
        soal_stack.append(soal_kuis[indeks])
        soal_kuis.pop(indeks)
        messagebox.showinfo("Sukses", "Soal berhasil dihapus!")
    except:
        messagebox.showerror("Error", "Indeks tidak valid!")

# Fungsi undo soal
def undo_soal():
    if soal_stack:
        soal_kuis.append(soal_stack.pop())
        messagebox.showinfo("Undo", "Perubahan terakhir berhasil dibatalkan.")
    else:
        messagebox.showerror("Error", "Tidak ada yang bisa di-undo.")

# Fungsi bersihkan form soal
def bersihkan_form_soal():
    input_soal.delete(0, tk.END)
    input_opsi1.delete(0, tk.END)
    input_opsi2.delete(0, tk.END)
    input_opsi3.delete(0, tk.END)
    var_jawaban.set("")
    input_indeks.delete(0, tk.END)

# Fungsi mulai kuis
# Fungsi untuk mulai kuis
def mulai_kuis():
    if not soal_kuis:
        messagebox.showerror("Error", "Belum ada soal yang tersedia!")
        return
    
    # Memuat semua soal dari soal_kuis ke dalam queue
    soal_queue.clear()
    for soal in soal_kuis:
        soal_queue.append(soal)
        
    main_menu_frame.pack_forget()
    tampilkan_soal(0, 0)

# Fungsi tampilkan soal
def tampilkan_soal(indeks, skor):
    if not soal_queue:
        messagebox.showinfo("Kuis Selesai", f"Skor Anda: {skor}")
        main_menu_frame.pack()
        return

    soal_data = soal_queue.popleft()
    soal_text.set(f"{indeks+1}. {soal_data['soal']}")
    opsi_1_button.config(text=soal_data['opsi'][0], command=lambda: cek_jawaban(indeks, skor, 0, soal_data))
    opsi_2_button.config(text=soal_data['opsi'][1], command=lambda: cek_jawaban(indeks, skor, 1, soal_data))
    opsi_3_button.config(text=soal_data['opsi'][2], command=lambda: cek_jawaban(indeks, skor, 2, soal_data))

def cek_jawaban(indeks, skor, pilihan, soal_data):
    if pilihan == soal_data["jawaban"]:
        skor += 1
    tampilkan_soal(indeks + 1, skor)

# GUI Setup
root = tk.Tk()
root.title("Quiztopia")
root.geometry("600x500")

# Frame Login
login_frame = tk.Frame(root)
tk.Label(login_frame, text="Login", font=("Arial", 16)).pack(pady=10)
tk.Label(login_frame, text="Username").pack()
input_username = tk.Entry(login_frame)
input_username.pack()
tk.Label(login_frame, text="Password").pack()
input_password = tk.Entry(login_frame, show="*")
input_password.pack()
tk.Button(login_frame, text="Login", command=login).pack(pady=10)
login_frame.pack()

# Frame Menu Utama
main_menu_frame = tk.Frame(root)
tk.Label(main_menu_frame, text="Menu Utama", font=("Arial", 16)).pack(pady=10)
tk.Button(main_menu_frame, text="Mulai Kuis", command=mulai_kuis).pack()
tk.Button(main_menu_frame, text="Edit Soal", command=lambda: [main_menu_frame.pack_forget(), edit_frame.pack()]).pack()
tk.Button(main_menu_frame, text="Keluar", command=root.quit).pack()

# Frame Edit Soal
edit_frame = tk.Frame(root)
tk.Label(edit_frame, text="Tambah/Edit Soal").pack()
input_soal = tk.Entry(edit_frame)
input_soal.pack()
input_opsi1 = tk.Entry(edit_frame)
input_opsi1.pack()
input_opsi2 = tk.Entry(edit_frame)
input_opsi2.pack()
input_opsi3 = tk.Entry(edit_frame)
input_opsi3.pack()
var_jawaban = tk.StringVar()
tk.Entry(edit_frame, textvariable=var_jawaban).pack()
input_indeks = tk.Entry(edit_frame)
input_indeks.pack()
tk.Button(edit_frame, text="Tambah/Edit", command=tambah_edit_soal).pack()
tk.Button(edit_frame, text="Hapus Soal", command=hapus_soal).pack()
tk.Button(edit_frame, text="Undo", command=undo_soal).pack()
tk.Button(edit_frame, text="Kembali", command=lambda: [edit_frame.pack_forget(), main_menu_frame.pack()]).pack()

# Kuis Frame
soal_text = tk.StringVar()
tk.Label(root, textvariable=soal_text, font=("Arial", 14)).pack()
opsi_1_button = tk.Button(root)
opsi_2_button = tk.Button(root)
opsi_3_button = tk.Button(root)
opsi_1_button.pack(pady=5)
opsi_2_button.pack(pady=5)
opsi_3_button.pack(pady=5)

root.mainloop()
