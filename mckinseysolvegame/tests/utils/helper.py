import json
import random

num_examples = 10000
# num_examples = 500000
output_file = f"input_examples_{num_examples}.json"


def generate_input_examples():
    examples = []
    for i in range(num_examples):
        calories_provided = random.randint(100, 6000)
        calories_needed = random.randint(0, 4500)
        food_sources = list(set(
            [f"Species{random.randint(1, num_examples)}" for _ in range(random.randint(0, 10))]))
        example = {
            "name": f"Species{i + 1}",
            "calories_provided": calories_provided,
            "calories_needed": calories_needed,
            "food_sources": food_sources
        }
        examples.append(example)
    with open(output_file, "w") as f:
        json.dump(examples, f, indent=4)


generate_input_examples()
