import pygame
import random
import copy
pygame.init()

width = 800
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")

clock = pygame.time.Clock()
run = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

cols = 100
rows = 100

buffer = 50

grid = []
grid_2 = []

Buttons = []
Cells = []

toggle = True

sim_go = False

box_width = (width - (2 * buffer)) / cols
box_height = (height - (2 * buffer)) / rows


# Function that brightens image by certain amount
def brighten_image(image, brighten):
    image.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
    return image


# Function that darkens image by certain amount
def darken_image(image, darken):
    image.fill((darken, darken, darken), special_flags=pygame.BLEND_RGB_SUB)
    return image


class Cell:
    def __init__(self, num, x, y):
        self.num = num
        self.x = x
        self.y = y
        self.is_hovering = False
        self.is_pressed_down = False
        self.is_pressed_down = False
        self.is_pressed_up = False
        self.rect = (self.x * box_width + buffer, self.y * box_height + (buffer // 2), box_width, box_height)

    def __repr__(self):
        return str(self.num)

    def state_check(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovering:
            self.is_hovering = False

        if self.rect[0] + self.rect[2] > mouse_pos[0] > self.rect[0] and self.rect[1] + self.rect[3] > mouse_pos[
            1] > self.rect[1] and not self.is_hovering:
            self.is_hovering = True

        if self.is_pressed_up:
            if not toggle:
                if self.num == 0:
                    self.num = 1
                else:
                    self.num = 0
            if toggle:
                if grid_2[self.y][self.x].num == 0:
                    grid_2[self.y][self.x].num = 1
                else:
                    grid_2[self.y][self.x].num = 0
            self.is_pressed_up = False


class Button:
    def __init__(self, image, rect, center, button_press_command):
        self.image = pygame.image.load(image)
        self.center = center
        self.rect = pygame.Rect(self.center[0] - (rect[2] // 2), self.center[1] - (rect[3] // 2), rect[2], rect[3])

        # Making a hover over version of itself (lighter and slightly bigger)
        self.image_lighter = self.image.copy()
        self.image_lighter = brighten_image(self.image_lighter, 20)
        self.image_lighter = pygame.transform.scale(self.image_lighter, (int(rect[2] * 1.2), int(rect[3] * 1.2)))

        # Making a press down version of itself (darker)
        self.image_darker = self.image.copy()
        self.image_darker = darken_image(self.image_darker, 50)

        # Start by displaying default version of itself
        self.image_to_display = self.image
        self.is_hovering = False
        self.is_pressed_down = False
        self.is_pressed_up = False
        self.button_press_command = button_press_command
        Buttons.append(self)

    def state_check(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovering:
            self.is_hovering = False

        if self.rect[0] + self.rect[2] > mouse_pos[0] > self.rect[0] and self.rect[1] + self.rect[3] > mouse_pos[
            1] > self.rect[1] and not self.is_hovering:
            self.is_hovering = True

        if self.is_pressed_up:
            self.button_press_command()
            self.is_pressed_up = False

        if self.is_hovering and not self.is_pressed_down:
            self.image_to_display = self.image_lighter
        elif self.is_pressed_down and self.is_hovering:
            self.image_to_display = self.image_darker
        else:
            self.image_to_display = self.image

    def get_center_cor(self):
        if self.is_hovering and not self.is_pressed_down:
            return self.center[0] - ((self.rect[2] * 1.2) // 2), self.center[1] - ((self.rect[3] * 1.2) // 2)
        elif not self.is_hovering or self.is_pressed_down:
            return self.center[0] - (self.rect[2] // 2), self.center[1] - (self.rect[3] // 2)


def create_new_grid():
    global grid_2
    global grid
    grid.clear()
    grid_2.clear()
    for i in range(rows):
        lst = []
        for j in range(cols):
            random_number = random.randint(1, 10)
            if random_number <= 1:
                new_cell = Cell(1, j, i)
                lst.append(new_cell)
                Cells.append(new_cell)
            else:
                new_cell = Cell(0, j, i)
                lst.append(new_cell)
                Cells.append(new_cell)
        grid.append(lst)

    grid_2 = copy.deepcopy(grid)


def check_events():
    global run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Stops Program
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Checks event to object and Changes object state
            for obj in Buttons:
                if obj.is_hovering:
                    obj.is_pressed_down = True
            for obj in Cells:
                if obj.is_hovering:
                    obj.is_pressed_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # Checks event to object and Changes object state
            for obj in Buttons:
                if obj.is_hovering:
                    obj.is_pressed_down = False
                    obj.is_pressed_up = True
            for obj in Cells:
                if obj.is_hovering:
                    obj.is_pressed_down = False
                    obj.is_pressed_up = True

    for obj in Buttons:
        obj.state_check()
    for obj in Cells:
        obj.state_check()


def update_grid():
    global grid
    global grid_2
    global toggle
    print("")
    print("")
    print("")
    if not toggle:
        for row in grid:
            for cell in row:
                neighbour_sum = check_neighbours(cell, grid)
                if cell.num == 1 and neighbour_sum == 2 or neighbour_sum == 3:
                    grid_2[cell.y][cell.x].num = 1
                elif cell.num == 0 and neighbour_sum == 3:
                    grid_2[cell.y][cell.x].num = 1
                else:
                    grid_2[cell.y][cell.x].num = 0
        toggle = True

    elif toggle:
        for row in grid_2:
            for cell in row:
                neighbour_sum = check_neighbours(cell, grid_2)
                if cell.num == 1 and neighbour_sum == 2 or neighbour_sum == 3:
                    grid[cell.y][cell.x].num = 1
                elif cell.num == 0 and neighbour_sum == 3:
                    grid[cell.y][cell.x].num = 1
                else:
                    grid[cell.y][cell.x].num = 0
        toggle = False


def check_neighbours(cell, given_grid):
    global grid
    global grid_2
    neighbour_sum = 0
    x = cell.x
    y = cell.y
    # Top Left
    if x == 0 or y == 0:
        pass
    else:
        if given_grid[y - 1][x - 1].num == 1:
            neighbour_sum += 1

    # Top Middle
    if y == 0:
        pass
    else:
        if given_grid[y - 1][x].num == 1:
            neighbour_sum += 1

    # Top Right
    if y == 0 or x == cols - 1:
        pass
    else:
        if given_grid[y - 1][x + 1].num == 1:
            neighbour_sum += 1

    # Middle Right
    if x == cols - 1:
        pass
    else:
        if given_grid[y][x + 1].num == 1:
            neighbour_sum += 1

    # Bottom Right
    if x == cols - 1 or y == rows - 1:
        pass
    else:
        if given_grid[y + 1][x + 1].num == 1:
            neighbour_sum += 1

    # Bottom Middle
    if y == rows - 1:
        pass
    else:
        if given_grid[y + 1][x].num == 1:
            neighbour_sum += 1

    # Bottom Left
    if y == rows - 1 or x == 0:
        pass
    else:
        if given_grid[y + 1][x - 1].num == 1:
            neighbour_sum += 1

    # Middle Left
    if x == 0:
        pass
    else:
        if given_grid[y][x - 1].num == 1:
            neighbour_sum += 1
    return neighbour_sum


def draw_grid(given_grid):
    global buffer
    global box_width
    global box_height

    for row in given_grid:
        for cell in row:
            cell_rect = (cell.x * box_width + buffer, cell.y * box_height + (buffer // 2), box_width, box_height)
            if cell.num == 0:
                pygame.draw.rect(win, WHITE, cell_rect)
            elif cell.num == 1:
                pygame.draw.rect(win, BLACK, cell_rect)
    for i in range(cols + 1):
        pygame.draw.line(win, BLACK, (i * box_width + buffer, (buffer // 2)), (i * box_width + buffer, height - (buffer // 2) * 3))
    for j in range(rows + 1):
        pygame.draw.line(win, BLACK, (buffer, j * box_height + (buffer // 2)), (height - buffer, j * box_height + (buffer // 2)))


def draw_buttons():
    for button in Buttons:
        win.blit(button.image_to_display, button.get_center_cor())


def draw():
    win.fill(WHITE)
    if sim_go:
        update_grid()
    if toggle:
        draw_grid(grid_2)
    elif not toggle:
        draw_grid(grid)
    draw_buttons()
    pygame.display.update()


def next_frame():
    if not sim_go:
        update_grid()


def stop_frame():
    global sim_go
    sim_go = False


def run_game():
    global sim_go
    sim_go = True


def main():
    create_new_grid()
    while run:
        clock.tick(25)
        check_events()
        draw()
    pygame.quit()


next_button = Button('next_frame_b.png', (0, 0, 130, 35), (width // 5, height - (buffer // 2) * 1.5), next_frame)
stop_button = Button('stop_frame_b.png', (0, 0, 130, 35), ((width // 5) * 2, height - (buffer // 2) * 1.5), stop_frame)
run_button = Button('Run_b.png', (0, 0, 130, 35), ((width // 5) * 3, height - (buffer // 2) * 1.5), run_game)
new_button = Button('new_b.png', (0, 0, 130, 35), ((width // 5) * 4, height - (buffer // 2) * 1.5), create_new_grid)


main()


