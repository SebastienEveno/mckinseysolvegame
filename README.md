# McKinsey Solve Game

<p align="center">
    <img src="https://github.com/SebastienEveno/mckinseysolvegame/actions/workflows/python-package.yml/badge.svg?branch=master" />
    <a href="https://pypi.org/project/mckinseysolvegame" alt="Python Versions">
        <img src="https://img.shields.io/pypi/pyversions/mckinseysolvegame.svg?logo=python&logoColor=white" /></a>
    <a href="https://pypi.org/project/mckinseysolvegame" alt="PyPi">
        <img src="https://img.shields.io/pypi/v/mckinseysolvegame" /></a>
    <a href="https://pepy.tech/project/mckinseysolvegame" alt="Downloads">
        <img src="https://pepy.tech/badge/mckinseysolvegame" /></a>
</p>

This Python package helps solving the Ecosystem Building game from the McKinsey Solve Game. 
In this game, you need to find a sustainable chain of 8 species among many species (39 in total). 

This package provides a function called `find_sustainable_food_chain`, which takes a list of species as input and returns a solution that optimizes the creation of sustainable food chains, maximizing the count of species involved.

## Rules of the Game

A set of 39 species is given. From this set, you need to build a sustainable food chain.
Species are divided into producers and animals. Producers do not need calories to survive and consume only natural resources. Animals consume other animals and producers and need calories to survive.
Animals follow the following rules:
- The species with the highest calories provided eats first.
- It eats the species providing the highest calories provided as a food source. In case of a tie, it will eat half from each of the two species with the same calories.
- Eating consumes calories from the food source by the amount needed by the predator. You need calories provided greater than zero for a species to survive and all calories needed equal to zero after they eat.

If a species does not get enough calories or reaches zero with its own calories provided, the food chain is not sustainable.

## Installation

To install mckinseysolvegame, simply use pip:

```sh
pip install mckinseysolvegame
```

## Usage

### Define the input species

```python
from mckinseysolvegame import Species

my_species = [
    Species(
        name="Producer1", 
        calories_provided=4000, 
        calories_needed=0, 
        depth_range="0-30m", 
        temperature_range="28.3-30", 
        food_sources=[]
    ),
    Species(
        name="Producer2", 
        calories_provided=4050, 
        calories_needed=0, 
        depth_range="0-30m", 
        temperature_range="28.3-30", 
        food_sources=[]
    ),
    Species(
        name="Producer3", 
        calories_provided=5000, 
        calories_needed=0, 
        depth_range="0-30m", 
        temperature_range="28.3-30", 
        food_sources=[]
    ),
    Species(
        name="Animal1", 
        calories_provided=1000, 
        calories_needed=1050, 
        depth_range="0-30m", 
        temperature_range="28.3-30", 
        food_sources=["Producer1"]
    ),
    Species(
        name="Animal2", 
        calories_provided=800, 
        calories_needed=900, 
        depth_range="0-30m", 
        temperature_range="28.3-30", 
        food_sources=["Animal1", "Producer3"]
    )
]
```

### Find the species that form a sustainable food chain

```python
from mckinseysolvegame import Solver

result = Solver.find_sustainable_food_chain(my_species)
result.to_json()
```

The API will return a JSON object with the following format:
```json
{
    "numberOfSpecies": 9,
    "species": [
        "Fire Coral", 
        "Common Eel Grass", 
        "Widgeon Grass",
        "Queen Parrotfish", 
        "Blue Striped Angelfish",
        "Common Dolphinfish", 
        "Wahoo", 
        "Short-tail Stingray",
        "Gem Tang"
    ]
}
```
This object contains the maximum number of species that can sustain, as well as the list of species names.

## Contributing

We welcome contributions to mckinseysolvegame! If you find a bug or would like to request a new feature, please open an issue on
the [Github repository](https://github.com/sebastieneveno/mckinseysolvegame).
If you would like to contribute code, please submit a pull request.

## License

mckinseysolvegame is released under the [MIT License](https://opensource.org/licenses/MIT).

## To Do List
- Consider the case eating half of calories provided in case of a tie
