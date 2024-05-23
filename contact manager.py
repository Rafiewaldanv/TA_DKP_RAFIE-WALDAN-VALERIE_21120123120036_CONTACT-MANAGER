import tkinter as tk  # Import modul tkinter untuk GUI
from tkinter import messagebox as mb  # Import modul messagebox dari tkinter
from tkinter import ttk  # Import modul ttk dari tkinter untuk widget yang ditingkatkan
from collections import deque  # Import modul deque untuk implementasi antrian

# Membuat kelas Contact yang merepresentasikan kontak
class Contact:
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def __str__(self):
        return f"Name: {self.name}, Address: {self.address}, Phone: {self.phone}"

# Membuat kelas ContactManager untuk mengelola kontak
class ContactManager:
    def __init__(self):
        self.contacts = []  # Variabel untuk menyimpan daftar kontak
        self.stack = []  # Variabel untuk menyimpan kontak yang dihapus (untuk undo)
        self.queue = deque()  # Variabel untuk menyimpan kontak yang dihapus (untuk undo)

        self.window = tk.Tk()  # Membuat jendela aplikasi menggunakan kelas Tk dari modul tkinter
        self.window.title("Contact Manager")  # Mengatur judul jendela
        self.window.configure(bg="brown")  # Mengatur latar belakang jendela

        self.create_form_panel()  # Membuat panel form untuk memasukkan data kontak
        self.create_table_panel()  # Membuat panel tabel untuk menampilkan daftar kontak
        self.create_button_panel()  # Membuat panel tombol untuk melakukan aksi terkait kontak

        self.window.protocol("WM_DELETE_WINDOW", self.exit_program)  # Mengatur tindakan saat jendela ditutup

        while True:
            try:
                self.window.update()  # Memperbarui tampilan jendela
            except tk.TclError:
                break  # Keluar dari perulangan saat jendela ditutup

    def create_form_panel(self):
        # Membuat panel form untuk memasukkan data kontak
        self.form_frame = tk.Frame(self.window)
        self.form_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        name_label = tk.Label(self.form_frame, text="Name:")
        name_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.name_entry = tk.Entry(self.form_frame)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.name_entry.bind('<Return>', lambda event: self.address_entry.focus_set())

        address_label = tk.Label(self.form_frame, text="Address:")
        address_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.address_entry = tk.Entry(self.form_frame)
        self.address_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.address_entry.bind('<Return>', lambda event: self.phone_entry.focus_set())

        phone_label = tk.Label(self.form_frame, text="Phone:")
        phone_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.phone_entry = tk.Entry(self.form_frame)
        self.phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.phone_entry.bind('<Return>', lambda event: self.process_form())

    def create_table_panel(self):
        # Membuat panel tabel untuk menampilkan daftar kontak
        self.table_frame = tk.Frame(self.window)
        self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)

        self.table = ttk.Treeview(self.table_frame, columns=("Name", "Address", "Phone"), show='headings')
        self.table.heading("Name", text="Name")
        self.table.heading("Address", text="Address")
        self.table.heading("Phone", text="Phone")
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.bind("<<TreeviewSelect>>", self.select_contact)

    def create_button_panel(self):
        # Membuat panel tombol untuk melakukan aksi terkait kontak
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        add_button = tk.Button(self.button_frame, text="Add Contact", command=self.add_contact, bg="light blue")
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        edit_button = tk.Button(self.button_frame, text="Edit Contact", command=self.edit_contact, bg="orange")
        edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(self.button_frame, text="Delete Contact", command=self.delete_contact, bg="pink")
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        undo_button = tk.Button(self.button_frame, text="Undo Delete", command=self.undo_delete, bg="light green")
        undo_button.pack(side=tk.LEFT, padx=5, pady=5)

        exit_button = tk.Button(self.button_frame, text="Exit", command=self.exit_program, bg="red")
        exit_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def process_form(self):
        # Memproses form untuk menambah atau mengedit kontak
        while True:
            if self.table.selection():
                self.edit_contact()
            else:
                self.add_contact()

            # Menanyakan apakah ingin menambahkan kontak lagi
            if not mb.askyesno("Add Another Contact", "Apakah ingin menambahkan kontak lagi?"):
                break

    def add_contact(self):
        # Menambahkan kontak baru ke daftar kontak
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()

        if not name:
            mb.showerror("Error", "Anda harus mengisi Nama")
            return
        elif not address:
            mb.showerror("Error", "Anda harus mengisi Alamat")
            return
        elif not phone:
            mb.showerror("Error", "Anda harus mengisi Nomor Telepon")
            return
        elif not phone.isdigit():
            mb.showerror("Error", "Nomor Telepon harus diisi dengan angka")
            return

        contact = Contact(name, address, phone)
        self.contacts.append(contact)
        self.table.insert("", tk.END, values=(contact.name, contact.address, contact.phone))
        self.clear_form()

    def clear_form(self):
        # Menghapus data yang ada di form setelah ditambahkan atau diubah
        self.name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.name_entry.focus_set()

    def delete_contact(self):
        # Menghapus kontak yang dipilih dari daftar kontak
        selected_item = self.table.selection()
        if selected_item:
            index = self.table.index(selected_item)
            contact = self.contacts.pop(index)
            self.table.delete(selected_item)
            self.stack.append(contact)
            self.queue.append(contact)

    def undo_delete(self):
        # Mengembalikan kontak yang terakhir dihapus dari stack ke daftar kontak
        if self.queue:
            contact = self.queue.pop()
            self.contacts.append(contact)
            self.table.insert("", tk.END, values=(contact.name, contact.address, contact.phone))

    def select_contact(self, event):
        # Menampilkan data kontak yang dipilih pada form
        selected_item = self.table.selection()
        if selected_item:
            item = self.table.item(selected_item)
            values = item['values']
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(tk.END, values[0])
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(tk.END, values[1])
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(tk.END, values[2])

    def edit_contact(self):
        # Mengedit kontak yang dipilih dengan data yang diisi pada form
        selected_item = self.table.selection()
        if selected_item:
            index = self.table.index(selected_item)
            contact = self.contacts[index]
            name = self.name_entry.get()
            address = self.address_entry.get()
            phone = self.phone_entry.get()

            if not name:
                mb.showerror("Error", "Anda harus mengisi Nama")
                return
            elif not address:
                mb.showerror("Error", "Anda harus mengisi Alamat")
                return
            elif not phone:
                mb.showerror("Error", "Anda harus mengisi Nomor Telepon")
                return
            elif not phone.isdigit():
                mb.showerror("Error", "Phone harus diisi dengan angka")
                return

            contact.name = name
            contact.address = address
            contact.phone = phone
            self.table.item(selected_item, values=(contact.name, contact.address, contact.phone))
            self.clear_form()

    def exit_program(self):
        # Menutup program setelah konfirmasi dari pengguna
        if mb.askokcancel("Quit", "Apakah kamu benar ingin keluar dari program ini?"):
            self.window.destroy()

contact_manager = ContactManager()
