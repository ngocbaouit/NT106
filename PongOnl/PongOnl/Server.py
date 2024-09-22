import socket
import threading
import pickle
import random
import pygame

# Server settings
HOST = 'localhost'  # Or your server IP address
PORT = 5555

# Game state
player_positions = [150, 150]  # Initial positions for two players
ball_position = [340, 200]     # Initial ball position
ball_speed = [2, 2]
player_scores = [0, 0]         # Player scores
item_positions = [[random.randint(0, 650), random.randint(0, 370)] for _ in range(8)]

# Initialize ball size and active status for second ball
ball_size = [10, 10]
ball2_active = False
ball2_position = [0, 0]
ball2_speed = [0, 0]

# Lock for synchronizing access to game state
game_state_lock = threading.Lock()

# Function to handle client connections
def handle_client(conn, player_id):
    global player_positions
    global ball_position
    global ball_speed
    global player_scores
    global item_positions
    global ball_size
    global ball2_active
    global ball2_position
    global ball2_speed
    
    try:
        initial_data = pickle.dumps((player_id, ball_position, player_positions, player_scores, item_positions, ball_size, ball2_active, ball2_position, ball2_speed))
        conn.send(initial_data)
        print(f"Sent initial data to player {player_id}: {initial_data}")
    except Exception as e:
        print(f"Error sending initial data to player {player_id}: {e}")
        conn.close()
        return
    
    while True:
        try:
            data = pickle.loads(conn.recv(1024))
            if not data:
                break
            player_positions[player_id] = data['position']
            
            with game_state_lock:
                # Update ball position only on the server side
                ball_position[0] += ball_speed[0]
                ball_position[1] += ball_speed[1]
                
                if ball2_active:
                    ball2_position[0] += ball2_speed[0]
                    ball2_position[1] += ball2_speed[1]

                # Simple collision with walls
                if ball_position[1] <= 0 or ball_position[1] >= 390:
                    ball_speed[1] = -ball_speed[1]
                if ball_position[0] <= 0:
                    player_scores[1] += 1
                    ball_position = [340, 200]
                if ball_position[0] >= 670:
                    player_scores[0] += 1
                    ball_position = [340, 200]

                if ball2_active:
                    if ball2_position[1] <= 0 or ball2_position[1] >= 390:
                        ball2_speed[1] = -ball2_speed[1]
                    if ball2_position[0] <= 0:
                        player_scores[1] += 1
                        ball2_active = False
                    if ball2_position[0] >= 670:
                        player_scores[0] += 1
                        ball2_active = False

                # Handle ball and paddle collisions
                if ball_position[0] <= 35 and player_positions[0] < ball_position[1] < player_positions[0] + 50:
                    ball_speed[0] = -ball_speed[0]
                if ball_position[0] >= 635 and player_positions[1] < ball_position[1] < player_positions[1] + 50:
                    ball_speed[0] = -ball_speed[0]

                if ball2_active:
                    if ball2_position[0] <= 35 and player_positions[0] < ball2_position[1] < player_positions[0] + 50:
                        ball2_speed[0] = -ball2_speed[0]
                    if ball2_position[0] >= 635 and player_positions[1] < ball2_position[1] < player_positions[1] + 50:
                        ball2_speed[0] = -ball2_speed[0]

                # Handle item collisions
                for i, pos in enumerate(item_positions):
                    item_rect = pygame.Rect(pos[0], pos[1], 30, 30)
                    ball_rect = pygame.Rect(ball_position[0], ball_position[1], ball_size[0], ball_size[1])
                    if ball_rect.colliderect(item_rect):
                        if i == 0:
                            ball_speed[0] *= 1.2
                            ball_speed[1] *= 1.2
                        elif i == 1:
                            ball_speed[0] *= 0.8
                            ball_speed[1] *= 0.8
                        elif i == 2:
                            ball_speed[1] = -ball_speed[1]
                        elif i == 3:
                            if ball_speed[0] > 0:
                                player_positions[1] = min(player_positions[1] + 25, 350)
                            else:
                                player_positions[0] = min(player_positions[0] + 25, 350)
                        elif i == 4:
                            if ball_speed[0] > 0:
                                player_positions[0] = max(player_positions[0] - 25, 50)
                            else:
                                player_positions[1] = max(player_positions[1] - 25, 50)
                        elif i == 5:
                            ball_size[0] = min(ball_size[0] * 1.5, 30)
                            ball_size[1] = min(ball_size[1] * 1.5, 30)
                        elif i == 6:
                            ball_size[0] = max(ball_size[0] * 0.75, 10)
                            ball_size[1] = max(ball_size[1] * 0.75, 10)
                        elif i == 7:
                            if not ball2_active:
                                ball2_position = ball_position.copy()
                                ball2_speed = [-ball_speed[0], ball_speed[1]]
                                ball2_active = True
                        # Move the item to a new random position
                        item_positions[i] = [random.randint(0, 650), random.randint(0, 370)]

            game_state = (ball_position, player_positions, player_scores, item_positions, ball_size, ball2_active, ball2_position, ball2_speed)
            conn.sendall(pickle.dumps(game_state))
        except Exception as e:
            print(f"Error during game loop for player {player_id}: {e}")
            break
    
    conn.close()

# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)  # We expect two players
    
    print("Server started. Waiting for connections...")
    
    player_id = 0
    while player_id < 2:
        conn, addr = server.accept()
        print(f"Player {player_id} connected from {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, player_id))
        thread.start()
        player_id += 1
    
    server.close()

if __name__ == "__main__":
    main()
