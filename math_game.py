import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(" PEMDAS GAME")

icon_image = pygame.image.load("assets/heart.png")
pygame.display.set_icon(icon_image)

# Load background image
background_image = pygame.image.load("assets/background.gif").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load heart image
heart_image = pygame.image.load("assets/heart.png")
heart_image = pygame.transform.scale(heart_image, (30, 30))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)
problem_font = pygame.font.Font(None, 48)  # Larger font for the problem text

# Load sound effects
pygame.mixer.music.load("assets/8bit.mp3")
start_sound = pygame.mixer.Sound("assets/start.mp3")
correct_sound = pygame.mixer.Sound("assets/correct.mp3")
game_over_sound = pygame.mixer.Sound("assets/game_over.mp3")

# Variables
problems = []
for _ in range(5):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    num3 = random.randint(1, 10)
    num4 = random.randint(1, 10)
    num5 = random.randint(1, 10)
    operation1 = random.choice(["+", "-"])
    operation2 = random.choice(["*", "/"])
    operation3 = random.choice(["/", "-"])
    operation4 = random.choice(["*", "+"])
    problem = f"{num1} {operation1} {num2} {operation2} {num3} {operation3} {num4} {operation4} {num5}"
    problems.append(problem)

current_problem_index = 0
user_input = ""
result = None
lives = 3
score = 0

# Additional space below
bottom_space = 50

# Text input field parameters with larger dimensions and additional space below
text_input_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 27 + bottom_space, 300, 54)
border_width = 2
border_color = WHITE



# Cursor parameters
cursor_color = WHITE
cursor_width = 2
cursor_timer = 0
cursor_visible = True

# Button parameters
button_radius = 10
button_margin = 20
start_button_rect = pygame.Rect(screen_width // 2 - 100, 300, 200, 50)
exit_button_rect = pygame.Rect(screen_width // 2 - 100, 400, 200, 50)
retry_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 50)

# Main menu
menu_running = True
pygame.mixer.music.play(-1)  # Play the music on loop
while menu_running:
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    
    # Draw title with glowing effect
    title_text = title_font.render("PEMDAS GAME", True, WHITE)
    title_rect = title_text.get_rect(center=(screen_width // 2, 150))
    for i in range(10, 0, -1):
        text_surface = pygame.Surface(title_rect.size, pygame.SRCALPHA)
        alpha_value = min(255, i * 25)
        text_surface.fill((255, 255, 255, alpha_value))
        text_surface.blit(title_text, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        screen.blit(text_surface, title_rect)
    
    # Draw sub-title
    sub_title_font = pygame.font.Font(None, 30)
    sub_title_text = sub_title_font.render("Develop by: Eunice Jamaica", True, WHITE)
    sub_title_rect = sub_title_text.get_rect(center=(screen_width // 2, 540))
    screen.blit(sub_title_text, sub_title_rect)

    # Draw rounded buttons
    start_button_color = YELLOW if start_button_rect.collidepoint(pygame.mouse.get_pos()) else BLUE
    exit_button_color = YELLOW if exit_button_rect.collidepoint(pygame.mouse.get_pos()) else BLUE
    pygame.draw.rect(screen, start_button_color, start_button_rect, border_radius=button_radius)
    pygame.draw.rect(screen, exit_button_color, exit_button_rect, border_radius=button_radius)

    # Display button text
    start_text = font.render("Start", True, BLACK)
    exit_text = font.render("Exit", True, BLACK)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
    screen.blit(start_text, start_text_rect)
    screen.blit(exit_text, exit_text_rect)
    
    pygame.display.flip()

    # Event handling for main menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mixer.music.stop()  # Stop the background music
                start_sound.play()  # Play start sound
                pygame.time.delay(1000)  # Delay to allow sound to play
                pygame.mixer.music.play(-1)  # Play the music again from the beginning
                menu_running = False
            elif exit_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()

# Game loop
running = True
game_over = False  # Variable to track whether the game is over
start_time = pygame.time.get_ticks()  # Start the timer when the game loop begins
cursor_blink_time = 500  # Blink interval in milliseconds
last_blink_time = 0  # Time of the last cursor blink
cursor_visible = True  # Initially visible

while running:
    # Blit background image
    screen.blit(background_image, (0, 0))

    if not game_over:
        # Display lives
        for i in range(lives):
            screen.blit(heart_image, (screen_width - 40 - i * 40, 10))

        if lives > 0:  # If the user still has lives, continue the game
            # Display current problem
            problem_text = problem_font.render(f"Problem {current_problem_index + 1}", True, WHITE)
            problem_rect = problem_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
            screen.blit(problem_text, problem_rect)

            # Display equation with font size 100px
            equation_text = pygame.font.Font(None, 100).render(problems[current_problem_index], True, WHITE)
            equation_rect = equation_text.get_rect(center=(screen_width // 2, screen_height // 2 - 60))
            screen.blit(equation_text, equation_rect)

            # Draw text input field border
            pygame.draw.rect(screen, border_color, text_input_rect, border_width, border_radius=10)

            # Display user input and result
            input_text = font.render(user_input, True, WHITE)
            input_rect = input_text.get_rect(center=text_input_rect.center)
            screen.blit(input_text, input_rect)

            # Update cursor visibility
            current_time = pygame.time.get_ticks()
            if current_time - last_blink_time >= cursor_blink_time:
                cursor_visible = not cursor_visible
                last_blink_time = current_time

            # Draw cursor
            if cursor_visible:
                cursor_position = input_rect.right + 2, input_rect.centery
                pygame.draw.line(screen, cursor_color, (cursor_position[0], cursor_position[1] - 10),
                                 (cursor_position[0], cursor_position[1] + 10), cursor_width)

            # Display score
            score_text = font.render(f"Score: {score}", True, WHITE)
            score_rect = score_text.get_rect(topleft=(10, 10))
            screen.blit(score_text, score_rect)

            # Calculate remaining time
            current_time = pygame.time.get_ticks()
            remaining_time = max(0, 15000 - (current_time - start_time))
            seconds_remaining = remaining_time // 1000

            # Display countdown timer in the top center corner
            timer_text = font.render(f"Time Left: {seconds_remaining}", True, WHITE)
            timer_rect = timer_text.get_rect(midtop=(screen_width // 2, 10))
            screen.blit(timer_text, timer_rect)


            # Check if time is up
            if remaining_time <= 0:
                lives -= 1
                current_problem_index += 1
                start_time = current_time
                user_input = ""

                if lives <= 0:
                    game_over = True
                    result = "Game Over! No lives left."
                    game_over_sound.play()  # Play game over sound
                    pygame.mixer.music.stop()  # Stop background music
                elif current_problem_index == len(problems):
                    game_over = True
                    game_over_sound.play()
                    pygame.mixer.music.stop()

                # Play fail sound when lives decrease
                pygame.mixer.Sound("assets/fail.mp3").play()

        else:  # If the user has no lives left, display "Game Over" and final score
            game_over = True
            game_over_sound.play()
            pygame.mixer.music.stop()

        pygame.display.flip()

    else:  # Game over state
        # Create a surface with semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(128)  # Adjust transparency level (0-255)
        overlay.fill((0, 0, 0))  # Fill with black color

        # Blit the overlay onto the screen
        screen.blit(overlay, (0, 0))
        # Define font sizes
        default_font_size = 24
        game_over_font_size = 150

        # Load default font
        default_font = pygame.font.Font(None, default_font_size)

        # Load font for "Game Over" text
        game_over_font = pygame.font.Font(None, game_over_font_size)

        # Display "Game Over" message with larger font size
        game_over_text = game_over_font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))  # Adjusted y-coordinate
        screen.blit(game_over_text, game_over_rect)



        # Display final score
        final_score_text = game_over_font.render(f"Score: {score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(final_score_text, final_score_rect)

        # Draw retry button
        retry_button_color = YELLOW if retry_button_rect.collidepoint(pygame.mouse.get_pos()) else BLUE
        pygame.draw.rect(screen, retry_button_color, retry_button_rect, border_radius=button_radius)

        # Display retry button text
        retry_text = font.render("Retry", True, BLACK)
        retry_text_rect = retry_text.get_rect(center=retry_button_rect.center)
        screen.blit(retry_text, retry_text_rect)

        # Event handling for retry button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(pygame.mouse.get_pos()):
                    # Reset game variables
                    current_problem_index = 0
                    user_input = ""
                    result = None
                    lives = 3
                    score = 0
                    start_time = pygame.time.get_ticks()
                    game_over = False
                    pygame.mixer.Sound("assets/start.mp3").play()  # Play start sound
                    pygame.mixer.music.play(-1)  # Restart the music

        pygame.display.flip()

    # Event handling for input and game loop termination
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if lives > 0:
                        try:
                            answer = eval(problems[current_problem_index])
                            if float(user_input) == round(answer, 2):  # Round off the answer to 2 decimal places
                                result = "Correct!"
                                score += 1
                                current_problem_index += 1
                                user_input = ""
                                correct_sound.play()  # Play sound for correct answer
                                start_time = pygame.time.get_ticks()  # Reset timer
                                if current_problem_index == len(problems):
                                    game_over = True
                            else:
                                result = "Incorrect! Try again."
                                if current_problem_index < len(problems):
                                    user_input = ""  # Clear input for the next problem
                                    pygame.mixer.Sound("assets/buzz.mp3").play()
                        except ValueError:
                            result = "Invalid Input"
                        except ZeroDivisionError:
                            result = "Division by zero"
                        except Exception as e:
                            result = f"Error: {str(e)}"

                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

pygame.quit()
sys.exit()
