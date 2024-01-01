# Paint Challenge V1.0
# Copyright (C) 2024, Sourceduty - All Rights Reserved.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from fpdf import FPDF
import challenge_generator

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Painting Challenge App")
        self.current_file = None

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.pen_color = "black"
        self.pen_size = 2
        self.drawing = False

        # Create a menu bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Create File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_canvas)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_command(label="Export Image as PDF", command=self.export_as_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        # Create a frame for the "Generate Challenge" button on the left side
        challenge_frame = ttk.Frame(root)
        challenge_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a button to generate a drawing challenge
        self.generate_challenge_button = ttk.Button(challenge_frame, text="Generate Challenge", command=self.generate_challenge)
        self.generate_challenge_button.pack()

        # Create a label frame for the challenge text
        challenge_label_frame = ttk.LabelFrame(root, text="Challenge", padding=(10, 5))
        challenge_label_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Create a label to display the challenge
        self.challenge_label = ttk.Label(challenge_label_frame, text="", anchor=tk.W)
        self.challenge_label.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.pen_color, width=self.pen_size)
            self.last_x = x
            self.last_y = y

    def stop_drawing(self, event):
        self.drawing = False

    def new_canvas(self):
        self.canvas.delete("all")
        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.canvas.delete("all")
                for line in file:
                    coords = [int(coord) for coord in line.strip().split()]
                    self.canvas.create_line(*coords)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                for item in self.canvas.find_all():
                    coords = self.canvas.coords(item)
                    file.write(" ".join(map(str, coords)) + "\n")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                for item in self.canvas.find_all():
                    coords = self.canvas.coords(item)
                    file.write(" ".join(map(str, coords)) + "\n")
            self.current_file = file_path

    def export_as_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")])
        if file_path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_xy(0, 0)
            pdf.image("canvas.png", x=0, y=0, w=210)
            pdf.output(file_path)

    def generate_challenge(self):
        # Use the submodule to generate a new challenge
        challenge = challenge_generator.generate_challenge()

        # Display the generated challenge
        challenge_text = f"   ● {challenge}   "
        self.challenge_label.config(text=challenge_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
