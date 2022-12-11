import sqlite3
import random #test


def createGroups():
    allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]
    groupNumbers = input("wie viel Gruppen soll es geben?(zwischen 2 und 8 und nur gerade): ")
    #TODO error meldung einbauen, wenn gruppenzahl falsch eingegeben
    groupNumbers = int(groupNumbers)
    for i in range(groupNumbers):                                       # TODO team_nameX, team_nameY
        cur.execute("CREATE TABLE IF NOT EXISTS " + allGroupNames[i] +   " (team_name TEXT PRIMARY KEY,\
                                                                            cups INTEGER,\
                                                                            points INTEGER,\
                                                                            rank INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS " + allGroupNames[i] + "_group_stage (team_name1 TEXT,\
                                                                         team_name2 TEXT,\
                                                                         result_for_team1 INTEGER,\
                                                                         result_for_team2 INTEGER   )")
        # TODO Create Table only when needed
        cur.execute("CREATE TABLE IF NOT EXISTS eight_finals            (team_name1 TEXT,\
                                                                         team_name2 TEXT,\
                                                                         result_for_team1 INTEGER,\
                                                                         result_for_team2 INTEGER,\
                                                                         winner TEXT)")

        cur.execute("CREATE TABLE IF NOT EXISTS quater_finals           (team_name1 TEXT,\
                                                                         team_name2 TEXT,\
                                                                         result_for_team1 INTEGER,\
                                                                         result_for_team2 INTEGER,\
                                                                         winner TEXT)")

        cur.execute("CREATE TABLE IF NOT EXISTS semi_finals             (team_name1 TEXT,\
                                                                         team_name2 TEXT,\
                                                                         result_for_team1 INTEGER,\
                                                                         result_for_team2 INTEGER,\
                                                                         winner TEXT)")

        cur.execute("CREATE TABLE IF NOT EXISTS finals                   (team_name1 TEXT,\
                                                                         team_name2 TEXT,\
                                                                         result_for_team1 INTEGER,\
                                                                         result_for_team2 INTEGER   )")
    return groupNumbers, allGroupNames

def createGroupStage(allGroupNames, groupNumbers):
    for indexGroup in range(groupNumbers):
        cur.execute("SELECT team_name FROM " + allGroupNames[indexGroup])
        groupX = cur.fetchall()
        cur.execute("SELECT count() FROM " + allGroupNames[indexGroup])
        groupSize = cur.fetchall()
        groupSize = groupSize[0][0]

        groupStage = []
        print(allGroupNames[indexGroup])
        for j in range(groupSize - 1):
            for i in range(j + 1, groupSize):
                groupStage.append([groupX[j][0], groupX[i][0]])
        pos = 0

        for _ in range(len(groupStage)):
            print(groupStage[pos][0] + " vs " + groupStage[pos][1])
            cur.execute("INSERT INTO " + allGroupNames[indexGroup] + "_group_stage VALUES ('" + groupStage[pos][0] + "', '" + groupStage[pos][1] + "', 0, 0)")
            groupStage.pop(pos)
            # TODO smarter solution??
            if pos == 0:
                pos -= 1
            else: 
                pos += 1

def addNewTeam(allTeamNames):
    teamName = input("Teamname = ")
    allTeamNames.append(teamName)
    return allTeamNames

def printGroups(groupNumbers, allGroupNames):
    for i in range(groupNumbers):
        cur.execute("SELECT * FROM " + allGroupNames[i])
        print(allGroupNames[i], cur.fetchall())

def printGroupStage(groupNumbers, allGroupNames):
    for i in range(groupNumbers):
        cur.execute("SELECT * FROM " + allGroupNames[i] + "_group_stage")
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
                ('SpVgg Warnweste', 0, 0, 1),
                ('Team2', 0, 0, 1),
                ('Team3', 0, 0, 1),
                ('Team4', 0, 0, 1),
                ]
    allTeamsGroupB = [
                ('Auffallen durch Umfallen', 0, 0, 1),
                ('Scheissdanixdannfahltdanix', 0, 0, 1),
                ('Team8', 0, 0, 1),
                ('Team9', 0, 0, 1),
                ]
    allTeamsGroupC = [
                ('Team11', 0, 0, 1),
                ('Team12', 0, 0, 1),
                ('Team13', 0, 0, 1),
                ('Team14', 0, 0, 1),
                ]
    allTeamsGroupD = [
                ('Team16', 0, 0, 1),
                ('Team17', 0, 0, 1),
                ('Team18', 0, 0, 1),
                ('Team19', 0, 0, 1),
                ]
    allTeamsGroupE = [
                ('Team21', 0, 0, 1),
                ('Team22', 0, 0, 1),
                ('Team23', 0, 0, 1),
                ('Team24', 0, 0, 1),
                ]
    allTeamsGroupF = [
                ('Team26', 0, 0, 1),
                ('Team27', 0, 0, 1),
                ('Team28', 0, 0, 1),
                ('Team29', 0, 0, 1),
                ]
    allTeamsGroupG = [
                ('Team31', 0, 0, 1),
                ('Team32', 0, 0, 1),
                ('Team33', 0, 0, 1),
                ('Team34', 0, 0, 1),
                ]
    allTeamsGroupH = [
                ('Team36', 0, 0, 1),
                ('Team37', 0, 0, 1),
                ('Team38', 0, 0, 1),
                ('Team39', 0, 0, 1),
                ]

    cur.executemany("INSERT INTO groupA VALUES (?,?,?,?)", allTeamsGroupA)
    cur.executemany("INSERT INTO groupB VALUES (?,?,?,?)", allTeamsGroupB)
    cur.executemany("INSERT INTO groupC VALUES (?,?,?,?)", allTeamsGroupC)
    cur.executemany("INSERT INTO groupD VALUES (?,?,?,?)", allTeamsGroupD)
    cur.executemany("INSERT INTO groupE VALUES (?,?,?,?)", allTeamsGroupE)
    cur.executemany("INSERT INTO groupF VALUES (?,?,?,?)", allTeamsGroupF)
    cur.executemany("INSERT INTO groupG VALUES (?,?,?,?)", allTeamsGroupG)
    cur.executemany("INSERT INTO groupH VALUES (?,?,?,?)", allTeamsGroupH)

    createGroupStage(allGroupNames, groupNumbers)
    spiltTeams(allTeamNames, groupNumbers, allGroupNames)
    printGroups(groupNumbers, allGroupNames)
    
    
if __name__ == "__main__":
    conn = sqlite3.connect('beerpong.db')
    cur = conn.cursor()
    
    main()
    
    conn.commit()
    conn.close()
