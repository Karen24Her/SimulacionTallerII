
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import math
import time

class ParabolicMotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Movimiento Parabólico")
        
        self.create_widgets()
        
    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(frame, text="Posición Inicial X0:").grid(row=0, column=0)
        self.x0_entry = tk.Entry(frame)
        self.x0_entry.grid(row=0, column=1)
        
        tk.Label(frame, text="Altura Inicial Y0:").grid(row=1, column=0)
        self.y0_entry = tk.Entry(frame)
        self.y0_entry.grid(row=1, column=1)
        
        tk.Label(frame, text="Magnitud Velocidad Inicial:").grid(row=2, column=0)
        self.v0_entry = tk.Entry(frame)
        self.v0_entry.grid(row=2, column=1)
        
        tk.Label(frame, text="Ángulo Velocidad Inicial:").grid(row=3, column=0)
        self.angle_entry = tk.Entry(frame)
        self.angle_entry.grid(row=3, column=1)
        
        tk.Label(frame, text="Gravedad:").grid(row=4, column=0)
        self.gravity_entry = tk.Entry(frame)
        self.gravity_entry.insert(0, "9.81")
        self.gravity_entry.grid(row=4, column=1)
        
        tk.Label(frame, text="Intervalo Efecto del Viento T':").grid(row=5, column=0)
        self.wind_interval_entry = tk.Entry(frame)
        self.wind_interval_entry.insert(0, "0.1")
        self.wind_interval_entry.grid(row=5, column=1)
        
        self.start_button = tk.Button(frame, text="Start", command=self.start_simulation)
        self.start_button.grid(row=6, columnspan=2)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_tabs()
        
    def create_tabs(self):
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)
        self.tab3 = tk.Frame(self.notebook)
        
        self.notebook.add(self.tab1, text="Simulación")
        self.notebook.add(self.tab2, text="Resultados")
        self.notebook.add(self.tab3, text="Animación")
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.tab1)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.results_table = ttk.Treeview(self.tab2, columns=("Rebote", "Tiempo de Vuelo", "Máxima Altura", "Desplazamiento"), show="headings")
        self.results_table.heading("Rebote", text="Rebote")
        self.results_table.heading("Tiempo de Vuelo", text="Tiempo de Vuelo")
        self.results_table.heading("Máxima Altura", text="Máxima Altura")
        self.results_table.heading("Desplazamiento", text="Desplazamiento")
        self.results_table.pack(fill=tk.BOTH, expand=True)

        self.animation_canvas = tk.Canvas(self.tab3, width=800, height=600, bg="white")
        self.animation_canvas.pack(fill=tk.BOTH, expand=True)
        
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
                if len(flight_times) >= 2:
                    break
            
            positions.append((x, y))
        
        total_flight_time = sum(flight_times)
        total_max_height = max(max_heights)
        total_displacement = sum(displacements)
        
        self.ax.clear()
        self.ax.plot([p[0] for p in positions], [p[1] for p in positions], marker='o')
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title("Trayectoria de Movimiento Parabólico")
        self.canvas.draw()
        
        # Limpiar la tabla antes de insertar nuevos resultados
        for i in self.results_table.get_children():
            self.results_table.delete(i)
        
        for i, (time, height, displacement) in enumerate(zip(flight_times, max_heights, displacements), 1):
            self.results_table.insert("", "end", values=(i, time, height, displacement))
        
        # Insertar los totales en la tabla
        self.results_table.insert("", "end", values=("Total", total_flight_time, total_max_height, total_displacement))
        
        self.animate_trajectory(positions)
        
        messagebox.showinfo("Simulación Completa", "La simulación ha finalizado.")
    
    def animate_trajectory(self, positions):
        self.animation_canvas.delete("all")
        bunny = self.animation_canvas.create_oval(0, 0, 20, 20, fill="grey")
        
        # Ajustar la escala de la animación al tamaño del canvas
        max_x = max(p[0] for p in positions)
        max_y = max(p[1] for p in positions)
        
        scale_x = 800 / max_x
        scale_y = 600 / max_y
        
        for x, y in positions:
            scaled_x = x * scale_x
            scaled_y = 600 - (y * scale_y)  # Invertir el eje Y para que la animación sea correcta
            self.animation_canvas.coords(bunny, scaled_x, scaled_y, scaled_x + 20, scaled_y + 20)
            self.root.update()
            time.sleep(0.05)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParabolicMotionApp(root)
    root.mainloop()
