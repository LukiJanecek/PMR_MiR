import tkinter as tk
from tkinter import Menu
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Visualization")
        
        # Hlavní menu
        menu_bar = Menu(root)
        self.root.config(menu=menu_bar)
        
        data_menu = Menu(menu_bar, tearoff=0)
        menu_items = ["Brakes", "Temp", "Battery", "Current", "Speed"]
        for item in menu_items:
            data_menu.add_command(label=item, command=lambda i=item: self.update_plot(i))
        menu_bar.add_cascade(label="Select Data", menu=data_menu)
        
        # Rámec pro obsah
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Listbox vlevo
        self.listbox = tk.Listbox(main_frame, height=20, width=30)
        self.listbox.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        
        # Graf vpravo
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Inicializace s nějakými daty
        self.data = {item: [random.randint(0, 100) for _ in range(10)] for item in menu_items}
        self.update_plot("Brakes")
        
    def update_plot(self, category):
        """Aktualizuje listbox a graf pro vybranou kategorii."""
        self.listbox.delete(0, tk.END)
        values = self.data[category]
        for val in values:
            self.listbox.insert(tk.END, val)
        
        self.ax.clear()
        self.ax.plot(values, marker='o', linestyle='-')
        self.ax.set_title(category)
        self.ax.set_ylabel("Value")
        self.ax.set_xlabel("Time")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()
