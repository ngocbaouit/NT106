import pygame, sys, random

screen_width = 1280
screen_height = 800

initial_ball_speed = 6  # Reset the ball speed
# Store the original size of the bars
original_bar_height = 100
player = pygame.Rect(50, screen_height // 2, 10, original_bar_height)
cpu = pygame.Rect(screen_width - 50, screen_height // 2, 10, original_bar_height)

# Store the original size of the ball
original_ball_size = 20
ball = pygame.Rect(screen_width // 2 - 10, screen_height // 2 - 10, original_ball_size, original_ball_size)

item4_hit = False
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = screen_width/2 - 10
    ball.y = random.randint(10,100)
    ball_speed_x = initial_ball_speed  # Reset the ball speed
    ball_speed_y = initial_ball_speed  # Reset the ball speed
    ball_speed_x *= random.choice([-1,1])
    ball_speed_y *= random.choice([-1,1])

def point_won(winner):
    global ball_speed_x, ball_speed_y, player_points, cpu_points, item4_hit, ball2_active
    if winner == "player":
        player_points += 2 if item4_hit else 1
        item4_hit = False
    elif winner == "cpu":
        cpu_points += 2 if item4_hit else 1
        item4_hit = False

    ball_speed = initial_ball_speed
    # Reset the bar sizes
    cpu.height = original_bar_height
    player.height = original_bar_height

    # Reset the size of the ball
    ball.width = original_ball_size
    ball.height = original_ball_size
    
    reset_ball()

    # Reset ball2 if it was active
    if ball2_active:
        ball2_active = False

def animate_ball():
    global ball_speed_x, ball_speed_y, ball2_speed_x, ball2_speed_y, ball2_active, cpu_points, player_points
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    if ball.colliderect(item):
        ball_speed_x *= 1.2
        ball_speed_y *= 1.2
        # Move the item to a new random position
        item.x = random.randint(0, screen_width)
        item.y = random.randint(0, screen_height)
    if ball.colliderect(item2):
        ball_speed_x *= 0.8
        ball_speed_y *= 0.8
        item2.x = random.randint(0, screen_width)
        item2.y = random.randint(0, screen_height)
    if ball.colliderect(item3):
        ball_speed_y *= -1
        item3.x = random.randint(0, screen_width)
        item3.y = random.randint(0, screen_height)
    if ball.colliderect(item4):
        item4_hit = True
        item4.x = random.randint(0, screen_width)
        item4.y = random.randint(0, screen_height)
    if ball.colliderect(item5):
        # Increase the length of the player's bar by 1.5 times
        if ball_speed_x > 0:  # Ball is moving to the right, player2's bar increases
            player.height *= 1.5
        else:  # Ball is moving to the left, player1's bar increases
            cpu.height *= 1.5
        item5.x = random.randint(0, screen_width)
        item5.y = random.randint(0, screen_height)
    if ball.colliderect(item6):
        if ball_speed_x > 0:
            cpu.height *= 0.75
        else:
            player.height *= 0.75
        item6.x = random.randint(0, screen_width)
        item6.y = random.randint(0, screen_height)
    if ball.colliderect(item7):
        # Increase the size of the ball by 1.5 times
        ball.width *= 1.5
        ball.height *= 1.5
        item7.x = random.randint(0, screen_width)
        item7.y = random.randint(0, screen_height)
    if ball.colliderect(item8):
        # Decrease the size of the ball by 0.75 times
        ball.width *= 0.75
        ball.height *= 0.75
        item8.x = random.randint(0, screen_width)
        item8.y = random.randint(0, screen_height)
    if ball.colliderect(item9):
        game_over = True
        if player_points > cpu_points:
            win_surface = score_font.render("You win!", True, "white")
        elif cpu_points > player_points:
            win_surface = score_font.render("You win!", True, "white")
        else:
            win_surface = score_font.render("Its a tie!", True, "white")
        screen.blit(win_surface, (screen_width/2, screen_height/2))
        pygame.display.update()
        pygame.time.wait(6000)
        pygame.quit()
        sys.exit()
    if ball.colliderect(item10):
        # Create a second ball
        ball2.x = random.randint(0, screen_width)
        ball2.y = random.randint(0, screen_height)
        ball2_speed_x = 6
        ball2_speed_y = 6
        ball2_speed_x *= random.choice([-1, 1])
        ball2_speed_y *= random.choice([-1, 1])
        ball2_active = True
        item10.x = random.randint(0, screen_width)
        item10.y = random.randint(0, screen_height)

    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1
    if ball.right >= screen_width:
        point_won("cpu")
    if ball.left <= 0:
        point_won("player")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    if ball.colliderect(cpu) or ball.colliderect(player):
        ball_speed_x *= -1

    if ball2_active:
        ball2.x += ball2_speed_x
        ball2.y += ball2_speed_y
        
        if ball2.colliderect(item):
            ball2_speed_x *= 1.2
            ball2_speed_y *= 1.2
            item.x = random.randint(0, screen_width)
            item.y = random.randint(0, screen_height)
        if ball2.colliderect(item2):
            ball2_speed_x *= 0.8
            ball2_speed_y *= 0.8
            item2.x = random.randint(0, screen_width)
            item2.y = random.randint(0, screen_height)
        if ball2.colliderect(item3):
            ball2_speed_y *= -1
            item3.x = random.randint(0, screen_width)
            item3.y = random.randint(0, screen_height)
        if ball2.colliderect(item4):
            item4_hit = True
            item4.x = random.randint(0, screen_width)
            item4.y = random.randint(0, screen_height)
        if ball2.colliderect(item5):
            if ball2_speed_x > 0:
                player.height *= 1.5
            else:
                cpu.height *= 1.5
            item5.x = random.randint(0, screen_width)
            item5.y = random.randint(0, screen_height)
        if ball2.colliderect(item6):
            if ball2_speed_x > 0:
                cpu.height *= 0.75
            else:
                player.height *= 0.75
            item6.x = random.randint(0, screen_width)
            item6.y = random.randint(0, screen_height)
        if ball2.colliderect(item7):
            ball2.width *= 1.5
            ball2.height *= 1.5
            item7.x = random.randint(0, screen_width)
            item7.y = random.randint(0, screen_height)
        if ball2.colliderect(item8):
            ball2.width *= 0.75
            ball2.height *= 0.75
            item8.x = random.randint(0, screen_width)
            item8.y = random.randint(0, screen_height)
        if ball2.colliderect(item9):
            game_over = True
            if player_points > cpu_points:
                win_surface = score_font.render("You win!", True, "white")
            elif cpu_points > player_points:
                win_surface = score_font.render("You win!", True, "white")
            else:
                win_surface = score_font.render("Its a tie!", True, "white")
            screen.blit(win_surface, (screen_width/2, screen_height/2))
            pygame.display.update()
            pygame.time.wait(6000)
            pygame.quit()
            sys.exit()
        if ball2.colliderect(item10):
            ball2.x = random.randint(0, screen_width)
            ball2.y = random.randint(0, screen_height)
            ball2_speed_x = 6
            ball2_speed_y = 6
            ball2_speed_x *= random.choice([-1, 1])
            ball2_speed_y *= random.choice([-1, 1])
            item10.x = random.randint(0, screen_width)
            item10.y = random.randint(0, screen_height)

        if ball2.bottom >= screen_height or ball2.top <= 0:
            ball2_speed_y *= -1
        if ball2.right >= screen_width:
            point_won("cpu")
        if ball2.left <= 0:
            point_won("player")
        if ball2.colliderect(cpu) or ball2.colliderect(player):
            ball2_speed_x *= -1


def animate_player():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0

    if player.bottom >= screen_height:
        player.bottom = screen_height

def animate_cpu():
    global cpu_speed
    cpu.y += cpu_speed

    if ball.centery <= cpu.centery:
        cpu_speed = -6
    if ball.centery >= cpu.centery:
        cpu_speed = 6

    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height

pygame.mixer.init()

pygame.init()

clock = pygame.time.Clock()

screen_width = 1280
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Pong Game!")

clock = pygame.time.Clock()

ball = pygame.Rect(0,0,30,30)
ball.center = (screen_width/2, screen_height/2)

cpu = pygame.Rect(0,0,20,100)
cpu.centery = screen_height/2

player = pygame.Rect(0,0,20,100)
player.midright = (screen_width, screen_height/2)

ball_speed_x = 6
ball_speed_y = 6
player_speed = 0
cpu_speed = 6

cpu_points, player_points = 0, 0

score_font = pygame.font.Font(None, 100)

#Load background
background_image = pygame.image.load('img/background1.jpg').convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load the item image
item_image = pygame.image.load('img/tangtoc.png')
item_image = pygame.transform.scale(item_image, (30, 30)).convert_alpha()

# Create the item
item = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 30, 30)

# Load the second item image
item2_image = pygame.image.load('img/giamtoc.png')
item2_image = pygame.transform.scale(item2_image, (30, 30)).convert_alpha()

# Create the second item
item2 = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 30, 30)

# Load the third item image
item3_image = pygame.image.load('img/doihuong.png')
item3_image = pygame.transform.scale(item3_image, (30, 30)).convert_alpha()

# Create the third item
item3 = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 30, 30)

# Load the fourth item image
item4_image = pygame.image.load('img/x2diem.png')
item4_image = pygame.transform.scale(item4_image, (30, 30)).convert_alpha()

# Create the fourth item
item4 = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 30, 30)

# Load the fifth item image
item5_image = pygame.image.load('img/biggerbar.png')
item5_image = pygame.transform.scale(item5_image, (30, 30)).convert_alpha()

# Create the fifth item
item5 = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 30, 30)

# Load the sixth item image
item6_image = pygame.image.load('img/smallerbar.png')
item6_image = pygame.transform.scale(item6_image, (30, 30)).convert_alpha()

# Create the sixth item
item6 = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 30, 30)

# Load the seventh item image
item7_image = pygame.image.load('img/upsizeball.png')
item7_image = pygame.transform.scale(item7_image, (30, 30)).convert_alpha()

# Create the seventh item
item7 = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 30, 30)

# Load the eighth item image
item8_image = pygame.image.load('img/downsizeball.png')
item8_image = pygame.transform.scale(item8_image, (30, 30)).convert_alpha()

# Create the eighth item
item8 = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 30, 30)

# Load the nineth item image
item9_image = pygame.image.load('img/exit.png')
item9_image = pygame.transform.scale(item9_image, (30, 30)).convert_alpha()

# Create the nineth item
item9 = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 30, 30)

# Load the tenth item image
item10_image = pygame.image.load('img/plusball.png')
item10_image = pygame.transform.scale(item10_image, (30, 30)).convert_alpha()

# Create the tenth item
item10 = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 30, 30)

#Load and play backkground music:
pygame.mixer.music.load('sounds/background_music.mp3')
pygame.mixer.music.play(-1)  # The -1 makes the music loop indefinitely

# Define ball2 and ball2_active before the game loop
ball2 = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 30, 30)
ball2_active = False
ball2_speed_x = 6
ball2_speed_y = 6

start_time = pygame.time.get_ticks()
game_over = False

while not game_over:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -6
            if event.key == pygame.K_DOWN:
                player_speed = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed = 0
            if event.key == pygame.K_DOWN:
                player_speed = 0

    # Check if 60 seconds have passed to end the game
    current_time = pygame.time.get_ticks()
    if (current_time - start_time) > 60000:
        game_over = True
        if player_points > cpu_points:
            win_surface = score_font.render("You win!", True, "white")
            screen.blit(win_surface, (screen_width/2, screen_height/2))
            pygame.display.update()
            pygame.time.wait(6000)
            break
        elif cpu_points > player_points:
            win_surface = score_font.render("You win!", True, "white")
            screen.blit(win_surface, (screen_width/4, screen_height/2))
            pygame.display.update()
            pygame.time.wait(6000)
            break
        else:  # In case of a tie
            win_surface = score_font.render("It's a tie!", True, "white")
            screen.blit(win_surface, (screen_width/2 - win_surface.get_width()/2, screen_height/2))
            pygame.display.update()
            pygame.time.wait(6000)
            break
    # game_over = False
    # if game_over:
    #     pygame.mixer.music.stop()

    # #Check if a player has reached 10 points
    # if player_points >= 10:
    #     win_surface = score_font.render("You win!", True, "white")
    #     screen.blit(win_surface, (screen_width/2, screen_height/2))
    #     pygame.display.update()
    #     pygame.time.wait(6000)
    #     break
    # elif cpu_points >= 10:
    #     win_surface = score_font.render("You win!", True, "white")
    #     screen.blit(win_surface, (screen_width/4, screen_height/2))
    #     pygame.display.update()
    #     pygame.time.wait(6000)
    #     break
    
    #Change the positions of the game objects
    animate_ball()
    animate_player()
    animate_cpu()

    #Clear the screen
    screen.fill('black')

    # Draw the background image
    screen.blit(background_image, (0, 0))

    #Draw the score
    cpu_score_surface = score_font.render(str(cpu_points), True, "white")
    player_score_surface = score_font.render(str(player_points), True, "white")
    screen.blit(cpu_score_surface,(screen_width/4,20))
    screen.blit(player_score_surface,(3*screen_width/4,20))


    remaining_time = 60 - (current_time - start_time) / 1000
    time_text = f"{int(remaining_time)}"
    time_surface = score_font.render(time_text, True, (255, 255, 255))
    time_x = screen_width / 2 - time_surface.get_width() / 2
    time_y = 20
    screen.blit(time_surface, (time_x, time_y))

    #Draw the game objects
    pygame.draw.aaline(screen,'white',(screen_width/2, 0), (screen_width/2, screen_height))
    pygame.draw.ellipse(screen,'white',ball)

    if ball2_active:
        pygame.draw.ellipse(screen, 'white', ball2)
    pygame.draw.rect(screen,'white',cpu)
    pygame.draw.rect(screen,'white',player)

    # Draw the item
    screen.blit(item_image, item)
    
    # Draw the second item
    screen.blit(item2_image, item2)

    # Draw the third item
    screen.blit(item3_image, item3)
    
    # Draw the fourth item
    screen.blit(item4_image, item4)

    # Draw the fifth item
    screen.blit(item5_image, item5)

    # Draw the sixth item
    screen.blit(item6_image, item6)

    # Draw the seventh item
    screen.blit(item7_image, item7)

    # Draw the eighth item
    screen.blit(item8_image, item8)

    # Draw the nineth item
    screen.blit(item9_image, item9)

    # Draw the tenth item
    screen.blit(item10_image, item10)

    # Update the display
    pygame.display.flip()

    #Update the display
    pygame.display.update()
    clock.tick(60)
