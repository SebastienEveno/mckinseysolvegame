import copy
from itertools import combinations, groupby
from typing import List

from mckinseysolvegame.domain.models import Species


class Solver:
    def __init__(self):
        pass

    @staticmethod
    def _simulate_eating(species: List[Species]):
        species_dict = {s.name: {'calories_needed': s.calories_needed,
                                 'calories_provided': s.calories_provided} for s in species}

        for s in sorted(species, key=lambda x: x.calories_provided, reverse=True):
            if s.calories_needed == 0 or not s.food_sources:
                # does not need to eat (producer) or cannot eat
                continue

            s.food_sources.sort(
                key=lambda x: x.calories_provided, reverse=True)

            if len(s.food_sources) > 1 and \
                    s.food_sources[0].name in species_dict and \
                    s.food_sources[1].name in species_dict and \
                    species_dict[s.food_sources[1].name]['calories_provided'] == species_dict[s.food_sources[0].name]['calories_provided'] and \
                    species_dict[s.food_sources[0].name]['calories_provided'] >= species_dict[s.name]['calories_needed'] / 2:
                half_calories_needed = int(
                    species_dict[s.name]['calories_needed'] / 2)
                species_dict[s.food_sources[0].name]['calories_provided'] -= half_calories_needed
                species_dict[s.food_sources[1].name]['calories_provided'] -= half_calories_needed
                species_dict[s.name]['calories_needed'] = 0
                species_dict[s.name]['eats'] = [
                    s.food_sources[0].name, s.food_sources[1].name]
                continue  # only eat once

            for food in s.food_sources:
                if food.name in species_dict and species_dict[food.name]['calories_provided'] > species_dict[s.name]['calories_needed']:
                    species_dict[food.name]['calories_provided'] -= species_dict[s.name]['calories_needed']
                    species_dict[s.name]['calories_needed'] = 0
                    species_dict[s.name]['eats'] = [food.name]
                    break  # only eat once

        return species_dict

    def find_sustainable_food_chain(self, species: List[Species]) -> dict:
        maximum_food_chain_length = 8
        species_copy = copy.deepcopy(species)
        if not species_copy:
            return {}

        self._populate_food_sources(species_copy)

        species_copy.sort(key=lambda x: x.depth_range)
        grouped_species = {key: list(group) for key, group in groupby(
            species_copy, key=lambda x: x.depth_range)}

        longest_sustainable_chain_per_depth_range = {}
        for depth_range, species_copy in grouped_species.items():
            n = min(maximum_food_chain_length, len(species_copy))
            species_copy.sort(key=lambda x: x.calories_provided, reverse=True)

            optimal_list = []
            for length in range(1, n + 1):
                for combination in combinations(species_copy, length):
                    combination = list(combination)
                    if self._is_sustainable(combination) and len(combination) > len(optimal_list):
                        optimal_list = combination

            optimal_list.sort(key=lambda x: x.calories_provided, reverse=True)
            eating_steps = self._simulate_eating(optimal_list)
            longest_sustainable_chain_per_depth_range[depth_range] = eating_steps

        _, max_value = max(
            longest_sustainable_chain_per_depth_range.items(), key=lambda x: len(x[1]))

        return max_value

    @staticmethod
    def _populate_food_sources(species: List[Species]) -> None:
        for s in species:
            if not s.food_sources:
                continue
            food_sources_as_species = []
            for food_source in s.food_sources:
                matching_species = [
                    x for x in species if x.name == food_source]
                if matching_species:
                    food_sources_as_species.append(matching_species[0])
            s.food_sources = food_sources_as_species

    def _is_sustainable(self, species: List[Species]) -> bool:
        if not species:
            return False

        if not any(s.calories_needed == 0 for s in species):
            return False

        species_dict = self._simulate_eating(species)

        return all([self._is_species_sustainable(species) for species in list(species_dict.values())])

    @staticmethod
    def _is_species_sustainable(species: dict[str, int]) -> bool:
        return species['calories_needed'] == 0 and species['calories_provided'] > 0
