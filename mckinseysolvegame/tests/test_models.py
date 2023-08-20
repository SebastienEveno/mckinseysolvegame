import pytest
from marshmallow import ValidationError

from mckinseysolvegame.domain.models import OptimizationResult, Species


# region deserialization
def test_deserialize_species():
    # Arrange
    species_json = '[{"name": "Species 1", "calories_provided": 2, \
        "calories_needed": 3, "food_sources": []},' \
        '{"name": "Species 2", "calories_provided": 4, "calories_needed": 2, \
            "food_sources": []}]'

    # Act
    species = Species.from_json(species_json, many=True)

    # Assert
    assert len(species) == 2
    assert isinstance(species[0], Species)
    assert species[0].name == 'Species 1'
    assert species[0].calories_provided == 2
    assert species[0].calories_needed == 3
    assert species[0].food_sources == []
    assert isinstance(species[1], Species)
    assert species[1].name == 'Species 2'
    assert species[1].calories_provided == 4
    assert species[1].calories_needed == 2
    assert species[1].food_sources == []


def test_deserialize_species_with_long_name():
    # Arrange
    species_json = '{"name": "A very long contract name that exceeds the \
        maximum length of 64 characters", ' \
        '"start": 2, "duration": 3, "price": 5}'

    # Act
    with pytest.raises(ValidationError) as e:
        _ = Species.from_json(species_json)

    # Assert
    assert 'name' in e.value.messages
    assert 'Longer than maximum length 64.' in e.value.messages['name']


def test_deserialize_species_with_negative_calories_provided():
    # Arrange
    species_json = '{"name": "Species 1", "calories_provided": -2, \
        "calories_needed": 3, "food_sources": []}'
    # Act
    with pytest.raises(ValidationError) as e:
        _ = Species.from_json(species_json)
    # Assert
    assert 'calories_provided' in e.value.messages
    assert 'Must be greater than or equal to 1.' \
        in e.value.messages['calories_provided']


def test_deserialize_species_with_negative_calories_needed():
    # Arrange
    species_json = '{"name": "Species 1", "calories_provided": 1, \
        "calories_needed": -3, "food_sources": []}'
    # Act
    with pytest.raises(ValidationError) as e:
        _ = Species.from_json(species_json)
    # Assert
    assert 'calories_needed' in e.value.messages
    assert 'Must be greater than or equal to 0.' \
        in e.value.messages['calories_needed']


def test_deserialize_species_with_wrong_type():
    invalid_species = {"name": "invalid", "calories_provided": "not_an_int",
                       "calories_needed": 10, "food_sources": []}
    with pytest.raises(ValidationError):
        _ = Species.from_json(invalid_species)

    invalid_species = {"name": "invalid", "calories_provided": 10,
                       "calories_needed": "not_an_int", "food_sources": []}
    with pytest.raises(ValidationError):
        _ = Species.from_json(invalid_species)

    invalid_species = {"name": "invalid", "calories_provided": 10,
                       "calories_needed": 10, "food_sources": [1, ]}
    with pytest.raises(ValidationError):
        _ = Species.from_json(invalid_species)


def test_deserialize_species_with_missing_required_field():
    json_data = '{"name": "Species 1", "calories_provided": 2, \
        "calories_needed": 3}'
    with pytest.raises(ValidationError) as e:
        _ = Species.from_json(json_data)
    assert "food_sources" in e.value.messages
    assert "required field" in str(e.value)


def test_deserialize_species_with_extra_field():
    json_data = '{"name": "Species 1", "calories_provided": 2, \
        "calories_needed": 3, "food_sources": [], "extra_field": "value"}'
    with pytest.raises(ValidationError) as error:
        _ = Species.from_json(json_data)
    assert "extra_field" in error.value.messages
    assert "Unknown field." in str(error.value)


def test_optimization_result_deserialization():
    # Test valid deserialization
    input_data = {
        'number_of_species': 3,
        'species': ['Species1', 'Species2', 'Species3']
    }
    try:
        result = OptimizationResult.from_json(input_data)
        assert isinstance(result, OptimizationResult)
        assert result.number_of_species == 3
        assert result.species == ['Species1', 'Species2', 'Species3']
    except ValidationError:
        pytest.fail('Deserialization should not raise an error.')

    # Test deserialization with missing required fields
    invalid_data = [
        {},
        {'number_of_species': 3},
        {'species': ['Species1', 'Species2']},
    ]
    for data in invalid_data:
        with pytest.raises(ValidationError):
            _ = OptimizationResult.from_json(data)

    # Test deserialization with invalid field types
    invalid_data = [
        {'number_of_species': 'Invalid number of species type',
            'species': ['Species1', 'Species2', 'Species3']},
        {'number_of_species': 1, 'species': 'Contract1'},
        {'number_of_species': 2, 'species': ['Contract1', 2, 'Contract3']},
    ]
    for data in invalid_data:
        with pytest.raises(ValidationError):
            _ = OptimizationResult.from_json(data)

# endregion


def test_serialize_species():
    species = Species("Species 1", 2, 3, [])
    serialized = species.to_json("dict")
    expected = {
        "name": "Species 1",
        "calories_provided": 2,
        "calories_needed": 3,
        "food_sources": []
    }
    assert serialized == expected


def test_optimization_result_serialization():
    # Test valid serialization
    result = OptimizationResult(number_of_species=3, species=[
                                'Species1', 'Species2', 'Species3'])
    try:
        serialized = result.to_json()
        assert isinstance(serialized, dict)
        assert serialized == {'number_of_species': 3, 'species': [
            'Species1', 'Species2', 'Species3']}
    except ValidationError:
        pytest.fail('Serialization should not raise an error.')
