import sys
import json

def count(paths):
    n_tips_list = []
    for path in paths:
        with open(path, 'r') as open_json:
            tips_json = json.load(open_json)
            n_tips = 0
            for tips in tips_json:
                n_tips += tips_json[tips]['count']
            n_tips_list += [n_tips]
    return n_tips_list

def print_count(n_tips_list, paths):
    for n_tips, path in zip(n_tips_list, paths):
        print(path, ":", n_tips, "tips")

def main():
    if len(sys.argv) < 2:
        print("jsonのpathくれ")
    n_tips_list = count(sys.argv[1:])
    print_count(n_tips_list, sys.argv[1:])


if __name__ == "__main__":
    main()
