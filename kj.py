import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import math


class ParabolicMotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Movimiento Parabólico")

        self.style = ttk.Style()
        self.style.theme_use("clam")  # Puedes probar con 'default', 'clam', 'alt', 'classic'

        # Estilos personalizados
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))
        self.style.configure('TButton', background='#005f5f', foreground='white', font=('Arial', 12, 'bold'))
        self.style.map('TButton', background=[('active', '#007f7f')])
        self.style.configure('Treeview', font=('Arial', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Arial', 12, 'bold'), background='#007f7f', foreground='white')
        self.style.map('Treeview.Heading', background=[('active', '#005f5f')])

        self.create_widgets()

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

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_tabs()

    def create_tabs(self):
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Simulación")
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
                if len(flight_times) >= 2:  # Limitar a 2 rebotes para evitar demasiadas iteraciones
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
        for i, (x_pos, y_pos) in enumerate(positions):
            if y_pos in max_heights and y_pos > 0:
                self.ax.annotate(f'Máxima Altura: {y_pos:.2f}', xy=(x_pos, y_pos), xytext=(x_pos + 0.5, y_pos + 0.5),
                                 arrowprops=dict(facecolor='green', shrink=0.05), fontsize=10)
            if y_pos == 0 and x_pos != x0:
                self.ax.annotate(f'Rebote en X: {x_pos:.2f}', xy=(x_pos, y_pos), xytext=(x_pos + 0.5, y_pos + 0.5),
                                 arrowprops=dict(facecolor='red', shrink=0.05), fontsize=10)

        self.ax.legend()
        self.canvas.draw()

        # Limpiar la tabla antes de insertar nuevos resultados
        for i in self.results_table.get_children():
            self.results_table.delete(i)

        for i, (time, height, displacement) in enumerate(zip(flight_times, max_heights, displacements), 1):
            self.results_table.insert("", "end", values=(i, time, height, displacement))

        # Insertar los totales en la tabla
        self.results_table.insert("", "end", values=("Total", total_flight_time, total_max_height, total_displacement))

        messagebox.showinfo("Simulación Completa", "La simulación ha finalizado.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ParabolicMotionApp(root)
    root.mainloop()
