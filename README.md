# pygame-sara-walking

Demo of a walking directional sprite animation

Since I'm no artist, the sprite is Sara, the logo of opengameart.org, in a
version provided by William.Thompsonj here:
https://opengameart.org/content/lpc-sara

The pygame.sprite.Sprite class makes use of two attributes, rect and image.

Changing the attribute image to a @property function, the class can select
different sprites on its current state (direction, phase in animation, ...).

This short demonstration shows a cycle of 6 animation steps for the 4
directions nort, south, east, west.
