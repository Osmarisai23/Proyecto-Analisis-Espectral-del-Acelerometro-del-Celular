import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import numpy as np

# Integración correcta de Matplotlib en Tkinter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Importación de módulos del proyecto
from scripts.leer_datos import leer_datos
from scripts.procesar_senal import procesar_senal
from scripts.fft_espectral import fft_espectral
from scripts.comparar import comparar
from scripts.tabla_comparativa import crear_tabla_comparativa
from scripts.tabla_armonicos import crear_tabla_armonicos

class DashboardProfesionalCompleto:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis del Acelerómetro del Celular")
        self.root.geometry("1300x750")
        self.root.configure(bg="#1e1e2e")

        # Variables globales del sistema
        self.rutas = {"Caminar": None, "Correr": None}
        self.resultados = {}

        # --- ESTILOS DE LA INTERFAZ ---
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            ".",
            background="#1e1e2e",
            foreground="#cdd6f4",
            font=("Segoe UI", 10)
        )

        self.style.configure(
            "TLabelframe",
            background="#181825",
            bordercolor="#45475a",
            borderwidth=1
        )

        self.style.configure(
            "TLabelframe.Label",
            background="#181825",
            foreground="#cba6f7",
            font=("Segoe UI", 10, "bold")
        )

        self.style.configure(
            "TButton",
            background="#313244",
            foreground="#cdd6f4",
            borderwidth=0,
            padding=5,
            font=("Segoe UI", 9, "bold")
        )

        self.style.map(
            "TButton",
            background=[("active", "#b4befe")],
            foreground=[("active", "#11111b")]
        )

        self.style.configure(
            "Accent.TButton",
            background="#89b4fa",
            foreground="#11111b"
        )

        self.style.configure(
            "Success.TButton",
            background="#a6e3a1",
            foreground="#11111b"
        )

        # --- LAYOUT PRINCIPAL ---
        self.panel_izquierdo = tk.Frame(root, bg="#181825", width=360)
        self.panel_izquierdo.pack(side="left", fill="y", padx=10, pady=10)
        self.panel_izquierdo.pack_propagate(False)

        self.panel_derecho = tk.Frame(root, bg="#11111b")
        self.panel_derecho.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(
            self.panel_izquierdo,
            text="DASHBOARD DE ACTIVIDADES",
            font=("Segoe UI", 12, "bold"),
            bg="#181825",
            fg="#f5e0dc"
        ).pack(pady=10)

        # --- 1. CARGA DE ARCHIVOS ---
        frame_carga = ttk.LabelFrame(
            self.panel_izquierdo,
            text=" 1. Importación de Señales "
        )
        frame_carga.pack(fill="x", padx=10, pady=5)

        ttk.Button(
            frame_carga,
            text="Cargar CSV Caminar",
            command=lambda: self.subir_archivo("Caminar")
        ).pack(fill="x", padx=10, pady=4)

        self.lbl_caminar = tk.Label(
            frame_carga,
            text="No se ha cargado archivo",
            fg="#f38ba8",
            bg="#181825",
            font=("Segoe UI", 9, "italic")
        )
        self.lbl_caminar.pack(anchor="w", padx=12)

        ttk.Button(
            frame_carga,
            text="Cargar CSV Correr",
            command=lambda: self.subir_archivo("Correr")
        ).pack(fill="x", padx=10, pady=4)

        self.lbl_correr = tk.Label(
            frame_carga,
            text="No se ha cargado archivo",
            fg="#f38ba8",
            bg="#181825",
            font=("Segoe UI", 9, "italic")
        )
        self.lbl_correr.pack(anchor="w", padx=12, pady=2)

        # --- 2. BOTONES DE VISUALIZACIÓN ---
        frame_acciones = ttk.LabelFrame(
            self.panel_izquierdo,
            text=" 2. Módulos de Visualización "
        )
        frame_acciones.pack(fill="x", padx=10, pady=5)

        ttk.Button(
            frame_acciones,
            text="Ver Gráficas: Caminar",
            command=lambda: self.dibujar_analisis_individual("Caminar")
        ).pack(fill="x", padx=10, pady=4)

        ttk.Button(
            frame_acciones,
            text="Ver Espectrograma: Caminar",
            command=lambda: self.dibujar_espectrograma_individual("Caminar")
        ).pack(fill="x", padx=10, pady=4)

        ttk.Button(
            frame_acciones,
            text="Ver Gráficas: Correr",
            command=lambda: self.dibujar_analisis_individual("Correr")
        ).pack(fill="x", padx=10, pady=4)

        ttk.Button(
            frame_acciones,
            text="Ver Espectrograma: Correr",
            command=lambda: self.dibujar_espectrograma_individual("Correr")
        ).pack(fill="x", padx=10, pady=4)

        ttk.Button(
            frame_acciones,
            text="Mostrar Comparación Cruzada",
            style="Accent.TButton",
            command=self.dibujar_comparativa_total
        ).pack(fill="x", padx=10, pady=8)

        ttk.Button(
            frame_acciones,
            text="Generar Tabla Comparativa",
            style="Success.TButton",
            command=self.generar_tabla_comparativa
        ).pack(fill="x", padx=10, pady=4)

        ttk.Button(
            frame_acciones,
            text="Generar Tabla de Armónicos",
            style="Success.TButton",
            command=self.generar_tabla_armonicos
        ).pack(fill="x", padx=10, pady=4)

        # --- 3. CONSOLA DE MÉTRICAS ---
        frame_metricas = ttk.LabelFrame(
            self.panel_izquierdo,
            text=" 3. Historial de Métricas "
        )
        frame_metricas.pack(fill="both", expand=True, padx=10, pady=10)

        self.txt_reporte = tk.Text(
            frame_metricas,
            bg="#1e1e2e",
            fg="#a6e3a1",
            font=("Consolas", 9),
            borderwidth=0,
            highlightthickness=0,
            padx=8,
            pady=8
        )
        self.txt_reporte.pack(fill="both", expand=True)
        self.txt_reporte.insert("1.0", "Carga datos para iniciar...")
        self.txt_reporte.config(state="disabled")

        # --- LIENZO GLOBAL DE MATPLOTLIB ---
        self.fig = plt.figure(facecolor="#11111b")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.panel_derecho)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def subir_archivo(self, actividad):
        archivo = filedialog.askopenfilename(
            title=f"Subir CSV {actividad}",
            filetypes=[("Archivos CSV", "*.csv")]
        )

        if archivo:
            self.rutas[actividad] = archivo
            nombre = os.path.basename(archivo)

            if actividad == "Caminar":
                self.lbl_caminar.config(
                    text=f"✓ {nombre}",
                    fg="#a6e3a1",
                    font=("Segoe UI", 9, "bold")
                )
            else:
                self.lbl_correr.config(
                    text=f"✓ {nombre}",
                    fg="#a6e3a1",
                    font=("Segoe UI", 9, "bold")
                )

            self.calcular_metricas_background(actividad, archivo)

    def calcular_metricas_background(self, actividad, ruta):
        t, ax, ay, az = leer_datos(ruta)
        senal = procesar_senal(ax, ay, az)

        (
            f,
            P1,
            frecuencia_dom,
            cadencia,
            pico_max,
            energia_espectral,
            f_psd,
            psd
        ) = fft_espectral(senal, t)

        self.resultados[actividad] = {
            "t": t,
            "senal": senal,
            "f": f,
            "P1": P1,
            "fd": frecuencia_dom,
            "cad": cadencia,
            "pico": pico_max,
            "en": energia_espectral,
            "f_psd": f_psd,
            "psd": psd
        }

        self.actualizar_consola_texto()

    def actualizar_consola_texto(self):
        self.txt_reporte.config(state="normal")
        self.txt_reporte.delete("1.0", tk.END)

        texto = "=== MÉTRICAS DEL SISTEMA ===\n\n"

        for act in ["Caminar", "Correr"]:
            if act in self.resultados:
                res = self.resultados[act]
                texto += f"[{act.upper()}]\n"
                texto += f"• Freq Dom: {res['fd']:.2f} Hz\n"
                texto += f"• Cadencia: {res['cad']:.1f} ppm\n"
                texto += f"• Pico Máx: {res['pico']:.2f}\n"
                texto += f"• Energía:  {res['en']:.2f}\n\n"
            else:
                texto += f"[{act.upper()}]\n"
                texto += "• Esperando datos...\n\n"

        self.txt_reporte.insert("1.0", texto)
        self.txt_reporte.config(state="disabled")

    def limpiar_lienzo(self):
        self.fig.clear()

    def dibujar_analisis_individual(self, actividad):
        if actividad not in self.resultados:
            messagebox.showerror(
                "Error",
                f"Primero debes cargar el archivo CSV de {actividad}."
            )
            return

        self.limpiar_lienzo()
        res = self.resultados[actividad]

        axes = self.fig.subplots(3, 1)

        self.fig.suptitle(
            f"Análisis Espectral - {actividad}",
            fontsize=13,
            fontweight="bold",
            color="#cdd6f4"
        )

        for ax in axes:
            ax.set_facecolor("#1e1e2e")
            ax.tick_params(colors="#cdd6f4", labelsize=8)
            ax.xaxis.label.set_color("#cdd6f4")
            ax.yaxis.label.set_color("#cdd6f4")
            ax.title.set_color("#cba6f7")
            ax.grid(True, linestyle="--", alpha=0.3)

        axes[0].plot(res["t"], res["senal"], color="#a6e3a1")
        axes[0].set_title("Señal en el Tiempo", fontsize=10)
        axes[0].set_xlabel("Tiempo (s)")
        axes[0].set_ylabel("Magnitud")

        axes[1].plot(res["f"], res["P1"], color="#89b4fa")
        axes[1].axvline(
            res["fd"],
            color="#f38ba8",
            linestyle="--",
            label=f"Dom: {res['fd']:.2f} Hz"
        )
        axes[1].set_xlim(0, 10)
        axes[1].set_title("Análisis Espectral FFT", fontsize=10)
        axes[1].set_xlabel("Frecuencia (Hz)")
        axes[1].set_ylabel("Magnitud")
        axes[1].legend(prop={"size": 8})

        axes[2].semilogy(res["f_psd"], res["psd"], color="#f9e2af")
        axes[2].set_xlim(0, 10)
        axes[2].set_title("Densidad Espectral de Potencia (PSD)", fontsize=10)
        axes[2].set_xlabel("Frecuencia (Hz)")
        axes[2].set_ylabel("Potencia")

        self.fig.tight_layout(rect=[0, 0, 1, 0.95])
        self.canvas.draw()

    def dibujar_espectrograma_individual(self, actividad):
        if actividad not in self.resultados:
            messagebox.showerror(
                "Error",
                f"Primero debes cargar el archivo CSV de {actividad}."
            )
            return

        self.limpiar_lienzo()
        res = self.resultados[actividad]

        dt = np.mean(np.diff(res["t"]))
        fs = 1 / dt

        ax = self.fig.add_subplot(111)
        ax.set_facecolor("#1e1e2e")
        ax.tick_params(colors="#cdd6f4")
        ax.xaxis.label.set_color("#cdd6f4")
        ax.yaxis.label.set_color("#cdd6f4")

        _, _, _, im = ax.specgram(
            res["senal"],
            Fs=fs,
            NFFT=256,
            noverlap=220,
            cmap="viridis",
            vmin=-80,
            vmax=20
        )

        ax.set_ylim(0, 8)
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Frecuencia (Hz)")
        ax.set_title(
            f"Espectrograma Dinámico - {actividad}",
            color="#cba6f7",
            fontsize=12,
            fontweight="bold"
        )

        cbar = self.fig.colorbar(im, ax=ax)
        cbar.ax.yaxis.set_tick_params(color="#cdd6f4")
        cbar.set_label("Intensidad", color="#cdd6f4")

        self.fig.tight_layout()
        self.canvas.draw()

    def dibujar_comparativa_total(self):
        if not self.rutas["Caminar"] or not self.rutas["Correr"]:
            messagebox.showerror(
                "Error",
                "Debes cargar ambos archivos (.csv) para ver la comparación."
            )
            return

        self.limpiar_lienzo()
        axes = self.fig.subplots(3, 1)

        for ax in axes:
            ax.set_facecolor("#1e1e2e")
            ax.tick_params(colors="#cdd6f4", labelsize=8)
            ax.xaxis.label.set_color("#cdd6f4")
            ax.yaxis.label.set_color("#cdd6f4")
            ax.title.set_color("#cba6f7")
            ax.grid(True, linestyle="--", alpha=0.3)

        comparar(
            self.rutas["Caminar"],
            self.rutas["Correr"],
            self.fig,
            axes
        )

        self.fig.tight_layout(rect=[0, 0, 1, 0.95])
        self.canvas.draw()

    def generar_tabla_comparativa(self):
        if "Caminar" not in self.resultados or "Correr" not in self.resultados:
            messagebox.showerror(
                "Error",
                "Debes cargar ambos archivos CSV para generar la tabla comparativa."
            )
            return

        self.limpiar_lienzo()
        
        datos_tabla, columnas = crear_tabla_comparativa(self.resultados)

        ax = self.fig.add_subplot(111)
        ax.set_facecolor("#1e1e2e")
        ax.axis("off")

        tabla = ax.table(
            cellText=datos_tabla,
            colLabels=columnas,
            cellLoc="center",
            loc="center"
        )

        tabla.auto_set_font_size(False)
        tabla.set_fontsize(8)
        tabla.scale(1.2, 2)

        for key, cell in tabla.get_celld().items():
            cell.set_edgecolor("#45475a")
            cell.set_text_props(color="#cdd6f4")

            if key[0] == 0:
                cell.set_facecolor("#313244")
                cell.set_text_props(weight="bold", color="#f5e0dc")
            else:
                cell.set_facecolor("#1e1e2e")

        ax.set_title(
            "Tabla General Comparativa",
            color="#cba6f7",
            fontsize=16,
            fontweight="bold",
            pad=20
        )

        self.fig.tight_layout()
        self.canvas.draw()

    def generar_tabla_armonicos(self):
        if "Caminar" not in self.resultados or "Correr" not in self.resultados:
            messagebox.showerror(
                "Error",
                "Debes cargar ambos archivos CSV para generar la tabla de armónicos."
            )
            return

        self.limpiar_lienzo()

        datos_armonicos = []

        datos_armonicos, columnas = crear_tabla_armonicos(self.resultados)

        ax = self.fig.add_subplot(111)
        ax.set_facecolor("#1e1e2e")
        ax.axis("off")

        tabla = ax.table(
            cellText=datos_armonicos,
            colLabels=columnas,
            cellLoc="center",
            loc="center"
        )

        tabla.auto_set_font_size(False)
        tabla.set_fontsize(8)
        tabla.scale(1.1, 2)

        for key, cell in tabla.get_celld().items():
            cell.set_edgecolor("#45475a")
            cell.set_text_props(color="#cdd6f4")

            if key[0] == 0:
                cell.set_facecolor("#313244")
                cell.set_text_props(weight="bold", color="#f5e0dc")
            else:
                cell.set_facecolor("#1e1e2e")

        ax.set_title(
            "Tabla de Armónicos",
            color="#cba6f7",
            fontsize=16,
            fontweight="bold",
            pad=20
        )

        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardProfesionalCompleto(root)
    root.mainloop()