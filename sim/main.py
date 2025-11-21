import pygame
import sys
from graphslam.graph import Graph
# --- Initialization ---
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
CAPTION = "WASD Ball Controller"

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 69, 0) # Bright red-orange

# Ball properties
BALL_RADIUS = 25
BALL_START_X = SCREEN_WIDTH // 2
BALL_START_Y = SCREEN_HEIGHT // 2
BALL_SPEED = 5

# --- Setup ---
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()

# Ball state (position)
ball_x = BALL_START_X
ball_y = BALL_START_Y

# Movement flags (booleans to track which keys are pressed)
moving_up = False
moving_down = False
moving_left = False
moving_right = False

# --- Game Loop ---
def game_loop():
    global ball_x, ball_y, moving_up, moving_down, moving_left, moving_right
    trajectory = []
    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Key Down Events (Key Pressed)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    moving_up = True
                elif event.key == pygame.K_s:
                    moving_down = True
                elif event.key == pygame.K_a:
                    moving_left = True
                elif event.key == pygame.K_d:
                    moving_right = True

            # Key Up Events (Key Released)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    moving_up = False
                elif event.key == pygame.K_s:
                    moving_down = False
                elif event.key == pygame.K_a:
                    moving_left = False
                elif event.key == pygame.K_d:
                    moving_right = False

        # --- Game State Update (Movement) ---
        
        # Calculate new position based on flags
        if moving_up:
            ball_y -= BALL_SPEED
        if moving_down:
            ball_y += BALL_SPEED
        if moving_left:
            ball_x -= BALL_SPEED
        if moving_right:
            ball_x += BALL_SPEED

        # --- Boundary Checking (Keep the ball on screen) ---
        
        # Horizontal bounds
        if ball_x - BALL_RADIUS < 0:
            ball_x = BALL_RADIUS
        elif ball_x + BALL_RADIUS > SCREEN_WIDTH:
            ball_x = SCREEN_WIDTH - BALL_RADIUS
            
        # Vertical bounds
        if ball_y - BALL_RADIUS < 0:
            ball_y = BALL_RADIUS
        elif ball_y + BALL_RADIUS > SCREEN_HEIGHT:
            ball_y = SCREEN_HEIGHT - BALL_RADIUS

        # --- Drawing ---
        trajectory.append((ball_x, ball_y))
        # Fill the screen with black
        screen.fill(BLACK)
        
        # Draw the ball
        pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), BALL_RADIUS)

        # --- Update Display and Clock ---
        pygame.display.flip()
        
        # Limit frame rate
        clock.tick(60)

    def write_g2o(filename, trajectory):
      with open(filename, "w") as f:
      # Write vertices
        for i, (x, y) in enumerate(trajectory):
          f.write(f"VERTEX_SE2 {i} {x} {y} 0\n")

        # Write edges between consecutive poses
        for i in range(len(trajectory) - 1):
            x1, y1 = trajectory[i]
            x2, y2 = trajectory[i+1]

            dx = x2 - x1
            dy = y2 - y1
            dtheta = 0

            # A simple information matrix (high confidence)
            info = "1000 0 0 1000 0 1000"

            f.write(f"EDGE_SE2 {i} {i+1} {dx} {dy} {dtheta} {info}\n")
    
    write_g2o("trajectory.g2o", trajectory)
    print("Saved trajectory.g2o!")
    
    # --- Quit Pygame ---
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()