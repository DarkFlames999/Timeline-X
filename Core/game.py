import pygame
def run_game():


    # Initialize Pygame 
    pygame.init()

    # Create the game window 
    info = pygame.display.Info()

    player_speed = 25

    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

    clock = pygame.time.Clock()

    player_pos = pygame.Vector2(window.get_width() / 2, window.get_height() / 2)

    pygame.display.set_caption("Timeline-X")

    running = True

    while running:
        dt = clock.tick(240) / 1000   # high refresh rate OK!

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
        

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]):
            player_pos.y -= player_speed * dt
        if keys[pygame.K_s]:
            player_pos.y += player_speed * dt
        if keys[pygame.K_a]:
            player_pos.x -= player_speed * dt
        if keys[pygame.K_d]:
            player_pos.x += player_speed * dt


        window.fill((0, 0, 0))
        pygame.draw.circle(window, "purple", player_pos, 10)
        pygame.display.flip()

    pygame.quit()

