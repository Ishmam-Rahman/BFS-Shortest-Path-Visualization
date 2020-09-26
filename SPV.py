import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("BFS Shortest Path Visualization")

RED = (235, 56, 255)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (0, 0, 255)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

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

	def up_ok(self, grid):
		return self.row-1>=0 and (grid[self.row-1][self.col].color == WHITE or grid[self.row-1][self.col].color == TURQUOISE)

	def down_ok(self, grid):
		return self.row+1 < self.total_rows and (grid[self.row+1][self.col].color == WHITE or grid[self.row+1][self.col].color == TURQUOISE)

	def right_ok(self, grid):
		return self.col+1 < self.total_rows and (grid[self.row][self.col+1].color == WHITE or grid[self.row][self.col+1].color == TURQUOISE)

	def left_ok(self, grid):
		return self.col-1 >=0 and (grid[self.row][self.col-1].color == WHITE or grid[self.row][self.col-1].color == TURQUOISE)

	def found_end(self, grid):
		return grid[self.row][self.col].color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))




def reconstruct_path(came_from, current, draw, start):
	print('OKKKK')
	while current != start:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):

	open_set = []
	came_from = {}
	open_set.append(start)

	while len(open_set) > 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set[0]

		if current.up_ok( grid):
			Curspot = grid[current.row-1][current.col]
			came_from[Curspot] = current
			if Curspot == end:
				reconstruct_path(came_from, end, draw, start)
				end.make_end()
				start.make_start()
				draw()
				return True
			Curspot.make_open()
			open_set.append(Curspot)
			came_from[Curspot] = current

		if current.down_ok( grid):
			Curspot = grid[current.row+1][current.col]
			came_from[Curspot] = current
			if Curspot == end:
				reconstruct_path(came_from, end, draw, start)
				end.make_end()
				start.make_start()
				draw()
				return True
			Curspot.make_open()
			open_set.append(Curspot)
			came_from[Curspot] = current

		if current.right_ok( grid):
			Curspot = grid[current.row][current.col+1]
			came_from[Curspot] = current

			if Curspot == end:
				reconstruct_path(came_from, end, draw, start)
				end.make_end()
				start.make_start()
				draw()
				return True

			Curspot.make_open()
			open_set.append(Curspot)
			came_from[Curspot] = current

		if current.left_ok( grid):
			Curspot = grid[current.row][current.col-1]
			came_from[Curspot] = current
			if Curspot == end:
				reconstruct_path(came_from, end, draw, start)
				end.make_end()
				start.make_start()
				draw()
				return True
			Curspot.make_open()
			open_set.append(Curspot)
			came_from[Curspot] = current

		draw()

		del open_set[0]
		if current != start:
			current.make_closed()
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


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
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

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)