import random

class Pokemon:
    def __init__(self, name, ptype, health, attack, defense, sp_attack, sp_defense, speed, level, experience, is_wild):
        self.name = name
        self.type = ptype
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
        self.level = level
        self.experience = experience
        self.moves = []
        self.is_wild = is_wild

    def attack_opponent(self, opponent, move):
        if move in self.moves:
            damage = self.calculate_damage(opponent, move)
            opponent.take_damage(damage)
            print(f"{self.name} used {move.name}! It dealt {damage} damage.")
        else:
            print(f"{self.name} doesn't know {move.name}!")

    def calculate_damage(self, opponent, move):
        if move.category == "physical":
            damage = ((2 * self.level / 5 + 2) * move.power * (self.attack / opponent.defense)) / 50 + 2
        else:
            damage = ((2 * self.level / 5 + 2) * move.power * (self.sp_attack / opponent.sp_defense)) / 50 + 2

        if move.type == "Fire" and opponent.type == "Grass":
            damage *= 2
        elif move.type == "Water" and opponent.type == "Fire":
            damage *= 2
        elif move.type == "Grass" and opponent.type == "Water":
            damage *= 2
        else:
            damage *= 1

        return int(damage)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print(f"{self.name} fainted!")

    def gain_experience(self, exp):
        self.experience += exp
        print(f"{self.name} gained {exp} experience points!")
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.max_health += 10
        self.health = self.max_health
        self.attack += 2
        self.defense += 2
        self.sp_attack += 2
        self.sp_defense += 2
        self.speed += 2
        print(f"{self.name} leveled up to level {self.level}!")

    def learn_move(self, move):
        if len(self.moves) < 4:
            self.moves.append(move)
            print(f"{self.name} learned {move.name}!")
        else:
            print(f"{self.name} can't learn more than 4 moves!")

    def get_stat(self, stat):
        return getattr(self, stat)

class Move:
    def __init__(self, name, mtype, power, accuracy, category, effect=None):
        self.name = name
        self.type = mtype
        self.power = power
        self.accuracy = accuracy
        self.category = category
        self.effect = effect

    def apply_effect(self, target):
        if self.effect:
            self.effect(target)

class Trainer:
    def __init__(self, name):
        self.name = name
        self.team = []
        self.inventory = []

    def catch_pokemon(self, wild_pokemon):
        pokeball = self.inventory.pop() if self.inventory else None
        if pokeball:
            catch_rate = random.randint(0, 100)
            if catch_rate < 50:
                self.team.append(wild_pokemon)
                print(f"{self.name} caught {wild_pokemon.name}!")
            else:
                print(f"{self.name} failed to catch {wild_pokemon.name}.")
        else:
            print("No Pokeballs left!")

    def use_item(self, item, target):
        item.use(target)

    def battle(self, opponent_trainer):
        while self.team and opponent_trainer.team:
            my_pokemon = self.team[0]
            opp_pokemon = opponent_trainer.team[0]
            while my_pokemon.health > 0 and opp_pokemon.health > 0:
                my_move = random.choice(my_pokemon.moves)
                my_pokemon.attack_opponent(opp_pokemon, my_move)
                if opp_pokemon.health > 0:
                    opp_move = random.choice(opp_pokemon.moves)
                    opp_pokemon.attack_opponent(my_pokemon, opp_move)
            if my_pokemon.health == 0:
                self.team.pop(0)
            if opp_pokemon.health == 0:
                opponent_trainer.team.pop(0)
        if self.team:
            print(f"{self.name} wins the battle!")
        else:
            print(f"{opponent_trainer.name} wins the battle!")

class Item:
    def __init__(self, name, itype, effect):
        self.name = name
        self.type = itype
        self.effect = effect

    def use(self, target):
        self.effect(target)

# Example usage:
fire_blast = Move("Fire Blast", "Fire", 110, 85, "special")
tackle = Move("Tackle", "Normal", 40, 100, "physical")

charmander = Pokemon("Charmander", "Fire", 39, 52, 43, 60, 50, 65, 5, 0, False)
bulbasaur = Pokemon("Bulbasaur", "Grass", 45, 49, 49, 65, 65, 45, 5, 0, False)

charmander.learn_move(fire_blast)
charmander.learn_move(tackle)
bulbasaur.learn_move(tackle)

ash = Trainer("Ash")
ash.team.append(charmander)

misty = Trainer("Misty")
misty.team.append(bulbasaur)

ash.battle(misty)
