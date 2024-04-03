import tkinter as tk
import random

class JogoCoelho:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo do Coelho")
        self.master.geometry("400x400")

        self.canvas = tk.Canvas(self.master, bg="white", width=400, height=400)
        self.canvas.pack()

        # Carregar imagem do coelho
        self.coelho_gif = tk.PhotoImage(file="coelho.gif")
        self.coelho = self.canvas.create_image(20, 200, image=self.coelho_gif, anchor=tk.NW)

        self.obstaculos = []
        self.criar_obstaculos()

        # Vincular eventos de teclado
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)

    def criar_obstaculos(self):
        for _ in range(3):
            x = random.randint(100, 350)
            y = random.randint(100, 350)
            obstaculo = self.canvas.create_rectangle(x, y, x+20, y+20, fill="red")
            self.obstaculos.append(obstaculo)

    def move_left(self, event):
        self.canvas.move(self.coelho, -5, 0)

    def move_right(self, event):
        self.canvas.move(self.coelho, 5, 0)

    def move_up(self, event):
        self.canvas.move(self.coelho, 0, -5)

    def move_down(self, event):
        self.canvas.move(self.coelho, 0, 5)

def main():
    root = tk.Tk()
    jogo = JogoCoelho(root)
    root.mainloop()

if __name__ == "__main__":
    main()
