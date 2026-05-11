# enemy.py - Düşman karakterlerini temsil eden modül
import random

class Enemy:
    def __init__(self, name, hp, damage, xp_reward, level=1):
        self.name = name
        self.level = level
        self.max_hp = hp
        self.current_hp = hp
        self.damage = damage
        self.xp_reward = xp_reward
        self.stunned = False

    def attack(self):
        if self.stunned:
            self.stunned = False
            print(f"  {self.name} felç! Bu tur saldıramadı.")
            return 0
        return self.damage + random.randint(-1, 3)

    def take_damage(self, damage):
        before = self.current_hp
        self.current_hp = max(0, self.current_hp - damage)
        return before - self.current_hp

    def is_alive(self):
        return self.current_hp > 0

    def get_xp_reward(self):
        return self.xp_reward

    def show_stats(self):
        print(f"  [{self.name}] HP: {self.current_hp}/{self.max_hp} | Level: {self.level}")
