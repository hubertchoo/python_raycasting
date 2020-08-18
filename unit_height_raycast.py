import pygame
import time
from pygame.locals import *
import math

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier", 16)

# Floor plan for map
# Each element in the map takes up a 1x1 grid space
floor_plan =  [
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 3, 2, 3, 0, 0, 2],
            [2, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 3, 1, 0, 0, 2, 0, 0, 0, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 2, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 3, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 2, 3, 2, 1, 2, 0, 1],
            [1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 2],
            [2, 3, 1, 0, 0, 2, 0, 0, 2, 1, 3, 2, 0, 2, 0, 0, 3, 0, 3, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 2, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 3, 0, 1, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 3, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1],
            [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],]

# Each element in the map takes up a 1x1 grid space
floor_plan = [list(x) for x in zip(*floor_plan)]


####------Colours------####
BLACK     = (  0,   0,   0)
BLUE      = (  0,   0, 150)
BROWN     = (139,  69,  19)
CYAN      = (  0, 255, 255)
DARKBLUE  = (  0,   0,  64)
DARKBROWN = ( 36,  18,   5)
DARKGREEN = (  0,  64,   0)
DARKGREY  = ( 64,  64,  64)
DARKRED   = ( 64,   0,   0)
GREY      = (128, 128, 128)
GREEN     = (  0, 150,   0)
LIME      = (  0, 255,   0)
MAGENTA   = (255,   0, 255)
MAROON    = (128,   0,   0)
NAVYBLUE  = (  0,   0, 128)
OLIVE     = (128, 128,   0)
PURPLE    = (128,   0, 128)
RED       = (150,   0,   0)
SILVER    = (192, 192, 192)
TEAL      = (  0, 128, 128)
WHITE     = (255, 255, 255)
YELLOW    = (255, 255,   0)
####-------------------####

def main():
    # Display Settings
    showShadows = True
    mapMode     = False     # Toggle map mode using 'm' key
    textureMode = True      # Toggle between texture for walls or color blocks
    textureFile = 'texture_assets/blood_wall.bmp'

    # Importing texture for walls
    texture    = pygame.image.load(textureFile)
    tex_height = texture.get_height()
    tex_width  = texture.get_width()

    # For selecting wallcolors that correspond to floor plan above
    # Values in floor_plan corresponds to index of color in wallcolors
    wallcolors = [ [], RED, BLUE, GREEN, SILVER]

    # Initial Player State
    position         = [7.5, 7]      # x, y coordinates
    FOV              = 60.0          # Field of View in degrees
    direction        = 335.0         # Direction player is facing. 90 deg refers to North
    collision_radius = 0.2           # Radius of player, such that player is not a point
    projection_level = 0             # Level of view. 0 means that player eye level is at mid of wall.
                                     # Positive is upwards of wall, negative is downwards
    crouch = False

    # Create Window
    WIDTH  = 1000
    HEIGHT = 800
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Python Raycaster (Unit Height)")

    # Run until the user asks to quit
    running = True

    # Dictionary to check if a particular key is KEYDOWN at a moment in time
    # necessary to allow pressing of multiple keys at the same time
    keys = {}

    while running:
        
        while direction > 360:
            direction -= 360
        while direction < 0:
            direction += 360

        for event in pygame.event.get():
            # Window close button
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                # Escape button triggers quitting of program
                if event.key == K_ESCAPE:
                    running = False
                # 'm' key toggles mapMode
                elif event.key == K_m:
                    mapMode = not mapMode
                # 'c' key triggers crouch and uncrouch
                elif event.key == K_c:
                    if crouch == False:
                        crouch = True
                        projection_level -= 60
                    else:
                        crouch = False
                        projection_level += 60
                else:
                    keys[event.key] = True

            if event.type == KEYUP:
                keys[event.key] = False
                keys.pop(event.key, None)

        def move(direction, forward):
            # Direction refers to angle player is facing, 90 deg being North
            # forward is a boolean. True refers to movement forward, False refers to movement backwards
            units_per_move = 0.03 # Speed of movement
            if crouch:
                units_per_move = 0.020 # Move slower when crouched
            quadrant = direction // 90
            # collision box is the x and y margin to simulate player collision radius
            if quadrant == 0:
                y_change = -math.sin(direction/180 * math.pi) * units_per_move
                x_change = -math.cos(direction/180 * math.pi) * units_per_move
                collision_box = (-collision_radius, -collision_radius)
            elif quadrant == 1:
                basic_angle = 180 - direction
                y_change = -math.sin(basic_angle/180 * math.pi) * units_per_move
                x_change = math.cos(basic_angle/180 * math.pi) * units_per_move
                collision_box = (collision_radius, -collision_radius)
            elif quadrant == 2:
                basic_angle = direction - 180
                y_change = math.sin(basic_angle/180 * math.pi) * units_per_move
                x_change = math.cos(basic_angle/180 * math.pi) * units_per_move
                collision_box = (collision_radius, collision_radius)
            elif quadrant == 3:
                basic_angle = 360 - direction
                y_change = math.sin(basic_angle/180 * math.pi) * units_per_move
                x_change = -math.cos(basic_angle/180 * math.pi) * units_per_move
                collision_box = (-collision_radius, collision_radius)
            else:
                x_change, y_change = 0, 0
                collision_box = (0, 0)
            if not forward:
                x_change, y_change = -x_change, -y_change
                collision_box = (-collision_box[0], -collision_box[1])

            # Check individually if x and y axis movement have wall collision
            # This will allow sliding across one axis when other is blocked
            movement = [0, 0]
            future_x = position[0] + x_change + collision_box[0]
            future_y = position[1] + y_change
            if floor_plan[int(future_x)][int(future_y)] == 0:
                movement[0] = x_change
            future_x = position[0] + x_change
            future_y = position[1] + y_change + collision_box[1]
            if floor_plan[int(future_x)][int(future_y)] == 0:
                movement[1] = y_change
            
            return movement
                
        x_change = 0
        y_change = 0
        
        # Limit fps to maximum of 60fps
        dt = clock.tick(60)
        # Adjust move speed to be the same regardless of FPS
        x_change *= dt/16.66
        y_change *= dt/16.66

        for key in keys:
            if key == K_w:     # Move forwardd
                x_change, y_change = move(direction, True)
                position[0] += x_change
                position[1] += y_change
            
            elif key == K_s:  # Move backwards
                x_change, y_change = move(direction, False)
                position[0] += x_change
                position[1] += y_change
                
            elif key == K_a:  # Turn left
                # Adjust rotation speed to be the same regardless of FPS
                direction -= 1/16.66*dt

            elif key == K_d: # Turn right
                direction += 1/16.66*dt
            
            elif key == K_UP:     # Look up
                # Looking up and down is an illusion.
                # No change to actual angle of elevation of view. Images are only moved up or down.
                projection_level -= 10
                # Set maximum upwards angle
                projection_level = max(projection_level, -1400)
            
            elif key == K_DOWN:     # Look down
                projection_level += 10
                # Set maximum downwards angle
                projection_level = min(projection_level, 1400)
                
        if mapMode:
            height_grids = len(floor_plan[0])
            width_grids = len(floor_plan)
            # Draw grid lines
            screen.fill((255, 255, 255))
            for i in range(height_grids):
                row = HEIGHT/height_grids*i
                pygame.draw.line(screen, (128, 128, 128), (0, row), (WIDTH, row))
            for i in range(width_grids):
                col = WIDTH/width_grids*i
                pygame.draw.line(screen, (128, 128, 128), (col, 0), (col, HEIGHT))

            if not textureMode:
            # Color grid squares with their wallcolors
                for i in range(width_grids):
                    for j in range(height_grids):
                        if floor_plan[i][j] != 0:
                            color = wallcolors[floor_plan[i][j]]
                            #draw vertically
                            pygame.draw.line(screen, color, ((i+0.5)*WIDTH/width_grids, j*HEIGHT/height_grids), ((i+0.5)*WIDTH/width_grids, (j+1)*HEIGHT/height_grids), WIDTH//width_grids)
                        
            else:
                for i in range(width_grids):
                    for j in range(height_grids):
                        if floor_plan[i][j] != 0:
                            # Color grid squares with their textures
                            a = texture.subsurface(0, 0, tex_width, tex_height) # x, y, width, height
                            a = a.copy()
                            a = pygame.transform.scale(a, (int(WIDTH/width_grids), int(HEIGHT/height_grids)))
                            screen.blit(a, (i*WIDTH/width_grids, j*HEIGHT/height_grids))

        # Fill floor color
        if not mapMode:
            screen.fill((50,50,50))

        color = wallcolors[1]

        column = 0 # Number of rays casted

        # Cast rays from left to right
        while column < WIDTH:

            left_limit = direction - FOV/2
            if left_limit > 360:
                left_limit = left_limit - 360
            elif left_limit < 0:
                left_limit = left_limit + 360

            increment = FOV/WIDTH
            curr_angle = left_limit + increment * column
            
            
            if curr_angle > 360:
                curr_angle -= 360
            elif curr_angle < 0:
                curr_angle += 360

            beta = abs(direction - curr_angle)/180 * math.pi # Used to remove fisheye distortion later on

            # Get the basic angle

            # First quadrant
            # i_dir and j_dir refers to the row and column index change direction for a ray of the particular quadrant
            i_dir = -1
            j_dir = -1
            # second quadrant
            if 90 <= curr_angle < 180: 
                curr_angle = 180 - curr_angle
                i_dir = -1
                j_dir = 1
            # third quadrant
            elif 180 <= curr_angle < 270:
                curr_angle = curr_angle - 180
                i_dir = 1
                j_dir = 1
            # fourth quadrant
            elif 270 <= curr_angle < 360:
                curr_angle = 360 - curr_angle
                i_dir = 1
                j_dir = -1
            
            curr_angle_radian = curr_angle/180 * math.pi # in radians
            tangent = math.tan(curr_angle_radian + 0.00000000000000001)
            cosine = math.cos(curr_angle_radian + 0.000000000000000001)

            shortest_distance = 999
            shortest_spot = None
            
            # Find first intersection with a vertical grid line
            if j_dir == -1:
                delta_x = position[0] - int(position[0]) 
            else:
                delta_x = int(position[0] + 1) - position[0]
            delta_y = delta_x * tangent * i_dir
            # vert_intersection refers to point of intersection of ray with vertical grid line
            vert_intersection = [None, position[1] + delta_y]
            if j_dir == -1:
                vert_intersection[0] = int(position[0])
            else:
                vert_intersection[0] = int(position[0]) +1
            
            hit_wall = False # First instance of ray hitting wall

            # (grid_x, grid_y) is the grid being checked for wall
            grid_x = vert_intersection[0]
            if j_dir == -1:
                grid_x -= 1
            grid_y = vert_intersection[1]
            
            # While ray has not hit any wall and is still in bounds of floor plan
            while not hit_wall and 0 <= int(grid_x) < len(floor_plan) and 0 <= int(grid_y) < len(floor_plan[0]):
                # check if that grid square is a wall
                if floor_plan[int(grid_x)][int(grid_y)] != 0:
                    hit_wall = True
                    distance = abs(vert_intersection[0] - position[0])/ cosine
                    if distance < shortest_distance and distance != 0:
                        shortest_distance = distance
                        color = wallcolors[floor_plan[int(grid_x)][int(grid_y)]]
                        shortest_spot = vert_intersection
                        tex_x = int(tex_width*(vert_intersection[1]%1))
                        dim = False
                else:
                    # Go on to the next vertical intersection
                    vert_intersection[0] = vert_intersection[0] + j_dir
                    delta_y = tangent * i_dir
                    vert_intersection[1] = vert_intersection[1] + delta_y

                    # Calculate the grid to be checked
                    grid_x = vert_intersection[0]
                    if j_dir == -1:
                        grid_x -= 1
                    grid_y = vert_intersection[1]

            
            # Find first intersection with a horizontal grid line
            if i_dir == -1:
                delta_y = position[1] - int(position[1]) 
            else:
                delta_y = int(position[1] + 1) - position[1]
            delta_x = delta_y / tangent * j_dir

            # hor_intersection is the point of intersection, not the same as the grid being checked
            hor_intersection = [position[0] + delta_x, None]
            if i_dir == -1:
                hor_intersection[1] = int(position[1])
            else:
                hor_intersection[1] = int(position[1] +1)

            hit_wall = False
            # Calculate the grid to be checked
            grid_x = hor_intersection[0]
            grid_y = hor_intersection[1]
            if i_dir == -1:
                grid_y -= 1

            # while ray has not hit any wall and is still in bounds of floor plan
            while not hit_wall and 0 <= int(grid_x) < len(floor_plan) and 0 <= int(grid_y) < len(floor_plan[0]):
                # Check if that grid square is a wall
                if floor_plan[int(grid_x)][int(grid_y)] != 0:
                    hit_wall = True
                    distance = abs(hor_intersection[0] - position[0])/ cosine
                    if distance < shortest_distance and distance != 0:
                        shortest_distance = distance
                        color = wallcolors[floor_plan[int(grid_x)][int(grid_y)]]
                        shortest_spot = hor_intersection
                        tex_x = int(tex_width*(hor_intersection[0]%1))
                        dim = True
                else:
                    # Go on to the next horizontal intersection
                    hor_intersection[1] = hor_intersection[1] + i_dir
                    delta_y = 1/tangent * j_dir
                    hor_intersection[0] = hor_intersection[0] + delta_y

                    # Calculate the grid to be checked
                    grid_x = hor_intersection[0]
                    grid_y = hor_intersection[1]
                    if i_dir == -1:
                        grid_y -= 1
            
            # Showing rays in mapMode
            if (column % 5 == 0) and shortest_spot != None and mapMode:
                height_grids = len(floor_plan[0])
                width_grids = len(floor_plan)
                pygame.draw.line(screen, (0,0,0), (position[0]* WIDTH/width_grids, position[1]* HEIGHT/height_grids), (shortest_spot[0]* WIDTH/width_grids, shortest_spot[1]* HEIGHT/height_grids))
            
            # Creating of walls
            
            if not mapMode:
                if shortest_spot != None:
                    slice_height = HEIGHT/(shortest_distance* math.cos(beta))
                    draw_y = [None, None] # Start and end y coordinates of line
                    draw_y[0] = HEIGHT/2.0 - slice_height/2.0 - projection_level
                    draw_y[1] = HEIGHT/2.0 + slice_height/2.0 + projection_level
                    if not textureMode:
                        draw_y[0] = max(0, draw_y[0])
                        draw_y[1] = min(HEIGHT, draw_y[1])

                if textureMode:
                    if crouch:
                        draw_y[0] = HEIGHT/2.0 - slice_height/2.0 - projection_level - 120
                        
                    # Crops the appropriate column of texture
                    a = texture.subsurface(tex_x, 0, 1, tex_height) # x, y, width, height
                    # Scales column of texture according to distance
                    # However, when player is very near to wall, image is scaled to infinity
                    # and causes lag
                    a = a.copy()
                    a = pygame.transform.scale(a, (2, int(slice_height)))
                    if dim and showShadows:
                        a.fill((160, 160, 160, 0), special_flags=BLEND_MULT)
                    screen.blit(a, (column, draw_y[0]))
                else:
                    if dim and showShadows:
                        temp = []
                        for i in color:
                            temp.append(i//1.15) # Alter color code to dim color
                        color = temp
                    pygame.draw.line(screen, color, (column, draw_y[0]), (column, draw_y[1]), 2) # 2 refers to thickness of line
            
            if not mapMode:
                pygame.draw.line(screen, (25, 25, 25), (column, 0), (column, draw_y[0]), 2)
            
            column += 2
        fps_text = font.render('FPS: ' + str(int(clock.get_fps())), True, WHITE)
        screen.blit(fps_text, (10,10))

        # Flip the display
        pygame.display.flip()

        
    pygame.quit()

main()
                
            
