import pytest

from mckinseysolvegame.domain.models import Species
from mckinseysolvegame.domain.services.optimization_service import Solver


@pytest.mark.parametrize(
    "species, expected_output",
    [
        (
            [],
            {}
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
            {
                'Species1': {
                    'calories_needed': 0,
                    'calories_provided': 1000
                }
            }
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
            {
                'Species3': {
                    'calories_needed': 0,
                    'calories_provided': 3000
                },
                'Species2': {
                    'calories_needed': 0,
                    'calories_provided': 2000
                },
                'Species1': {
                    'calories_needed': 0,
                    'calories_provided': 1000
                }
            }
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
            {
                'Producer3': {
                    'calories_needed': 0,
                    'calories_provided': 2000
                },
                'Producer2': {
                    'calories_needed': 0,
                    'calories_provided': 2000
                },
                'Producer1': {
                    'calories_needed': 0,
                    'calories_provided': 1000
                },
                'Animal1': {
                    'calories_needed': 0,
                    'calories_provided': 100,
                    'eats': ['Producer3']
                }
            }
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
            {
                'Producer3': {
                    'calories_needed': 0,
                    'calories_provided': 3000
                },
                'Producer2': {
                    'calories_needed': 0,
                    'calories_provided': 2000
                },
                'Producer1': {
                    'calories_needed': 0,
                    'calories_provided': 1000
                }
            }
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
            {
                'Animal1': {
                    'calories_needed': 0,
                    'calories_provided': 100
                },
                'Animal3': {
                    'calories_needed': 0,
                    'calories_provided': 100,
                    'eats': ['Animal1']
                },
                'Animal4': {
                    'calories_needed': 0,
                    'calories_provided': 350,
                    'eats': ['Animal3']
                }
            }
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
            {
                'Animal1': {
                    'calories_needed': 0,
                    'calories_provided': 100
                },
                'Animal2': {
                    'calories_needed': 0,
                    'calories_provided': 400,
                    'eats': ['Animal1']
                },
                'Animal4': {
                    'calories_needed': 0,
                    'calories_provided': 50,
                    'eats': ['Animal2']
                },
                'Animal5': {
                    'calories_needed': 0,
                    'calories_provided': 50,
                    'eats': ['Animal4']
                },
                'Animal6': {
                    'calories_needed': 0,
                    'calories_provided': 150,
                    'eats': ['Animal5']
                }
            }
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
            {
                'Producer3': {
                    'calories_needed': 0,
                    'calories_provided': 3000
                },
                'Producer2': {
                    'calories_needed': 0,
                    'calories_provided': 2000
                },
                'Producer1': {
                    'calories_needed': 0,
                    'calories_provided': 1000
                }
            }
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
            {
                'Producer3': {
                    'calories_needed': 0,
                    'calories_provided': 3000
                },
                'Producer2': {
                    'calories_needed': 0,
                    'calories_provided': 100
                },
                'Producer1': {
                    'calories_needed': 0,
                    'calories_provided': 100
                },
                'Animal2': {
                    'calories_needed': 0,
                    'calories_provided': 200,
                    'eats': ['Producer2']
                },
                'Animal1': {
                    'calories_needed': 0,
                    'calories_provided': 100,
                    'eats': ['Producer1']
                }
            }
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
            {
                'Producer3': {
                    'calories_needed': 0,
                    'calories_provided': 5000
                },
                'Producer2': {
                    'calories_needed': 0,
                    'calories_provided': 4050
                },
                'Producer1': {
                    'calories_needed': 0,
                    'calories_provided': 2950
                },
                'Animal1': {
                    'calories_needed': 0,
                    'calories_provided': 1000,
                    'eats': ['Producer1']
                }
            }
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
            {
                'Producer3': {
                    'calories_needed': 0,
                    'calories_provided': 5000
                },
                'Producer2': {
                    'calories_needed': 0,
                    'calories_provided': 4050
                },
                'Producer1': {
                    'calories_needed': 0,
                    'calories_provided': 2950
                },
                'Animal1': {
                    'calories_needed': 0,
                    'calories_provided': 100,
                    'eats': ['Producer1']
                },
                'Animal2': {
                    'calories_needed': 0,
                    'calories_provided': 800,
                    'eats': ['Animal1']
                },
            }
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
            {
                'Producer3': {
                    'calories_needed': 0,
                    'calories_provided': 4100
                },
                'Producer2': {
                    'calories_needed': 0,
                    'calories_provided': 4050
                },
                'Producer1': {
                    'calories_needed': 0,
                    'calories_provided': 2950
                },
                'Animal1': {
                    'calories_needed': 0,
                    'calories_provided': 1000,
                    'eats': ['Producer1']
                },
                'Animal2': {
                    'calories_needed': 0,
                    'calories_provided': 800,
                    'eats': ['Producer3']
                },
            }
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
                            "Flameback Angelfish"
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
                        food_sources=[
                            "Queen Parrotfish"
                        ]
                        )
            ],
            {
                'Fire Coral': {
                    'calories_needed': 0,
                    'calories_provided': 1150
                },
                'Widgeon Grass': {
                    'calories_needed': 0,
                    'calories_provided': 50
                },
                'Common Eel Grass': {
                    'calories_needed': 0,
                    'calories_provided': 400
                },
                'Queen Parrotfish': {
                    'calories_needed': 0,
                    'calories_provided': 700,
                    'eats': ['Fire Coral']
                },
                'Blue Striped Angelfish': {
                    'calories_needed': 0,
                    'calories_provided': 1250,
                    'eats': ['Common Eel Grass']
                },
                'Queen Angelfish': {
                    'calories_needed': 0,
                    'calories_provided': 2600,
                    'eats': ['Queen Parrotfish']
                },
                'Wahoo': {
                    'calories_needed': 0,
                    'calories_provided': 1700,
                    'eats': ['Blue Striped Angelfish']
                },
                'Gem Tang': {
                    'calories_needed': 0,
                    'calories_provided': 1250,
                    'eats': ['Widgeon Grass']
                }
            }
        ),
        (
            [
                Species(name="Red Moss",
                        calories_provided=3000,
                        calories_needed=0,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=[]),
                Species(name="Sea Fan",
                        calories_provided=3500,
                        calories_needed=0,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=[]),
                Species(name="Sea Lettuce",
                        calories_provided=3000,
                        calories_needed=0,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=[]),
                Species(name="Blue Jellyfish",
                        calories_provided=4500,
                        calories_needed=3000,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=["Sea Lettuce", "Red Moss"]),
                Species(name="Glass Squid",
                        calories_provided=3850,
                        calories_needed=3750,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=["Shrimp"]),
                Species(name="Great White Shark",
                        calories_provided=6000,
                        calories_needed=4250,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=["Green Sea Turtle", "Loggerhead Sea Turtle", "Lanternfish"]),
                Species(name="Green Sea Turtle",
                        calories_provided=4400,
                        calories_needed=3000,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=["Lanternfish", "Sea Lettuce", "Sea Urchin", "Spadefish"]),
                Species(name="Lanternfish",
                        calories_provided=3300,
                        calories_needed=2700,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=["Shrimp"]),
                Species(name="Loggerhead Sea Turtle",
                        calories_provided=4400,
                        calories_needed=4350,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=["Blue Jellyfish", "Lanternfish", "Sea Lettuce", "Spadefish", "Sea Urchin"]),
                Species(name="Sea Urchin",
                        calories_provided=2100,
                        calories_needed=3000,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=["Sea Fan", "Sea Lettuce"]),
                Species(name="Shrimp",
                        calories_provided=2750,
                        calories_needed=1450,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=["Red Moss", "Sea Lettuce"]),
                Species(name="Spadefish",
                        calories_provided=2100,
                        calories_needed=2400,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=["Sea Fan"]),
                Species(name="Swordfish",
                        calories_provided=5250,
                        calories_needed=3750,
                        depth_range="0-10m",
                        temperature_range="26.7-28.2",
                        food_sources=["Glass Squid", "Lanternfish", "Shrimp"])
            ],
            {
                'Great White Shark': {
                    'calories_needed': 0,
                    'calories_provided': 6000,
                    'eats': ['Green Sea Turtle', 'Loggerhead Sea Turtle']
                },
                'Blue Jellyfish': {
                    'calories_needed': 0,
                    'calories_provided': 150,
                    'eats': ['Sea Lettuce', 'Red Moss']
                },
                'Green Sea Turtle': {
                    'calories_needed': 0,
                    'calories_provided': 2275,
                    'eats': ['Lanternfish']
                },
                'Loggerhead Sea Turtle': {
                    'calories_needed': 0,
                    'calories_provided': 2275,
                    'eats': ['Blue Jellyfish']
                },
                'Lanternfish': {
                    'calories_needed': 0,
                    'calories_provided': 300,
                    'eats': ['Shrimp']
                },
                'Red Moss': {
                    'calories_needed': 0,
                    'calories_provided': 775
                },
                'Sea Lettuce': {
                    'calories_needed': 0,
                    'calories_provided': 775
                },
                'Shrimp': {
                    'calories_needed': 0,
                    'calories_provided': 50,
                    'eats': ['Red Moss', 'Sea Lettuce']
                }
            }
        )
    ]
)
def test_find_sustainable_food_chain(species, expected_output):
    result = Solver().find_sustainable_food_chain(species)
    assert result == expected_output
