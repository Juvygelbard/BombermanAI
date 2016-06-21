import tkinter as tk

IMAGE_PATH = 'BombermanAI\\Images\\'
TILE_SIZE = 32
IMG_TABLE = [(0, IMAGE_PATH + 'floor_tile.png'),
             (1,  IMAGE_PATH + 'stone_tile.png'),
             (2,  IMAGE_PATH + 'steel_tile.png'),
             ('X',  IMAGE_PATH + 'bomb.gif'),
			 ('@',  IMAGE_PATH + 'blast.gif'),
             ('A',  IMAGE_PATH + 'bomber1.png'),
             ('B',  IMAGE_PATH + 'bomber2.png'),
             ('C',  IMAGE_PATH + 'bomber3.png'),
             ('D',  IMAGE_PATH + 'bomber4.png'),
             ('E',  IMAGE_PATH + 'bomber5.png')]

class Canvas:
    def __init__(self, master, height, width):
        self.master = master
        self.canvas = tk.Canvas(self.master, height=height*TILE_SIZE, width=width*TILE_SIZE)
        self.canvas.pack()
        self.load_img_board()

    def load_img_board(self):
        self.img_board = {}
        for (n, filename) in IMG_TABLE:
            self.img_board[n] = tk.PhotoImage(file=filename)

    def paint_board(self, board):
        for y in range(len(board)):
            for x in range(len(board[0])):
                self.canvas.create_image((x+0.5)*TILE_SIZE, (y+0.5)*TILE_SIZE, image=self.img_board[board[y][x]])

    def clear_board(self):
        self.canvas.delete("all")
from queue import Queue

class MainFrame:
    def __init__(self, viewer):
        self.viewer = viewer
        self.viewer.map_queue = Queue()
        self.root = tk.Tk()
        self.cnvs = None

        self.root.after(500, self.update_canvas)
        self.root.mainloop()

    def update_canvas(self):
        if not self.viewer.map_queue.empty():
            board = self.viewer.map_queue.get(block=False)

            if self.cnvs==None:
                self.cnvs = Canvas(self.root, len(board), len(board[0]))
            self.cnvs.clear_board()
            self.cnvs.paint_board(board)
        self.root.after(250, self.update_canvas)