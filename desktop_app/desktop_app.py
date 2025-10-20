#!/usr/bin/env python3
"""
DESKTOP APP SIMPLE - Sistema REP
Aplicación de escritorio optimizada para ver datos del servidor
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from datetime import datetime
import threading

class DesktopAppSimple:
    def __init__(self):
        self.server_url = "http://192.168.5.53:5000"
        self.setup_window()
        self.create_interface()
        
    def setup_window(self):
        """Configurar ventana principal"""
        self.root = tk.Tk()
        self.root.title("Sistema REP - Desktop")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E7D32")
        
    def create_interface(self):
        """Crear interfaz simple"""
        # Título
        title = tk.Label(self.root, text="🌱 Sistema REP - Desktop", 
                        font=('Arial', 18, 'bold'), fg="white", bg="#2E7D32")
        title.pack(pady=20)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="white", relief="raised", bd=2)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Botón actualizar
        refresh_btn = tk.Button(main_frame, text="🔄 Actualizar Datos", 
                               command=self.update_data, bg="#4CAF50", fg="white",
                               font=('Arial', 12, 'bold'), pady=10)
        refresh_btn.pack(pady=10)
        
        # Estadísticas
        self.stats_frame = tk.Frame(main_frame, bg="white")
        self.stats_frame.pack(fill="x", pady=10)
        
        # Área de datos
        tk.Label(main_frame, text="📊 Escaneos Recientes:", bg="white",
                font=('Arial', 12, 'bold')).pack(anchor="w", padx=10)
        
        self.data_text = scrolledtext.ScrolledText(main_frame, height=20, 
                                                  font=('Consolas', 10))
        self.data_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="🔌 Listo", 
                                    bg="#1B5E20", fg="white")
        self.status_label.pack(fill="x", side="bottom")
        
        # Actualizar datos inicial
        self.update_data()
        
    def update_data(self):
        """Actualizar datos del servidor"""
        threading.Thread(target=self._fetch_data, daemon=True).start()
        
    def _fetch_data(self):
        """Obtener datos del servidor en hilo separado"""
        try:
            self.root.after(0, lambda: self.status_label.config(text="🔄 Actualizando..."))
            
            # Obtener estadísticas
            stats_response = requests.get(f"{self.server_url}/stats", timeout=5)
            
            if stats_response.status_code == 200:
                stats = stats_response.json()
                self.root.after(0, lambda: self._update_stats(stats))
            
            # Obtener usuarios
            users_response = requests.get(f"{self.server_url}/users", timeout=5)
            
            if users_response.status_code == 200:
                users = users_response.json()
                self.root.after(0, lambda: self._update_users(users))
                
            self.root.after(0, lambda: self.status_label.config(
                text=f"✅ Actualizado: {datetime.now().strftime('%H:%M:%S')}"))
                
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(
                text=f"❌ Error: {str(e)}"))
            
    def _update_stats(self, stats):
        """Actualizar estadísticas en UI"""
        # Limpiar stats frame
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
            
        # Crear boxes de estadísticas
        total_scans = stats.get('total_scans', 0)
        total_users = stats.get('total_users', 0)
        
        # Box 1: Total Scans
        scan_frame = tk.Frame(self.stats_frame, bg="#E3F2FD", relief="raised", bd=2)
        scan_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        tk.Label(scan_frame, text="📱 QRs Escaneados", bg="#E3F2FD",
                font=('Arial', 10, 'bold')).pack(pady=5)
        tk.Label(scan_frame, text=str(total_scans), bg="#E3F2FD",
                font=('Arial', 20, 'bold'), fg="#1976D2").pack()
        
        # Box 2: Total Users
        user_frame = tk.Frame(self.stats_frame, bg="#E8F5E8", relief="raised", bd=2)
        user_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        tk.Label(user_frame, text="👥 Usuarios Activos", bg="#E8F5E8",
                font=('Arial', 10, 'bold')).pack(pady=5)
        tk.Label(user_frame, text=str(total_users), bg="#E8F5E8",
                font=('Arial', 20, 'bold'), fg="#388E3C").pack()
        
    def _update_users(self, users):
        """Actualizar lista de usuarios"""
        self.data_text.delete(1.0, tk.END)
        
        self.data_text.insert(tk.END, f"📊 DATOS DEL SISTEMA REP\n")
        self.data_text.insert(tk.END, f"{'='*50}\n")
        self.data_text.insert(tk.END, f"🕐 Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if users:
            self.data_text.insert(tk.END, f"👥 USUARIOS Y ESCANEOS:\n")
            self.data_text.insert(tk.END, f"{'-'*50}\n")
            
            for i, user in enumerate(users, 1):
                name = user['name']
                scan_count = user['scan_count']
                last_scan = user['last_scan']
                
                self.data_text.insert(tk.END, f"{i:2d}. {name}\n")
                self.data_text.insert(tk.END, f"    📱 Escaneos: {scan_count}\n")
                self.data_text.insert(tk.END, f"    🕐 Último: {last_scan}\n\n")
        else:
            self.data_text.insert(tk.END, "📭 No hay escaneos registrados\n\n")
            
        # Información adicional
        self.data_text.insert(tk.END, f"🌐 SERVIDOR:\n")
        self.data_text.insert(tk.END, f"{'-'*50}\n")
        self.data_text.insert(tk.END, f"📡 URL: {self.server_url}\n")
        self.data_text.insert(tk.END, f"✅ Estado: Conectado\n")
        self.data_text.insert(tk.END, f"📱 Scanner App: Recibe en /scan\n")
        
    def run(self):
        """Ejecutar aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    print("🌱 Iniciando Desktop App...")
    app = DesktopAppSimple()
    app.run()

if __name__ == "__main__":
    main()