import time
import glob
import pygame

class AnimationManager:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Screen dimensions
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        self.frames_talking = [pygame.image.load(image) for image in sorted(glob.glob('images/marlies/talking*.png'))]
        self.frames_idle = [pygame.image.load(image) for image in sorted(glob.glob('images/marlies/idle*.png'))]

        
    def animate_character(self, speaking=True):
        running = True
        index = 0
        frames = self.frames_talking if speaking else self.frames_idle

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))  # White background
            self.screen.blit(frames[index], (100, 100))
            index = (index + 1) % len(frames)
            pygame.display.flip()
            time.sleep(0.3)  # Adjust for realistic speaking speed

        pygame.quit()

if __name__ == '__main__':
    anim_manager = AnimationManager()
    anim_manager.animate_character(speaking=True)  # Start the talking animation
