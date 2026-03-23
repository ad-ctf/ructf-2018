import random
import mimesis

top = 200000000
down = -200000000


def get_random_cords():
    return random.randint(down, top), random.randint(down, top), random.randint(down, top)


def get_random_header():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    first = "".join(random.choice(alphabet) for _ in range(8)).title()
    second = "".join(random.choice(alphabet) for _ in range(8)).title()
    return "{} {}ous #{}".format(first, second, random.randint(1, 1000))


def get_random_body():
    generator = mimesis.Food()
    return "Buy our {}! Drink our {}! Fresh {} & {}! Anything at our store!"\
        .format(generator.dish(), generator.drink(), generator.fruit(), generator.vegetable())
