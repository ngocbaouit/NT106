import pygame
import sys
import socket
import pickle

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 680
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Multiplayer Pong Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Player rectangles
player_width = 10
player1 = pygame.Rect(25, screen_height // 2 - 25, player_width, 50)
player2 = pygame.Rect(screen_width - 25 - player_width, screen_height // 2 - 25, player_width, 50)

# Ball rectangle
ball = pygame.Rect(screen_width // 2 - 5, screen_height // 2 - 5, 10, 10)

# Second ball rectangle
ball2 = pygame.Rect(0, 0, 10, 10)
ball2_active = False

# Scores
player1_score = 0
player2_score = 0

# Load background
background_image = pygame.image.load('img/background1.jpg').convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Network settings
HOST = 'localhost'  # Server IP address
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except Exception as e:
    print(f"Unable to connect to the server: {e}")
    pygame.quit()
    sys.exit()

# Receive initial game state from server
try:
    data = client.recv(1024)
    if not data:
        raise Exception("No data received from server")
    data = pickle.loads(data)
    player_id, ball_position, player_positions, player_heights, player_scores, item_positions, ball_size, ball2_active, ball2_position, ball2_speed, game_over, winner = data
    ball.x, ball.y = ball_position
    ball.width, ball.height = ball_size
    if ball2_active:
        ball2.x, ball2.y = ball2_position
        ball2.width, ball2.height = ball_size
    player1.y, player2.y = player_positions
    player1.height, player2.height = player_heights
    player1_score, player2_score = player_scores
except Exception as e:
    print(f"Error receiving initial data from server: {e}")
    client.close()
    pygame.quit()
    sys.exit()

# Define item rectangles
items = [pygame.Rect(pos[0], pos[1], 30, 30) for pos in item_positions]

# Load item images
item_images = [
    pygame.image.load('img/tangtoc.png').convert_alpha(),
    pygame.image.load('img/giamtoc.png').convert_alpha(),
    pygame.image.load('img/doihuong.png').convert_alpha(),
    pygame.image.load('img/x2diem.png').convert_alpha(),
    pygame.image.load('img/smallerbar.png').convert_alpha(),
    pygame.image.load('img/upsizeball.png').convert_alpha(),
    pygame.image.load('img/downsizeball.png').convert_alpha(),
    pygame.image.load('img/plusball.png').convert_alpha(),
    pygame.image.load('img/exit.png').convert_alpha(),
]
item_images = [pygame.transform.scale(img, (30, 30)) for img in item_images]

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            client.close()
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if player_id == 0:  # Controls for player 1
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= 6
        if keys[pygame.K_s] and player1.bottom < screen_height:
            player1.y += 6
    else:  # Controls for player 2
        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= 6
        if keys[pygame.K_DOWN] and player2.bottom < screen_height:
            player2.y += 6

    # Send the new position to the server
    try:
        player_positions[player_id] = player1.y if player_id == 0 else player2.y
        client.send(pickle.dumps({'position': player_positions[player_id]}))

        # Receive updated game state from server
        data = client.recv(1024)
        if not data:
            raise Exception("No data received from server")
        data = pickle.loads(data)
        ball_position, player_positions, player_heights, player_scores, item_positions, ball_size, ball2_active, ball2_position, ball2_speed, game_over, winner = data
        ball.x, ball.y = ball_position
        ball.width, ball.height = ball_size
        if ball2_active:
            ball2.x, ball2.y = ball2_position
            ball2.width, ball2.height = ball_size
        player1.y, player2.y = player_positions
        player1.height, player2.height = player_heights
        player1_score, player2_score = player_scores

        # Update item positions
        for i, pos in enumerate(item_positions):
            items[i].x, items[i].y = pos

        if game_over:
            win_text = "Player 1 wins!" if winner == 0 else "Player 2 wins!"
            win_surface = pygame.font.Font(None, 74).render(win_text, True, white)
            screen.blit(win_surface, (screen_width / 2 - win_surface.get_width() // 2, screen_height / 2))
            pygame.display.update()
            pygame.time.wait(6000)
            running = False
    except (ConnectionResetError, Exception) as e:
        print(f"Connection error: {e}")
        client.close()
        pygame.quit()
        sys.exit()

    # Drawing everything on the screen
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, white, player1)
    pygame.draw.rect(screen, white, player2)
    pygame.draw.ellipse(screen, white, ball)
    if ball2_active:
        pygame.draw.ellipse(screen, white, ball2)
    pygame.draw.aaline(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height))

    # Draw items
    for item, img in zip(items, item_images):
        screen.blit(img, item)

    # Display scores
    font = pygame.font.Font(None, 74)
    score_text = font.render(f"{player1_score}  {player2_score}", True, white)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 10))

    pygame.display.flip()
    clock.tick(60)
