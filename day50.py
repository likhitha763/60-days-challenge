"""
Futuristic Superhero Academy Simulator (Object-Oriented Design)
=============================================================
Phase: Object-Oriented Design

Description:
A futuristic academy trains superheroes with diverse powers, energy levels, and combat 
styles. This script implements a scalable, extensible Object-Oriented Programming (OOP) 
architecture where hero classes inherit shared traits, override specialized attacks, 
and interact dynamically in a training arena.

Real-World Impact:
- Game Engines: Managing modular entities, character behaviors, and physics interactions.
- Enterprise Software: Building extensible business logic and service architectures.
- Banking Systems: Structuring different account types and transaction behaviors via polymorphism.
"""

from abc import ABC, abstractmethod
import random

class Hero(ABC):
    """
    Abstract Base Class representing any hero entering the academy.
    Provides core attributes and shared behaviors while enforcing polymorphism.
    """
    def __init__(self, name: str, health: int, energy: int, power_level: int):
        self.name = name
        self.health = health
        self.max_health = health
        self.energy = energy
        self.power_level = power_level

    def is_alive(self) -> bool:
        """Returns True if the hero still has health remaining."""
        return self.health > 0

    def take_damage(self, amount: int):
        """Reduces hero health, ensuring it doesn't drop below zero."""
        self.health = max(0, self.health - amount)
        print(f"   [DAMAGE] {self.name} takes {amount} damage! (Health remaining: {self.health}/{self.max_health})")

    @abstractmethod
    def special_attack(self) -> tuple[str, int]:
        """
        Abstract method requiring all subclasses to implement their unique attack.
        Returns a tuple of (attack_description, damage_dealt).
        """
        pass

    def display_stats(self):
        """Displays current hero status."""
        print(f"Hero: {self.name} | HP: {self.health}/{self.max_health} | Energy: {self.energy} | Power: {self.power_level}")


class Speedster(Hero):
    """Speedster hero type: Focuses on rapid multi-hit strikes."""
    def special_attack(self) -> tuple[str, int]:
        if self.energy < 15:
            return f"{self.name} is too exhausted for a Lightning Dash! (Basic Punch)", 10
        self.energy -= 15
        damage = self.power_level * 2
        return f"{self.name} unleashes a Lightning Dash, striking at hypersonic speed!", damage


class TechHero(Hero):
    """Tech-based hero type: Relies on high-tech gadgets and laser systems."""
    def special_attack(self) -> tuple[str, int]:
        if self.energy < 25:
            return f"{self.name}'s reactor is depleted! (Backup Blaster)", 15
        self.energy -= 25
        damage = self.power_level * 3
        return f"{self.name} fires a concentrated Plasma Beam from their exoskeleton!", damage


class Brawler(Hero):
    """Brawler hero type: Deals massive crushing damage at close range."""
    def special_attack(self) -> tuple[str, int]:
        if self.energy < 20:
            return f"{self.name} is out of stamina! (Heavy Slam)", 12
        self.energy -= 20
        damage = self.power_level * 4
        return f"{self.name} executes a Seismic Ground Slam, shattering the training floor!", damage


def simulate_training_battle(hero1: Hero, hero2: Hero):
    """
    Simulates a dynamic training duel between two academy heroes, 
    demonstrating polymorphism and dynamic interaction.
    """
    print(f"\n==================================================")
    print(f" ARENA DUEL: {hero1.name} vs {hero2.name}")
    print(f"==================================================")
    
    round_num = 1
    fighters = [hero1, hero2]
    
    while fighters[0].is_alive() and fighters[1].is_alive():
        print(f"\n--- Round {round_num} ---")
        attacker, defender = fighters[0], fighters[1]
        
        # Attacker executes special attack (Polymorphism in action)
        desc, damage = attacker.special_attack()
        print(desc)
        defender.take_damage(damage)
        
        if not defender.is_alive():
            print(f"\n>>> {defender.name} has been incapacitated! {attacker.name} wins the duel! <<<")
            break
            
        # Swap turns for the next round
        fighters.reverse()
        round_num += 1
        
        # Prevent infinite loops in friendly training matches
        if round_num > 10:
            print("\n>>> Match Time Limit Reached: It's a Draw! <<<")
            break


# --- Execution and Testing ---
if __name__ == "__main__":
    print("=== FUTURISTIC SUPERHERO ACADEMY SIMULATOR ===")
    
    # Initialize academy roster
    flash_clone = Speedster(name="Mercury", health=100, energy=60, power_level=12)
    iron_clone = TechHero(name="CyberKnight", health=120, energy=80, power_level=10)
    hulk_clone = Brawler(name="Titanus", health=150, energy=50, power_level=15)
    
    print("\n[Academy Roster Initialized]")
    flash_clone.display_stats()
    iron_clone.display_stats()
    hulk_clone.display_stats()
    
    # Simulate battles
    simulate_training_battle(flash_clone, iron_clone)
    simulate_training_battle(hulk_clone, flash_clone)


"""
--- LINKEDIN REFLECTION ---
Post Title: Building Scalable Systems with Object-Oriented Design 🦸‍♂️⚡

As software systems grow from a handful of scripts to enterprise-grade architectures, 
maintainability becomes everything. Today, for the ABTalks Challenge, I built a Futuristic 
Superhero Academy Simulator using core Object-Oriented Programming (OOP) principles.

By leveraging:
1. Inheritance & Abstraction: Creating a clean `Hero` base class with shared stats and core methods.
2. Method Overriding & Polymorphism: Allowing `Speedster`, `TechHero`, and `Brawler` to implement 
   their own unique combat styles while keeping the interface completely uniform.
3. Encapsulation: Managing health and energy states cleanly within entity boundaries.

Whether you're designing game engines, banking transaction layers, or microservices, mastering 
OOP patterns ensures your codebase can scale smoothly to accommodate hundreds of new features or heroes!

#SoftwareEngineering #ObjectOrientedProgramming #Python #DesignPatterns #GameDev #CodingJourney
"""
