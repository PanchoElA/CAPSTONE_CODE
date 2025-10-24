#!/usr/bin/env python3
"""
DESKTOP APP COMPLETO - Sistema REP
Aplicación de escritorio con estadísticas y generación de QRs
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import requests
from datetime import datetime
import threading
import qrcode
import io
import hashlib
import secrets
from PIL import Image, ImageTk
import os

class DesktopAppCompleto:
    def __init__(self):
        self.server_url = "http://192.168.5.53:5000"
        self.qr_secret_key = "REP_CODELPA_2025_SEGURO"  # Clave para validar QRs auténticos
        self.generated_qrs = []  # Lista de QRs generados
        self.setup_window()
        self.create_interface()
        
    def setup_window(self):
        """Configurar ventana principal"""
        self.root = tk.Tk()
        self.root.title("Sistema REP - Desktop Completo")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2E7D32")
        
    def create_interface(self):
        """Crear interfaz con tabs"""
        # Título
        title = tk.Label(self.root, text="🌱 Sistema REP - Desktop Completo", 
                        font=('Arial', 18, 'bold'), fg="white", bg="#2E7D32")
        title.pack(pady=15)
        
        # Crear notebook para tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Tab 1: Estadísticas
        self.create_stats_tab()
        
        # Tab 2: Generador QR
        self.create_qr_generator_tab()
        
        # Status bar
        self.status_label = tk.Label(self.root, text="🔌 Listo", 
                                    bg="#1B5E20", fg="white", font=('Arial', 10))
        self.status_label.pack(fill="x", side="bottom")
        
        # Actualizar datos inicial
        self.update_data()
        
    def create_stats_tab(self):
        """Crear tab de estadísticas"""
        stats_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(stats_frame, text="📊 Estadísticas")
        
        # Botón actualizar
        refresh_btn = tk.Button(stats_frame, text="🔄 Actualizar Datos", 
                               command=self.update_data, bg="#4CAF50", fg="white",
                               font=('Arial', 12, 'bold'), pady=8)
        refresh_btn.pack(pady=10)
        
        # Estadísticas
        self.stats_frame = tk.Frame(stats_frame, bg="white")
        self.stats_frame.pack(fill="x", pady=10)
        
        # Área de datos
        tk.Label(stats_frame, text="📊 Escaneos y Usuarios:", bg="white",
                font=('Arial', 12, 'bold')).pack(anchor="w", padx=10)
        
        self.data_text = scrolledtext.ScrolledText(stats_frame, height=25, 
                                                  font=('Consolas', 9))
        self.data_text.pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_qr_generator_tab(self):
        """Crear tab generador de QRs"""
        qr_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(qr_frame, text="🔲 Generar QRs")
        
        # Título del tab
        tk.Label(qr_frame, text="🔲 Generador de Códigos QR Seguros", 
                font=('Arial', 14, 'bold'), bg="white", fg="#2E7D32").pack(pady=15)
        
        # Frame principal dividido
        main_qr_frame = tk.Frame(qr_frame, bg="white")
        main_qr_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Panel izquierdo - Controles
        left_panel = tk.Frame(main_qr_frame, bg="white", relief="raised", bd=1)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Tipo de QR
        tk.Label(left_panel, text="📋 Tipo de Código QR:", bg="white",
                font=('Arial', 11, 'bold')).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.qr_type = tk.StringVar(value="TERCEROS")
        type_frame = tk.Frame(left_panel, bg="white")
        type_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Radiobutton(type_frame, text="🏢 Terceros", variable=self.qr_type, 
                      value="TERCEROS", bg="white", font=('Arial', 10)).pack(anchor="w")
        tk.Radiobutton(type_frame, text="🌱 CODELPA", variable=self.qr_type, 
                      value="CODELPA", bg="white", font=('Arial', 10)).pack(anchor="w")
        
        # Identificador/Nombre
        tk.Label(left_panel, text="🏷️ Identificador:", bg="white",
                font=('Arial', 11, 'bold')).pack(anchor="w", padx=10, pady=(15, 5))
        
        self.qr_identifier = tk.Entry(left_panel, font=('Arial', 11), width=30)
        self.qr_identifier.pack(padx=10, pady=5)
        
        # Botones
        button_frame = tk.Frame(left_panel, bg="white")
        button_frame.pack(fill="x", padx=10, pady=20)
        
        generate_btn = tk.Button(button_frame, text="🔲 Generar QR", 
                               command=self.generate_qr, bg="#2196F3", fg="white",
                               font=('Arial', 11, 'bold'), pady=8)
        generate_btn.pack(fill="x", pady=5)
        
        save_btn = tk.Button(button_frame, text="💾 Descargar QR", 
                           command=self.save_qr, bg="#4CAF50", fg="white",
                           font=('Arial', 11, 'bold'), pady=8)
        save_btn.pack(fill="x", pady=5)
        
        clear_btn = tk.Button(button_frame, text="🗑️ Limpiar", 
                            command=self.clear_qr, bg="#FF9800", fg="white",
                            font=('Arial', 11, 'bold'), pady=8)
        clear_btn.pack(fill="x", pady=5)
        
        # Lista de QRs generados
        tk.Label(left_panel, text="📋 QRs Generados:", bg="white",
                font=('Arial', 11, 'bold')).pack(anchor="w", padx=10, pady=(20, 5))
        
        self.qr_list = tk.Listbox(left_panel, height=8, font=('Consolas', 9))
        self.qr_list.pack(fill="x", padx=10, pady=5)
        
        # Panel derecho - Vista previa QR
        right_panel = tk.Frame(main_qr_frame, bg="white", relief="raised", bd=1)
        right_panel.pack(side="right", fill="both", padx=(10, 0))
        
        tk.Label(right_panel, text="👁️ Vista Previa del QR", bg="white",
                font=('Arial', 12, 'bold')).pack(pady=15)
        
        # Area para mostrar QR
        self.qr_display_frame = tk.Frame(right_panel, bg="white", width=300, height=300)
        self.qr_display_frame.pack(pady=20, padx=20)
        self.qr_display_frame.pack_propagate(False)
        
        self.qr_image_label = tk.Label(self.qr_display_frame, text="🔲\n\nGenera un QR\npara visualizarlo aquí",
                                      bg="white", fg="gray", font=('Arial', 12))
        self.qr_image_label.pack(expand=True)
        
        # Info del QR actual
        self.qr_info_text = scrolledtext.ScrolledText(right_panel, height=6, 
                                                     font=('Consolas', 9), wrap="word")
        self.qr_info_text.pack(fill="x", padx=20, pady=20)
        
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
            error_msg = str(e)
            self.root.after(0, lambda: self.status_label.config(
                text=f"❌ Error: {error_msg}"))
            
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
        self.data_text.insert(tk.END, f"📱 Scanner App: Solo acepta QRs autorizados\n")
        
    def generate_secure_qr_code(self, qr_type, identifier):
        """Generar código QR seguro con firma digital"""
        # Crear timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Crear ID único
        unique_id = secrets.token_hex(8)
        
        # Crear contenido del QR
        qr_content = f"{qr_type}_{identifier}_{timestamp}_{unique_id}"
        
        # Crear firma de seguridad
        security_hash = hashlib.sha256(
            f"{qr_content}_{self.qr_secret_key}".encode()
        ).hexdigest()[:16]
        
        # QR final con firma
        final_qr_code = f"REP_{qr_content}_{security_hash}"
        
        return {
            'code': final_qr_code,
            'type': qr_type,
            'identifier': identifier,
            'timestamp': timestamp,
            'unique_id': unique_id,
            'security_hash': security_hash,
            'display_name': f"{qr_type} - {identifier}"
        }
        
    def generate_qr(self):
        """Generar nuevo QR"""
        qr_type = self.qr_type.get()
        identifier = self.qr_identifier.get().strip()
        
        if not identifier:
            messagebox.showwarning("Advertencia", "Por favor ingresa un identificador")
            return
            
        try:
            # Generar QR seguro
            qr_data = self.generate_secure_qr_code(qr_type, identifier)
            
            # Crear imagen QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data['code'])
            qr.make(fit=True)
            
            # Crear imagen
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_data['image'] = qr_image
            
            # Agregar a lista
            self.generated_qrs.append(qr_data)
            
            # Actualizar UI
            self.display_qr(qr_data)
            self.update_qr_list()
            
            self.status_label.config(text=f"✅ QR generado: {qr_data['display_name']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar QR: {str(e)}")
            
    def display_qr(self, qr_data):
        """Mostrar QR en la interfaz"""
        try:
            # Redimensionar imagen para mostrar
            qr_image = qr_data['image']
            qr_image = qr_image.resize((250, 250), Image.Resampling.LANCZOS)
            
            # Convertir para Tkinter
            photo = ImageTk.PhotoImage(qr_image)
            
            # Mostrar imagen
            self.qr_image_label.configure(image=photo, text="")
            self.qr_image_label.image = photo  # Mantener referencia
            
            # Mostrar info
            self.qr_info_text.delete(1.0, tk.END)
            self.qr_info_text.insert(tk.END, f"🔲 CÓDIGO QR GENERADO\n")
            self.qr_info_text.insert(tk.END, f"{'='*40}\n")
            self.qr_info_text.insert(tk.END, f"📋 Tipo: {qr_data['type']}\n")
            self.qr_info_text.insert(tk.END, f"🏷️ ID: {qr_data['identifier']}\n")
            self.qr_info_text.insert(tk.END, f"🕐 Fecha: {qr_data['timestamp']}\n")
            self.qr_info_text.insert(tk.END, f"🔐 Hash: {qr_data['security_hash']}\n\n")
            self.qr_info_text.insert(tk.END, f"📱 CÓDIGO COMPLETO:\n")
            self.qr_info_text.insert(tk.END, f"{'-'*40}\n")
            self.qr_info_text.insert(tk.END, f"{qr_data['code']}\n\n")
            self.qr_info_text.insert(tk.END, f"✅ Este QR es válido para Scanner App")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar QR: {str(e)}")
            
    def update_qr_list(self):
        """Actualizar lista de QRs generados"""
        self.qr_list.delete(0, tk.END)
        for i, qr in enumerate(self.generated_qrs, 1):
            display_text = f"{i:2d}. {qr['display_name']} ({qr['timestamp']})"
            self.qr_list.insert(tk.END, display_text)
            
    def save_qr(self):
        """Guardar QR actual"""
        if not self.generated_qrs:
            messagebox.showwarning("Advertencia", "No hay QRs generados para guardar")
            return
            
        try:
            # Último QR generado
            current_qr = self.generated_qrs[-1]
            
            # Diálogo para guardar
            filename = f"QR_{current_qr['type']}_{current_qr['identifier']}_{current_qr['timestamp']}.png"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialname=filename
            )
            
            if file_path:
                # Guardar imagen en alta resolución
                qr_image = current_qr['image']
                qr_image = qr_image.resize((500, 500), Image.Resampling.LANCZOS)
                qr_image.save(file_path)
                
                messagebox.showinfo("Éxito", f"QR guardado en:\n{file_path}")
                self.status_label.config(text=f"💾 QR guardado: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar QR: {str(e)}")
            
    def clear_qr(self):
        """Limpiar QR actual"""
        self.qr_identifier.delete(0, tk.END)
        self.qr_image_label.configure(image="", text="🔲\n\nGenera un QR\npara visualizarlo aquí")
        self.qr_image_label.image = None
        self.qr_info_text.delete(1.0, tk.END)
        self.status_label.config(text="🧹 QR limpiado")
        
    def run(self):
        """Ejecutar aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    print("🌱 Iniciando Desktop App Completo...")
    app = DesktopAppCompleto()
    app.run()

if __name__ == "__main__":
    main()