from re import findall
from random import randrange, choice

from item import Item
from heros import Warrior, Archer, Magician
from enemies import Golem, Lizard, Witch


class Game:
    ROLE_SELECT = {"1": Warrior, "2": Archer, "3": Magician}
    ITEMS = {"sword": 3, "bow": 3, "spell": 10}
    ENEMIES_COUNT = 30

    _game = None # save instance here (a kind of singleton)

    @classmethod
    def start(cls):
        try:
            game = Game()
            game.register()
            game.run()
        except KeyboardInterrupt: # catch Ctrl+C and return stats
            cls.finish()

    @classmethod
    def finish(cls, quit=True):
        player = cls._game.player
        print("\n%s properties:" % player.nickname)
        for prop in player.PROPS:
            print("%s: %d" % (prop, getattr(player, prop)))
        print("Lvl: %d" % player.lvl)
        print("Game over. Thanks for the game")
        if quit:
            exit()


    def __init__(self):
        self.__class__._game = self
        self.area_size = 1000
        self.enemies, self.items = {}, {}
        self.__spread_items()
        self.__spread_enemies()
        self.player = None

    @staticmethod
    def fight(initiator, enemy):
        print("\n%s attacked %s" % (initiator.nickname, enemy.nickname))
        while initiator.alive() and enemy.alive():
            initiator.attack(enemy)
            enemy.attack(initiator)
            winner, looser = initiator, enemy
            if not initiator.alive():
                winner, looser = enemy, initiator
            elif not enemy.alive():
                winner, looser = initiator, enemy
            else:
                continue

            print("%s has been slain" % looser.nickname)
            winner.earn_exp(looser.exp)


    def register(self):
        print("Almost RPG\nChoose your hero:")
        for num, role in self.ROLE_SELECT.items():
            print("%s. %s" % (num, role.__name__))
        role_number = input("Please type 1-3: ")
        while role_number not in self.ROLE_SELECT.keys(): # role validation
            role_number = input("Wrong choice.\nPlease type 1-3: ")

        role = self.ROLE_SELECT[role_number]
        nickname = None
        while not nickname: # at least one char
           nickname = input("Please choose a name for your %s: " % role.__name__)


        self.player = role(nickname)

    def run(self):
        while self.player.alive and self.enemies:
            position = self.get_position()

            if position in self.enemies.keys():
                Game.fight(self.player, self.enemies[position]) # start fighting process
                del self.enemies[position] # remove enemy from the game
                if not self.player.position == position: # magician doesn't move to enemy while fighting
                    self.player.move(*position)
            elif position in self.items.keys():
                self.player.move(*position)
                self.player.open_item(self.items[position])
                del self.items[position] # remove item from the game

        if not self.player.alive:
            reason = "You dead. Game over :("
        else:
            reason = "You won. All enemies are defeated!"

        restart = input(r'{reason} (\nWould you like to restart? (y/n)')
        if restart == "y":
            self.__class__.finish(quit=False)
            self.__class__.start()
        else:
            self.__class__.finish()

    def get_position(self): # should be static but self is usefull for debug
        text = input("\nPlease move (type 2 numbers, \d \d): ")
        if text == "debug": # if you type debug -> you'll go into debugger
            import pdb
            pdb.set_trace()
            self.get_position()
        try:
            position = findall(r'(\d+).?(\d+)', text)[0]
            return (int(position[0]), int(position[1]))
        except (IndexError, TypeError):
            print("Wrong numbers, try again")
            return self.get_position()


    def __spread_items(self):
        for type in Item.TYPES:
            for i in range(1, self.ITEMS[type]):
                location = self.__random_location()
                while self.items.get(location): # location should be unique
                    location = self.__random_location()
                self.items[location] = Item(i * 20, i * 2, type) # price, weight, type
        print("Items: %s" % self.items.keys())

    def __spread_enemies(self):
        for i in range(self.ENEMIES_COUNT):
            location = self.__random_location()
            while self.enemies.get(location): # don't overwrite existing enemies
                location = self.__random_location()
            self.enemies[location] = choice([Golem, Lizard, Witch])(position=location)
        print("Enemies: %s" % self.enemies.keys())

    def __random_location(self):
        # return random coordinates within game area
        return (randrange(0, self.area_size), randrange(0, self.area_size))


if __name__ == "__main__":
    Game.start()
