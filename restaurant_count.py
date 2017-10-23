import sys
import json

def count(paths):
    for path in paths:
        with open(path, 'r') as open_json:
            tips_json = json.load(open_json)
            print(path, ":", len(tips_json), "restaurants")

def main():
    if len(sys.argv) < 2:
        print("jsonのpathくれ")
    count(sys.argv[1:])

if __name__ == "__main__":
    main()
