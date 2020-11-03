from random import randrange
from aggressor import Aggressor

class Enemy(Aggressor):
    PROPS = ("hp", "mp", "agility", "ad")
    def __init__(self, **kwargs):
        self.exp = randrange(100, 200)
        self.lvl = 1
        self.position = kwargs["position"]
        self.nickname = self.__class__.__name__
        for prop in self.PROPS:
            setattr(self, prop, kwargs[prop])

    def get_dmg(self, dmg):
        self.hp -= dmg
        return dmg

    def _choose_damage(self, *args):
        return self.ad

    def earn_exp(self, exp):
        self.exp += exp


class Lizard(Enemy):
    def __init__(self, **kwargs):
       Enemy.__init__(self, hp=120, mp=1, agility=20, ad=30, **kwargs)

class Golem(Enemy):
    def __init__(self, **kwargs):
       Enemy.__init__(self, hp=250, mp=1, agility=1, ad=5, **kwargs)

class Witch(Enemy):
    def __init__(self, **kwargs):
       Enemy.__init__(self, hp=100, mp=1, agility=20, ad=50, **kwargs)

