"""
Script for taking a list of prompts and creating different city variants.
"""

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Script for taking a list of prompts and creating different city variants."
    )

    parser.add_argument("input_file", help="Path to the input file containing the stubs")

    args = parser.parse_args()

    with open(args.input_file, "r") as file:
        stubs = [l.strip() for l in file.readlines()]

    cities = ["Tokyo", "London", "New York", "Mexico City", "Mumbai", "QQQ"]
    labels = ["Japan", "UK", "US", "Mexico", "India", "Neutral"]
    letters = "ABCDEF"

    for s, stub in enumerate(stubs):
        for c, city in enumerate(cities):
            fields = [s, letters[c], stub.replace("QQQ", city), labels[c]]
            print("\t".join((str(f) for f in fields)))


if __name__ == "__main__":
    main()
