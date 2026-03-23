import random

from mimesis import Choice, Food

CHEMICAL_ELEMENTS = [
    "Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon",
    "Nitrogen", "Oxygen", "Fluorine", "Neon", "Sodium", "Magnesium",
    "Aluminium", "Silicon", "Phosphorus", "Sulfur", "Chlorine", "Argon",
    "Potassium", "Calcium", "Scandium", "Titanium", "Vanadium", "Chromium",
    "Manganese", "Iron", "Cobalt", "Nickel", "Copper", "Zinc", "Gallium",
    "Germanium", "Arsenic", "Selenium", "Bromine", "Krypton", "Rubidium",
    "Strontium", "Yttrium", "Zirconium", "Niobium", "Molybdenum",
    "Technetium", "Ruthenium", "Rhodium", "Palladium", "Silver", "Cadmium",
    "Indium", "Tin", "Antimony", "Tellurium", "Iodine", "Xenon", "Cesium",
    "Barium", "Lanthanum", "Cerium", "Praseodymium", "Neodymium",
    "Promethium", "Samarium", "Europium", "Gadolinium", "Terbium",
    "Dysprosium", "Holmium", "Erbium", "Thulium", "Ytterbium", "Lutetium",
    "Hafnium", "Tantalum", "Tungsten", "Rhenium", "Osmium", "Iridium",
    "Platinum", "Gold", "Mercury", "Thallium", "Lead", "Bismuth",
    "Polonium", "Astatine", "Radon", "Francium", "Radium", "Actinium",
    "Thorium", "Protactinium", "Uranium", "Neptunium", "Plutonium",
    "Americium", "Curium", "Berkelium", "Californium", "Einsteinium",
    "Fermium", "Mendelevium", "Nobelium", "Lawrencium", "Rutherfordium",
    "Dubnium", "Seaborgium", "Bohrium", "Hassium", "Meitnerium",
    "Darmstadtium", "Roentgenium", "Copernicium", "Nihonium", "Flerovium",
    "Moscovium", "Livermorium", "Tennessine", "Oganesson",
]

top = 200000000
down = -200000000


def get_random_cords():
    return random.randint(down, top), random.randint(down, top), random.randint(down, top)


def get_random_header():
    generator = Choice()
    first = generator.choice(CHEMICAL_ELEMENTS)
    second = generator.choice(CHEMICAL_ELEMENTS)
    return "{} {}ous #{}".format(first, second, random.randint(1, 1000))


def get_random_body():
    generator = Food("en")
    return "Buy our {}! Drink our {}! Fresh {} & {}! Anything at our store!"\
        .format(generator.dish(), generator.drink(), generator.fruit(), generator.vegetable())
