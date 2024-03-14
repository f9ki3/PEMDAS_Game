import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Random PEMDAS Problems")

# Load background image
background_image = pygame.image.load("assets/background.gif").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load heart image
heart_image = pygame.image.load("assets/heart.png")
heart_image = pygame.transform.scale(heart_image, (30, 30))

# Colors
BLACK = (255, 255, 255)
WHITE = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)
problem_font = pygame.font.Font(None, 48)  # Larger font for the problem text

# Load sound effects
start_sound = pygame.mixer.Sound("assets/start.mp3")
correct_sound = pygame.mixer.Sound("assets/correct.mp3")
game_over_sound = pygame.mixer.Sound("assets/game_over.mp3")  # Load game over sound

# Variables
problems = []
for _ in range(5):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    num3 = random.randint(1, 10)
    operation1 = random.choice(["+", "-"])
    operation2 = random.choice(["*", "/"])
    problem = f"{num1} {operation1} {num2} {operation2} {num3}"
    problems.append(problem)

current_problem_index = 0
user_input = ""
result = None
lives = 3
score = 0

# Text input field parameters
text_input_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 18, 200, 36)
border_width = 2
border_color = BLACK

# Cursor parameters
cursor_color = BLACK
cursor_width = 2
cursor_timer = 0
cursor_visible = True

# Button parameters
button_radius = 10
button_margin = 20
start_button_rect = pygame.Rect(screen_width // 2 - 100, 300, 200, 50)
exit_button_rect = pygame.Rect(screen_width // 2 - 100, 400, 200, 50)

# Play background music
pygame.mixer.init()
pygame.mixer.music.load("assets/8bit.mp3")

# Main menu
menu_running = True
while menu_running:
    screen.fill(WHITE)

    # Blit background image
    screen.blit(background_image, (0, 0))

    # Draw title with glowing effect
    title_text = title_font.render("PEMDAS GAME", True, BLACK)
    title_rect = title_text.get_rect(center=(screen_width // 2, 150))
    for i in range(10, 0, -1):
        text_surface = pygame.Surface(title_rect.size, pygame.SRCALPHA)
        alpha_value = min(255, i * 25)
        text_surface.fill((255, 255, 255, alpha_value))
        text_surface.blit(title_text, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        screen.blit(text_surface, title_rect)

    # Draw rounded buttons
    start_button_color = YELLOW if start_button_rect.collidepoint(pygame.mouse.get_pos()) else BLUE
    exit_button_color = YELLOW if exit_button_rect.collidepoint(pygame.mouse.get_pos()) else BLUE

    pygame.draw.rect(screen, start_button_color, start_button_rect, border_radius=button_radius)
    pygame.draw.rect(screen, exit_button_color, exit_button_rect, border_radius=button_radius)

    # Display button text
    start_text = font.render("Start", True, WHITE)
    exit_text = font.render("Exit", True, WHITE)

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
                pygame.mixer.music.play(-1)  # Play the music again from the beginning
                menu_running = False
            elif exit_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()

# Game loop
running = True
game_over = False  # Variable to track whether the game is over
start_time = pygame.time.get_ticks()  # Start the timer when the game loop begins
while running:

    # Blit background image
    screen.blit(background_image, (0, 0))

    if not game_over:
        # Display lives
        for i in range(lives):
            screen.blit(heart_image, (screen_width - 40 - i * 40, 10))

        if lives > 0:  # If the user still has lives, continue the game
            # Display current problem
            problem_text = problem_font.render(f"Problem {current_problem_index + 1}", True, BLACK)
            problem_rect = problem_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
            screen.blit(problem_text, problem_rect)

            # Display equation with font size 100px
            equation_text = font.render(problems[current_problem_index], True, BLACK)
            equation_text = pygame.font.Font(None, 100).render(problems[current_problem_index], True, BLACK)  # Change the font size to 100px
            equation_rect = equation_text.get_rect(center=(screen_width // 2, screen_height // 2 - 60))
            screen.blit(equation_text, equation_rect)

            # Draw text input field border
            pygame.draw.rect(screen, border_color, text_input_rect, border_width, border_radius=10)

            # Display user input and result
            input_text = font.render(user_input, True, BLACK)
            input_rect = input_text.get_rect(center=text_input_rect.center)
            screen.blit(input_text, input_rect)

            # Draw cursor
            if cursor_visible:
                cursor_position = input_rect.right + 2, input_rect.centery
                pygame.draw.line(screen, cursor_color, (cursor_position[0], cursor_position[1] - 10),
                                 (cursor_position[0], cursor_position[1] + 10), cursor_width)

            # Display score
            score_text = font.render(f"Score: {score}", True, BLACK)
            score_rect = score_text.get_rect(topleft=(10, 10))
            screen.blit(score_text, score_rect)

            # Calculate remaining time
            current_time = pygame.time.get_ticks()
            remaining_time = max(0, 15000 - (current_time - start_time))
            seconds_remaining = remaining_time // 1000

            # Display countdown timer
            timer_text = font.render(f"Time Left: {seconds_remaining}", True, BLACK)
            timer_rect = timer_text.get_rect(center=(screen_width // 2, 50))
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
        else:  # If the user has no lives left, display "Game Over" and final score
            game_over = True
            game_over_sound.play()
            pygame.mixer.music.stop()

        pygame.display.flip()

    else:  # Game over state
        # Display "Game Over" message
        game_over_text = font.render("Game Over", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        # Display final score
        final_score_text = font.render(f"Your Score: {score}", True, BLACK)
        final_score_rect = final_score_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(final_score_text, final_score_rect)

        pygame.display.flip()

        # Wait for player to press a key before exiting
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        waiting = False
                    else:
                        waiting = False

        running = False  # End the game loop

    # Event handling
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
