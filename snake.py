import random
import pygame
from pygame.constants import K_SPACE
import mysql.connector



pygame.init()
pygame.mixer.init()

screen_width = 600
screen_height = 600

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Next_Coders")


color = (0, 0, 225)
black = (0, 0, 0)
white = (225, 225, 225)
clock = pygame.time.Clock()


def snake_body(window, color, snake_full_body, width, height):
    for x1, y1 in snake_full_body:
        pygame.draw.rect(window, color, [x1, y1, width, height])


bg2 = pygame.image.load("2.png")
bg2 = pygame.transform.scale(
    bg2, (screen_width, screen_height))

outro = pygame.image.load("outro.png")
outro = pygame.transform.scale(
    outro, (screen_width, screen_height))
intro = pygame.image.load("intro.png")
intro = pygame.transform.scale(
    intro, (screen_width, screen_height))


def homepage(user):
    pygame.mixer.music.load("game_intro.mp3")
    pygame.mixer.music.play()
    exit_game = False
    while not exit_game:
        window.blit(intro, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    main(user)

        pygame.display.update()
        clock.tick(55)


def main(user):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="23z7bnn3",
        database="snake_game"
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT score FROM users WHERE username = %s
    ''', (user,))
    result = cursor.fetchone()

    
    if result:
        userHighScore= result[0]  # Returning the score



    x = 45 #?initial x_coordinates
    y = 55 #?initial y_coordinates
    
    width = 20
    height = 20

    vel_x = 0
    vel_y = 0

    food_x = random.randint(100, screen_width-100)
    food_y = random.randint(100, screen_height-110)

    exit_game = True
    game_over = False

    speed = 20

    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    score = 0

    frog_image = pygame.image.load("frog.png")
    frog_image = pygame.transform.scale(frog_image, (30, 30))

    snake_full_body = []
    snake_length = 1

    while exit_game:
        if game_over:
            window.blit(outro, (0, 0))
            textsurface = myfont.render(
                "Game Over ! Press Space to Continue", True, black)
            window.blit(textsurface, [30, 220])
            score_outro = myfont.render("Score :"+str(score), True, black)
            window.blit(score_outro, [230, 280])
            PrevScore_outro = myfont.render("Previous High Score :"+str(userHighScore), True, black)
            window.blit(PrevScore_outro, [150, 350])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    exit_game = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        homepage()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    vel_x = - 10
                    vel_y = 0
                if keys[pygame.K_RIGHT]:
                    vel_x = 10
                    vel_y = 0
                if keys[pygame.K_UP]:
                    vel_y = - 10
                    vel_x = 0
                if keys[pygame.K_DOWN]:
                    vel_y = 10
                    vel_x = 0

            x += vel_x
            y += vel_y

            if(x >= screen_width):
                x = 0
            if(x < 0):
                x = screen_width
            if(y >= screen_height):
                y = 0
            if(y < 0):
                y = screen_height
               

            window.blit(bg2, (0, 0))

            if abs(x-food_x) < 20 and abs(y-food_y) < 20:
                score += 1

                pygame.mixer.music.load("SNAKE FOOD.mp3")
                pygame.mixer.music.play()

                food_x = random.randint(100, screen_width-100)
                food_y = random.randint(100, screen_height-110)

                if(score % 10 == 0) and score > 0:
                    speed += 5

                snake_length += 3

            window.blit(frog_image, (food_x, food_y))

            face = []
            face.append(x)
            face.append(y)
            snake_full_body.append(face)

            if len(snake_full_body) > snake_length:
                del snake_full_body[0]

            if face in snake_full_body[:-1]:
                if(score>userHighScore):
                    cursor.execute('''
                                UPDATE users SET score = %s WHERE username = %s
                        ''', (score, user))
                    conn.commit()
                    conn.close()
                pygame.mixer.music.load("dead_sound.mp3")
                pygame.mixer.music.play()
                game_over = True

            snake_body(window, black, snake_full_body, width, height)

            textsurface = myfont.render(f"{str(score)}", True, (225, 225, 225))
            window.blit(textsurface, [5, 5])
            highScore = myfont.render("HighScore :"+str(userHighScore), True, black)
            window.blit(highScore, [400, 5])

        pygame.display.update()
        clock.tick(speed)

    pygame.quit()
    quit()


# main()
# homepage()



def initialize_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="23z7bnn3",
        database="snake_game"
    )
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255) ,
            score INT DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()
#  authenticate a user
def authenticate_user(username, password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="23z7bnn3",
        database="snake_game"
    )
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM users WHERE username = %s AND password = %s
    ''', (username, password))

    user = cursor.fetchone()

    conn.close()

    return user

#  register a new user
def register_user(username, password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="23z7bnn3",
        database="snake_game"
    )
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        ''', (username, password))
        conn.commit()
        print("User registered successfully!")
        homepage(username)
    except mysql.connector.IntegrityError:
        print("Username already exists! Please choose a different username.")

    conn.close()



initialize_database()

userInput=input("Press S for SignUp or L for LogIn : ")
if(userInput=="S" or userInput=="s"):
    user=input("Enter username : ")
    password=input("Enter password : ")
    register_user(user, password)
    
if(userInput=="l" or userInput=="L"):
    user=input("Enter username : ")
    password=input("Enter password : ")
    authenticated_user = authenticate_user(user, password)
    if authenticated_user:
        print("Authentication successful!")
        homepage(user)
    else:
        print("Invalid username or password!")