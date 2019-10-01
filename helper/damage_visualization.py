import pygame

dmg_color = {
    "physical": (255, 140, 0),
    "magic": (226, 121, 252),
    "true_damage": (255, 255, 255)
}


class DummyDamage:
    def __init__(self, amount, stat_pos, kind: str):
        self.color = dmg_color[kind]
        self.amount = int(amount)
        self.create = pygame.time.get_ticks()
        self.start_pos = stat_pos
        self.font = pygame.font.SysFont("Comic Sans Ms", 25)
        self.duration = 2000

    def render(self, surface):
        state = pygame.time.get_ticks() - self.create
        text = self.font.render(str(self.amount), False, self.color)
        surface.blit(text, (self.start_pos[0],
                            int(self.start_pos[1] - (state / self.duration * 50))))

    def is_active(self, time):
        state = time - self.create
        if state >= self.duration:
            return False
        else:
            return True
