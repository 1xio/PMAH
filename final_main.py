import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from pymongo import MongoClient
import bcrypt

# ------------------------------
# Configuración de MongoDB
# ------------------------------
client = MongoClient('mongodb://localhost:27017/')
db = client['PMAH']
collection = db['allcredentials']

# ------------------------------
# Funciones para manejo de contraseñas
# ------------------------------
def generate_hash_bcrypt(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(stored_hash, password):
    return bcrypt.checkpw(password.encode(), stored_hash.encode())

def normalize_platform(platform):
    parts = platform.split()
    normalized = ' '.join(part.capitalize() for part in parts)
    return normalized

def store_password(username, platform, password):
    platform = normalize_platform(platform)
    hashed_password = generate_hash_bcrypt(password)
    entry = {'username': username, 'platform': platform, 'hash': hashed_password}
    
    if collection.find_one({'username': username, 'platform': platform}):
        messagebox.showinfo("Información", "Ya se encuentra almacenada esta contraseña.")
        return
    
    collection.insert_one(entry)
    messagebox.showinfo("Éxito", "Contraseña almacenada exitosamente.")

def get_stored_hash(username, platform):
    platform = normalize_platform(platform)
    entry = collection.find_one({'username': username, 'platform': platform})
    if entry:
        return entry['hash']
    return None

def update_password(username, platform, old_password, new_password):
    platform = normalize_platform(platform)
    stored_hash = get_stored_hash(username, platform)
    if stored_hash and verify_password(stored_hash, old_password):
        new_hash = generate_hash_bcrypt(new_password)
        collection.update_one({'username': username, 'platform': platform}, {'$set': {'hash': new_hash}})
        return "Contraseña actualizada correctamente."
    else:
        return "La contraseña antigua es incorrecta o el usuario no existe."

def delete_password(username, platform):
    platform = normalize_platform(platform)
    result = collection.delete_one({'username': username, 'platform': platform})
    if result.deleted_count > 0:
        return f"Contraseña para el usuario '{username}' en la plataforma '{platform}' eliminada correctamente."
    else:
        return f"No se encontró una contraseña para el usuario '{username}' en la plataforma '{platform}'."

def view_passwords():
    table_window = tk.Toplevel()
    table_window.title("Información Almacenada")
    table_window.geometry("1280x720")

    frame = tk.Frame(table_window)
    frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    x_scrollbar = tk.Scrollbar(frame, orient="horizontal")
    x_scrollbar.pack(side="bottom", fill="x")

    tree = ttk.Treeview(frame, columns=("Usuario", "Plataforma", "Hash"), show='headings', xscrollcommand=x_scrollbar.set)
    tree.heading("Usuario", text="Usuario")
    tree.heading("Plataforma", text="Plataforma")
    tree.heading("Hash", text="Hash")

    for entry in collection.find():
        username = entry.get('username', '')
        platform = entry.get('platform', '')
        stored_hash = entry.get('hash', '')
        tree.insert("", tk.END, values=(username, platform, stored_hash))

    tree.pack(expand=True, fill=tk.BOTH, side="left")
    x_scrollbar.config(command=tree.xview)

# ------------------------------
# Interfaz gráfica de usuario (GUI)
# ------------------------------
class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PMAH")
        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.store_btn = ttk.Button(self.frame, text="Almacenar contraseña", command=self.store_password)
        self.store_btn.pack(pady=5)

        self.verify_btn = ttk.Button(self.frame, text="Verificar contraseña", command=self.verify_password)
        self.verify_btn.pack(pady=5)

        self.update_btn = ttk.Button(self.frame, text="Actualizar contraseña", command=self.update_password)
        self.update_btn.pack(pady=5)

        self.delete_btn = ttk.Button(self.frame, text="Eliminar contraseña", command=self.delete_password)
        self.delete_btn.pack(pady=5)

        self.view_btn = ttk.Button(self.frame, text="Información Almacenada", command=view_passwords)
        self.view_btn.pack(pady=5)

        self.quit_btn = ttk.Button(self.frame, text="Cerrar Aplicación", command=self.root.quit, style="Quit.TButton")
        self.quit_btn.pack(pady=20)

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("TButton",
                    font=("Segoe UI", 12),
                    padding=10,
                    relief="flat",
                    background="#0078D7",
                    foreground="white",
                    borderwidth=1)
        style.map("TButton",
              background=[('active', '#005A9E')],
              foreground=[('active', 'white')])

        style.configure("TLabel",
                    font=("Segoe UI", 16),
                    foreground="#333333")

        style.configure("Treeview",
                    background="#F2F2F2",
                    foreground="#333333",
                    fieldbackground="#FFFFFF")

        style.configure("Treeview.Heading",
                    font=("Segoe UI", 14, "bold"),
                    background="#E1E1E1",
                    foreground="#333333")

        style.configure("Horizontal.TScrollbar",
                    gripcount=0,
                    background="#C0C0C0",
                    troughcolor="#E1E1E1",
                    arrowcolor="#333333",
                    borderwidth=1,
                    relief="flat")

        style.configure("Vertical.TScrollbar",
                    gripcount=0,
                    background="#C0C0C0",
                    troughcolor="#E1E1E1",
                    arrowcolor="#333333",
                    borderwidth=1,
                    relief="flat")

        style.configure("Quit.TButton",
                    font=("Segoe UI", 12),
                    padding=10,
                    relief="flat",
                    background="#FF0000",
                    foreground="white",
                    borderwidth=1)
        style.map("Quit.TButton",
              background=[('active', '#CC0000')],
              foreground=[('active', 'white')])

    def store_password(self):
        username = simpledialog.askstring("Almacenar contraseña", "Ingrese el nombre de usuario:")
        platform = simpledialog.askstring("Almacenar contraseña", "Ingrese la plataforma o aplicación:")
        password = simpledialog.askstring("Almacenar contraseña", "Ingrese la nueva contraseña:", show='*')

        if username and platform and password:
            store_password(username, platform, password)
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser llenados.")

    def verify_password(self):
        username = simpledialog.askstring("Verificar contraseña", "Ingrese el nombre de usuario:")
        platform = simpledialog.askstring("Verificar contraseña", "Ingrese la plataforma o aplicación:")
        password = simpledialog.askstring("Verificar contraseña", "Ingrese la contraseña para verificar:", show='*')

        if username and platform and password:
            stored_hash = get_stored_hash(username, platform)
            if stored_hash and verify_password(stored_hash, password):
                messagebox.showinfo("Éxito", "La contraseña es correcta.")
            else:
                messagebox.showerror("Error", "La contraseña es incorrecta o no existe.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser llenados.")

    def update_password(self):
        username = simpledialog.askstring("Actualizar contraseña", "Ingrese el nombre de usuario:")
        platform = simpledialog.askstring("Actualizar contraseña", "Ingrese la plataforma o aplicación:")
        old_password = simpledialog.askstring("Actualizar contraseña", "Ingrese la contraseña antigua:", show='*')
        new_password = simpledialog.askstring("Actualizar contraseña", "Ingrese la nueva contraseña:", show='*')

        if username and platform and old_password and new_password:
            result = update_password(username, platform, old_password, new_password)
            messagebox.showinfo("Resultado", result)
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser llenados.")

    def delete_password(self):
        username = simpledialog.askstring("Eliminar contraseña", "Ingrese el nombre de usuario:")
        platform = simpledialog.askstring("Eliminar contraseña", "Ingrese la plataforma o aplicación:")

        if username and platform:
            result = delete_password(username, platform)
            messagebox.showinfo("Resultado", result)
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser llenados.")

# ------------------------------
# Inicialización de la aplicación
# ------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
