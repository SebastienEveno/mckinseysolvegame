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
    Species(name="Widgeon Grass",
            calories_provided=4950,
            calories_needed=0,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=[]),
    Species(name="Fire Coral",
            calories_provided=5850,
            calories_needed=0,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=[]),
    Species(name="Common Eel Grass",
            calories_provided=4950,
            calories_needed=0,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=[]),
    Species(name="Yellow Tube Sponge",
            calories_provided=4600,
            calories_needed=0,
            depth_range="31-60m",
            temperature_range="26.7-28.2",
            food_sources=[]),
    Species(name="Green Zoanthid",
            calories_provided=5050,
            calories_needed=0,
            depth_range="31-60m",
            temperature_range="26.7-28.2",
            food_sources=[]),
    Species(name="Peacock's Tail Algae",
            calories_provided=4100,
            calories_needed=0,
            depth_range="31-60m",
            temperature_range="26.7-28.2",
            food_sources=[]),
    Species(name="Stalked Kelp",
            calories_provided=4650,
            calories_needed=0,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[]),
    Species(name="Rock Weed",
            calories_provided=4600,
            calories_needed=0,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[]),
    Species(name="Purple Hydrocoral",
            calories_provided=5600,
            calories_needed=0,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[]),
    Species(name="Blue Striped Angelfish",
            calories_provided=3750,
            calories_needed=4550,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=["Common Eel Grass"]),
    Species(name="Blue Shark",
            calories_provided=4650,
            calories_needed=2150,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[
                "Bicolour Angelfish",
                "Majestic Angelfish",
                "Northern Red Snapper",
                "Coral Trout",
                "Swordfish",
                "Sailfin Tang",
                "Powder Blue Tang",
                "Flame Angelfish",
                "Eyestripe Surgeonfish"
                ]),
    Species(name="Bicolour Angelfish",
            calories_provided=1900,
            calories_needed=440,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[
                "Powder Blue Tang",
                "Flame Angelfish",
                "Eyestripe Surgeonfish",
                "Stalked Kelp",
                "Purple Hydrocoral"
                ]),
    Species(name="Bicolour Parrotfish",
            calories_provided=3400,
            calories_needed=8800,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=[
                "Widgeon Grass",
                "Common Eel Grass",
                "Fire Coral"
                ]),
    Species(name="Wahoo",
            calories_provided=1700,
            calories_needed=2500,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=[
                "Short-tail Stingray",
                "Blue Striped Angelfish"
                ]),
    Species(name="Swordfish",
            calories_provided=2000,
            calories_needed=500,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[
                "Bicolour Angelfish"
                ]),
    Species(name="Short-tail Stingray",
            calories_provided=1450,
            calories_needed=2050,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=[
                "Common Dolphinfish",
                "Foxface Rabbitfish"
                ]),
    Species(name="Sailfin Tang",
            calories_provided=2500,
            calories_needed=4800,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[
                "Rock Weed"
                ]),
    Species(name="Queen Parrotfish",
            calories_provided=3800,
            calories_needed=4700,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=["Fire Coral"]),
    Species(name="Queen Angelfish",
            calories_provided=2600,
            calories_needed=3100,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=[
                "Blue Striped Angelfish",
                "Queen Parrotfish",
                "Common Eel Grass"
                ]),
    Species(name="Powder Blue Tang",
            calories_provided=3600,
            calories_needed=4350,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[
                "Stalked Kelp",
                "Purple Hydrocoral"
                ]),
    Species(name="Porcupine Pufferfish",
            calories_provided=2600,
            calories_needed=3800,
            depth_range="31-60m",
            temperature_range="26.7-28.2",
            food_sources=[
                "Peacock's Tail Algae",
                "Passer Angelfish"
                ]),
    Species(name="Passer Angelfish",
            calories_provided=2250,
            calories_needed=4600,
            depth_range="31-60m",
            temperature_range="26.7-28.2",
            food_sources=[
                "Peacock's Tail Algae"
                ]),
    Species(name="Pacific Tripletail",
            calories_provided=2150,
            calories_needed=2900,
            depth_range="31-60m",
            temperature_range="26.7-28.2",
            food_sources=[
                "Coral Beauty"
                ]),
    Species(name="Olive Ridley Turtle",
            calories_provided=3550,
            calories_needed=4400,
            depth_range="31-60m",
            temperature_range="26.7-28.2",
            food_sources=[
                "Green Zoanthid",
                "Pacific Tripletail"
                ]),
    Species(name="Northern Red Snapper",
            calories_provided=1200,
            calories_needed=2150,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[
                "Majestic Angelfish",
                "Sailfin Tang",
                "Flame Angelfish",
                "Eyestripe Surgeonfish"
                ]),
    Species(name="Majestic Angelfish",
            calories_provided=1150,
            calories_needed=3200,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[
                "Sailfin Tang",
                "Powder Blue Tang",
                "Eyestripe Surgeonfish",
                "Stalked Kelp"
                ]),
    Species(name="Long Finned Pilot Whale",
            calories_provided=3100,
            calories_needed=950,
            depth_range="31-60m",
            temperature_range="26.7-28.2",
            food_sources=[
                "Pacific Tripletail"
                ]),
    Species(name="Indo-Pacific Sailfish",
            calories_provided=1600,
            calories_needed=5600,
            depth_range="31-60m",
            temperature_range="26.7-28.2",
            food_sources=[
                "Pacific Tripletail",
                "Coral Beauty",
                "Flameback Angelfish"
                ]),
    Species(name="Hawksbill Sea Turtle",
            calories_provided=2800,
            calories_needed=4950,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=[
                "Blue Striped Angelfish",
                "Queen Parrotfish",
                "Foxface Rabbitfish",
                "Common Eel Grass",
                "Fire Coral"
                ]),
    Species(name="Gem Tang",
            calories_provided=1250,
            calories_needed=4900,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=["Widgeon Grass"]),
    Species(name="Foxface Rabbitfish",
            calories_provided=800,
            calories_needed=4050,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=[
                "Widgeon Grass",
                "Fire Coral"
                ]),
    Species(name="Flameback Angelfish",
            calories_provided=2900,
            calories_needed=4750,
            depth_range="31-60m",
            temperature_range="26.7-28.2",
            food_sources=[
                "Green Zoanthid"
                ]),
    Species(name="Flame Angelfish",
            calories_provided=2200,
            calories_needed=4000,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[
                "Stalked Kelp",
                "Rock Weed"
                ]),
    Species(name="Eyestripe Surgeonfish",
            calories_provided=1050,
            calories_needed=3900,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[
                "Stalked Kelp",
                "Rock Weed"
                ]),
    Species(name="Cuvier Beaked Whale",
            calories_provided=1400,
            calories_needed=2250,
            depth_range="31-60m",
            temperature_range="26.7-28.2",
            food_sources=[
                "Coral Beauty",
                "Flameback Angelfish"
                ]),
    Species(name="Coral Trout",
            calories_provided=1850,
            calories_needed=3000,
            depth_range="61-90m",
            temperature_range="25-26.6",
            food_sources=[
                "Bicolour Angelfish",
                "Powder Blue Tang",
                "Flame Angelfish"
                ]),
    Species(name="Coral Beauty",
            calories_provided=2650,
            calories_needed=4900,
            depth_range="31-60m",
            temperature_range="26.7-28.2",
            food_sources=[
                "Yellow Tube Sponge",
                "Peacock's Tail Algae"
                ]),
    Species(name="Common Dolphinfish",
            calories_provided=2150,
            calories_needed=2100,
            depth_range="0-30m",
            temperature_range="28.3-30",
            food_sources=["Queen Parrotfish"])
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
    "species": [
        "Purple Hydrocoral", 
        "Stalked Kelp", 
        "Blue Shark", 
        "Rock Weed",
        "Powder Blue Tang", 
        "Flame Angelfish", 
        "Swordfish", 
        "Bicolour Angelfish",
        "Northern Red Snapper", 
        "Eyestripe Surgeonfish"
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
