import tkinter as tk
from music21 import stream, note, pitch

class MIDIPartiture:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de partituras musicales")
        self.root.geometry("800x600")
        self.label_pc_set = tk.Label(self.root, text="Clases de altura:")
        self.label_pc_set.pack(padx=10, pady=10)
        self.textbox_pc_set = tk.Text(self.root, width=50, height=1)
        self.textbox_pc_set.pack(padx=10, pady=10)
        self.label_transposicion = tk.Label(self.root, text="Intervalo de transposición:")
        self.label_transposicion.pack(padx=10, pady=10)
        self.textbox_transposicion = tk.Text(self.root, width=10, height=1)
        self.textbox_transposicion.pack(padx=10, pady=10)
        self.label_nombre_partitura = tk.Label(self.root, text="Nombre de la partitura:")
        self.label_nombre_partitura.pack(padx=10, pady=10)
        self.textbox_nombre_partitura = tk.Text(self.root, width=50, height=1)
        self.textbox_nombre_partitura.pack(padx=10, pady=10)
        self.button = tk.Button(self.root, text="Generar partitura", command=self.generar_partitura)
        self.button.pack(padx=10, pady=10)
        self.etiqueta = tk.Label(self.root, text="", wraplength=400)
        self.etiqueta.pack(padx=10, pady=10)
        self.textbox_pc_set.focus_set()  # Establece el foco en el primer campo de texto
        self.root.bind("<Tab>", self.cambiar_foco)  # Asigna la tecla Tab para cambiar el foco

    def cambiar_foco(self, event):
        widget_actual = self.root.focus_get()
        if widget_actual == self.textbox_pc_set:
            self.textbox_transposicion.focus_set()
        elif widget_actual == self.textbox_transposicion:
            self.textbox_nombre_partitura.focus_set()
        elif widget_actual == self.textbox_nombre_partitura:
            self.button.focus_set()

    def generar_partitura(self):
        texto_pc_set = self.textbox_pc_set.get("1.0", tk.END)
        texto_transposicion = self.textbox_transposicion.get("1.0", tk.END)
        texto_nombre_partitura = self.textbox_nombre_partitura.get("1.0", tk.END)
        try:
            pc_set = [int(x) for x in texto_pc_set.split(",")]
            intervalo_transposicion = int(texto_transposicion)
            nombre_partitura = texto_nombre_partitura.strip()
            if not nombre_partitura:
                raise ValueError("Nombre de la partitura no puede estar vacío")
            partitura = stream.Stream()
            for pc in pc_set:
                nota = note.Note(pitch.Pitch(pc))
                partitura.append(nota)
            partitura_transpuesta = partitura.transpose(intervalo_transposicion)
            partitura.append(partitura_transpuesta)
            partitura.write('midi', fp=f"{nombre_partitura}.mid")
            self.etiqueta.config(text=f"Partitura '{nombre_partitura}' generada correctamente")
            self.limpiar_campos()
        except ValueError as e:
            self.etiqueta.config(text=f"Error: {e}")

    def limpiar_campos(self):
        self.textbox_pc_set.delete("1.0", tk.END)
        self.textbox_transposicion.delete("1.0", tk.END)
        self.textbox_nombre_partitura.delete("1.0", tk.END)
        self.textbox_pc_set.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = MIDIPartiture(root)
    root.mainloop()