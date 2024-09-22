import socket
import threading
import pickle
import random
import pygame
import mysql.connector
from datetime import datetime
import pytz
import uuid

# Server settings
HOST = 'localhost'  # Or your server IP address
PORT = 5555

# MySQL settings
db_config = {
    'user': 'root',
    'password': '07042004',
    'host': 'localhost',
    'database': 'pong',
}

# Game state
player_positions = [150, 150]  # Initial positions for two players
player_heights = [50, 50]      # Initial heights for two players
ball_position = [340, 200]     # Initial ball position
ball_speed = [0.5, 0.5]
player_scores = [0, 0]         # Player scores
item_positions = [[random.randint(0, 650), random.randint(0, 370)] for _ in range(9)]
game_over = False
winner = None

# Initialize ball size and active status for second ball
ball_size = [10, 10]
ball2_active = False
ball2_position = [0, 0]
ball2_speed = [0, 0]

# Lock for synchronizing access to game state
game_state_lock = threading.Lock()

# Function to reset game state
def reset_game_state():
    global ball_position, ball_speed, player_heights, ball_size, ball2_active, ball2_position, ball2_speed
    ball_position = [340, 200]
    ball_speed = [0.5, 0.5]
    player_heights = [50, 50]
    ball_size = [10, 10]
    ball2_active = False
    ball2_position = [0, 0]
    ball2_speed = [0, 0]

# Function to save match data to MySQL
def save_match_to_db(player1_id, player2_id, score1, score2, match_date, winner_name):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        add_match = ("INSERT INTO matches (ID_trận, ID_user1, ID_user2, Điểm_user1, Điểm_user2, Thời_gian, Người_thắng) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        match_id = str(uuid.uuid4())
        match_data = (match_id, player1_id, player2_id, score1, score2, match_date, winner_name)
        cursor.execute(add_match, match_data)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Match data saved to database.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to handle client connections
def handle_client(conn, player_id, player1_id, player2_id):
    global player_positions, player_heights, ball_position, ball_speed, player_scores, item_positions, ball_size, ball2_active, ball2_position, ball2_speed, game_over, winner

    try:
        initial_data = pickle.dumps((player_id, ball_position, player_positions, player_heights, player_scores, item_positions, ball_size, ball2_active, ball2_position, ball2_speed, game_over, winner))
        conn.send(initial_data)
        print(f"Sent initial data to player {player_id}")
    except Exception as e:
        print(f"Error sending initial data to player {player_id}: {e}")
        conn.close()
        return

    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    match_start_date = datetime.now(vn_tz).date()

    while True:
        try:
            data = pickle.loads(conn.recv(1024))
            if not data:
                break
            player_positions[player_id] = data['position']

            with game_state_lock:
                if game_over:
                    conn.sendall(pickle.dumps((ball_position, player_positions, player_heights, player_scores, item_positions, ball_size, ball2_active, ball2_position, ball2_speed, game_over, winner)))
                    break

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
                    reset_game_state()
                if ball_position[0] >= 670:
                    player_scores[0] += 1
                    reset_game_state()

                if ball2_active:
                    if ball2_position[1] <= 0 or ball2_position[1] >= 390:
                        ball2_speed[1] = -ball2_speed[1]
                    if ball2_position[0] <= 0:
                        player_scores[1] += 1
                        ball2_active = False
                        reset_game_state()
                    if ball2_position[0] >= 670:
                        player_scores[0] += 1
                        ball2_active = False
                        reset_game_state()

                # Handle ball and paddle collisions
                if ball_position[0] <= 35 and player_positions[0] < ball_position[1] < player_positions[0] + player_heights[0]:
                    ball_speed[0] = -ball_speed[0]
                if ball_position[0] >= 635 and player_positions[1] < ball_position[1] < player_positions[1] + player_heights[1]:
                    ball_speed[0] = -ball_speed[0]

                if ball2_active:
                    if ball2_position[0] <= 35 and player_positions[0] < ball2_position[1] < player_positions[0] + player_heights[0]:
                        ball2_speed[0] = -ball2_speed[0]
                    if ball2_position[0] >= 635 and player_positions[1] < ball2_position[1] < player_positions[1] + player_heights[1]:
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
                                player_heights[1] = min(player_heights[1] * 1.5, 150)
                            else:
                                player_heights[0] = min(player_heights[0] * 1.5, 150)
                        elif i == 4:
                            if ball_speed[0] > 0:
                                player_heights[0] = max(player_heights[0] * 0.75, 25)
                            else:
                                player_heights[1] = max(player_heights[1] * 0.75, 25)
                        elif i == 5:
                            ball_size[0] = min(ball_size[0] * 1.5, 30)
                            ball_size[1] = min(ball_size[1] * 1.5, 30)
                        elif i == 6:
                            ball_size[0] = max(ball_size[0] * 0.25, 10)
                            ball_size[1] = max(ball_size[1] * 0.25, 10)
                        elif i == 7:
                            if not ball2_active:
                                ball2_position = ball_position.copy()
                                ball2_speed = [-ball_speed[0], ball_speed[1]]
                                ball2_active = True
                        elif i == 8:
                            game_over = True
                            if player_scores[0] > player_scores[1]:
                                winner_name = get_username(player1_id)
                            elif player_scores[1] > player_scores[0]:
                                winner_name = get_username(player2_id)
                            else:
                                winner_name = "Tie"
                            match_end_date = datetime.now(vn_tz).date()
                            match_duration_str = str(match_end_date)
                            save_match_to_db(player1_id, player2_id, player_scores[0], player_scores[1], match_duration_str, winner_name)
                            break  # Exit the loop if the game is over
                            
                        # Move the item to a new random position
                        item_positions[i] = [random.randint(0, 650), random.randint(0, 370)]

                # Check for game over
                if player_scores[0] >= 10:
                    game_over = True
                    winner = 0
                    winner_name = get_username(player1_id)  # Get username from database
                elif player_scores[1] >= 10:
                    game_over = True
                    winner = 1
                    winner_name = get_username(player2_id)  # Get username from database
                else:
                    winner_name = "Tie"

                if game_over:
                    match_end_date = datetime.now(vn_tz).date()
                    match_duration_str = str(match_end_date)
                    save_match_to_db(player1_id, player2_id, player_scores[0], player_scores[1], match_duration_str, winner_name)

            game_state = (ball_position, player_positions, player_heights, player_scores, item_positions, ball_size, ball2_active, ball2_position, ball2_speed, game_over, winner)
            conn.sendall(pickle.dumps(game_state))
        except Exception as e:
            print(f"Error during game loop for player {player_id}: {e}")
            break

    conn.close()

# Function to get username from database
def get_username(user_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = ("SELECT Tên_người_dùng FROM users WHERE ID_user = %s")
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        if result:
            return result[0]
        else:
            return "Unknown"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Unknown"

# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)  # We expect two players

    print("Server started. Waiting for connections...")

    player1_id = 1  # Fetch or assign player 1 ID from your users table
    player2_id = 2  # Fetch or assign player 2 ID from your users table

    player_id = 0
    while player_id < 2:
        conn, addr = server.accept()
        print(f"Player {player_id} connected from {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, player_id, player1_id, player2_id))
        thread.start()
        player_id += 1

    server.close()

if __name__ == "__main__":
    main()
