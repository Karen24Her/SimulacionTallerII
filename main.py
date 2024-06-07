import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

class MovimientoParabolicoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movimiento Parabólico")
        self.geometry("800x600")

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))

        self.create_widgets()

        self.viento = {"magnitud": random.randint(0, 20), "angulo": random.randint(0, 360)}

    def create_widgets(self):
        self.create_label_entry("Posición inicial X0:", 0)
        self.create_label_entry("Altura inicial Y0:", 1)
        self.create_label_entry("Magnitud velocidad inicial:", 2)
        self.create_label_entry("Ángulo velocidad inicial:", 3)
        self.create_label_entry("Gravedad:", 4)
        self.create_label_entry("Intervalo efecto del viento (T'):", 5)

        self.start_button = ttk.Button(self, text="Iniciar", command=self.start_simulation)
        self.start_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.canvas = tk.Canvas(self, width=600, height=400, bg="white")
        self.canvas.grid(row=7, column=0, columnspan=2, pady=10)

        self.chart = ttk.Notebook(self)
        self.chart.grid(row=8, column=0, columnspan=2)

        self.chart_frame = ttk.Frame(self.chart)
        self.chart.add(self.chart_frame, text="Gráfico")

        self.table_frame = ttk.Frame(self.chart)
        self.chart.add(self.table_frame, text="Tabla")

        self.reiniciar_button = ttk.Button(self, text="Reiniciar", command=self.reiniciar)
        self.reiniciar_button.grid(row=9, column=0, columnspan=2, pady=10)

    def create_label_entry(self, text, row):
        label = ttk.Label(self, text=text)
        label.grid(row=row, column=0, sticky="e", padx=10, pady=5)
        entry = ttk.Entry(self)
        entry.grid(row=row, column=1, padx=10, pady=5)
        setattr(self, f'entry_{row}', entry)

    def start_simulation(self):
        try:
            if any(not entry.get() for entry in [self.entry_0, self.entry_1, self.entry_2, self.entry_3, self.entry_4, self.entry_5]):
                raise ValueError("Todos los campos deben ser llenados.")

            self.x0 = float(self.entry_0.get())
            self.y0 = float(self.entry_1.get())
            self.v0 = float(self.entry_2.get())
            self.angle = math.radians(float(self.entry_3.get()))
            self.gravity = float(self.entry_4.get())
            self.interval = float(self.entry_5.get())

            self.time = 0
            self.x_values = []
            self.y_values = []

            self.max_height_total = 0
            self.displacement_total = 0
            self.tiempo_vuelo_total = 0

            self.simulate_step()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def simulate_step(self):
        if self.y0 >= 0:
            x = self.x0 + self.v0 * math.cos(self.angle) * self.time + self.viento["magnitud"] * math.cos(math.radians(self.viento["angulo"])) * self.time
            y = self.y0 + self.v0 * math.sin(self.angle) * self.time - 0.5 * self.gravity * self.time ** 2

            if y > self.max_height_total:
                self.max_height_total = y

            if y < 0:
                y = 0

            self.x_values.append(x)
            self.y_values.append(400 - y)

            if len(self.x_values) > 1:
                self.canvas.create_line(self.x_values[-2], self.y_values[-2], self.x_values[-1], self.y_values[-1], fill="blue")

            self.time += 0.1

            self.after(10, self.simulate_step)  # Llama a simulate_step cada 10ms para evitar el bloqueo de la interfaz
        else:
            self.update_table()

    def update_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.table_frame, text="Tiempo de vuelo total:").grid(row=0, column=0)
        ttk.Label(self.table_frame, text=f"{round(self.time, 2)} s").grid(row=0, column=1)

        ttk.Label(self.table_frame, text="Máxima altura total:").grid(row=1, column=0)
        ttk.Label(self.table_frame, text=f"{round(self.max_height_total, 2)} m").grid(row=1, column=1)

        displacement_total = self.x_values[-1] if self.x_values else 0
        ttk.Label(self.table_frame, text="Desplazamiento total:").grid(row=2, column=0)
        ttk.Label(self.table_frame, text=f"{round(displacement_total, 2)} m").grid(row=2, column=1)

    def reiniciar(self):
        self.canvas.delete("all")
        self.chart.select(self.chart_frame)
        self.viento = {"magnitud": random.randint(0, 20), "angulo": random.randint(0, 360)}

if __name__ == "__main__":
    app = MovimientoParabolicoApp()
    app.mainloop()
