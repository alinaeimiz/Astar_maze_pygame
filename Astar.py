import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_mode("A* Path Finding Algorithm")



RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_row):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_row = total_row
        
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WIDTH
    
    def make_start(self):
        self.color = ORANGE
        
    def make_end(self):
        self.color = TURQUOISE
        
    def make_barrier(self):
        self.color = BLACK
    
    def make_open(self):
        self.color = GREEN
    
    def make_closed(self):
        self.color = RED
    
    def make_path(self):
        self.color = PURPLE
        
    def draw(self, win): #draw the block 
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    
    def __lt__(self, other):
        return False


#heuristic function                 
def h(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return abs(x1, x2) + abs(y1, y2)


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
     
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width,i * gap))
        
        for j in range(rows):
            pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    
    for row in grid:
        for node in row:
            Node.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()
    

def get_clicked_pos(pos, rows, width):
    gap = rows // width
    y, x = pos
    
    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    
    start = None
    end = None
    
    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if pygame.mouse.get_passed()[0]:# Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                
                if not start and node != end: #make start point when we haven't start point at first
                    start = node
                    start.make_start()
                    
                if not end and node != start: #make end point when we haven't end point at second click
                    end = node
                    end.make_end()
                
                if node != start and node != end: #make barrier if we are not clicking on the start and end point
                    Node.make_barrier()  
                    
            elif pygame.mouse.get_passed()[2]: #Right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if node == start: #removing start point 
                    start = None
                elif node == end: #removing end pint
                    end = None
                    
            if  event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end: #start using algorithm using SPACE KEY
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)  #finding neighbors node
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                if event.key == pygame.K_c: # reset using C KEY
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()
    
main(WIN, WIDTH)