from random import random, randint
from aggressor import Aggressor

class Hero(Aggressor):
    NEXT_LVL_EXP = 500
    PROPS = ("power", "ad", "agility", "ip", "hp", "mp")
    # ad = Attack Damage
    # ip = Inteliigence Points
    # hp = Health Points
    # mp = Mana Points

    def __init__(self, nickname, **kwargs):
        self.nickname = nickname
        self.items = []
        self.exp = 0 # experience
        self.position = (0, 0) # startup position
        self.lvl = 1 # Level
        for prop in self.PROPS:
            setattr(self, prop, kwargs[prop])

    def get_dmg(self, dmg):
        if not self.alive: # don't receive dmg if hero is dead
            return
        if self._try_dodge(): # a chance to dodge dmg
            print(f"{self.nickname} dodged damage")
            return
        dmg_left = self._try_shield(dmg) # try block dmg and return dmg left
        self.hp -= dmg_left
        return self.hp

    def open_item(self, item):
        if random() >= 0.5: # 50% chance
            self.items.append(item)
            print("Found and taken a %s" % item.type)
            return item
        else:
            print("Found a %s, could not take" % item.type)

    def _try_shield(self, dmg):
        return dmg  # no shield

    def _choose_damage(self, enemy):
        try:
            item = [item for item in self.items if item.type == "sword"][0]
        except IndexError:
            item = None
        return self.ad + (item and 100 or 0) # ad + 100 if hero has sword

    def _try_dodge(self):
        # archer has 30% chance to dodge, his initial agility=150
        # that means that 5 agility = 1% for dodge chance
        return randint(0, 10) >= self.agility / 5.0

    def _can_attack(self, enemy):
        return self.position == enemy.position

    def earn_exp(self, exp):
        self.exp += exp
        print("%s earned %d exp" % (self.nickname, exp))
        if self.exp <= self.NEXT_LVL_EXP:
            return
        self.lvl += 1
        print("%s has reached level: %d!" % (self.nickname, self.lvl))
        for prop in self.PROPS:
            setattr(self, prop, getattr(self, prop) + self.SCALES.get(
                prop, self.SCALES["default"])
            )

