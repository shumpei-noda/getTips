import sys
import json

def count(paths):
    n_restaurant_list = []
    for path in paths:
        with open(path, 'r') as open_json:
            tips_json = json.load(open_json)
            n_restaurant_list += [len(tips_json)]

    return n_restaurant_list

def print_count(n_restaurant_list, paths):
    for n_restaurant, path in zip(n_restaurant_list, paths):
        print(path, ":", n_restaurant, "restaurants")

def main():
    if len(sys.argv) < 2:
        print("jsonのpathくれ")
    n_restaurant_list = count(sys.argv[1:])
    print_count(n_restaurant_list, sys.argv[1:])

if __name__ == "__main__":
    main()
