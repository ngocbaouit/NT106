import pygame
import sys
import socket
import pickle
import random

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

# Game objects
player_width = 10
player_height = 50

# Player rectangles
player1 = pygame.Rect(25, screen_height // 2 - player_height // 2, player_width, player_height)
player2 = pygame.Rect(screen_width - 25 - player_width, screen_height // 2 - player_height // 2, player_width, player_height)

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
client.connect((HOST, PORT))

# Receive initial game state from server
try:
    data = client.recv(1024)
    if not data:
        raise Exception("No data received from server")
    data = pickle.loads(data)
    player_id, ball_position, player_positions, player_scores, item_positions, ball_size, ball2_active, ball2_position, ball2_speed = data
    ball.x, ball.y = ball_position
    ball.width, ball.height = ball_size
    if ball2_active:
        ball2.x, ball2.y = ball2_position
        ball2.width, ball2.height = ball_size
    player1.y, player2.y = player_positions
    player1_score, player2_score = player_scores
except Exception as e:
    print(f"Error receiving initial data from server: {e}")
    client.close()
    pygame.quit()
    sys.exit()

# Define item rectangles
item = pygame.Rect(item_positions[0][0], item_positions[0][1], 30, 30)
item2 = pygame.Rect(item_positions[1][0], item_positions[1][1], 30, 30)
item3 = pygame.Rect(item_positions[2][0], item_positions[2][1], 30, 30)
item5 = pygame.Rect(item_positions[3][0], item_positions[3][1], 30, 30)
item6 = pygame.Rect(item_positions[4][0], item_positions[4][1], 30, 30)
item7 = pygame.Rect(item_positions[5][0], item_positions[5][1], 30, 30)
item8 = pygame.Rect(item_positions[6][0], item_positions[6][1], 30, 30)
item9 = pygame.Rect(item_positions[7][0], item_positions[7][1], 30, 30)

# Load item images
item_images = [
    pygame.image.load('img/tangtoc.jpg').convert_alpha(),
    pygame.image.load('img/giamtoc.jpg').convert_alpha(),
    pygame.image.load('img/doihuong.png').convert_alpha(),
    pygame.image.load('img/x2diem.png').convert_alpha(),
    pygame.image.load('img/smallerbar.png').convert_alpha(),
    pygame.image.load('img/bigball.png').convert_alpha(),
    pygame.image.load('img/smallball.png').convert_alpha(),
    pygame.image.load('img/plusball.png').convert_alpha(),
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
    player_positions[player_id] = player1.y if player_id == 0 else player2.y
    client.send(pickle.dumps({'position': player_positions[player_id]}))

    # Receive updated game state from server
    try:
        data = client.recv(1024)
        if not data:
            raise Exception("No data received from server")
        data = pickle.loads(data)
        ball_position, player_positions, player_scores, item_positions, ball_size, ball2_active, ball2_position, ball2_speed = data
        ball.x, ball.y = ball_position
        ball.width, ball.height = ball_size
        if ball2_active:
            ball2.x, ball2.y = ball2_position
            ball2.width, ball2.height = ball_size
        player1.y, player2.y = player_positions
        player1_score, player2_score = player_scores

        # Update item positions
        item.x, item.y = item_positions[0]
        item2.x, item2.y = item_positions[1]
        item3.x, item3.y = item_positions[2]
        item5.x, item5.y = item_positions[3]
        item6.x, item6.y = item_positions[4]
        item7.x, item7.y = item_positions[5]
        item8.x, item8.y = item_positions[6]
        item9.x, item9.y = item_positions[7]
    except Exception as e:
        print(f"Error receiving game state from server: {e}")
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
    screen.blit(item_images[0], item)
    screen.blit(item_images[1], item2)
    screen.blit(item_images[2], item3)
    screen.blit(item_images[3], item5)
    screen.blit(item_images[4], item6)
    screen.blit(item_images[5], item7)
    screen.blit(item_images[6], item8)
    screen.blit(item_images[7], item9)

    # Display scores
    font = pygame.font.Font(None, 74)
    score_text = font.render(f"{player1_score}  {player2_score}", True, white)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 10))

    pygame.display.flip()
    clock.tick(60)
