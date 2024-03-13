import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()
pygame.display.set_caption("Random PEMDAS Problems")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

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

# Main loop
running = True
while running:
    screen.fill(WHITE)  # Change the screen color to white

    if lives > 0:  # If the user still has lives, continue the game
        # Display current problem
        problem_text = font.render(problems[current_problem_index], True, BLACK)
        problem_rect = problem_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(problem_text, problem_rect)

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

        # Display lives and score
        lives_text = font.render(f"Lives: {lives}", True, BLACK)
        lives_rect = lives_text.get_rect(topright=(screen_width - 10, 10))
        screen.blit(lives_text, lives_rect)

        score_text = font.render(f"Score: {score}", True, BLACK)
        score_rect = score_text.get_rect(topleft=(10, 10))
        screen.blit(score_text, score_rect)

        if result is not None:
            result_text = font.render(result, True, RED if result.startswith("Incorrect") else BLACK)
            result_rect = result_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
            screen.blit(result_text, result_rect)
    else:  # If the user has no lives left, display "Game Over"
        game_over_text = font.render("Game Over", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(game_over_text, game_over_rect)

    pygame.display.flip()

    # Cursor blinking timer
    cursor_timer += 1
    if cursor_timer >= 30:
        cursor_timer = 0
        cursor_visible = not cursor_visible

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                if lives > 0:
                    try:
                        answer = eval(problems[current_problem_index])
                        if float(user_input) == answer:
                            result = "Correct!"
                            score += 1
                            current_problem_index += 1
                            user_input = ""
                            if current_problem_index == len(problems):
                                running = False
                        else:
                            result = "Incorrect! Try again."
                            lives -= 1
                            if lives == 0:
                                result = "Game Over! No lives left."
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
