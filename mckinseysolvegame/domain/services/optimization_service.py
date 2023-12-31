from itertools import groupby
from typing import List

import numpy as np

from mckinseysolvegame.domain.models import Species, OptimizationResult


class Solver:
    @staticmethod
    def find_sustainable_food_chain(species_list: List[Species]) -> OptimizationResult:
        # Check that input is consistent
        # ...

        if not species_list:
            return OptimizationResult(0, [])

        # Find the group of producers that maximize the calories provided
        producers = [s for s in species_list if s.calories_needed == 0]
        grouped_producers = {key: list(group) for key, group in groupby(producers, key=lambda x: x.depth_range)}

        depth_range_calories = {}
        for depth_range, producers_group in grouped_producers.items():
            total_calories = sum(species.calories_provided for species in producers_group)
            depth_range_calories[depth_range] = total_calories

        # Find the depth range with the highest total calories
        highest_calories_range = max(depth_range_calories, key=depth_range_calories.get)

        # Restrict the list of species to the list of species with matching depth_range
        species_list = [s for s in species_list if s.depth_range == highest_calories_range]

        # Find sustainable food chain
        n = len(species_list)
        species_list.sort(key=lambda x: x.calories_provided, reverse=True)
        dp = [1] * n
        p = [-1] * n
        all_chains = [[] for _ in range(n)]  # List to store all chains for each species

        for i in range(n):
            # Iterate through previous species
            for j in range(i):
                # Check if the j-th species can be a food source for the i-th species
                if species_list[j].name in species_list[i].food_sources and species_list[j].calories_provided > species_list[i].calories_needed:
                    # Update dp and predecessor array if a longer chain is found
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
                        p[i] = j
            # Store the current chain in the all_chains list
            all_chains[i] = [i] + all_chains[p[i]] if p[i] != -1 else [i]

        # Initialize sets to track unique species and unique chains
        unique_species = set()
        all_chains.sort(key=lambda x: len(x), reverse=True)
        unique_chains = []

        # Find chains containing producers and no duplicate species
        producers_indices = [i for i, species in enumerate(species_list) if species.calories_needed == 0]
        for chain in all_chains:
            if not any(val in unique_species for val in chain) and any(idx in chain for idx in producers_indices):
                unique_chains.append(chain)
                unique_species.update(chain)

        # Create a list of selected species based on unique chains
        selected_species = [species_list[i] for i in [x for c in unique_chains for x in c]]

        # Sort selected species based on calories provided
        selected_species.sort(key=lambda x: x.calories_provided, reverse=True)

        return OptimizationResult(len(selected_species), [s.name for s in selected_species])