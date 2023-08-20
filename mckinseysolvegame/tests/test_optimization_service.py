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
                Species(name="Species1",
                        calories_provided=1000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[])
            ],
            (1, ['Species1'])
        ),
        (
            [
                Species(name="Species1",
                        calories_provided=1000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Species2",
                        calories_provided=2000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Species3",
                        calories_provided=3000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[])
            ],
            (3, ['Species3', 'Species2', 'Species1'])
        ),
        (
            [
                Species(name="Producer1",
                        calories_provided=1000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer2",
                        calories_provided=2000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer3",
                        calories_provided=3000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Animal1",
                        calories_provided=100,
                        calories_needed=1000,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Producer1", "Producer2", "Producer3"])
            ],
            (4, ['Producer3', 'Producer2', 'Producer1', 'Animal1'])
        ),
        (
            # Test case: only one animal - only one food source but cannot eat
            # as calories needed = calories provided
            [
                Species(name="Producer1",
                        calories_provided=1000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer2",
                        calories_provided=2000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer3",
                        calories_provided=3000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Animal1",
                        calories_provided=100,
                        calories_needed=1000,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Producer1"])
            ],
            (3, ['Producer3', 'Producer2', 'Producer1'])
        ),
        (
            [
                Species(name="Animal1", calories_provided=1000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Animal2", calories_provided=800,
                        calories_needed=900,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Animal1"]),
                Species(name="Animal3", calories_provided=500,
                        calories_needed=900,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Animal1"]),
                Species(name="Animal4", calories_provided=350,
                        calories_needed=400,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Animal3"])
            ],
            (3, ['Animal1', 'Animal3', 'Animal4'])
        ),
        (
            [
                Species(name="Animal1",
                        calories_provided=1000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Animal2",
                        calories_provided=800,
                        calories_needed=900,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Animal1"]),
                Species(name="Animal3",
                        calories_provided=500,
                        calories_needed=900,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Animal1"]),
                Species(name="Animal4",
                        calories_provided=350,
                        calories_needed=400,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Animal2"]),
                Species(name="Animal5",
                        calories_provided=250,
                        calories_needed=300,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Animal4"]),
                Species(name="Animal6",
                        calories_provided=150,
                        calories_needed=200,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Animal5"]),
            ],
            (5, ['Animal1', 'Animal2', 'Animal4', 'Animal5', 'Animal6'])
        ),
        (
            # Test case: only one animal - calories needed higher than
            # provided by food sources
            [
                Species(name="Producer1",
                        calories_provided=1000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer2",
                        calories_provided=2000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer3",
                        calories_provided=3000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Animal1",
                        calories_provided=100,
                        calories_needed=3000,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Producer1"])
            ],
            (3, ['Producer3', 'Producer2', 'Producer1'])
        ),
        (
            # Test case: two animals - the two eat different producers
            [
                Species(name="Producer1",
                        calories_provided=1000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer2",
                        calories_provided=2000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer3",
                        calories_provided=3000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Animal1",
                        calories_provided=100,
                        calories_needed=900,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Producer1"]),
                Species(name="Animal2",
                        calories_provided=200,
                        calories_needed=1900,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Producer2"])
            ],
            (5, ['Producer3', 'Producer2', 'Producer1', 'Animal2', 'Animal1'])
        ),
        (
            # Test case: two animals - Animal2 cannot eat Animal1
            [
                Species(name="Producer1",
                        calories_provided=4000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer2",
                        calories_provided=4050,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer3",
                        calories_provided=5000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Animal1",
                        calories_provided=1000,
                        calories_needed=1050,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Producer1"]),
                Species(name="Animal2",
                        calories_provided=800,
                        calories_needed=1000,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Animal1"])
            ],
            (4, ['Producer3', 'Producer2', 'Producer1', 'Animal1'])
        ),
        (
            # Test case: two animals - Animal2 can eat Animal1
            [
                Species(name="Producer1",
                        calories_provided=4000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer2",
                        calories_provided=4050,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer3",
                        calories_provided=5000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Animal1",
                        calories_provided=1000,
                        calories_needed=1050,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Producer1"]),
                Species(name="Animal2",
                        calories_provided=800,
                        calories_needed=900,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Animal1"])
            ],
            (5, ['Producer3', 'Producer2', 'Producer1', 'Animal1', 'Animal2'])
        ),
        (
            # Test case: two animals - Animal2 can eat Animal1, Producer3
            [
                Species(name="Producer1",
                        calories_provided=4000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer2",
                        calories_provided=4050,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Producer3",
                        calories_provided=5000,
                        calories_needed=0,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=[]),
                Species(name="Animal1",
                        calories_provided=1000,
                        calories_needed=1050,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Producer1"]),
                Species(name="Animal2",
                        calories_provided=800,
                        calories_needed=900,
                        depth_range="Depth",
                        temperature_range="Temperature",
                        food_sources=["Animal1", "Producer3"])
            ],
            (5, ['Producer3', 'Producer2', 'Producer1', 'Animal1', 'Animal2'])
        ),
        (
            [
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
                            ]
                        ),
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
                            ]
                        ),
                Species(name="Bicolour Parrotfish",
                        calories_provided=3400,
                        calories_needed=8800,
                        depth_range="0-30m",
                        temperature_range="28.3-30",
                        food_sources=[
                            "Widgeon Grass",
                            "Common Eel Grass",
                            "Fire Coral"
                            ]
                        ),
                Species(name="Wahoo",
                        calories_provided=1700,
                        calories_needed=2500,
                        depth_range="0-30m",
                        temperature_range="28.3-30",
                        food_sources=[
                            "Short-tail Stingray",
                            "Blue Striped Angelfish"
                            ]
                        ),
                Species(name="Swordfish",
                        calories_provided=2000,
                        calories_needed=500,
                        depth_range="61-90m",
                        temperature_range="25-26.6",
                        food_sources=[
                            "Bicolour Angelfish"
                            ]
                        ),
                Species(name="Short-tail Stingray",
                        calories_provided=1450,
                        calories_needed=2050,
                        depth_range="0-30m",
                        temperature_range="28.3-30",
                        food_sources=[
                            "Common Dolphinfish",
                            "Foxface Rabbitfish"
                            ]
                        ),
                Species(name="Sailfin Tang",
                        calories_provided=2500,
                        calories_needed=4800,
                        depth_range="61-90m",
                        temperature_range="25-26.6",
                        food_sources=[
                            "Rock Weed"
                            ]
                        ),
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
                            ]
                        ),
                Species(name="Powder Blue Tang",
                        calories_provided=3600,
                        calories_needed=4350,
                        depth_range="61-90m",
                        temperature_range="25-26.6",
                        food_sources=[
                            "Stalked Kelp",
                            "Purple Hydrocoral"
                            ]
                        ),
                Species(name="Porcupine Pufferfish",
                        calories_provided=2600,
                        calories_needed=3800,
                        depth_range="31-60m",
                        temperature_range="26.7-28.2",
                        food_sources=[
                            "Peacock's Tail Algae",
                            "Passer Angelfish"
                            ]
                        ),
                Species(name="Passer Angelfish",
                        calories_provided=2250,
                        calories_needed=4600,
                        depth_range="31-60m",
                        temperature_range="26.7-28.2",
                        food_sources=[
                            "Peacock's Tail Algae"
                            ]
                        ),
                Species(name="Pacific Tripletail",
                        calories_provided=2150,
                        calories_needed=2900,
                        depth_range="31-60m",
                        temperature_range="26.7-28.2",
                        food_sources=[
                            "Coral Beauty"
                            ]
                        ),
                Species(name="Olive Ridley Turtle",
                        calories_provided=3550,
                        calories_needed=4400,
                        depth_range="31-60m",
                        temperature_range="26.7-28.2",
                        food_sources=[
                            "Green Zoanthid",
                            "Pacific Tripletail"
                            ]
                        ),
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
                            ]
                        ),
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
                            ]
                        ),
                Species(name="Long Finned Pilot Whale",
                        calories_provided=3100,
                        calories_needed=950,
                        depth_range="31-60m",
                        temperature_range="26.7-28.2",
                        food_sources=[
                            "Pacific Tripletail"
                            ]
                        ),
                Species(name="Indo-Pacific Sailfish",
                        calories_provided=1600,
                        calories_needed=5600,
                        depth_range="31-60m",
                        temperature_range="26.7-28.2",
                        food_sources=[
                            "Pacific Tripletail",
                            "Coral Beauty",
                            "Flameback  Angelfish"
                            ]
                        ),
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
                            ]
                        ),
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
                            ]
                        ),
                Species(name="Flameback Angelfish",
                        calories_provided=2900,
                        calories_needed=4750,
                        depth_range="31-60m",
                        temperature_range="26.7-28.2",
                        food_sources=[
                            "Green Zoanthid"
                            ]
                        ),
                Species(name="Flame Angelfish",
                        calories_provided=2200,
                        calories_needed=4000,
                        depth_range="61-90m",
                        temperature_range="25-26.6",
                        food_sources=[
                            "Stalked Kelp",
                            "Rock Weed"
                            ]
                        ),
                Species(name="Eyestripe Surgeonfish",
                        calories_provided=1050,
                        calories_needed=3900,
                        depth_range="61-90m",
                        temperature_range="25-26.6",
                        food_sources=[
                            "Stalked Kelp",
                            "Rock Weed"
                            ]
                        ),
                Species(name="Cuvier Beaked Whale",
                        calories_provided=1400,
                        calories_needed=2250,
                        depth_range="31-60m",
                        temperature_range="26.7-28.2",
                        food_sources=[
                            "Coral Beauty",
                            "Flameback Angelfish"
                            ]
                        ),
                Species(name="Coral Trout",
                        calories_provided=1850,
                        calories_needed=3000,
                        depth_range="61-90m",
                        temperature_range="25-26.6",
                        food_sources=[
                            "Bicolour Angelfish",
                            "Powder Blue Tang",
                            "Flame Angelfish"
                            ]
                        ),
                Species(name="Coral Beauty",
                        calories_provided=2650,
                        calories_needed=4900,
                        depth_range="31-60m",
                        temperature_range="26.7-28.2",
                        food_sources=[
                            "Yellow Tube Sponge",
                            "Peacock's Tail Algae"
                            ]
                        ),
                Species(name="Common Dolphinfish",
                        calories_provided=2150,
                        calories_needed=2100,
                        depth_range="0-30m",
                        temperature_range="28.3-30",
                        food_sources=["Queen Parrotfish"])
            ],
            (9, ['Fire Coral', 'Common Eel Grass', 'Widgeon Grass',
                 'Queen Parrotfish', 'Blue Striped Angelfish',
                 'Common Dolphinfish', 'Wahoo', 'Short-tail Stingray',
                 'Gem Tang'])
        )
    ]
)
def test_find_sustainable_food_chain(species, expected_output):
    result = Solver.find_sustainable_food_chain(species)
    assert result.number_of_species == expected_output[0]
    assert result.species == expected_output[1]
