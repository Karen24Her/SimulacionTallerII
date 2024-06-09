import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import math
import time

class ParabolicMotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Movimiento Parabólico")

        # Configurar la ventana para pantalla completa
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.exit_fullscreen)

        self.style = ttk.Style()
        self.style.theme_use("classic")

        # Estilos personalizados
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))
        self.style.configure('TButton', background='#005f5f', foreground='white', font=('Arial', 12, 'bold'))
        self.style.map('TButton', background=[('active', '#007f7f')])
        self.style.configure('Treeview', font=('Arial', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Arial', 12, 'bold'), background='#007f7f', foreground='white')
        self.style.map('Treeview.Heading', background=[('active', '#005f5f')])

        # Estilos para las pestañas del Notebook
        self.style.configure('TNotebook.Tab', font=('Arial', 12, 'bold'), padding=[10, 5], background='#005f5f', foreground='white')
        self.style.map('TNotebook.Tab', background=[('selected', '#007f7f')], foreground=[('selected', 'white')])

        self.create_widgets()

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(side=tk.LEFT, padx=10, pady=10)

        ttk.Label(frame, text="Posición Inicial X0:").grid(row=0, column=0, pady=5)
        self.x0_entry = ttk.Entry(frame)
        self.x0_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Altura Inicial Y0:").grid(row=1, column=0, pady=5)
        self.y0_entry = ttk.Entry(frame)
        self.y0_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Magnitud Velocidad Inicial:").grid(row=2, column=0, pady=5)
        self.v0_entry = ttk.Entry(frame)
        self.v0_entry.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Ángulo Velocidad Inicial:").grid(row=3, column=0, pady=5)
        self.angle_entry = ttk.Entry(frame)
        self.angle_entry.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="Gravedad:").grid(row=4, column=0, pady=5)
        self.gravity_entry = ttk.Entry(frame)
        self.gravity_entry.insert(0, "9.81")
        self.gravity_entry.grid(row=4, column=1, pady=5)

        ttk.Label(frame, text="Intervalo Efecto del Viento T':").grid(row=5, column=0, pady=5)
        self.wind_interval_entry = ttk.Entry(frame)
        self.wind_interval_entry.insert(0, "0.1")
        self.wind_interval_entry.grid(row=5, column=1, pady=5)

        self.start_button = ttk.Button(frame, text="Start", command=self.start_simulation)
        self.start_button.grid(row=6, columnspan=2, pady=10)

        self.reset_button = ttk.Button(frame, text="Reiniciar", command=self.reset_simulation)
        self.reset_button.grid(row=7, columnspan=2, pady=10)

        self.exit_button = ttk.Button(frame, text="Salir", command=self.root.quit)
        self.exit_button.grid(row=8, columnspan=2, pady=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Etiqueta con los nombres
        self.names_label = ttk.Label(frame, text="Karen Julieth Hernandez Chaparro\nDeisy Carolina Monroy Gutierrez", font=('Arial', 12, 'bold'))
        self.names_label.grid(row=9, columnspan=2, pady=10)

        self.create_tabs()

    def create_tabs(self):
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab3, text="Animación")
        self.notebook.add(self.tab1, text="Trayectoria")
        self.notebook.add(self.tab2, text="Resultados")

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.tab1)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.results_table = ttk.Treeview(self.tab2,
                                          columns=("Rebote", "Tiempo de Vuelo", "Máxima Altura", "Desplazamiento"),
                                          show="headings")
        self.results_table.heading("Rebote", text="Rebote")
        self.results_table.heading("Tiempo de Vuelo", text="Tiempo de Vuelo")
        self.results_table.heading("Máxima Altura", text="Máxima Altura")
        self.results_table.heading("Desplazamiento", text="Desplazamiento")
        self.results_table.pack(fill=tk.BOTH, expand=True)

        self.animation_canvas = tk.Canvas(self.tab3, width=800, height=600, bg="white")
        self.animation_canvas.pack(fill=tk.BOTH, expand=True)

        self.trajectory_label = tk.Label(self.animation_canvas, text="", font=('Arial', 14), bg="white")
        self.trajectory_label.pack(side=tk.TOP, pady=10)

        # Cargar y redimensionar la imagen del conejo
        self.bunny_image = Image.open("conejo.png")
        self.bunny_image = self.bunny_image.resize((100, 100), Image.Resampling.LANCZOS)
        self.bunny_photo = ImageTk.PhotoImage(self.bunny_image)

        # Cargar y redimensionar la imagen de fondo
        self.bg_image = Image.open("fondo.jpg")
        self.bg_image = self.bg_image.resize((1010, 750), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Cargar y redimensionar la imagen de la casa
        self.house_image = Image.open("casa.png")
        self.house_image = self.house_image.resize((50, 100), Image.Resampling.LANCZOS)
        self.house_photo = ImageTk.PhotoImage(self.house_image)

        # Crear recuadro para las anotaciones
        self.annotation_frame = ttk.LabelFrame(self.tab1, text="Anotaciones")
        self.annotation_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Crear tabla de anotaciones
        self.annotation_table = ttk.Treeview(self.annotation_frame, columns=("Tipo", "Detalle"), show="headings")
        self.annotation_table.heading("Tipo", text="Tipo")
        self.annotation_table.heading("Detalle", text="Detalle")
        self.annotation_table.column("Tipo", width=100, anchor=tk.CENTER)
        self.annotation_table.column("Detalle", width=300, anchor=tk.W)

        # Crear scrollbar para la tabla de anotaciones
        self.scrollbar = ttk.Scrollbar(self.annotation_frame, orient="vertical", command=self.annotation_table.yview)
        self.annotation_table.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.annotation_table.pack(fill=tk.BOTH, expand=True)

    def start_simulation(self):
        try:
            x0 = float(self.x0_entry.get())
            y0 = float(self.y0_entry.get())
            v0 = float(self.v0_entry.get())
            angle = float(self.angle_entry.get())
            g = float(self.gravity_entry.get())
            wind_interval = float(self.wind_interval_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")
            return

        vx0 = v0 * math.cos(math.radians(angle))
        vy0 = v0 * math.sin(math.radians(angle))

        t = 0
        x = x0
        y = y0
        vx = vx0
        vy = vy0

        wind_speed = random.uniform(0, 20)
        wind_angle = random.uniform(0, 360)
        wind_vx = wind_speed * math.cos(math.radians(wind_angle))
        wind_vy = wind_speed * math.sin(math.radians(wind_angle))

        positions = [(x, y)]
        flight_times = []
        max_heights = []
        displacements = []

        max_height = y0

        while y >= 0:
            t += wind_interval
            x += vx * wind_interval
            y += vy * wind_interval - 0.5 * g * wind_interval ** 2
            vy -= g * wind_interval

            if y > max_height:
                max_height = y

            if y < 0:  # Rebote
                y = 0
                vy = -vy * 0.5  # Reducción de velocidad después del rebote
                flight_times.append(t)
                max_heights.append(max_height)
                displacements.append(x - x0)
                max_height = y0  # Reiniciar la altura máxima para el siguiente rebote
                if len(flight_times) >= 2:  # Limitar a 5 rebotes para evitar demasiadas iteraciones
                    break

            positions.append((x, y))

        total_flight_time = sum(flight_times)
        total_max_height = max(max_heights)
        total_displacement = sum(displacements)

        self.ax.clear()
        self.ax.plot([p[0] for p in positions], [p[1] for p in positions], marker='o', color='b', linestyle='-',
                     linewidth=2, markersize=6, label="Trayectoria")
        self.ax.set_xlabel("Desplazamiento (X)", fontsize=12)
        self.ax.set_ylabel("Altura (Y)", fontsize=12)
        self.ax.set_title("Trayectoria de Movimiento Parabólico", fontsize=14, fontweight='bold')
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Añadir anotaciones para la altura máxima y los puntos de rebote
        self.annotation_table.delete(*self.annotation_table.get_children())  # Limpiar la tabla de anotaciones
        for i, (x_pos, y_pos) in enumerate(positions):
            if y_pos in max_heights and y_pos > 0:
                annotation_text = f'Máxima Altura en X={x_pos:.2f}: {y_pos:.2f}'
                self.annotation_table.insert("", "end", values=("Altura Máxima", annotation_text))
                self.ax.text(x_pos, y_pos, f'{y_pos:.2f}', fontsize=10, ha='right')

            if y_pos == 0 and x_pos != x0:
                annotation_text = f'Rebote en X={x_pos:.2f}'
                self.annotation_table.insert("", "end", values=("Rebote", annotation_text))
                self.ax.text(x_pos, y_pos, f'{x_pos:.2f}', fontsize=10, ha='right')

        self.ax.legend()
        self.canvas.draw()

        # Limpiar la tabla antes de insertar nuevos resultados
        for i in self.results_table.get_children():
            self.results_table.delete(i)

        for i, (time, height, displacement) in enumerate(zip(flight_times, max_heights, displacements), 1):
            self.results_table.insert("", "end", values=(i, time, height, displacement))

        # Insertar los totales en la tabla
        self.results_table.insert("", "end", values=("Total", total_flight_time, total_max_height, total_displacement))

        self.animate_trajectory(positions, total_displacement)

    def reset_simulation(self):
        # Limpiar las entradas
        self.x0_entry.delete(0, tk.END)
        self.y0_entry.delete(0, tk.END)
        self.v0_entry.delete(0, tk.END)
        self.angle_entry.delete(0, tk.END)
        self.gravity_entry.delete(0, tk.END)
        self.wind_interval_entry.delete(0, tk.END)
        self.gravity_entry.insert(0, "9.81")
        self.wind_interval_entry.insert(0, "0.1")

        # Limpiar la gráfica
        self.ax.clear()
        self.ax.set_xlabel("Desplazamiento (X)", fontsize=12)
        self.ax.set_ylabel("Altura (Y)", fontsize=12)
        self.ax.set_title("Trayectoria de Movimiento Parabólico", fontsize=14, fontweight='bold')
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        self.canvas.draw()

        # Limpiar la tabla de resultados
        for i in self.results_table.get_children():
            self.results_table.delete(i)

        # Limpiar la tabla de anotaciones
        self.annotation_table.delete(*self.annotation_table.get_children())

        # Limpiar la etiqueta de trayectoria
        self.trajectory_label.config(text="")

    def animate_trajectory(self, positions, total_displacement):
        self.animation_canvas.delete("all")

        # Dibujar la imagen de fondo
        self.animation_canvas.create_image(0, 0, image=self.bg_photo, anchor=tk.NW)

        bunny = self.animation_canvas.create_image(0, 0, image=self.bunny_photo, anchor=tk.NW)

        # Ajustar la escala de la animación al tamaño del canvas
        max_x = max(p[0] for p in positions)
        max_y = max(p[1] for p in positions)

        scale_x = 800 / max_x
        scale_y = 600 / max_y

        for x, y in positions:
            scaled_x = x * scale_x
            scaled_y = 600 - (y * scale_y)  # Invertir el eje Y para que la animación sea correcta
            self.animation_canvas.coords(bunny, scaled_x, scaled_y)
            self.root.update()
            time.sleep(0.05)

        # Colocar la imagen de la casa en la posición final del conejito
        final_x, final_y = positions[-1]
        scaled_final_x = final_x * scale_x
        scaled_final_y = 600 - (final_y * scale_y)  # Invertir el eje Y para que la animación sea correcta
        self.animation_canvas.create_image(scaled_final_x, scaled_final_y - 50, image=self.house_photo, anchor=tk.NW)

        # Actualizar la etiqueta de trayectoria con la distancia total recorrida
        self.trajectory_label.config(text=f"El conejito ha recorrido una distancia total de {total_displacement:.2f} unidades.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ParabolicMotionApp(root)
    root.mainloop()
