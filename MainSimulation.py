import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1000, 650
color_choices = ["green", "blue", "red", "teal", "orange", "purple", "pink"]
collision_counter = 0
max_collisions = 15

class Particle:
    def __init__(self, color, vx, vy, mass):
        self.color = color
        # Particle speed vector components
        self.Vx = vx
        self.Vy = vy
        # Particle mass in kilograms
        self.mass = mass
        # Make the size of a particle proportionate to it's size
        self.size = mass * 2
        # Create the pygame particle instance
        self.particle = pygame.Rect(random.randrange(50, WIDTH - 50), random.randrange(50, HEIGHT-50),
                                    self.size, self.size)

    def animate(self):
        """Function to animate and dipsplay particles on the screen"""
        global collision_counter
        self.particle.x += self.Vx
        self.particle.y += self.Vy

        # Detect collisions with the screen edges
        # These collisions are perfectly ellastic so we reverse the particle's speed
        if self.particle.top <= 0 or self.particle.bottom >= HEIGHT:
            collision_counter += 1
            self.Vy = -self.Vy

        if self.particle.left <= 0 or self.particle.right >= WIDTH:
            collision_counter += 1
            self.Vx = -self.Vx

        # Draw the particle
        pygame.draw.ellipse(simulation_screen, self.color, self.particle)

        # Write the mass on each particle
        txt_size = self.size // 5
        txt = pygame.font.SysFont("Arial", txt_size)
        txt = txt.render(f"m={self.mass}Kg", True, "Black")
        text_rect = txt.get_rect(center=self.particle.center)  # Center the text on the particle
        simulation_screen.blit(txt, text_rect)  # Blit the text onto the screen



    # Check for collision with another particle
    def is_colliding(self, other):
        dx = self.particle.centerx - other.particle.centerx
        dy = self.particle.centery - other.particle.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance < (self.size / 2 + other.size / 2)

    def handle_collision(self, other):
        """Handle the collision by updating the particle speeds"""
        global collision_counter
        if self.is_colliding(other):
            collision_counter += 1

            # Collision physics handling

            # Calculate new velocities before updating
            new_Vx_self = ((self.Vx * (self.mass - other.mass) + 2 * (other.mass * other.Vx))
                           / (self.mass + other.mass))
            new_Vy_self = ((self.Vy * (self.mass - other.mass) + 2 * (other.mass * other.Vy))
                           / (self.mass + other.mass))

            new_Vx_other = ((other.Vx * (other.mass - self.mass) + 2 * (self.mass * self.Vx))
                            / (self.mass + other.mass))
            new_Vy_other = ((other.Vy * (other.mass - self.mass) + 2 * (self.mass * self.Vy))
                            / (self.mass + other.mass))


            # Update velocities for both particles
            self.Vx = new_Vx_self
            self.Vy = new_Vy_self

            other.Vx = new_Vx_other
            other.Vy = new_Vy_other


            # Separate the particles to prevent "sticking"
            overlap_distance = (self.size / 2 + other.size / 2) - math.sqrt(
                (self.particle.centerx - other.particle.centerx) ** 2 +
                (self.particle.centery - other.particle.centery) ** 2)

            # Move them apart based on their velocities
            if overlap_distance > 0:
                self.particle.x += int(overlap_distance * (self.particle.centerx - other.particle.centerx) / (
                            self.size / 2 + other.size / 2))
                self.particle.y += int(overlap_distance * (self.particle.centery - other.particle.centery) / (
                            self.size / 2 + other.size / 2))
                other.particle.x -= int(overlap_distance * (self.particle.centerx - other.particle.centerx) / (
                            self.size / 2 + other.size / 2))
                other.particle.y -= int(overlap_distance * (self.particle.centery - other.particle.centery) / (
                            self.size / 2 + other.size / 2))



simulation_screen = pygame.display.set_mode((WIDTH, HEIGHT)) 	 # affichage de la fenêtre
pygame.display.set_caption("Particle Simulator") 		# affiche le titre de la fenêtre

RUNNING = True
ticker = pygame.time.Clock()


def create_particles(nb):
    """Function to initialize multiple particles"""
    particles = []

    for _ in range(nb):
        mass = random.randrange(5, 80)
        intial_Vy = random.randrange(-5, 5)
        intial_Vx = random.randrange(-5, 5)
        particles.append(Particle(random.choice(color_choices), intial_Vx, intial_Vy, mass))

    return particles

# Create the particles
particles = create_particles(10)

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # Fill the screen to erase the previous frame
    simulation_screen.fill((0, 0, 0))

    # Animate and detect collisions between particles
    for i, particle in enumerate(particles):
        particle.animate()

        # Check collision with other particles
        for next_particle in particles[i + 1:]:
            particle.handle_collision(next_particle)

    # Update screen
    ticker.tick(60)
    pygame.display.flip()


pygame.quit()
