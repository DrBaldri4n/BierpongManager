import sqlite3
import random


def createGroups():
    allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]
    groupNumbers = input("wie viel Gruppen soll es geben?(zwischen 2 und 8 und nur gerade): ")
    #TODO error meldung einbauen, wenn gruppenzahl falsch eingegeben
    groupNumbers = int(groupNumbers)
    for i in range(groupNumbers):
        cur.execute("CREATE TABLE IF NOT EXISTS " + allGroupNames[i] +   " (team_name TEXT PRIMARY KEY,\
                                                                            points INTEGER,\
                                                                            cups INTEGER)")
    return groupNumbers, allGroupNames

def addNewTeam(allTeamNames):
    teamName = input("Teamname = ")
    allTeamNames.append(teamName)
    return allTeamNames

def printGroups(groupNumbers, allGroupNames):
    for i in range(groupNumbers):
        cur.execute("SELECT * FROM " + allGroupNames[i])
        print(allGroupNames[i], cur.fetchall())


def spiltTeams(allTeamNames, groupNumbers, allGroupNames):
    teamNumbers = len(allTeamNames)
    x = teamNumbers / groupNumbers
    while len(allTeamNames) > 0:
        rdmGroup = random.randint(0, int(groupNumbers) - 1)
        currentGroup = allGroupNames[rdmGroup]
        cur.execute("SELECT count() FROM " + currentGroup)
        lenGroupX = cur.fetchall()
        if lenGroupX[0][0] < int(x):
            cur.execute("INSERT INTO " + currentGroup + " VALUES ('" + allTeamNames[0] + "', 0, 0)")
            allTeamNames.remove(allTeamNames[0])



def main():
    groupNumbers, allGroupNames = createGroups()
    allTeamNames = []

    # while True:
    #     allTeamNames = addNewTeam(allTeamNames)
    #     anotherTeam = input("möchten sie noch ein Team hinzufügen? (0 = nein | 1 = ja): ")
    #     if int(anotherTeam) == 0:
    #         break

    #only for tests!!!!
    allTeamsGroupA = [
                ('Team1', 0, 0),
                ('Team2', 0, 0),
                ('Team3', 0, 0),
                ('Team4', 0, 0),
                ('Team5', 0, 0),
                ]
    allTeamsGroupB = [
                ('Team6', 0, 0),
                ('Team7', 0, 0),
                ('Team8', 0, 0),
                ('Team9', 0, 0),
                ('Team10', 0, 0),
                ]
    allTeamsGroupC = [
                ('Team11', 0, 0),
                ('Team12', 0, 0),
                ('Team13', 0, 0),
                ('Team14', 0, 0),
                ('Team15', 0, 0),
                ]
    allTeamsGroupD = [
                ('Team16', 0, 0),
                ('Team17', 0, 0),
                ('Team18', 0, 0),
                ('Team19', 0, 0),
                ('Team20', 0, 0),
                ]
    cur.executemany("INSERT INTO groupA VALUES (?,?,?)", allTeamsGroupA)
    cur.executemany("INSERT INTO groupB VALUES (?,?,?)", allTeamsGroupB)
    cur.executemany("INSERT INTO groupC VALUES (?,?,?)", allTeamsGroupC)
    cur.executemany("INSERT INTO groupD VALUES (?,?,?)", allTeamsGroupD)
    spiltTeams(allTeamNames, groupNumbers, allGroupNames)
    printGroups(groupNumbers, allGroupNames)
    
    
if __name__ == "__main__":
    conn = sqlite3.connect('beerpong.db')
    cur = conn.cursor()
    
    main()
    
    conn.commit()
    conn.close()


