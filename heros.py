from hero import Hero

class Warrior(Hero):
    SCALES = {"default": 10, "hp": 200, "ad": 20}

    def __init__(self, nickname):
        Hero.__init__(self, nickname, ad=150, power=100, agility=150, ip=1, hp=500, mp=10)


class Archer(Hero):
    SCALES = {"default": 10, "hp": 50, "ad": 50, "agility": 30}

    def __init__(self, nickname):
        Hero.__init__(self, nickname, ad=200, power=20, agility=150, ip=30, hp=200, mp=20)

    def open_item(self, item):
        print("Found and taken a %s" % item.type)
        return item # Archer always opens


class Magician(Hero):
    SCALES = {"default": 10, "mp": 1000, "hp": 30, "ad": 10}
    def __init__(self, nickname):
        Hero.__init__(self, nickname, ad=40, power=5, agility=30, ip=300, hp=100, mp=5000)

    def choose_damage(self, enemy):
        if enemy.hp <= self.ad:
            return self.ad
        spell = Magician.__find_index(self.items, lambda i: i.type == "spell")
        if spell is not None and self.mp >= 100:
            del self.items[spell]
            self.mana -= 100
            return 1000
        return self.ad

    def _can_attack(self, *args): # position doesn't matter
        return True

    def _try_shield(self, dmg):
        if self.mp < dmg:
            self.mp = 0 # don't go negative
            return dmg - self.mp
        else:
            self.mp -= dmg
        return 0

    @staticmethod
    def __find_index(lst, fn): # helper for finding elements in array
          return next(i for i, x in enumerate(lst) if fn(x))



