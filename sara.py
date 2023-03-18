import pygame

from enum import Enum, auto

BLACK = pygame.Color('black')
FPS = 60
W = H = 256
W2, H2 = W // 2, H // 2

pygame.init()
pygame.display.set_caption('Walking Sara Demo')
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

sheet = pygame.image.load('SaraFullSheet.png').convert_alpha()


class Directions(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


PLAYER_CONTROL = {
    pygame.K_w: Directions.NORTH,
    pygame.K_d: Directions.EAST,
    pygame.K_s: Directions.SOUTH,
    pygame.K_a: Directions.WEST,
}


def _sprite_row(sheet, x0, y0, w, h, count):
    return [sheet.subsurface(pygame.Rect(x0 + _ * w, y0, w, h))
            for _ in range(count)]


imgdef = {
    Directions.NORTH: _sprite_row(sheet, 0, 64 *  8, 64, 64, 6),
    Directions.EAST:  _sprite_row(sheet, 0, 64 * 11, 64, 64, 6),
    Directions.SOUTH: _sprite_row(sheet, 0, 64 * 10, 64, 64, 6),
    Directions.WEST:  _sprite_row(sheet, 0, 64 *  9, 64, 64, 6),
}


class Walker(pygame.sprite.Sprite):
    def __init__(self, imgdef, *groups):
        super().__init__(groups)

        self.imgdef = imgdef
        self.direction = Directions.EAST

        self.anim_idx = 0
        self.cooldown = self._cooldown = 0.1

        # This assumes, all sprites have the same dimention.  If that's not the
        # case, rect also needs to become a property with additional setter to
        # get the current sprite dimensions from the current sprite image.
        self.rect = self.image.get_rect()
        self.rect.center = W2, H2

    def update(self, dt):
        """Called by pygame.sprite.Grou's update method.
        Cycles the animation.  dt is the delta time between frames.
        """
        self.cooldown -= dt
        if self.cooldown > 0:
            return

        self.cooldown = self._cooldown
        self.anim_idx = (self.anim_idx + 1) % len(self.imgdef[self.direction])

    @property
    def image(self):
        """Used by pygame.sprite.Group's draw method
        """
        return self.imgdef[self.direction][self.anim_idx]


sara_group = pygame.sprite.Group()
sara = Walker(imgdef, sara_group)

running = True
while running:
    dt = clock.get_time() / 1000.0

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False
            elif e.key in PLAYER_CONTROL:
                sara.direction = PLAYER_CONTROL[e.key]
                sara.anim_idx = 0

    screen.fill(BLACK)
    sara_group.update(dt)
    sara_group.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
