import json

def main():
    groups = readJson()
    print(groups)
    
def readJson():
    f = open('BierpongGroups.json')
    groups = json.load(f)
    f.close()
    return groups

if __name__ == "__main__":
    main()