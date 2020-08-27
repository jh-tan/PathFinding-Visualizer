import pygame
import time
import math
import random
from queue import PriorityQueue,Queue

SIZE = width, height = 800, 800
WIDTH = 800
WIN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("PathFinding Visualization")

BLUE = (34, 123, 255)
LIGHTBLUE = (135, 204, 255)
RED = (255, 0, 0)
YELLOW = (255, 214, 98)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
TURQUOISE = (175, 237, 255)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neightbors = []
        self.width = width
        self.total_rows = total_rows
        self.visited= False
    
    def set_visited(self):
        self.visited = True

    def get_visited(self):
        return False

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == BLUE

    def is_open(self):
        return self.color == LIGHTBLUE

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == GREEN

    def is_end(self):
        return self.color == RED

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = BLUE

    def make_open(self):
        self.color = LIGHTBLUE

    def make_start(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = RED

    def make_path(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neightbors = []

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
            self.neightbors.append(grid[self.row - 1][self.col])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN
            self.neightbors.append(grid[self.row + 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
            self.neightbors.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #RIGHT
            self.neightbors.append(grid[self.row][self.col + 1])
        


        # IF DIAGONAL IS ALLOW
        # if self.row <self.total_rows -1 and self.col>0 and not grid[self.row+1][self.col-1].is_barrier(): #DIAG-LEFT-DOWN
        #     self.neightbors.append(grid[self.row+1][self.col-1])

        # if self.row <self.total_rows -1 and self.col<self.total_rows-1 and not grid[self.row+1][self.col+1].is_barrier(): #DIAG-RIGHT-DOWN
        #     self.neightbors.append(grid[self.row+1][self.col+1])

        # if self.row >0 and self.col>0 and not grid[self.row-1][self.col-1].is_barrier(): #DIAG-LEFT-UP
        #     self.neightbors.append(grid[self.row-1][self.col-1])

        # if self.row >0 and self.col<self.total_rows-1 and not grid[self.row-1][self.col+1].is_barrier(): #DIAG-RIGHT-UP
        #     self.neightbors.append(grid[self.row-1][self.col+1])

    def __lt__(self, other):
        return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def clear_path(grid):
    for i in grid:
        for j in i:
            if j.color != WHITE and j.color != BLACK:
                j.reset()
            else:
                continue
    
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0, i * gap),(width, i * gap))

    for i in range(rows):
        pygame.draw.line(win,GREY,(i * gap, 0),(i * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    #Draw grid line
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width //rows
    y,x = pos

    row = y // gap
    col = x // gap
    
    return row, col

def reconstruct_path(came_from,start, current, draw):
    while current in came_from:
        current = came_from[current]
        if current == start:
            break
        current.make_path()
        draw()

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def generate_obstacle(draw,grid,ROWS):
    for x in range(750):
        r=random.randint(0,ROWS-1)
        c=random.randint(0,ROWS-1)
        grid[r][c].make_barrier()

def algorithm(draw, grid, start, end):
    #count is used if there are two node with same F value, then the later one will be used
    count = 0
    open_set = PriorityQueue()
    #(F-value, count, node)
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start]=0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(),end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end :
            reconstruct_path(came_from,start,end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neightbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        # time.sleep(0.5)
        draw()

        if current != start:
            current.make_closed()
    
    return False

def bfs(draw,grid,start,end):
    visited = [start]
    cell = [start]
    came_from = {}
    while cell:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = cell.pop(0) 

        if current == end:
            reconstruct_path(came_from,start,end, draw)
            end.make_end()
            return True

        for neighbors in current.neightbors:
            if neighbors not in visited:
                came_from[neighbors] = current
                visited.append(neighbors)
                cell.append(neighbors)
                neighbors.make_open()
            
            # if neighbors == end:
            #     reconstruct_path(came_from,start,end, draw)
            #     end.make_end()
            #     return True

        draw()
        # time.sleep(0.5)
        if current != start:
            current.make_closed()

    return False

def dijkstra(draw, grid, start, end):
    frontier = PriorityQueue()
    frontier.put((0,start))
    came_from = {}
    cost = {}
    cost[start] = 0


    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = frontier.get()[1]

        if current == end:
            reconstruct_path(came_from, start, end, draw)
            end.make_end()
            return True

        for neighbour in current.neightbors:
            new_cost = cost[current] + 1
            if neighbour not in cost or new_cost < cost[neighbour]:
                cost[neighbour] = new_cost
                frontier.put((new_cost,neighbour))
                neighbour.make_open()
                came_from[neighbour] = current
        draw()
        if current != start:
            current.make_closed()
    
    return False


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot!=end and not spot.is_barrier():
                    start = spot
                    start.make_start()
                
                elif not end and spot!=start and not spot.is_barrier():
                    end = spot
                    end.make_end()

                elif spot !=end and spot!= start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                
                elif spot == end:
                    end = None

            # Start visualize
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win,grid,ROWS,width),grid, start,end)
                
                if event.key == pygame.K_2 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_3 and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # Reset board and clear everything
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                
                # Clear everything except obstacle
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = clear_path(grid)

                # Randomly generate obstacle
                if event.key == pygame.K_g:
                    grid=make_grid(ROWS,width)
                    start = None
                    end = None
                    generate_obstacle(lambda:draw(win,grid,ROWS,width),grid,ROWS)

    pygame.quit()

main(WIN,WIDTH)
