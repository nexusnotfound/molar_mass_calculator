import json
import os
import sys
from typing import Any


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


ELEMENT_PROPERTIES = dict(json.load(open(resource_path("elements.json"), "r")))
NAME_PREFIXES = [
    "Mono", "Di", "Tri", "Tetra", "Penta", "Hexa", "Hepta", "Octo", "Nona", "Deca",
    "Undeca", "Dodeca", "Trideca", "Tetradeca", "Pentadeca", "Hexadeca", "Heptadeca", "Octadeca", "Nonadeca", "Icosa",
    "Henicosa", "Docosa", "Tricosa"
]


def parse(formula: str) -> tuple[int, dict[str, int]]:
    amounts = {}
    molecule_amount = 1
    last_type = ""
    current_amount = ""
    last_char_num = False
    formula += "."
    for char in formula:
        if char.isdigit():
            current_amount += char
            last_char_num = True
        else:
            if char.replace(" ", "") == "":
                continue
            if char.islower():
                last_type += char
            else:
                if last_type != "":
                    if last_char_num:
                        amounts.update({last_type: int(current_amount)})
                    else:
                        amounts.update({last_type: 1})
                elif current_amount.isnumeric():
                    molecule_amount = int(current_amount)
                current_amount = ""
                last_char_num = False
                last_type = char

    return molecule_amount, amounts


def get_element_name(symbol: str) -> str:
    if symbol in ELEMENT_PROPERTIES:
        return ELEMENT_PROPERTIES.get(symbol).get("name")
    else:
        return ""


def get_element_mass(symbol: str) -> str:
    if symbol in ELEMENT_PROPERTIES:
        return ELEMENT_PROPERTIES.get(symbol).get("mass")
    else:
        return ""


def get_element_data(symbol: str) -> str | None | dict[Any, Any]:
    if symbol in ELEMENT_PROPERTIES:
        return ELEMENT_PROPERTIES.get(symbol)
    else:
        return {}


def get_element_prefix(symbol: str, amount: int, first_molecule=False) -> str:
    if symbol in ELEMENT_PROPERTIES:
        element = ELEMENT_PROPERTIES[symbol]
    else:
        return ""

    molecule_regex = element.get("fname").split(".")
    element_name = element.get("name")

    if len(NAME_PREFIXES) < amount - 1:
        molecule_prefix = f"{amount}-"
    else:
        molecule_prefix = NAME_PREFIXES[amount - 1]

    if amount == 1 and first_molecule:
        molecule_prefix = ""
    else:
        element_name = element_name.lower()

    if molecule_regex != ["-"]:
        if amount > 0:
            element_name = element_name.replace(molecule_regex[0], molecule_regex[1])

    return molecule_prefix + element_name
