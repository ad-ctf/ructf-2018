import random

from mimesis import Food, Text

top = 200000000
down = -200000000


def get_random_cords():
    return random.randint(down, top), random.randint(down, top), random.randint(down, top)


def get_random_header():
    generator = Text("en")
    first = generator.word().title()
    second = generator.word().title()
    return "{} {}ous #{}".format(first, second, random.randint(1, 1000))


def get_random_body():
    generator = Food("en")
    return "Buy our {}! Drink our {}! Fresh {} & {}! Anything at our store!"\
        .format(generator.dish(), generator.drink(), generator.fruit(), generator.vegetable())
