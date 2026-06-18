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
        req= requests.get(f"https://pokeapi.co/api/v2/pokemon/{args.name.lower()}")
        if req.status_code != 200:
            print(f"Couldnt find a pokemon: {args.name}")
            sys.exit(1)
        data= req.json()
        types = [t["type"]["name"] for t in data["types"]]
        abilities = [a["ability"]["name"] for a in data["abilities"]]
        height_dm = data["height"]
        weight_hg = data["weight"]
        if args.imperial:
            height = height_dm * 3.937
            weight = weight_hg * 0.220462
            print(f"{data['name'].title()} (#{data['id']})")
            print(f"Height: {height:.1f} in")
            print(f"Weight: {weight:.1f} lb")
        else:
            height = height_dm / 10
            weight = weight_hg / 10
            print(f"{data['name'].title()} (#{data['id']})")
            print(f"Height: {height:.1f} m")
            print(f"Weight: {weight:.1f} kg")
        print(f"Types: {', '.join(types)}")
        print(f"Abilities: {', '.join(abilities)}")
    elif args.command == "compare":
        req1 = requests.get(f"https://pokeapi.co/api/v2/pokemon/{args.name1.lower()}")
        req2 = requests.get(f"https://pokeapi.co/api/v2/pokemon/{args.name2.lower()}")
        if req1.status_code != 200:
            print(f"Couldnt find a pokemon: {args.name1}")
            sys.exit(1)
        if req2.status_code !=200:
             print(f"Couldnt find a pokemon: {args.name2}")
             sys.exit(1)
        data1= req1.json()
        data2= req2.json()
        stats1= {s["stat"]["name"]: s["base_stat"] for s in data1["stats"]}
        stats2= {s["stat"]["name"]: s["base_stat"] for s in data2["stats"]}
        print(f"{data1['name'].title()} vs {data2['name'].title()}")
        for stat_name in stats1:
            print(f"{stat_name}: {stats1 [stat_name]} vs {stats2 [stat_name]}")
    elif args.command == "ability":
        req = requests.get(f"https://pokeapi.co/api/v2/ability/{args.ability_name.lower()}")
        if req.status_code != 200:
            print(f"Could find ability: {args.ability_name}")
            sys.exit(1)
        data = req.json()
        effect_text = "No description availiable"
        for entry in data["effect_entries"]:
            if entry["language"]["name"]== "en":
                effect_text = entry["effect"]
                break
        print(f"{data['name'].title()}")
        print(effect_text)
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)
if __name__ == "__main__":
    main()
    