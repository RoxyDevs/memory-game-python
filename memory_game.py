import pygame
import random
import time
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
CARD_SIZE = 100
CARD_MARGIN = 20
GRID_COLS = 4
GRID_ROWS = 4

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BACKGROUND = (50, 50, 50)

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 Memory Game - by RoxyDevs")

# Generar pares de cartas
def create_cards():
    symbols = ['🐱', '🐶', '🐼', '🐸', '🐯', '🐦', '🐬', '🐙']
    cards = symbols + symbols  # Duplicar para tener pares
    random.shuffle(cards)
    return cards

# Dibujar una carta
def draw_card(x, y, symbol, revealed=False):
    rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
    
    if revealed:
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)  # Borde
        font = pygame.font.Font(None, 60)
        text = font.render(symbol, True, BLUE)
        text_rect = text.get_rect(center=(x + CARD_SIZE//2, y + CARD_SIZE//2))
        screen.blit(text, text_rect)
    else:
        pygame.draw.rect(screen, BLUE, rect)
        pygame.draw.rect(screen, WHITE, rect, 2)  # Borde

# Dibujar texto
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Juego principal
def main():
    cards = create_cards()
    revealed = [False] * len(cards)
    selected = []
    moves = 0
    matches = 0
    game_started = False
    start_time = 0
    
    running = True
    while running:
        screen.fill(BACKGROUND)
        
        # Dibujar todas las cartas
        for i in range(len(cards)):
            row = i // GRID_COLS
            col = i % GRID_COLS
            x = col * (CARD_SIZE + CARD_MARGIN) + 150
            y = row * (CARD_SIZE + CARD_MARGIN) + 100
            
            draw_card(x, y, cards[i], revealed[i])
        
        # Dibujar información del juego
        draw_text(f"Movimientos: {moves}", 36, WHITE, WIDTH//2, 30)
        draw_text(f"Pares encontrados: {matches}/{len(cards)//2}", 36, WHITE, WIDTH//2, 70)
        
        if not game_started:
            draw_text("¡Haz clic para comenzar!", 48, GREEN, WIDTH//2, HEIGHT - 50)
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    game_started = True
                    start_time = time.time()
                
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                for i in range(len(cards)):
                    row = i // GRID_COLS
                    col = i % GRID_COLS
                    x = col * (CARD_SIZE + CARD_MARGIN) + 150
                    y = row * (CARD_SIZE + CARD_MARGIN) + 100
                    
                    card_rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
                    if card_rect.collidepoint(mouse_x, mouse_y) and not revealed[i] and len(selected) < 2:
                        revealed[i] = True
                        selected.append(i)
                        
                        if len(selected) == 2:
                            moves += 1
                            pygame.display.flip()
                            pygame.time.delay(500)  # Pausa para ver las cartas
                            
                            if cards[selected[0]] == cards[selected[1]]:
                                matches += 1
                                selected = []
                                
                                if matches == len(cards) // 2:
                                    game_time = time.time() - start_time
                                    draw_text(f"¡Ganaste! Tiempo: {game_time:.1f}s", 64, GREEN, WIDTH//2, HEIGHT//2)
                                    pygame.display.flip()
                                    pygame.time.delay(3000)
                                    return  # Reiniciar juego
                            else:
                                revealed[selected[0]] = False
                                revealed[selected[1]] = False
                                selected = []
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    while True:
        main()