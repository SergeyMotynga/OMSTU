from plants import Plant, Lumiere, Obscurite, Demi
from animals import Animal, Pauvre, Malheureux

def get_stats(world):
    stats = []
    # Подсчёт численности каждого вида
    lumiere_count = sum(1 for e in world.entities if isinstance(e, Lumiere))
    obscurite_count = sum(1 for e in world.entities if isinstance(e, Obscurite))
    demi_count = sum(1 for e in world.entities if isinstance(e, Demi))
    pauvre_count = sum(1 for e in world.entities if isinstance(e, Pauvre))
    malheureux_count = sum(1 for e in world.entities if isinstance(e, Malheureux))
    
    # Средний радиус обзора животных
    animals = [e for e in world.entities if isinstance(e, Animal)]
    avg_vision_radius = sum(e.vision_radius for e in animals) / len(animals) if animals else 0
    
    # Формирование статистики
    stats.append(f"Time: {world.time_manager.time_of_day} (Tick: {world.time_manager.tick})")
    stats.append(f"Lumiere: {lumiere_count}")
    stats.append(f"Obscurite: {obscurite_count}")
    stats.append(f"Demi: {demi_count}")
    stats.append(f"Pauvre: {pauvre_count}")
    stats.append(f"Malheureux: {malheureux_count}")
    stats.append(f"Average Vision Radius: {avg_vision_radius:.2f}")
    
    # Дополнительная информация о соседях для выбранного животного
    def get_animal_info(animal, world):
        if not animal:
            return "No animal selected"
        neighbors = animal.get_neighbors_in_vision(world)
        neighbor_types = [type(e).__name__ for _, _, e in neighbors if e]
        return f"Selected: {type(animal).__name__} at ({animal.x}, {animal.y})\n" \
               f"Vision Radius: {animal.vision_radius}\n" \
               f"Neighbors: {', '.join(neighbor_types) if neighbor_types else 'None'}"
    
    return "\n".join(stats), get_animal_info