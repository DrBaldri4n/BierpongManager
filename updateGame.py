import sqlite3

def incCups(group, teamX, cupsX, teamY, cupsY, cur):
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

def calcRank(group, cur):
    # first prio = points than highest number of cups
    cur.execute("SELECT * FROM " + group + " ORDER BY points DESC, cups DESC")
    teamInfo = cur.fetchall()

    for i in range(len(teamInfo)):
        cur.execute("UPDATE " + group + " SET rank = (?) WHERE team_name = (?)", (i + 1, teamInfo[i][0]))

def insertWinnerQF(teamXname, teamYname, teamXresult, teamYresult):
    cur, conn = openDB()
    winnerTeam = teamXname
    if int(teamXresult) < int(teamYresult):
        winnerTeam = teamYname
    cur.execute("UPDATE quater_finals \
                        SET winner = (?)\
                        WHERE team_name1 = (?) AND team_name2 = (?)", (winnerTeam, teamXname, teamYname))
    closeDB(conn)
    
def calcGroupWinner(teamInfo, cur):
    groupWinnerFirst = []
    groupWinnerSecond = []

    for groupCounter in range(len(teamInfo)):
        for teamCounter in range(len(teamInfo[1])):
            if teamInfo[groupCounter][teamCounter][3] == 1:
                groupWinnerFirst.append(teamInfo[groupCounter][teamCounter])
            elif teamInfo[groupCounter][teamCounter][3] == 2:
                groupWinnerSecond.append(teamInfo[groupCounter][teamCounter])

    return groupWinnerFirst, groupWinnerSecond

def addQuaterFinals(teamX, teamY, cupsX, cupsY):
    cur, conn = openDB()
    cur.execute("SELECT COUNT(*) FROM quater_finals")
    teamNumber = cur.fetchall()
    # TODO Error Handling
    if int(teamNumber[0][0]) < 4:
        cur.execute("INSERT INTO quater_finals (team_name1, team_name2, result_for_team1, result_for_team2, winner) VALUES (?,?,?,?,'x')", (teamX, teamY, cupsX, cupsY))
    closeDB(conn)

def addSF(teamX, teamY, cupsX, cupsY):
    cur, conn = openDB()
    cur.execute("SELECT COUNT(*) FROM semi_finals")
    teamNumber = cur.fetchall()
    # TODO Error Handling
    if int(teamNumber[0][0]) < 2:
        cur.execute("INSERT INTO semi_finals (team_name1, team_name2, result_for_team1, result_for_team2, winner) VALUES (?,?,?,?,'x')", (teamX, teamY, cupsX, cupsY))
    closeDB(conn)

# TODO not needed
def updateQF(teamX, teamY, cupsX, cupsY):
    cur, conn = openDB()
    cur.execute("UPDATE quater_finals SET result_for_team1 = " + cupsX + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    cur.execute("UPDATE quater_finals SET result_for_team2 = " + cupsY + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    closeDB(conn)

def catchQF():
    cur, conn = openDB()
    cur.execute("SELECT * FROM quater_finals")
    quaterFinalsTable = cur.fetchall()
    closeDB(conn)
    return quaterFinalsTable

# TODO very close to updateQuaterFinals
def updateFinals(teamX, teamY, cupsX, cupsY):
    cur, conn = openDB()
    cur.execute("UPDATE finals SET result_for_team1 = " + cupsX + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    cur.execute("UPDATE finals SET result_for_team2 = " + cupsY + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    closeDB(conn)

# TODO very close to catchQuaterFinals
def catchWinnerQF():
    cur, conn = openDB()
    cur.execute("SELECT winner FROM quater_finals")
    winnerQF = cur.fetchall()
    print(winnerQF)
    closeDB(conn)
    return winnerQF

def catchTeamInfo(groupNumber):
    cur, conn = openDB()
    allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]
    teamInfo = []

    for i in range(groupNumber):
        cur.execute("SELECT * FROM " + allGroupNames[i])
        teamInfo.append(cur.fetchall())

    groupWinnerFirst, groupWinnerSecond = calcGroupWinner(teamInfo, cur)
    closeDB(conn)
    return teamInfo, groupWinnerFirst, groupWinnerSecond

def printGroupStage(groupNumber, allGroupNames):
    for i in range(groupNumber):
        cur.execute("SELECT * FROM " + allGroupNames[i] + "_group_stage")
        print(allGroupNames[i], cur.fetchall())

def inputGameResults(group, teamX, teamY, cupsX, cupsY):
    cur, conn = openDB()

    cur.execute("UPDATE " + group + "_group_stage SET result_for_team1 = " + cupsX + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    cur.execute("UPDATE " + group + "_group_stage SET result_for_team2 = " + cupsY + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    incPoints(group, teamX, int(cupsX), teamY, int(cupsY), cur)
    incCups(group, teamX, cupsX, teamY, cupsY, cur)
    calcRank(group, cur)

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

def main(allGroupNames, groupNumber):    
    printGroupStage(groupNumber, allGroupNames)

    while True:
        catchTeamInfo(allGroupNames, groupNumber)
        inputResult = input("Eintragen eines Ergebnisses?(0 = nein | 1 = ja): ")
        if inputResult == "1":
            inputGameResults()
        gameEnd = input("programm beenden?(0 = nein | 1 = ja): ")
        if gameEnd == "1":
            break

    catchTeamInfo(allGroupNames, groupNumber)
    printGroupStage(groupNumber, allGroupNames)

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
    groupNumber = 4
    main(allGroupNames, groupNumber)
    
    conn.commit()
    conn.close()