import argparse
import requests
import sys

def main ():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    search_parser= subparser.add_parser("search", help="Look up a pokemon by its name")
    search_parser.add_argument("name", type=str, help="Name of the pokemon")
    unit_group= search_parser.add_mutually_exclusive_group()
    unit_group.add_argument("--metric", action="store_true", help="Show height/weight in metric")
    unit_group.add_argument("--imperial", action="store_true", help="Show height/weight in imperial")
    compare_parser= subparser.add_parser("compare", help="Compare the base stats of two pokemons")
    compare_parser.add_argument("name1", type=str, help="Choose your first pokemon to compare")
    compare_parser.add_argument("name2", type=str, help="Choose your second pokemon to compare")
    ability_parser= subparser.add_parser("ability", help="Look up an ability")
    ability_parser.add_argument("ability_name", type=str, help="Name of the ability")
    args = parser.parse_args()
    if args.command == "search":
        req= requests.get(f"https://pokeapi.co/api/v2/pokemon/ {args.name.lower()}")
        if req.status_code != 200:
            print(f"Couldnt find a pokemon: {args.name}")
            sys.exit(1)
        data= req.json()
        types = [t["type"]["name"] for t in data["types"]]
        abilities = [a["ability"]["name"] for a in data["abilities"]]
        height_dm = data
    