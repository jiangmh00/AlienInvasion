import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to key pressses."""
    if event.key == pygame.K_RIGHT: 
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_f:
        fire_bullet(ai_settings, screen, ship, bullets)
    # 在调试状态下无法正常退出，因为与IDLE退出方式冲突。
    elif event.key == pygame.K_q:
        sys.exit()       
def fire_bullet(ai_settings, screen, ship, bullets):
    """Creat a new bullet and add it to the bullets group."""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
    bullets):
    """Respond to key and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                aliens, bullets,mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
    bullets, mouse_x, mouse_y):
    """Start the game when button be pressed."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game settings.
        ai_settings.initialize_dynamic_settings()

        # Reset the game's statistical information.
        stats.reset_stats()
        stats.game_active = True

        # Reset scoreboard image.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty aliens list and bullets list.
        aliens.empty()
        bullets.empty()

        #Creat new aliens and center the new ship.
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Hid cursor.
        pygame.mouse.set_visible(False)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
        play_button):
    """Update images on the screen, and flip to the new screen."""
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Show the score.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Display the new screen.
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update position of bullets.
    bullets.update()

   # Get rid of bullets disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, 
        ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
    aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # Remove any bullets and aliens that have collided.
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        creat_fleet(ai_settings, screen, ship, aliens)

        # Level up.
        stats.level += 1
        sb.prep_level()

def get_number_aliens_x(ai_settings, alien_width):
    """Find the number of aliens in a row."""
    # Spacing between each alien is equal to one alien width.
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Find the number of rows."""
    available_space_y = (ai_settings.screen_height - 
        (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and add it to aliens."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def creat_fleet(ai_settings, screen, ship, aliens):
    """Create the fleet of aliens."""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)

    # Create the group of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings, screen, aliens, alien_number,
                row_number)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen,  stats, sb, ship, aliens, bullets):
    """Respond to the ship being hit by an alien."""
    if stats.ships_left > 1:                                            # 当表达式为>0时，实际飞船数为ship_limit+1，为什么？
        # Decrement ships_left.
        stats.ships_left -= 1

        # Reset scoreboard.
        sb.prep_ships()

        # Get rid of any remaining aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen,  stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update the positions of all aliens."""
    check_fleet_edges(ai_settings, aliens)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Check ship-alien collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    aliens.update()

def check_high_score(stats, sb):
    """Check whether present score is the highest."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()