import copy
from itertools import combinations, groupby
from typing import List
import pandas as pd

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
                continue

            current_food_sources = {k: v['calories_provided'] for k, v in species_dict.items(
            ) if k in [food.name for food in s.food_sources]}
            sorted_food_sources = dict(
                sorted(current_food_sources.items(), key=lambda item: item[1], reverse=True))

            if len(sorted_food_sources) > 1:
                first_species_name = list(sorted_food_sources.keys())[0]
                second_species_name = list(sorted_food_sources.keys())[1]

                if species_dict[second_species_name]['calories_provided'] == species_dict[first_species_name]['calories_provided'] and \
                        species_dict[first_species_name]['calories_provided'] >= species_dict[s.name]['calories_needed'] / 2:
                    half_calories_needed = int(
                        species_dict[s.name]['calories_needed'] / 2)
                    species_dict[first_species_name]['calories_provided'] -= half_calories_needed
                    species_dict[second_species_name]['calories_provided'] -= half_calories_needed
                    species_dict[s.name]['calories_needed'] = 0
                    species_dict[s.name]['eats'] = [
                        first_species_name, second_species_name]
                    continue  # only eat once

            for food_name in sorted_food_sources.keys():
                if species_dict[food_name]['calories_provided'] > species_dict[s.name]['calories_needed']:
                    species_dict[food_name]['calories_provided'] -= species_dict[s.name]['calories_needed']
                    species_dict[s.name]['calories_needed'] = 0
                    species_dict[s.name]['eats'] = [food_name]
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

    def solve_from_dataframe(self, df: pd.DataFrame) -> dict:
        # Ensure we don't modify the original dataframe
        df_copy = df.copy()

        # Convert the food_sources column to a list of strings
        df_copy['food_sources'] = df_copy['food_sources'].apply(
            lambda x: x.split(';') if pd.notna(x) else [])

        species_list = []
        for _, row in df_copy.iterrows():
            species = Species(
                name=row['name'],
                calories_provided=row['calories_provided'],
                calories_needed=row['calories_needed'],
                depth_range=row['depth_range'],
                temperature_range=row['temperature_range'],
                food_sources=row['food_sources']
            )
            species_list.append(species)
        return self.find_sustainable_food_chain(species_list)
