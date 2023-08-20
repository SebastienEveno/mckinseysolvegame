import glob
import json
import os
import time

import pytest

from mckinseysolvegame.domain.models import Species, SpeciesSchema
from mckinseysolvegame.domain.services.optimization_service import Solver


@pytest.mark.parametrize(
    "species, expected_output",
    [
        (
            [],
            (0, [])
        ),
        (
            [
                Species(name="Species1", calories_provided=1000,
                        calories_needed=0, food_sources=[])
            ],
            (1, ['Species1'])
        ),
        (
            [
                Species(name="Species1", calories_provided=1000,
                        calories_needed=0, food_sources=[]),
                Species(name="Species2", calories_provided=2000,
                        calories_needed=0, food_sources=[]),
                Species(name="Species3", calories_provided=3000,
                        calories_needed=0, food_sources=[])
            ],
            (3, ['Species3', 'Species2', 'Species1'])
        ),
        (
            [
                Species(name="Producer1", calories_provided=1000,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer2", calories_provided=2000,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer3", calories_provided=3000,
                        calories_needed=0, food_sources=[]),
                Species(name="Animal1", calories_provided=100,
                        calories_needed=1000,
                        food_sources=["Producer1", "Producer2", "Producer3"])
            ],
            (4, ['Producer3', 'Producer2', 'Producer1', 'Animal1'])
        ),
        (
            # Test case: only one animal - only one food source but cannot eat
            # as calories needed = calories provided
            [
                Species(name="Producer1", calories_provided=1000,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer2", calories_provided=2000,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer3", calories_provided=3000,
                        calories_needed=0, food_sources=[]),
                Species(name="Animal1", calories_provided=100,
                        calories_needed=1000, food_sources=["Producer1"])
            ],
            (3, ['Producer3', 'Producer2', 'Producer1'])
        ),
        (
            [
                Species(name="Animal1", calories_provided=1000,
                        calories_needed=0, food_sources=[]),
                Species(name="Animal2", calories_provided=800,
                        calories_needed=900, food_sources=["Animal1"]),
                Species(name="Animal3", calories_provided=500,
                        calories_needed=900, food_sources=["Animal1"]),
                Species(name="Animal4", calories_provided=350,
                        calories_needed=400, food_sources=["Animal3"])
            ],
            (3, ['Animal1', 'Animal3', 'Animal4'])
        ),
        (
            [
                Species(name="Animal1", calories_provided=1000,
                        calories_needed=0, food_sources=[]),
                Species(name="Animal2", calories_provided=800,
                        calories_needed=900, food_sources=["Animal1"]),
                Species(name="Animal3", calories_provided=500,
                        calories_needed=900, food_sources=["Animal1"]),
                Species(name="Animal4", calories_provided=350,
                        calories_needed=400, food_sources=["Animal2"]),
                Species(name="Animal5", calories_provided=250,
                        calories_needed=300, food_sources=["Animal4"]),
                Species(name="Animal6", calories_provided=150,
                        calories_needed=200, food_sources=["Animal5"]),
            ],
            (5, ['Animal1', 'Animal2', 'Animal4', 'Animal5', 'Animal6'])
        ),
        (
            # Test case: only one animal - calories needed higher than
            # provided by food sources
            [
                Species(name="Producer1", calories_provided=1000,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer2", calories_provided=2000,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer3", calories_provided=3000,
                        calories_needed=0, food_sources=[]),
                Species(name="Animal1", calories_provided=100,
                        calories_needed=3000, food_sources=["Producer1"])
            ],
            (3, ['Producer3', 'Producer2', 'Producer1'])
        ),
        (
            # Test case: two animals - the two eat different producers
            [
                Species(name="Producer1", calories_provided=1000,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer2", calories_provided=2000,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer3", calories_provided=3000,
                        calories_needed=0, food_sources=[]),
                Species(name="Animal1", calories_provided=100,
                        calories_needed=900, food_sources=["Producer1"]),
                Species(name="Animal2", calories_provided=200,
                        calories_needed=1900, food_sources=["Producer2"])
            ],
            (5, ['Producer3', 'Producer2', 'Producer1', 'Animal2', 'Animal1'])
        ),
        (
            # Test case: two animals - Animal2 cannot eat Animal1
            [
                Species(name="Producer1", calories_provided=4000,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer2", calories_provided=4050,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer3", calories_provided=5000,
                        calories_needed=0, food_sources=[]),
                Species(name="Animal1", calories_provided=1000,
                        calories_needed=1050, food_sources=["Producer1"]),
                Species(name="Animal2", calories_provided=800,
                        calories_needed=1000, food_sources=["Animal1"])
            ],
            (4, ['Producer3', 'Producer2', 'Producer1', 'Animal1'])
        ),
        (
            # Test case: two animals - Animal2 can eat Animal1
            [
                Species(name="Producer1", calories_provided=4000,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer2", calories_provided=4050,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer3", calories_provided=5000,
                        calories_needed=0, food_sources=[]),
                Species(name="Animal1", calories_provided=1000,
                        calories_needed=1050, food_sources=["Producer1"]),
                Species(name="Animal2", calories_provided=800,
                        calories_needed=900, food_sources=["Animal1"])
            ],
            (5, ['Producer3', 'Producer2', 'Producer1', 'Animal1', 'Animal2'])
        ),
        (
            # Test case: two animals - Animal2 can eat Animal1, Producer3
            [
                Species(name="Producer1", calories_provided=4000,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer2", calories_provided=4050,
                        calories_needed=0, food_sources=[]),
                Species(name="Producer3", calories_provided=5000,
                        calories_needed=0, food_sources=[]),
                Species(name="Animal1", calories_provided=1000,
                        calories_needed=1050, food_sources=["Producer1"]),
                Species(name="Animal2", calories_provided=800,
                        calories_needed=900,
                        food_sources=["Animal1", "Producer3"])
            ],
            (5, ['Producer3', 'Producer2', 'Producer1', 'Animal1', 'Animal2'])
        ),
        (
            [
                Species(name="WG", calories_provided=4950,
                        calories_needed=0, food_sources=[]),
                Species(name="FC", calories_provided=5850,
                        calories_needed=0, food_sources=[]),
                Species(name="CEG", calories_provided=4950,
                        calories_needed=0, food_sources=[]),
                Species(name="BSA", calories_provided=3750,
                        calories_needed=4550, food_sources=["CEG"]),
                Species(name="BP", calories_provided=3400,
                        calories_needed=8800,
                        food_sources=["WG", "CEG", "FC"]),
                Species(name="Wahoo", calories_provided=1700,
                        calories_needed=2500, food_sources=["StS", "BSA"]),
                Species(name="StS", calories_provided=1450,
                        calories_needed=2050, food_sources=["CD", "FR"]),
                Species(name="QP", calories_provided=3800,
                        calories_needed=4700, food_sources=["FC"]),
                Species(name="QA", calories_provided=2600,
                        calories_needed=3100,
                        food_sources=["BSA", "QP", "CEG"]),
                Species(name="HST", calories_provided=2800,
                        calories_needed=4950, food_sources=[
                            "BSA", "QP", "FR", "CEG", "FC"]),
                Species(name="GT", calories_provided=1250,
                        calories_needed=4900, food_sources=["WG"]),
                Species(name="FR", calories_provided=800,
                        calories_needed=4050, food_sources=["WG", "FC"]),
                Species(name="CD", calories_provided=2150,
                        calories_needed=2100, food_sources=["QP"])
            ],
            (9, ['FC', 'CEG', 'WG', 'QP', 'BSA', 'CD', 'Wahoo', 'StS', 'GT'])
        )
    ]
)
def test_find_sustainable_food_chain(species, expected_output):
    result = Solver.find_sustainable_food_chain(species)
    assert result.number_of_species == expected_output[0]
    assert result.species == expected_output[1]


@pytest.fixture
def input_examples():
    example_files = glob.glob("input_examples_*.json")
    examples = []
    for file in example_files:
        with open(file) as f:
            example = json.load(f)
            examples.append(example)
    return examples


@pytest.mark.timeout(300)  # Timeout set to 5 minutes (300 seconds)
def test_find_sustainable_food_chain_big_input():
    for i in [10000]:
        current_file_dir = os.path.dirname(__file__)
        input_file_relative_path = f"utils/input_examples_{i}.json"
        input_file_path = os.path.join(current_file_dir, 
                                       input_file_relative_path)
        with open(input_file_path, 'r') as f:
            payload = json.load(f)
            schema = SpeciesSchema(many=True)
            contracts = schema.load(payload)

        start_time = time.time()
        optimization_result = Solver.find_sustainable_food_chain(contracts)
        end_time = time.time()
        execution_time = end_time - start_time
        # Assert the execution time is less than 5 minutes (300 seconds)
        assert execution_time < 300
        assert isinstance(optimization_result.number_of_species, int)
        assert isinstance(optimization_result.species, list)
        assert all(isinstance(name, str)
                   for name in optimization_result.species)
