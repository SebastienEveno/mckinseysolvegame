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

This Python package helps you to solve the Ecosystem Building game from the McKinsey Solve Game. 
In this game, you need to find a sustainable chain of 8 species among many species (39 in total). 

This package offers to call the `find_sustainable_food_chain` method that accepts a list of species and returns a solution that maximizes the number of species that can create a sustainable food chain.

## Installation

To install mckinseysolvegame, simply use pip:

```sh
pip install mckinseysolvegame
```

## Usage

### Define the product

```python
from mckinseysolvegame import Species

my_species = [
    Species(name="Producer1", calories_provided=4000, calories_needed=0, food_sources=[]),
    Species(name="Producer2", calories_provided=4050, calories_needed=0, food_sources=[]),
    Species(name="Producer3", calories_provided=5000, calories_needed=0, food_sources=[]),
    Species(name="Animal1", calories_provided=1000, calories_needed=1050, food_sources=["Producer1"]),
    Species(name="Animal2", calories_provided=800, calories_needed=900, food_sources=["Animal1", "Producer3"])
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
    "number_of_species": 5,
    "species": ["Producer3", "Producer2", "Producer1", "Animal1", "Animal2"]
}
```
This object contains the maximum number of species that can sustain, as well as the list of species names.

## Contributing

We welcome contributions to mckinseysolvegame! If you find a bug or would like to request a new feature, please open an issue on
the [Github repository](https://github.com/sebastieneveno/mckinseysolvegame).
If you would like to contribute code, please submit a pull request.

## License

mckinseysolvegame is released under the [MIT License](https://opensource.org/licenses/MIT).
