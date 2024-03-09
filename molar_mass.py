import os
import sys

from formulalib import parse, get_element_name, get_element_mass

from decimal import Decimal, getcontext

# Set the precision of the Decimal module
getcontext().prec = 280


def precise_mult(a: str, b: str) -> float:
    a = Decimal(a)
    b = Decimal(b)
    return float(a * b)


def COLOR_GREEN(text: str) -> str:
    return f"\033[38;5;34m{text}\033[0m"


def main():
    print("Molecular Mass Calculator")
    print()
    while True:
        print("Enter molecular formula")
        formula = input("> ")

        molecule_amount, element_amounts = parse(formula)

        total_molar_mass = 0
        for element, amount in element_amounts.items():
            element_mass = get_element_mass(element)
            if element_mass != "":
                molar_mass = precise_mult(element_mass, str(amount))
                total_molar_mass += molar_mass
                print(f"{amount} {get_element_name(element)} ({element_mass} g/mol) atoms: {molar_mass} g/mol")
            else:
                print(f"Element symbol {element} not recognized.")
                sys.exit()
        print(f"A total of {molecule_amount} * {total_molar_mass} = {COLOR_GREEN(f'{precise_mult(str(total_molar_mass), str(molecule_amount))} g/mol')}")
        input()
        os.system("cls")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Cancelled")
