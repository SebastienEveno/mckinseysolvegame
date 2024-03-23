from itertools import groupby
from typing import List

import numpy as np

from mckinseysolvegame.domain.models import Species, OptimizationResult


class Solver:

    @staticmethod
    def find_sustainable_food_chain(species: List[Species]) -> OptimizationResult:
        # Check that input is consistent
        # ...

        if not species:
            return OptimizationResult([])

        species.sort(key=lambda x: x.depth_range)
        grouped_species = {key: list(group) for key, group in groupby(species, key=lambda x: x.depth_range)}
        
        longest_sustainable_chain_per_depth_range = {}
        for depth_range, species in grouped_species.items():
            # Find sustainable food chain
            n = len(species)
            species.sort(key=lambda x: x.calories_provided, reverse=True)
            dp = [1] * n
            p = [-1] * n
            all_chains = [[] for _ in range(n)]  # List to store all chains for each species

            for i in range(n):
                # Iterate through previous species
                for j in range(i):
                    # Check if the j-th species can be a food source for the i-th species
                    if species[j].name in species[i].food_sources and species[j].calories_provided > species[i].calories_needed:
                        # Update dp and predecessor array if a longer chain is found
                        if dp[j] + 1 > dp[i]:
                            dp[i] = dp[j] + 1
                            p[i] = j
                # Store the current chain in the all_chains list
                all_chains[i] = [i] + all_chains[p[i]] if p[i] != -1 else [i]

            # Initialize sets to track unique species and unique chains
            unique_species = set()
            all_chains.sort(key=lambda x: len(x), reverse=True)

            # Find chains containing producers and no duplicate species
            producers_indices = [i for i, species in enumerate(species) if species.calories_needed == 0]
            for chain in all_chains:
                if not any(val in unique_species for val in chain) and any(idx in chain for idx in producers_indices):
                    unique_species.update(chain)

            # Create a list of selected species based on unique chains
            selected_species = [species[i] for i in unique_species]

            # Sort selected species based on calories provided
            selected_species.sort(key=lambda x: x.calories_provided, reverse=True)

            longest_sustainable_chain_per_depth_range[depth_range] = [s.name for s in selected_species]

        _, max_value = max(longest_sustainable_chain_per_depth_range.items(), key=lambda x: len(x[1]))
        
        return OptimizationResult(max_value)
