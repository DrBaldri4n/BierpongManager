import random
import json

def main():
    groups = groupClassification()
    convertToJsonFile(groups)

def convertToJsonFile(groups):
    data = json.dumps(groups)
    with open('BierpongGroups.json', 'w') as f:
        json.dump(data, f, indent=2)
        print("New groups are created")

def groupClassification():
    groupNames = ["eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwoelf", "dreizeh", "vierze", "fuenfze", "sechsze", "siebzeh", "achtzeh", "neuzehn2", "zwanzig"]
    groupSize = 5
    groupNumber = 4

    #Random Classification from the groups
    groups = [[], [], [], []]
    for group in range(groupNumber):
        for _ in range(groupSize):
            rdmGroup = random.randint(0, (len(groupNames) - 1))
            groups[group].append(groupNames[rdmGroup])
            groupNames.pop(rdmGroup)
    return groups

if __name__ == "__main__":
    main()