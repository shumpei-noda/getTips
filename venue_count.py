import sys
import json

def count(paths):
    n_venue_list = []
    for path in paths:
        with open(path, 'r') as open_json:
            tips_json = json.load(open_json)
            n_venue_list += [len(tips_json)]

    return n_venue_list

def print_count(n_venue_list, paths):
    for n_venue, path in zip(n_venue_list, paths):
        print(path, ":", n_venue, "venues")

def main():
    if len(sys.argv) < 2:
        print("jsonのpathくれ")
    n_venue_list = count(sys.argv[1:])
    print_count(n_venue_list, sys.argv[1:])

if __name__ == "__main__":
    main()
