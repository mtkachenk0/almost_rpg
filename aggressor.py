class Aggressor:
    def __init__(self, **kwargs):
        self.hp = kwargs["hp"]
        self.position = (0, 0)
        self.nickname = kwargs["nickname"]
        self.ad = kwargs["ad"]

    def alive(self):
        return self.hp > 0

    def attack(self, enemy):
        if not self.alive:
            return
        if not self._can_attack(enemy):
            self.move(*enemy.position)
        dmg = self._choose_damage(enemy)
        if enemy.get_dmg(dmg):
            print(f"{self.nickname} dealt {dmg} of damage to {enemy.nickname}")

    def _can_attack(self, enemy):
        return enemy.position == self.position

    def move(self, x, y):
        position_was = self.position
        self.position = (x, y)
        print("%s moved from %d:%d to %d:%d" % (self.nickname, *position_was, *self.position))
