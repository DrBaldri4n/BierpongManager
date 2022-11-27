import sqlite3

def incCups(group, teamX, cupsX, teamY, cupsY):
    cur.execute("UPDATE " + group + " SET cups = cups + (?) WHERE team_name = (?)", (cupsX, teamX))
    cur.execute("UPDATE " + group + " SET cups = cups + (?) WHERE team_name = (?)", (cupsY, teamY))

def incPoints(group, teamX, cupsX, teamY, cupsY, cur):
    if cupsX > cupsY:
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (3, teamX))
    elif cupsX < cupsY:
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (3, teamY))
    else:
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (1, teamX))
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (1, teamY))

def printGroups(allGroupNames, groupNumbers):
    for i in range(groupNumbers):
        cur.execute("SELECT * FROM " + allGroupNames[i])
        print(allGroupNames[i], cur.fetchall())

def printGroupStage(groupNumbers, allGroupNames):
    for i in range(groupNumbers):
        cur.execute("SELECT * FROM " + allGroupNames[i] + "_group_stage")
        print(allGroupNames[i], cur.fetchall())

def inputGameResults(group, teamX, teamY, cupsX, cupsY):
    cur, conn = openDB()
    # group = input("Welche Gruppe?: ")
    # teamX = input("name des ersten Teams: ")
    # teamY = input("name des zweiten Teams: ")
    # cupsX = input("erziehlte Cups für " + teamX + ": ")
    # cupsY = input("erziehlte Cups für " + teamY + ": ")

    cur.execute("UPDATE " + group + "_group_stage SET result_for_team1 = " + cupsX + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    cur.execute("UPDATE " + group + "_group_stage SET result_for_team2 = " + cupsY + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    incPoints(group, teamX, int(cupsX), teamY, int(cupsY), cur)
    closeDB(conn)

def catchGroupStage(groupNumber):
    cur, conn = openDB()
    allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]
    allGroupStages = []
    for i in range(groupNumber):
        cur.execute("SELECT * FROM " + allGroupNames[i] + "_group_stage")
        allGroupStages.append(cur.fetchall())
    closeDB(conn)
    return allGroupStages 

def main(allGroupNames, groupNumbers):    
    printGroupStage(groupNumbers, allGroupNames)

    while True:
        printGroups(allGroupNames, groupNumbers)
        inputResult = input("Eintragen eines Ergebnisses?(0 = nein | 1 = ja): ")
        if inputResult == "1":
            inputGameResults()
        gameEnd = input("programm beenden?(0 = nein | 1 = ja): ")
        if gameEnd == "1":
            break

    printGroups(allGroupNames, groupNumbers)
    printGroupStage(groupNumbers, allGroupNames)

def closeDB(conn):
    conn.commit()
    conn.close()

def openDB():
    conn = sqlite3.connect('beerpong.db')
    cur = conn.cursor()
    return cur, conn

if __name__ == "__main__":
    conn = sqlite3.connect('beerpong.db')
    cur = conn.cursor()
    
    allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]
    groupNumbers = 4
    main(allGroupNames, groupNumbers)
    
    conn.commit()
    conn.close()