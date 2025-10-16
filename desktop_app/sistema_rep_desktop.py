#!/usr/bin/env python3
"""
SISTEMA REP - Aplicación de Escritorio
Reemplaza la interfaz web con una aplicación ejecutable para PC
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
import uuid
from datetime import datetime
import threading
import qrcode
from PIL import Image, ImageTk
import io
import webbrowser
import os

class SistemaREPDesktop:
    def __init__(self):
        # Intentar diferentes URLs del servidor
        self.server_urls = [
            "http://192.168.5.53:5000",
            "http://localhost:5000",
            "http://127.0.0.1:5000"
        ]
        self.server_url = self.server_urls[0]  # URL por defecto
        self.qrs_generados = []  # Lista para almacenar QRs generados
        self.setup_main_window()
        self.create_widgets()
        self.find_working_server()
    
    def setup_main_window(self):
        self.root = tk.Tk()
        self.root.title("SISTEMA REP - Gestión Sustentable")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2E7D32")
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colores corporativos
        self.style.configure('Title.TLabel', 
                           font=('Arial', 18, 'bold'),
                           foreground='white',
                           background="#2E7D32")
        
        self.style.configure('Header.TLabel',
                           font=('Arial', 12, 'bold'),
                           foreground='white',
                           background="#2E7D32")
        
        self.style.configure('Success.TButton',
                           font=('Arial', 10, 'bold'),
                           foreground='white')
    
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#2E7D32")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text="🌱 SISTEMA REP - GESTIÓN SUSTENTABLE",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Pestaña 1: Generador QR
        self.create_qr_generator_tab()
        
        # Pestaña 2: Dashboard REP
        self.create_dashboard_tab()
        
        # Pestaña 3: Consulta Cliente
        self.create_client_lookup_tab()
        
        # Pestaña 4: Configuración
        self.create_config_tab()
        
        # Status bar
        self.status_frame = tk.Frame(self.root, bg="#1B5E20", height=30)
        self.status_frame.pack(fill="x", side="bottom")
        
        self.status_label = tk.Label(self.status_frame,
                                   text="🔌 Conectado al servidor REP",
                                   bg="#1B5E20", fg="white",
                                   font=('Arial', 9))
        self.status_label.pack(side="left", padx=10, pady=5)
    
    def create_qr_generator_tab(self):
        # Frame para generador QR
        qr_frame = ttk.Frame(self.notebook)
        self.notebook.add(qr_frame, text="📱 Generador QR")
        
        # Título de sección
        ttk.Label(qr_frame, text="Generador de QR Únicos", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame para formulario
        form_frame = tk.Frame(qr_frame, bg="white", relief="raised", bd=2)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # Tipo de QR
        tipo_frame = tk.Frame(form_frame, bg="white")
        tipo_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(tipo_frame, text="Tipo de Balde:", bg="white",
                font=('Arial', 10, 'bold')).pack(side="left")
        
        self.tipo_var = tk.StringVar(value="CODELPA")
        tipo_codelpa = tk.Radiobutton(tipo_frame, text="CODELPA", 
                                     variable=self.tipo_var, value="CODELPA",
                                     bg="white", font=('Arial', 10))
        tipo_codelpa.pack(side="left", padx=10)
        
        tipo_tercero = tk.Radiobutton(tipo_frame, text="TERCERO", 
                                     variable=self.tipo_var, value="TERCERO",
                                     bg="white", font=('Arial', 10))
        tipo_tercero.pack(side="left", padx=10)
        
        # Marca del envase
        marca_frame = tk.Frame(form_frame, bg="white")
        marca_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(marca_frame, text="Marca del Envase:", bg="white",
                font=('Arial', 10, 'bold')).pack(side="left")
        self.marca_entry = tk.Entry(marca_frame, font=('Arial', 10), width=30)
        self.marca_entry.pack(side="left", padx=10)
        
        # Origen
        origen_frame = tk.Frame(form_frame, bg="white")
        origen_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(origen_frame, text="Origen:", bg="white",
                font=('Arial', 10, 'bold')).pack(side="left")
        self.origen_entry = tk.Entry(origen_frame, font=('Arial', 10), width=30)
        self.origen_entry.pack(side="left", padx=10)
        
        # Cantidad
        cantidad_frame = tk.Frame(form_frame, bg="white")
        cantidad_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(cantidad_frame, text="Cantidad:", bg="white",
                font=('Arial', 10, 'bold')).pack(side="left")
        self.cantidad_var = tk.IntVar(value=1)
        cantidad_spin = tk.Spinbox(cantidad_frame, from_=1, to=100, 
                                  textvariable=self.cantidad_var,
                                  font=('Arial', 10), width=10)
        cantidad_spin.pack(side="left", padx=10)
        
        # Botón generar
        btn_generar = tk.Button(form_frame, text="🎯 GENERAR QRs",
                               command=self.generar_qrs,
                               bg="#4CAF50", fg="white",
                               font=('Arial', 12, 'bold'),
                               relief="raised", bd=3)
        btn_generar.pack(pady=20)
        
        # Frame para resultados con layout mejorado
        self.result_frame = tk.Frame(qr_frame, bg="white")
        self.result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame izquierdo para texto
        text_frame = tk.Frame(self.result_frame, bg="white")
        text_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(text_frame, text="📝 Log de Generación:", bg="white",
                font=('Arial', 10, 'bold')).pack(anchor="w")
        
        # Área de texto para QRs generados
        self.qr_text = scrolledtext.ScrolledText(text_frame,
                                                height=15, width=50,
                                                font=('Consolas', 9))
        self.qr_text.pack(fill="both", expand=True)
        
        # Frame derecho para imágenes QR
        image_frame = tk.Frame(self.result_frame, bg="white", relief="sunken", bd=2)
        image_frame.pack(side="right", fill="both", padx=(10, 0))
        
        tk.Label(image_frame, text="🖼️ Códigos QR Generados:", bg="white",
                font=('Arial', 10, 'bold')).pack(pady=5)
        
        # Canvas con scroll para imágenes QR
        self.qr_canvas = tk.Canvas(image_frame, bg="white", width=300, height=400)
        qr_scrollbar = ttk.Scrollbar(image_frame, orient="vertical", command=self.qr_canvas.yview)
        self.qr_scrollable_frame = tk.Frame(self.qr_canvas, bg="white")
        
        self.qr_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.qr_canvas.configure(scrollregion=self.qr_canvas.bbox("all"))
        )
        
        self.qr_canvas.create_window((0, 0), window=self.qr_scrollable_frame, anchor="nw")
        self.qr_canvas.configure(yscrollcommand=qr_scrollbar.set)
        
        self.qr_canvas.pack(side="left", fill="both", expand=True)
        qr_scrollbar.pack(side="right", fill="y")
        
        # Botones de control
        control_frame = tk.Frame(image_frame, bg="white")
        control_frame.pack(fill="x", pady=5)
        
        btn_clear_qr = tk.Button(control_frame, text="🗑️ Limpiar",
                                command=self.limpiar_qrs,
                                bg="#F44336", fg="white",
                                font=('Arial', 9, 'bold'))
        btn_clear_qr.pack(side="left", padx=2)
        
        btn_save_all = tk.Button(control_frame, text="💾 Guardar Todos",
                                command=self.guardar_todos_qrs,
                                bg="#2196F3", fg="white",
                                font=('Arial', 9, 'bold'))
        btn_save_all.pack(side="left", padx=2)
        
        # Lista para almacenar QRs generados
        self.qrs_generados = []
    
    def create_dashboard_tab(self):
        # Frame para dashboard
        dash_frame = ttk.Frame(self.notebook)
        self.notebook.add(dash_frame, text="📊 Dashboard REP")
        
        ttk.Label(dash_frame, text="Dashboard y Reportes REP", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame para estadísticas
        stats_frame = tk.Frame(dash_frame, bg="white", relief="raised", bd=2)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Botón actualizar stats
        btn_stats = tk.Button(stats_frame, text="🔄 Actualizar Estadísticas",
                             command=self.actualizar_estadisticas,
                             bg="#2196F3", fg="white",
                             font=('Arial', 10, 'bold'))
        btn_stats.pack(pady=10)
        
        # Frame para mostrar stats
        self.stats_display = tk.Frame(stats_frame, bg="white")
        self.stats_display.pack(fill="x", padx=20, pady=10)
        
        # Área para reportes
        reports_frame = tk.Frame(dash_frame, bg="white", relief="raised", bd=2)
        reports_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(reports_frame, text="Reportes Mensuales", bg="white",
                font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Selector de lote
        lote_frame = tk.Frame(reports_frame, bg="white")
        lote_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(lote_frame, text="Lote (YYYYMM):", bg="white",
                font=('Arial', 10, 'bold')).pack(side="left")
        
        current_month = datetime.now().strftime("%Y%m")
        self.lote_entry = tk.Entry(lote_frame, font=('Arial', 10), width=10)
        self.lote_entry.insert(0, current_month)
        self.lote_entry.pack(side="left", padx=10)
        
        btn_reporte = tk.Button(lote_frame, text="📋 Ver Reporte",
                               command=self.ver_reporte,
                               bg="#FF9800", fg="white",
                               font=('Arial', 10, 'bold'))
        btn_reporte.pack(side="left", padx=10)
        
        btn_csv = tk.Button(lote_frame, text="💾 Exportar CSV",
                           command=self.exportar_csv,
                           bg="#9C27B0", fg="white",
                           font=('Arial', 10, 'bold'))
        btn_csv.pack(side="left", padx=10)
        
        # Área para mostrar reportes
        self.report_text = scrolledtext.ScrolledText(reports_frame,
                                                    height=15, width=80,
                                                    font=('Consolas', 9))
        self.report_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_client_lookup_tab(self):
        # Frame para consulta cliente
        client_frame = ttk.Frame(self.notebook)
        self.notebook.add(client_frame, text="👤 Consulta Cliente")
        
        ttk.Label(client_frame, text="Consulta de Cliente", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame para búsqueda
        search_frame = tk.Frame(client_frame, bg="white", relief="raised", bd=2)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        search_input_frame = tk.Frame(search_frame, bg="white")
        search_input_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(search_input_frame, text="Nombre del Cliente:", bg="white",
                font=('Arial', 10, 'bold')).pack(side="left")
        
        self.client_search_entry = tk.Entry(search_input_frame, 
                                           font=('Arial', 10), width=30)
        self.client_search_entry.pack(side="left", padx=10)
        self.client_search_entry.bind('<Return>', lambda e: self.buscar_cliente())
        
        btn_buscar = tk.Button(search_input_frame, text="🔍 Buscar",
                              command=self.buscar_cliente,
                              bg="#4CAF50", fg="white",
                              font=('Arial', 10, 'bold'))
        btn_buscar.pack(side="left", padx=10)
        
        # Área para mostrar información del cliente
        self.client_info_text = scrolledtext.ScrolledText(client_frame,
                                                         height=20, width=80,
                                                         font=('Consolas', 10))
        self.client_info_text.pack(fill="both", expand=True, padx=20, pady=10)
    
    def create_config_tab(self):
        # Frame para configuración
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuración")
        
        ttk.Label(config_frame, text="Configuración del Sistema", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame para configuración del servidor
        server_frame = tk.Frame(config_frame, bg="white", relief="raised", bd=2)
        server_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(server_frame, text="Configuración del Servidor", bg="white",
                font=('Arial', 12, 'bold')).pack(pady=5)
        
        server_input_frame = tk.Frame(server_frame, bg="white")
        server_input_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(server_input_frame, text="URL del Servidor:", bg="white",
                font=('Arial', 10, 'bold')).pack(side="left")
        
        self.server_entry = tk.Entry(server_input_frame, 
                                    font=('Arial', 10), width=40)
        self.server_entry.insert(0, self.server_url)
        self.server_entry.pack(side="left", padx=10)
        
        btn_test = tk.Button(server_input_frame, text="🔌 Probar Conexión",
                            command=self.test_connection,
                            bg="#2196F3", fg="white",
                            font=('Arial', 10, 'bold'))
        btn_test.pack(side="left", padx=10)
        
        btn_save = tk.Button(server_input_frame, text="💾 Guardar",
                            command=self.save_config,
                            bg="#4CAF50", fg="white",
                            font=('Arial', 10, 'bold'))
        btn_save.pack(side="left", padx=10)
        
        # Frame para información del sistema
        info_frame = tk.Frame(config_frame, bg="white", relief="raised", bd=2)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(info_frame, text="Información del Sistema", bg="white",
                font=('Arial', 12, 'bold')).pack(pady=5)
        
        info_text = """
🌱 SISTEMA REP - Gestión Sustentable v1.0

📱 Aplicaciones Conectadas:
   • App Scanner Android - Escaneo QR
   • App Sustentable Android - Consulta cliente
   • Sistema Desktop PC - Gestión completa

🔧 Funcionalidades:
   • Generación QR únicos (CODELPA/TERCERO)
   • Dashboard con estadísticas en tiempo real
   • Consulta de clientes y historial
   • Reportes mensuales automáticos
   • Exportación CSV para cumplimiento regulatorio

🌐 Conectividad:
   • Servidor centralizado en red WiFi
   • Sincronización automática entre aplicaciones
   • Base de datos SQLite compartida

📊 Cumplimiento REP:
   • Trazabilidad completa de envases
   • Reportes por lotes mensuales (YYYYMM)
   • Diferenciación REUSO vs VALORIZACIÓN
   • Puntos por sustentabilidad
        """
        
        info_label = tk.Label(info_frame, text=info_text, bg="white",
                             font=('Arial', 9), justify="left")
        info_label.pack(padx=20, pady=10, anchor="w")
    
    def generar_qrs(self):
        """Genera QRs únicos y los muestra"""
        tipo = self.tipo_var.get()
        marca = self.marca_entry.get().strip()
        origen = self.origen_entry.get().strip()
        cantidad = self.cantidad_var.get()
        
        # Validaciones
        if not marca or not origen:
            messagebox.showerror("Error", "Marca y Origen son obligatorios")
            return
            
        if cantidad <= 0 or cantidad > 50:
            messagebox.showerror("Error", "La cantidad debe estar entre 1 y 50")
            return
        
        # Probar conexión antes de generar
        try:
            response = requests.get(f"{self.server_url}/stats", timeout=3)
            if response.status_code != 200:
                messagebox.showerror("Error de Conexión", 
                                   f"No se puede conectar al servidor.\n"
                                   f"URL: {self.server_url}\n"
                                   f"Código: {response.status_code}")
                return
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", 
                               f"No se puede conectar al servidor.\n"
                               f"URL: {self.server_url}\n"
                               f"Error: {str(e)}\n\n"
                               f"Verifique que el servidor esté ejecutándose.")
            return
        
        self.qr_text.delete(1.0, tk.END)
        self.qr_text.insert(tk.END, f"🎯 Generando {cantidad} QRs tipo {tipo}...\n")
        self.qr_text.insert(tk.END, f"📡 Servidor: {self.server_url}\n")
        self.qr_text.insert(tk.END, f"🏷️ Marca: {marca} | 📍 Origen: {origen}\n\n")
        
        # Generar QRs en hilo separado
        threading.Thread(target=self._generar_qrs_thread, 
                        args=(tipo, marca, origen, cantidad), daemon=True).start()
    
    def _generar_qrs_thread(self, tipo, marca, origen, cantidad):
        """Hilo para generar QRs sin bloquear UI"""
        try:
            qrs_generados = []
            
            for i in range(cantidad):
                try:
                    # Enviar al servidor con los campos correctos
                    data = {
                        "tipo_qr": tipo,  # Campo correcto que espera el servidor
                        "marca_envase": marca,
                        "origen": origen,
                        "peso_envase_kg": 1.5,  # Peso por defecto
                        "lote_produccion": f"LOTE_{datetime.now().strftime('%Y%m%d')}"
                    }
                    
                    response = requests.post(f"{self.server_url}/generate_qr", 
                                           json=data, timeout=10)
                    
                    if response.status_code in [200, 201]:  # Aceptar ambos códigos
                        result = response.json()
                        qr_code = result.get('qr_id', f"{tipo}:ERROR")
                        
                        qrs_generados.append({
                            "qr_code": qr_code,
                            "marca": marca,
                            "origen": origen
                        })
                        
                        # Generar imagen QR
                        self.root.after(0, self._crear_imagen_qr, qr_code, marca, origen)
                        
                        # Actualizar UI en el hilo principal
                        self.root.after(0, self._update_qr_display, 
                                       f"✅ {qr_code} - {marca} ({origen})\n")
                    else:
                        error_msg = f"Error {response.status_code}"
                        if response.text:
                            try:
                                error_data = response.json()
                                error_msg = error_data.get('error', error_msg)
                            except:
                                error_msg = response.text[:100]
                        
                        self.root.after(0, self._update_qr_display, 
                                       f"❌ Error QR {i+1}: {error_msg}\n")
                        
                except requests.exceptions.RequestException as e:
                    self.root.after(0, self._update_qr_display, 
                                   f"❌ Error conexión QR {i+1}: {str(e)}\n")
                except Exception as e:
                    self.root.after(0, self._update_qr_display, 
                                   f"❌ Error QR {i+1}: {str(e)}\n")
            
            # Mostrar resumen final
            self.root.after(0, self._update_qr_display, 
                           f"\n🎉 Generación completada: {len(qrs_generados)}/{cantidad} QRs\n")
            
        except Exception as e:
            self.root.after(0, self._update_qr_display, 
                           f"\n❌ Error: {str(e)}\n")
    
    def _update_qr_display(self, text):
        """Actualiza el display de QRs generados"""
        self.qr_text.insert(tk.END, text)
        self.qr_text.see(tk.END)
    
    def _crear_imagen_qr(self, qr_code, marca, origen):
        """Crea y muestra la imagen del QR"""
        try:
            # Generar QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=4,
                border=2,
            )
            qr.add_data(qr_code)
            qr.make(fit=True)
            
            # Crear imagen
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img = qr_img.resize((150, 150), Image.Resampling.LANCZOS)
            
            # Convertir para tkinter
            photo = ImageTk.PhotoImage(qr_img)
            
            # Crear frame para este QR
            qr_item_frame = tk.Frame(self.qr_scrollable_frame, bg="white", 
                                    relief="raised", bd=1, padx=5, pady=5)
            qr_item_frame.pack(fill="x", pady=2)
            
            # Imagen QR
            qr_label = tk.Label(qr_item_frame, image=photo, bg="white")
            qr_label.image = photo  # Mantener referencia
            qr_label.pack()
            
            # Información del QR
            info_label = tk.Label(qr_item_frame, 
                                 text=f"{qr_code}\n{marca} - {origen}",
                                 bg="white", font=('Arial', 8, 'bold'),
                                 justify="center")
            info_label.pack(pady=2)
            
            # Botones de acción
            btn_frame = tk.Frame(qr_item_frame, bg="white")
            btn_frame.pack(fill="x", pady=2)
            
            btn_save = tk.Button(btn_frame, text="💾",
                                command=lambda: self._guardar_qr_individual(qr_code, qr_img),
                                bg="#4CAF50", fg="white",
                                font=('Arial', 8))
            btn_save.pack(side="left", padx=1)
            
            btn_print = tk.Button(btn_frame, text="🖨️",
                                 command=lambda: self._imprimir_qr(qr_code, qr_img),
                                 bg="#2196F3", fg="white",
                                 font=('Arial', 8))
            btn_print.pack(side="left", padx=1)
            
            btn_copy = tk.Button(btn_frame, text="📋",
                                command=lambda: self._copiar_qr_texto(qr_code),
                                bg="#FF9800", fg="white",
                                font=('Arial', 8))
            btn_copy.pack(side="left", padx=1)
            
            # Guardar datos del QR
            self.qrs_generados.append({
                'codigo': qr_code,
                'marca': marca,
                'origen': origen,
                'imagen': qr_img,
                'frame': qr_item_frame
            })
            
            # Actualizar scroll region
            self.qr_canvas.configure(scrollregion=self.qr_canvas.bbox("all"))
            
        except Exception as e:
            self.qr_text.insert(tk.END, f"❌ Error creando imagen QR: {str(e)}\n")
    
    def _guardar_qr_individual(self, qr_code, qr_img):
        """Guarda un QR individual"""
        try:
            filename = f"QR_{qr_code.replace(':', '_')}.png"
            qr_img.save(filename)
            messagebox.showinfo("Guardado", f"QR guardado como {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando QR: {str(e)}")
    
    def _imprimir_qr(self, qr_code, qr_img):
        """Abre el QR para imprimir"""
        try:
            filename = f"QR_TEMP_{qr_code.replace(':', '_')}.png"
            qr_img.save(filename)
            os.startfile(filename, "print")
        except Exception as e:
            messagebox.showerror("Error", f"Error imprimiendo QR: {str(e)}")
    
    def _copiar_qr_texto(self, qr_code):
        """Copia el texto del QR al portapapeles"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(qr_code)
            messagebox.showinfo("Copiado", f"Texto '{qr_code}' copiado al portapapeles")
        except Exception as e:
            messagebox.showerror("Error", f"Error copiando: {str(e)}")
    
    def limpiar_qrs(self):
        """Limpia todos los QRs generados"""
        try:
            # Limpiar frames de QR
            for widget in self.qr_scrollable_frame.winfo_children():
                widget.destroy()
            
            # Limpiar lista
            self.qrs_generados.clear()
            
            # Limpiar texto
            self.qr_text.delete(1.0, tk.END)
            self.qr_text.insert(tk.END, "🗑️ QRs limpiados. Listo para generar nuevos.\n\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error limpiando QRs: {str(e)}")
    
    def guardar_todos_qrs(self):
        """Guarda todas las imágenes QR generadas"""
        if not self.qrs_generados:
            messagebox.showwarning("Sin QRs", "No hay QRs generados para guardar")
            return
        
        try:
            # Crear carpeta con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = f"QRs_REP_{timestamp}"
            os.makedirs(folder_name, exist_ok=True)
            
            guardados = 0
            for qr_data in self.qrs_generados:
                filename = f"QR_{qr_data['codigo'].replace(':', '_')}.png"
                filepath = os.path.join(folder_name, filename)
                qr_data['imagen'].save(filepath)
                guardados += 1
            
            messagebox.showinfo("Guardado Completo", 
                              f"✅ {guardados} QRs guardados en carpeta:\n{folder_name}")
            
            # Abrir carpeta
            if messagebox.askyesno("Abrir Carpeta", "¿Deseas abrir la carpeta con los QRs?"):
                os.startfile(folder_name)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando QRs: {str(e)}")
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas del dashboard"""
        try:
            # Limpiar estadísticas anteriores
            for widget in self.stats_display.winfo_children():
                widget.destroy()
            
            # Obtener estadísticas del servidor
            response = requests.get(f"{self.server_url}/stats", timeout=5)
            
            if response.status_code == 200:
                stats = response.json()
                self._mostrar_estadisticas(stats)
            else:
                # Generar estadísticas básicas
                self._generar_estadisticas_basicas()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error obteniendo estadísticas: {str(e)}")
    
    def _mostrar_estadisticas(self, stats):
        """Muestra las estadísticas en el dashboard"""
        # Crear cards de estadísticas
        cards_frame = tk.Frame(self.stats_display, bg="white")
        cards_frame.pack(fill="x", pady=10)
        
        # Card QRs generados
        qr_card = tk.Frame(cards_frame, bg="#E3F2FD", relief="raised", bd=2)
        qr_card.pack(side="left", padx=10, pady=5, fill="both", expand=True)
        
        tk.Label(qr_card, text="📱 QRs Generados", bg="#E3F2FD",
                font=('Arial', 10, 'bold')).pack(pady=5)
        tk.Label(qr_card, text=str(stats.get('qrs_generados', 0)), bg="#E3F2FD",
                font=('Arial', 16, 'bold'), fg="#1976D2").pack()
        
        # Card Retornos procesados
        ret_card = tk.Frame(cards_frame, bg="#E8F5E8", relief="raised", bd=2)
        ret_card.pack(side="left", padx=10, pady=5, fill="both", expand=True)
        
        tk.Label(ret_card, text="♻️ Retornos", bg="#E8F5E8",
                font=('Arial', 10, 'bold')).pack(pady=5)
        tk.Label(ret_card, text=str(stats.get('retornos_total', 0)), bg="#E8F5E8",
                font=('Arial', 16, 'bold'), fg="#388E3C").pack()
        
        # Card Peso reciclado
        peso_card = tk.Frame(cards_frame, bg="#FFF3E0", relief="raised", bd=2)
        peso_card.pack(side="left", padx=10, pady=5, fill="both", expand=True)
        
        tk.Label(peso_card, text="⚖️ Peso Reciclado", bg="#FFF3E0",
                font=('Arial', 10, 'bold')).pack(pady=5)
        peso_kg = stats.get('peso_total_kg', 0)
        tk.Label(peso_card, text=f"{peso_kg:.1f} kg", bg="#FFF3E0",
                font=('Arial', 16, 'bold'), fg="#F57C00").pack()
        
        # Card Puntos otorgados
        puntos_card = tk.Frame(cards_frame, bg="#F3E5F5", relief="raised", bd=2)
        puntos_card.pack(side="left", padx=10, pady=5, fill="both", expand=True)
        
        tk.Label(puntos_card, text="⭐ Puntos Otorgados", bg="#F3E5F5",
                font=('Arial', 10, 'bold')).pack(pady=5)
        tk.Label(puntos_card, text=str(stats.get('puntos_total', 0)), bg="#F3E5F5",
                font=('Arial', 16, 'bold'), fg="#7B1FA2").pack()
    
    def _generar_estadisticas_basicas(self):
        """Genera estadísticas básicas desde la BD"""
        try:
            # Intentar obtener datos básicos
            response_profiles = requests.get(f"{self.server_url}/profiles", timeout=5)
            
            stats = {
                'qrs_generados': 0,
                'retornos_total': 0,
                'peso_total_kg': 0.0,
                'puntos_total': 0
            }
            
            if response_profiles.status_code == 200:
                profiles = response_profiles.json()
                stats['puntos_total'] = sum(p.get('points', 0) for p in profiles)
            
            self._mostrar_estadisticas(stats)
            
        except Exception as e:
            # Mostrar estadísticas vacías
            self._mostrar_estadisticas({})
    
    def ver_reporte(self):
        """Muestra el reporte mensual"""
        lote = self.lote_entry.get()
        
        if not lote or len(lote) != 6:
            messagebox.showerror("Error", "Formato de lote inválido (YYYYMM)")
            return
        
        try:
            response = requests.get(f"{self.server_url}/reporte_rep/{lote}", timeout=10)
            
            if response.status_code == 200:
                reporte = response.json()
                self._mostrar_reporte(reporte, lote)
            else:
                self.report_text.delete(1.0, tk.END)
                self.report_text.insert(tk.END, f"❌ No se encontró reporte para lote {lote}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error obteniendo reporte: {str(e)}")
    
    def _mostrar_reporte(self, reporte, lote):
        """Muestra el reporte en el área de texto"""
        self.report_text.delete(1.0, tk.END)
        
        texto_reporte = f"""
📋 REPORTE REP - LOTE {lote}
{'='*50}

📊 RESUMEN GENERAL:
   • Total Retornos: {reporte.get('total_retornos', 0)}
   • Peso Total: {reporte.get('peso_total_kg', 0):.2f} kg
   • Puntos Otorgados: {reporte.get('puntos_total', 0)}

🏢 DESTINOS:
   • REUSO CODELPA: {reporte.get('reuso_codelpa', 0)} retornos
   • VALORIZACIÓN INPROPLAS: {reporte.get('valorizacion_inproplas', 0)} retornos

📈 ESTADÍSTICAS POR ESTADO:
   • BUENO: {reporte.get('estado_bueno', 0)}
   • REPARABLE: {reporte.get('estado_reparable', 0)}
   • DAÑADO: {reporte.get('estado_danado', 0)}

🏪 TOP TIENDAS:
"""
        
        # Agregar top tiendas si están disponibles
        top_tiendas = reporte.get('top_tiendas', [])
        for i, tienda in enumerate(top_tiendas[:5], 1):
            texto_reporte += f"   {i}. {tienda.get('tienda', 'N/A')}: {tienda.get('retornos', 0)} retornos\n"
        
        # Agregar detalles por fecha si están disponibles
        if 'retornos_por_fecha' in reporte:
            texto_reporte += "\n📅 RETORNOS POR FECHA:\n"
            for fecha_info in reporte['retornos_por_fecha'][:10]:
                fecha = fecha_info.get('fecha', 'N/A')
                cantidad = fecha_info.get('cantidad', 0)
                texto_reporte += f"   • {fecha}: {cantidad} retornos\n"
        
        self.report_text.insert(tk.END, texto_reporte)
    
    def exportar_csv(self):
        """Exporta el reporte a CSV"""
        lote = self.lote_entry.get()
        
        if not lote or len(lote) != 6:
            messagebox.showerror("Error", "Formato de lote inválido (YYYYMM)")
            return
        
        try:
            response = requests.get(f"{self.server_url}/export_rep_csv/{lote}", timeout=10)
            
            if response.status_code == 200:
                # Guardar archivo CSV
                filename = f"reporte_rep_{lote}.csv"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                messagebox.showinfo("Éxito", f"Reporte exportado como {filename}")
                
                # Abrir archivo si el usuario quiere
                if messagebox.askyesno("Abrir archivo", "¿Deseas abrir el archivo CSV?"):
                    os.startfile(filename)
            else:
                messagebox.showerror("Error", "No se pudo exportar el reporte")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error exportando CSV: {str(e)}")
    
    def buscar_cliente(self):
        """Busca información de un cliente"""
        nombre = self.client_search_entry.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "Ingresa el nombre del cliente")
            return
        
        try:
            response = requests.get(f"{self.server_url}/cliente_retornos/{nombre}", timeout=10)
            
            if response.status_code == 200:
                cliente_data = response.json()
                self._mostrar_info_cliente(cliente_data, nombre)
            else:
                self.client_info_text.delete(1.0, tk.END)
                self.client_info_text.insert(tk.END, 
                    f"❌ Cliente '{nombre}' no encontrado.\n\n"
                    "🔍 Verifica:\n"
                    "• El nombre esté escrito correctamente\n"
                    "• El cliente haya escaneado al menos un QR\n"
                    "• La conexión con el servidor esté activa")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error buscando cliente: {str(e)}")
    
    def _mostrar_info_cliente(self, data, nombre):
        """Muestra la información del cliente"""
        self.client_info_text.delete(1.0, tk.END)
        
        profile = data.get('profile', {})
        retornos = data.get('retornos_recientes', [])
        total_retornos = data.get('total_retornos', 0)
        peso_total = data.get('peso_total_kg', 0)
        
        info_texto = f"""
👤 INFORMACIÓN DEL CLIENTE: {nombre}
{'='*50}

⭐ PUNTOS ACUMULADOS: {profile.get('points', 0)}
♻️ TOTAL RETORNOS: {total_retornos}
⚖️ PESO TOTAL RECICLADO: {peso_total:.2f} kg

📱 HISTORIAL RECIENTE (últimos 10):
"""
        
        if retornos:
            for i, retorno in enumerate(retornos, 1):
                qr_id = retorno.get('qr_id', 'N/A')
                marca = retorno.get('marca_envase', 'N/A')
                peso = retorno.get('peso_envase_kg', 0)
                puntos = retorno.get('puntos_otorgados', 0)
                destino = retorno.get('destino', 'N/A')
                fecha = retorno.get('fecha_retorno', 0)
                
                # Convertir timestamp a fecha legible
                if isinstance(fecha, (int, float)) and fecha > 0:
                    fecha_str = datetime.fromtimestamp(fecha).strftime("%d/%m/%Y %H:%M")
                else:
                    fecha_str = "N/A"
                
                info_texto += f"""
   {i}. QR: {qr_id}
      📦 Marca: {marca}
      ⚖️ Peso: {peso}kg
      ⭐ Puntos: {puntos}
      🎯 Destino: {destino}
      📅 Fecha: {fecha_str}
"""
        else:
            info_texto += "\n   📭 No hay retornos registrados"
        
        info_texto += f"""

🔗 CONECTIVIDAD:
   • ✅ Visible en App Scanner Android
   • ✅ Visible en App Sustentable Android  
   • ✅ Sincronizado con servidor REP
"""
        
        self.client_info_text.insert(tk.END, info_texto)
    
    def find_working_server(self):
        """Encuentra un servidor que funcione"""
        for url in self.server_urls:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    self.server_url = url
                    self.status_label.config(text=f"🔌 Conectado a {url}", fg="lightgreen")
                    messagebox.showinfo("Conexión", f"✅ Conectado a servidor: {url}")
                    return True
            except:
                continue
        
        # No se encontró servidor funcionando
        self.status_label.config(text="❌ Sin conexión - Inicia el servidor", fg="red")
        messagebox.showerror("Error", 
            "❌ No se puede conectar al servidor REP\n\n"
            "🔧 Soluciones:\n"
            "1. Ejecutar INICIAR_SERVIDOR_REP.bat\n"
            "2. Verificar que el puerto 5000 esté abierto\n"
            "3. Confirmar que están en la misma WiFi")
        return False
    
    def test_connection(self):
        """Prueba la conexión con el servidor"""
        try:
            response = requests.get(f"{self.server_url}/", timeout=5)
            
            if response.status_code == 200:
                self.status_label.config(text=f"🔌 Conectado a {self.server_url}", fg="lightgreen")
                messagebox.showinfo("Conexión", f"✅ Conexión exitosa: {self.server_url}")
            else:
                self.status_label.config(text="⚠️ Servidor responde con error", fg="orange")
                messagebox.showwarning("Conexión", f"⚠️ Servidor responde: {response.status_code}")
                
        except Exception as e:
            self.status_label.config(text="❌ Sin conexión al servidor", fg="red")
            messagebox.showerror("Error", 
                f"❌ Error de conexión: {str(e)}\n\n"
                "🔧 Soluciones:\n"
                "1. Iniciar servidor con INICIAR_SERVIDOR_REP.bat\n"
                "2. Verificar firewall y puerto 5000\n"
                "3. Probar con localhost en configuración")
    
    def save_config(self):
        """Guarda la configuración del servidor"""
        new_url = self.server_entry.get().strip()
        
        if not new_url:
            messagebox.showerror("Error", "URL del servidor no puede estar vacía")
            return
        
        # Validar formato URL básico
        if not (new_url.startswith('http://') or new_url.startswith('https://')):
            new_url = 'http://' + new_url
        
        self.server_url = new_url
        self.server_entry.delete(0, tk.END)
        self.server_entry.insert(0, self.server_url)
        
        messagebox.showinfo("Configuración", "✅ URL del servidor actualizada")
        
        # Probar nueva conexión
        self.test_connection()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    print("🌱 Iniciando Sistema REP Desktop...")
    app = SistemaREPDesktop()
    app.run()

if __name__ == "__main__":
    main()